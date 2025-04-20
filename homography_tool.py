import numpy as np
import cv2

class HomographyTool:
    """HomographyTool"""
    def __init__(self):
        self.points = []
        self.homography_image = np.zeros((0, 0))

    def add_point(self, x, y):
        if len(self.points) < 4:
            self.points.append([x, y])

    def clear_points(self):
        self.points = []

    def compute_homography(self, src_img, scale_x, scale_y):
        if len(self.points) != 4:
            raise ValueError("Exactly 4 points required.")

        scaled_pts = [[p[0] * scale_x, p[1] * scale_y] for p in self.points]
        dst_pts = [[0, 0],
                   [src_img.shape[1], 0],
                   [src_img.shape[1], src_img.shape[0]],
                   [0, src_img.shape[0]]]

        h, _ = cv2.findHomography(np.array(scaled_pts), np.array(dst_pts))
        self.homography_image = cv2.warpPerspective(src_img, h, (src_img.shape[1], src_img.shape[0]))
        return self.homography_image

    def save_homography(self, output_path):
        if self.homography_image.size == 0:
            raise ValueError("No homography image to save.")
        cv2.imwrite(output_path, self.homography_image)
        self.homography_image = np.zeros((0, 0))
        self.points = []

    def get_result_image(self):
        """Return the warped image if homography has been computed."""
        return self.homography_image  # or whatever attribute holds the warped result
