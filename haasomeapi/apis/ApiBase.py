import hmac
import hashlib
import inspect
import requests

from typing import Dict
from typing import List


class ApiBase:

    def __init__(self, connectionstring: str, privatekey: str):

        self.baseUrl = connectionstring
        self.privateKey = privatekey

    @staticmethod
    def generate_signature(parameters: Dict[str, str], privatekey: str):
        parameter_string = ""

        for key, value in parameters.items():
            parameter_string += "&" + key + "=" + value

        parameter_string = parameter_string.replace("&", "", 1)

        key = bytes(privatekey, 'UTF-8')
        message = bytes(parameter_string, 'UTF-8')

        digester = hmac.new(key, message, hashlib.sha256)
        signature = digester.digest()
        signature = signature.hex().replace("-", "").upper()

        return parameter_string, signature

    def _execute_request(self, endpoint: str, parameters: Dict[str, str]):

        # Authorize is set by default

        url = self.baseUrl + endpoint

        paramSig = ApiBase.generate_signature(parameters, self.privateKey)

        if not paramSig[0]:
            url = url + "?sig="+paramSig[1]
        else:
            url = url + "?"
            url = url + paramSig[0]
            url = url + "&sig="+paramSig[1]

        print(url)

        #return requests.get(url).json()
        test = requests.get(url).json()
        #print(test)
        return test

    @staticmethod
    def _from_json(data, cls):
        annotations: dict = cls.__annotations__ if hasattr(cls, '__annotations__') else None
        if issubclass(cls, List):
            list_type = cls.__args__[0]
            instance: list = list()
            for value in data:
                instance.append(ApiBase._from_json(value, list_type))
            return instance
        elif issubclass(cls, Dict):
                key_type = cls.__args__[0]
                val_type = cls.__args__[1]
                instance: dict = dict()
                for key, value in data.items():
                    instance.update(ApiBase._from_json(key, key_type), ApiBase._from_json(value, val_type))
                return instance
        else:
            instance: cls = cls()
            for name, value in data.items():
                func = lambda s: s[:1].lower() + s[1:] if s else ''
                name = func(name)
                field_type = annotations.get(name)
                if inspect.isclass(field_type) and isinstance(value, (dict, tuple, list, set, frozenset)):
                    setattr(instance, name, ApiBase._from_json(value, field_type))
                else:
                    setattr(instance, name, value)
            return instance