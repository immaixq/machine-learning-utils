import matplotlib.pyplot as plt
import matplotlib.patches as patches
import cv2
import logging
from utils.logger_config import setup_logging

setup_logging(
    log_level=logging.INFO, log_dir="output/logs", log_file="visualiser_log.txt"
)
logger = logging.getLogger(__name__)


class Visualizer:
    def __init__(self, img_path):
        self.img_path = img_path
        self.img = cv2.imread(img_path)
        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        self.img_size = self.img.shape[0]

    def visualise_yolo(self, annotation_txt_file):
        logger.info("Visualising YOLO annotation")
        try:
            with open(annotation_txt_file, "r") as f:
                annotation_txt_file = f.readlines()
        except Exception as e:
            logger.error(f"Error while reading annotation txt file: {e}")
            return

        # draw bounding boxes
        for annotation in annotation_txt_file:
            annotation = annotation.strip().split(" ")
            annotation = [float(i) for i in annotation]
            class_label, x_center, y_center, width, height = annotation
            x_min = int((x_center - width / 2) * self.img_size)
            x_max = int((x_center + width / 2) * self.img_size)
            y_min = int((y_center - height / 2) * self.img_size)
            y_max = int((y_center + height / 2) * self.img_size)

            class_label_txt = class_labels[int(class_label)] if class_labels else class_label
            class_label = f"{class_label_txt}: {round(x_center, 3)}, {round(y_center, 3)}, {round(width, 3)}, {round(height, 3)}"
            cv2.rectangle(self.img, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
            cv2.putText(
                self.img,
                str(class_label),
                (x_min, y_min - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2,
            )

        plt.imshow(self.img)
        plt.show()


if __name__ == "__main__":
    img_path = "/home/mai/Project/batch4/images/0.jpg"
    annotation_txt = (
        "/home/mai/Project/machine-learning-utils/output/coco_to_yolo/0.txt"
    )

    visualiser = Visualizer(img_path)
    visualiser.visualise_yolo(annotation_txt)
