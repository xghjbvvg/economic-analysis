import json


class ReponseBuilder(json.JSONEncoder):
    def __init__(self, success, data):
        self.success = success
        self.data = data