import json


def import_coco_config(config_path: str) -> dict:
    with open(config_path, "r") as file:
        config = json.load(file)
    return config
