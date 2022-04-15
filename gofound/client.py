import requests

from gofound.model import SearchOrder


class Client(object):
    """
    客户端
    """

    def __init__(self, url="http://127.0.0.1:5678/api"):
        self.url = url
        self.request = requests.Session()
        self.request.headers["Client-Type"] = "python"

    def query(self, query, page=1, limit=10, order=SearchOrder.DESC, highlight=None):
        res = self.request.post(self.url + "/query", json={
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
        res = self.request.post(self.url + "/index", json={
            "id": id,
            "text": text,
            "document": document
        })
        return res.json()

    def remove_document(self, id):
        """
        删除文档
        """
        res = self.request.post(self.url + "/remove", json={
            "id": id
        })
        return res.json()

    def flush_index(self):
        """
        刷新索引
        """
        res = self.request.post(self.url + "/dump")
        return res.json()
