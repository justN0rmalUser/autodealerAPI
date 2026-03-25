from pathlib import Path
import json
from jsonschema import validate, ValidationError, SchemaError

TMP_DIR = Path("C:\Windows\Temp")

class Parse_JSON_Config:
    def __init__(self, fpath: str | Path):
        jsonPath = fpath if isinstance(fpath, Path) else Path(fpath)
        instruct = self._getjson(jsonPath)

        if self._is_valid(instruct):
            

    def _getschema(self):
        with open(Path("C:\\Program Files\\_Scripts\\_auxiliary-soft\\db\\api.json"), encoding="utf-8") as FILE:
            return json.load(FILE)
        
    def _getjson(self, fp: Path):
        with open(fp, encoding="utf-8") as FILE:
            return json.load(FILE)

    def _is_valid(self, instruct: dict):
        try:
            schema = self._getschema()
            validate(instance=instruct, schema=schema)
        except SchemaError:
            print('some')
            return False
        except ValidationError:
            print('input')
            return False
        except Exception as exc:
            print(exc)
            return False            
        else:
            return True

    def get_method_name(self, instanceJSON: dict):
        return tuple(instanceJSON.keys())[0]