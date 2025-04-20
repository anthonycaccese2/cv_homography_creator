import os
import cv2

class ImageManager:
    """ImageManager"""
    def __init__(self, image_dir):
        self.image_dir = image_dir
        self.images = self._load_images()
        self.index = 0

    def _load_images(self):
        return [f for f in os.listdir(self.image_dir) if f.endswith('.jpg')]

    def has_images(self):
        return len(self.images) > 0

    def current_image_name(self):
        return self.images[self.index]

    def current_image_path(self):
        return os.path.join(self.image_dir, self.current_image_name())

    def current_image(self):
        return cv2.imread(self.current_image_path())

    def next_image(self):
        if self.index < len(self.images) - 1:
            self.index += 1
        else:
            self.index = 0
        return self.current_image()

    def prev_image(self):
        if self.index > 0:
            self.index -= 1
        else:
            self.index = len(self.images) - 1
        return self.current_image()

    def remove_current_image(self):
        if self.has_images():
            self.images.pop(self.index)
            if self.index >= len(self.images):
                self.index = 0