import gofound


def add_document():
    """
    添加索引
    """
    client = gofound.Client(url="http://127.0.0.1:5678/api")
    res = client.add_document(1000, "探访海南自贸港“样板间”", {
        "content": "洋浦经济开发区地处海南西北部洋浦半岛，是21世纪海上丝绸之路与西部陆海新通道的交汇节点。是国务院1992年批准设立的。我国第一个由外商成片开发、享受保税区政策的国家级开发区",
    })
    print(res)


def search():
    """
    搜索
    """
    client = gofound.Client(url="http://127.0.0.1:5678/api")
    res = client.query("探访海南自贸港", page=1, limit=10, order="desc")
    print(res)

    # 遍历数据
    if res.get('state'):
        documents = res.get('data').get('documents')
        if documents:
            for item in documents:
                print(item)


def remove():
    """
    删除索引
    """
    client = gofound.Client(url="http://127.0.0.1:5678/api")
    res = client.remove_document(1000)
    print(res)


if __name__ == '__main__':
    # add_document()
    search()
    # remove()