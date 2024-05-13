import json
import requests

class FromRequest():

    def __init__(self, call_variable, **kwargs) -> None:
        self.call_variable = call_variable
        self.url = kwargs.get("url")
        self.method = kwargs.get("method")
        self.headers = kwargs.get("headers")
        self.action = kwargs.get("action")
        self.body = kwargs.get("body")


    def prepare_body(self):
        r = json.dumps(self.body)
        for key, value in self.call_variable.items():
            r = r.replace(f"[[{key}]]", value)
        return json.loads(r)


    def run(self):
        body = self.prepare_body()
        headers = self.headers
        response = requests.request(self.method, self.url, headers=headers, data=body)
        print(response.status_code)
        if response.status_code == 200:
            return self.action["2xx"]
        elif response.status_code == 300:
            return self.action["3xx"]
        else :
            self.action["4xx"]