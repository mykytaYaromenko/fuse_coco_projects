import os
from utils import import_coco_config
import cv2
import sys

def _segment_image(image_path: str, annotation: dict, output_path: str) -> None:
    image = cv2.imread(image_path)
    x, y, w, h = map(int, annotation["bbox"])
    print(x, y, w, h)
    cropped_image = image[y:y+h, x:x+w]

    category_path = os.path.join(output_path)
    base_name = os.path.basename(image_path)
    cv2.imwrite(os.path.join(category_path, base_name), cropped_image)


def save_and_segment_labels(path_to_project: str, output_path: str) -> None:

    config = import_coco_config(os.path.join(path_to_project, "result.json"))

    image_paths = config["images"]
    annotations = config["annotations"]
    categories = config["categories"]

    for category in categories:
        os.makedirs(os.path.join(output_path, category["name"]), exist_ok=True)

    for annotation in annotations:
        category_name = next(cat["name"] for cat in categories if cat["id"] == annotation["category_id"])
        category_path = os.path.join(output_path, category_name)

        image_path = os.path.join(path_to_project, next(img["file_name"] for img in image_paths if img["id"] == annotation["image_id"]))

        _segment_image(image_path, annotation, category_path, category_name)


if __name__ == "__main__":
    path_to_project = sys.argv[1]
    output_path = sys.argv[2]

    save_and_segment_labels(path_to_project, output_path)
