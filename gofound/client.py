import requests
import aiohttp
from typing import Optional, Tuple, List, Union, NoReturn
import json
from urllib.parse import urljoin

from gofound.model import SearchOrder
from gofound.exceptions import DBException, AuthException

DEFAULT_JSON_DECODER = json.loads
DEFAULT_JSON_ENCODER = json.dumps


def check_url(url: str) -> str:
    if "api" not in url:
        if not url.endswith("/"):
            url += "/"
        url += "api/"
    elif not url.endswith("/"):
        url += "/"
    return url


class Client(object):
    """
    客户端
    """

    def __init__(self, url="http://127.0.0.1:5678/api/", database="default", auth=('admin', '123321')):
        self.url = check_url(url)
        self.db = database
        self.request = requests.Session()

        self.request.headers["Client-Type"] = "python"
        self.auth = auth

    def _post(self, url, json):
        res = self.request.post(urljoin(self.url, url), params={"database": self.db}, json=json, auth=self.auth)
        if res.status_code == 401:
            raise AuthException("401 Auth failed")

        if res.status_code != 200:
            raise DBException("Error:", res.status_code)
        return res

    def query(self, query, page=1, limit=10, order=SearchOrder.DESC, highlight=None):
        res = self._post("query", json={
            "query": query,
            "page": page,
            "limit": limit,
            "order": order,
            'highlight': highlight
        })
        return res.json()

    def add_document(self, id, text, document):
        """
        添加文档，如果id相同，就是更新
        """
        res = self._post("index", json={
            "id": id,
            "text": text,
            "document": document
        })
        return res.json()

    def add_documents(self, documents):
        """
        批量添加
        """
        res = self._post("index/batch", json=documents)
        return res.json()

    def remove_document(self, id):
        """
        删除文档
        """
        res = self._post("remove", json={
            "id": id
        })
        return res.json()


class AsyncClient:
    def __init__(self, url: Optional[str] = "http://127.0.0.1:5678/api/",
                 database: Optional[str] = "default",
                 client_session: aiohttp.ClientSession = None,
                 auth: Optional[Union[Tuple[str, str], aiohttp.BasicAuth]] = ('admin', '123321'),
                 **kwargs):
        if not url.endswith("/api"):
            url += "/api"
        self.url = url
        if isinstance(auth, aiohttp.BasicAuth):
            self.auth = auth
        else:
            self.auth = aiohttp.BasicAuth(auth[0], auth[1])
        self.db = database
        self.kw = kwargs
        self.loads = self.kw.pop("loads") if "loads" in self.kw else DEFAULT_JSON_DECODER  # json serialize
        self.dumps = self.kw.pop("dumps") if "dumps" in self.kw else DEFAULT_JSON_ENCODER
        self.session = client_session or aiohttp.ClientSession(json_serialize=self.dumps)

    async def send_request(self,
                           url: str,
                           json: Optional[dict] = None,
                           method: Optional[str] = "POST",
                           params: Optional[dict] = None) -> dict:
        async with self.session.request(method, urljoin(self.url, url),
                                        params=params,
                                        json=json,
                                        auth=self.auth,
                                        **self.kw) as res:
            if res.status == 401:
                raise AuthException("401 Auth failed")
            if res.status != 200:
                raise DBException(f"Error: {res.status} {await res.text()}")
            data = await res.json(loads=self.loads)
        return data

    async def query(self, query: str,
                    page: int = 1,
                    limit: int = 10,
                    order=SearchOrder.DESC,
                    highlight: Optional[dict] = None):
        if highlight is not None:
            json = {
                "query": query,
                "page": page,
                "limit": limit,
                "order": order,
                'highlight': highlight
            }
        else:
            json = {
                "query": query,
                "page": page,
                "limit": limit,
                "order": order,
            }
        return await self.send_request("query", json=json, params={"database": self.db})

    async def add_document(self, id: int, text: str, document: dict) -> Union[dict, NoReturn]:
        """
        添加文档，如果id相同，就是更新
        """
        return await self.send_request("index", json={
            "id": id,
            "text": text,
            "document": document
        }, params={"database": self.db})

    async def add_documents(self, documents: List[dict]) -> Union[dict, NoReturn]:
        """
        批量添加
        """
        return await self.send_request("index/batch", json=documents, params={"database": self.db})

    async def remove_document(self, id: int):
        """
        删除文档
        """
        return await self.send_request("remove", json={
            "id": id
        }, params={"database": self.db})

    async def status(self):
        """
        查询状态
        """
        return await self.send_request("status", method="GET")

    async def drop(self, database: Optional[str] = None):
        """
        删除数据库
        """
        if database is None:
            database = self.db
        return await self.send_request("drop", method="GET", params={"database": database})  # fixme 不好搞

    async def cut(self, query: str):
        return await self.send_request("word/cut", method="GET", params={"q": query})
