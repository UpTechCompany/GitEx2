class JSONRead:
    def __init__(self):
        pass

    def read_json_file(self, json_object):
        if isinstance(json_object, dict):
            for key, value in json_object.items():
                if isinstance(value, dict):
                    json_object[key] = self.read_json_file(value)
                elif isinstance(value, list):
                    json_object[key] = [self.read_json_file(item) for item in value]

        return json_object


