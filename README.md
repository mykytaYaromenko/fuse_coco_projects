## ✏️ Introduction

Fuse coco projects is the repository to work with coco projects. It is a collection of tools and scripts to work with coco projects.
It is a collection of tools and scripts to work with coco projects.


## 💿 Installation
```
 python3 -m venv .venv
 source .venv/bin/activate
 pip install -r requirements.txt 
 ````

## 🔧 Usage

### 1️⃣ fuse_coco_projects.py

#### Description
This script is used to fuse multiple coco projects into a single project. It takes a list of coco projects and fuses them into a single project. The fused project which contains the config file and file with images from all coco projects is saved in the output directory.

#### Usage
```
python3 fuse_coco_projects.py INPUT_DIR OUTPUT_DIR
```
Where INPUT_DIR is the directory containing the coco projects to be fused and OUTPUT_DIR is the directory where the fused project will be saved. 

#### Example
```
python3 fuse_coco_projects.py "data/input_dir" "data/output_dir"
```

### 2️⃣ save_and_segment_labels.py

#### Description
This script saves the annotations from the coco project in a json file and segments the labels in the images. The segmented images are saved in the output directories according to the category of the annotation.

#### Usage
```
python3 save_and_segment_labels.py INPUT_DIR OUTPUT_DIR
```
Where INPUT_DIR is the directory containing the coco project and OUTPUT_DIR is the directory where the segmented images will be saved.

#### Example
```
python3 save_and_segment_labels.py "data/input_dir" "data/output_dir"
```
For example there are the following annotations in the coco project:
```
{
    "annotations": [
        {
            "id": 1,
            "image_id": 1,
            "category_id": 1,
            "segmentation": [[1, 2, 3, 4, 5, 6, 7, 8]],
            "bbox": [1, 2, 3, 4],
            "area": 12
        },
        {
            "id": 2,
            "image_id": 1,
            "category_id": 2,
            "segmentation": [[1, 2, 3, 4, 5, 6, 7, 8]],
            "bbox": [1, 2, 3, 4],
            "area": 12
        }
    ],
    "categories": [
        {
            "id": 1,
            "name": "category1"
        },
        {
            "id": 2,
            "name": "category2"
        }
    ]
}
```
The segmented images will be saved in the following directories:
```
output_dir/category1
output_dir/category2
```
