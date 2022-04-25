import yaml
from parser import Parser
from json import Json


class Yaml(Parser):
    @staticmethod
    def serialize(obj):
        str_json = Json.serialize(obj)
        obj_json = Json.parse(str_json, is_buffer=True)
        my_str = yaml.dump(obj_json)
        return my_str

    @staticmethod
    def parse(my_str, is_buffer=False):
        raw_obj = yaml.load(my_str, Loader=yaml.FullLoader)
        if is_buffer is True:
            return raw_obj
        for key in raw_obj:
            if type(raw_obj[key]) is not int and "code" in raw_obj[key]:
                func_object = {}
                exec(raw_obj[key]["code"], {}, func_object)
                raw_obj[key] = func_object[raw_obj[key]["func_name"]]
            elif type(raw_obj[key]) is not int and "classname" in raw_obj[key]:
                attr_dict = {}
                if raw_obj[key]["attrs"] != 'None' and raw_obj[key]["attrs"] != {}:
                    for attr in raw_obj[key]["attrs"]:
                        attr_dict[attr] = raw_obj[key]["attrs"][attr]
                if raw_obj[key]["funcs"] != 'None' and raw_obj[key]["attrs"] != {}:
                    for func in raw_obj[key]["funcs"]:
                        attr_dict[func] = raw_obj[key]["funcs"][func]
                raw_obj[key] = type(
                    raw_obj[key]["classname"],
                    (),
                    attr_dict
                )
        return raw_obj
