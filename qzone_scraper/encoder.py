
class Encoder():
    @staticmethod
    def obj2dict(obj):
        if isinstance(obj, list):
            element = []
            for item in obj:
                element.append(Encoder.obj2dict(item))
            return element
        if not hasattr(obj, "__dict__"):
            return obj
        result = {}
        for key, val in obj.__dict__.items():
            if key.startswith("_"):
                continue
            element = Encoder.obj2dict(val)
            result[key] = element
        return result

    @staticmethod
    def dict2obj(dict_data, dtype):
        obj = dtype()
        obj.__dict__ = dict_data
        return obj