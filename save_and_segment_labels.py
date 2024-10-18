import os

import numpy as np

from utils import import_coco_config
import cv2
import sys

def _segment_image(image_path: str, annotation: dict) -> np.ndarray:
    image = cv2.imread(image_path)
    x, y, w, h = map(int, annotation["bbox"])
    cropped_image = image[y:y+h, x:x+w]

    return cropped_image


def save_and_segment_labels(path_to_project: str, output_path: str) -> None:

    config = import_coco_config(os.path.join(path_to_project, "result.json"))

    image_paths = config["images"]
    annotations = config["annotations"]
    categories = config["categories"]

    for category in categories:
        os.makedirs(os.path.join(output_path, category["name"]), exist_ok=True)

    count_of_saved_objects = 0
    for idx, annotation in enumerate(annotations):
        try:
            category_name = next(cat["name"] for cat in categories if cat["id"] == annotation["category_id"])
            category_path = os.path.join(output_path, category_name)

            image_path = os.path.join(path_to_project, next(img["file_name"] for img in image_paths if img["id"] == annotation["image_id"])).replace("\\", "/")
            base_name = os.path.basename(image_path).replace(".jpeg","") + f"_{annotation['id']}.jpeg"
            segmented_object = _segment_image(image_path, annotation)
            path_to_save = os.path.join(category_path, base_name)
            cv2.imwrite(path_to_save, segmented_object)
            print(f"Saved object {idx}/{len(annotations)} to {path_to_save}")
            count_of_saved_objects += 1
        except:
            print("Error in annotation for image: ", annotation["image_id"])
            continue
    print(f"Saved {count_of_saved_objects}/{len(annotations)} objects")

if __name__ == "__main__":
    path_to_project = sys.argv[1]
    output_path = sys.argv[2]

    save_and_segment_labels(path_to_project, output_path)
