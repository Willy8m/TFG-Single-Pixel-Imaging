import json

class ConfigIO:
    def __init__(self):
        pass

    def save(self, fname, dict_data):
        with open(fname, "w") as f:
            json.dump(dict_data, f, indent="    ")

    def load(self, fname):
        with open(fname, "r") as f:
            data = json.load(f, parse_int=False)
        # FIXME: Use a custom encoder...
        try:
            data["geometry"] = [int(i) for i in data["geometry"]]
        except:
            raise
        return data
