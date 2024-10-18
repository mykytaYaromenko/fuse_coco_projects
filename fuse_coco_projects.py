import os
import sys
import json
import shutil
from utils import import_coco_config
import copy


def _save_images_from_config(config: dict, project_path: str, dir_to_save: str) -> None:
    image_paths = config["images"]
    os.makedirs(os.path.join(dir_to_save, "images"), exist_ok=True)

    for image in image_paths:
        image_path = os.path.join(project_path, image["file_name"]).replace("\\", "/")
        base_name = os.path.basename(image_path)
        shutil.copyfile(image_path, os.path.join(dir_to_save, "images", base_name))


def _fuse_two_coco_projects(config: dict, project_path: str, dir_to_save: str) -> dict:
    start_id_of_images = len(config["images"])
    start_id_of_annotations = len(config["annotations"])

    with open(os.path.join(project_path, "result.json"), "r") as file:
        config_of_project_to_be_fused = json.load(file)

    copy_of_categories = copy.deepcopy(config_of_project_to_be_fused)["categories"]
    for category in config_of_project_to_be_fused["categories"]:
        if category["name"] not in [cat["name"] for cat in config["categories"]]:
            category_to_add = category
            category_to_add["id"] += len(config["categories"])
            config["categories"].append(category_to_add)

    # print(copy_of_categories)

    for image in config_of_project_to_be_fused["images"]:
        image["file_name"] = image["file_name"].replace("\\", "/")
        base_name = os.path.basename(image["file_name"])
        shutil.copyfile(os.path.join(project_path, image["file_name"]), os.path.join(dir_to_save,"images",  base_name))
        image["id"] += start_id_of_images
        config["images"].append(image)

    for annotation in config_of_project_to_be_fused["annotations"]:
        annotation["id"] += start_id_of_annotations
        annotation["image_id"] += start_id_of_images
        category_name = next(cat["name"] for cat in copy_of_categories if cat["id"] == annotation["category_id"])
        category_id = next(cat["id"] for cat in config["categories"] if cat["name"] == category_name)
        annotation["category_id"] = category_id
        config["annotations"].append(annotation)

    return config


def fuse_coco_projects(input_folder: str, output_order: str):
    project_list = os.listdir(input_folder)
    os.makedirs(output_order, exist_ok=True)
    os.makedirs(os.path.join(output_order, "fused_dataset"), exist_ok=True)
    os.makedirs(os.path.join(output_order, "fused_segmented_dataset"), exist_ok=True)
    path_to_first_project = os.path.join(input_folder, project_list[0])


    config = import_coco_config(os.path.join(path_to_first_project, "result.json"))
    _save_images_from_config(config, path_to_first_project ,os.path.join(output_order, "fused_dataset"))

    for idx, project in enumerate(project_list[1:]):
        project_path = os.path.join(input_folder, project)
        print(f"Processing {idx + 1}/{len(project_list)} project\n{project_path}")

        config = _fuse_two_coco_projects(config, project_path, os.path.join(output_order, "fused_dataset"))

    with open(os.path.join(output_order, "fused_dataset", "result.json"), "w") as file:
        json.dump(config, file, indent=4)


if __name__ == "__main__":
    input_folder = sys.argv[1]
    output_folder = sys.argv[2]
    fuse_coco_projects(input_folder, output_folder)
