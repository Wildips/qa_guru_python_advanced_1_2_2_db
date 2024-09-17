class Server:
    def __init__(self, env):
        self.reqres = {
            "dev": "",
            "beta": "",
            "rc": "http://127.0.0.1:8002",
        }[env]
        self.ninjacats = {
            "dev": "",
            "beta": "",
            "rc": "https://ninjactas.com",
        }[env]
