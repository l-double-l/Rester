import re
import os

class DictWrapper(object):
    def __init__(self, d):
        if isinstance(d, list):  # if the first level element is a list
            setattr(self, "._length", len(d))
            for index, item in enumerate(d):
                setattr(self, "[%s]" % index, DictWrapper(item))
        else:
            for key, value in d.items():
                if isinstance(value, list):
                    setattr(self, key, [DictWrapper(x) if isinstance(x, dict) else x for x in value])
                    setattr(self, "%s._length" % key, len(value) if hasattr(value, "__len__") else 0)
                    for index, item in enumerate(value):
                        setattr(self, "%s[%s]" % (key, index), DictWrapper(item) if isinstance(item, dict) else item)
                else:
                    setattr(self, key, DictWrapper(value)
                            if isinstance(value, dict) else self.__transform_value(value))

    def get(self, name, default):
        return self.__dict__.get(name, default)

    def __transform_value(self, value):
        if isinstance(value, str) or isinstance(value, unicode):
            m = re.search('@!(.*)!@', value)
            if m:
                with open(os.path.join('', m.group(1))) as f_xml:
                    return f_xml.read().replace('\n','')
            else:
                return value

        return value

    def __getattr__(self, name):
        levels = name.split(".")
        if len(levels) > 1:
            curr_level = levels.pop(0)
            return getattr(self.__dict__[curr_level], '.'.join(levels))
        else:
            try:
                return self.__dict__[name] # if name in self.__dict__ else None
            except KeyError:
                raise AttributeError(name)

    def __setattr__(self, key, value):
        self.__dict__[key] = DictWrapper(value) if isinstance(value, dict) else value

    def items(self):
        return self.__dict__

    def __getitem__(self, key):
        return self.__dict__[key]


class ResponseWrapper(object):
    def __init__(self, status, data, headers):
        self.status = status
        data = {key: (value.encode('ascii', 'replace') if isinstance(value, str) or isinstance(value, unicode) else value) for key, value in data.iteritems()}
        self.body = DictWrapper(data)
        self.headers = DictWrapper(headers)
        self.headers.status = status
