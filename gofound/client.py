import requests

from gofound.model import SearchOrder


class Client(object):
    """
    客户端
    """

    def __init__(self, url="http://127.0.0.1:5678/api", database="default", auth=('admin', '123321')):
        self.url = url
        self.request = requests.Session()

        self.request.headers["Client-Type"] = "python"
        self.auth = auth

    def _post(self, url, json):
        res = self.request.post(self.url + url, json=json, auth=self.auth)
        if res.status_code == 401:
            raise Exception("401 Auth failed")

        if res.status_code != 200:
            raise Exception("Error:", res.status_code)
        return res

    def query(self, query, page=1, limit=10, order=SearchOrder.DESC, highlight=None):
        res = self._post("/query", json={
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
        res = self._post("/index", json={
            "id": id,
            "text": text,
            "document": document
        })
        return res.json()

    def add_documents(self, documents):
        """
        批量添加
        """
        res = self._post("/index/batch", json=documents)
        return res.json()

    def remove_document(self, id):
        """
        删除文档
        """
        res = self._post("/remove", json={
            "id": id
        })
        return res.json()
