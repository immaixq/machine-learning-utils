import matplotlib.pyplot as plt
import matplotlib.patches as patches
from shapely.geometry import Polygon as ShapelyPolygon
from matplotlib.patches import Polygon as MatplotlibPolygon
import cv2
import logging
from utils.logger_config import setup_logging
import numpy as np

setup_logging(
    log_level=logging.INFO, log_dir="output/logs", log_file="visualiser_log.txt"
)
logger = logging.getLogger(__name__)


class Visualizer:
    def __init__(self, img_path):
        self.img_path = img_path
        self.img = cv2.imread(img_path)
        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        self.img_height, self.img_width = self.img.shape[:2]

    def visualise_yolo_bounding_box(self, annotation_txt_file, class_labels=None):
        logger.info("Visualising YOLO annotation in bounding box")
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
            print(annotation)
            class_label, x_center, y_center, width, height = annotation
            x_min = int((x_center - width / 2) * self.img_size)
            x_max = int((x_center + width / 2) * self.img_size)
            y_min = int((y_center - height / 2) * self.img_size)
            y_max = int((y_center + height / 2) * self.img_size)

            class_label_txt = (
                class_labels[int(class_label)] if class_labels else class_label
            )
            class_label = f"{class_label_txt}"
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

    def visualise_yolo_segmentation(self, annotation_txt_file, class_labels=None):
        logger.info("Visualising YOLO annotation in segmentation")
        try:
            with open(annotation_txt_file, "r") as f:
                annotation_lines = f.readlines()
        except Exception as e:
            logger.error(f"Error while reading annotation txt file: {e}")
            return

        fig, ax = plt.subplots()

        for annotation in annotation_lines:
            annotation = annotation.strip().split(" ")
            class_id = int(annotation[0])
            segmentation_points = list(map(float, annotation[1:]))
            # Reshape points to pairs of x,y coordinates
            segment_coordinates = np.array(segmentation_points).reshape(-1, 2)
            print(segment_coordinates)
            segment_coordinates[:, 0] = segment_coordinates[:, 0] * self.img_width
            segment_coordinates[:, 1] = segment_coordinates[:, 1] * self.img_height
            polygon = MatplotlibPolygon(
                segment_coordinates, closed=True, fill=True, edgecolor="red"
            )
            ax.add_patch(polygon)

        plt.imshow(self.img)
        plt.show()


if __name__ == "__main__":
    img_path = "/home/mai/Project/dbst-model-training/yolo/data/batch1/images/train/20230904_152225_000701.jpg"
    annotation_txt = "/home/mai/Project/dbst-model-training/yolo/data/batch1/labels/train/20230904_152225_000701.txt"

    class_labels = {
        0: "Cartons",
        1: "Bottle",
        2: "Cans",
        3: "Jars",
        4: "Sacks",
        5: "Pallet",
        6: "Rack Location Code",
    }

    visualiser = Visualizer(img_path)

    visualiser.visualise_yolo_segmentation(annotation_txt)
    # visualiser.visualise_yolo_bounding_box(annotation_txt, class_labels=class_labels)
