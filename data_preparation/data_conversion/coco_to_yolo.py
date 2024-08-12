from utils.logger_config import setup_logging
from utils.logger_config import get_root_dir
import logging
import json
import os

setup_logging(log_level=logging.INFO, log_dir="output/logs", log_file="log.txt")
logger = logging.getLogger(__name__)


def coco_to_json_converter(coco_json_file_path: str, coco_to_json_output_dir: str):
    logger.info("Converting COCO json file to YOLO format")
    # output dir
    os.makedirs(coco_to_json_output_dir, exist_ok=True)

    coco_to_json_path = os.path.dirname(coco_json_file_path)
    try:
        with open(coco_json_file_path, "r") as f:
            coco_json = json.load(f)
    except Exception as e:
        logger.error(f"Error while reading COCO json file: {e}")
        return

    for image in coco_json["images"]:
        image_id = image["id"]
        image_filename = image["file_name"]
        yolo_txt_file = os.path.join(
            coco_to_json_output_dir, image_filename.replace(".jpg", ".txt")
        )

        logger.info(f"Converting image {image_filename} to yolo format")

        with open(yolo_txt_file, "w") as f:
            for annotation in coco_json["annotations"]:
                if annotation["image_id"] == image_id:
                    bbox = annotation["bbox"]
                    class_id = annotation["category_id"]
                    x, y, w, h = bbox
                    x_center = (x + w / 2) / image["width"]
                    y_center = (y + h / 2) / image["height"]
                    width = w / image["width"]
                    height = h / image["height"]
                    f.write(
                        f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n"
                    )
                    logger.debug(f"Writing to {yolo_txt_file}")

    logger.info("Conversion complete")


if __name__ == "__main__":
    par_dir = get_root_dir()
    setup_logging(
        log_level=logging.DEBUG,
        log_dir=f"{par_dir}/output/logs",
        log_file="coco_to_yolo_log.txt",
    )
    coco_to_json_converter(
        coco_json_file_path=f"/home/mai/Project/batch4/annotations/instances_default.json",
        coco_to_json_output_dir=f"{par_dir}/outputgit/coco_to_yolo",
    )
