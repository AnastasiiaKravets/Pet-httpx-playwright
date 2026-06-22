import httpx

from config import settings


class API_Client():

    def __init__(self, **kwargs):
        # print(kwargs)
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        self.client = httpx.Client(base_url=settings.BASE_API_URL, timeout=60, headers = headers, **kwargs)

    def __enter__(self) -> API_Client:
        return self

    def __exit__(self, *_: object):
        self.client.close()
        print("client closed")

    def get(self, path: str, **kwargs):
        return self.client.get(path, **kwargs)

    def post(self, path: str, **kwargs):
        return self.client.post(path, **kwargs)

    def put(self, path: str, **kwargs):
        return self.client.put(path, **kwargs)

    def delete(self, path: str, **kwargs):
        return self.client.delete(path, **kwargs)

