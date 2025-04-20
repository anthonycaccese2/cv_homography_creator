import tkinter as tk
from image_manager import ImageManager
from homography_tool import HomographyTool
from ui import HomographyUI
import config

def main():
    """Main for the homography application."""
    root = tk.Tk()
    root.geometry(config.DEFAULT_GEOMETRY)
    image_manager = ImageManager(config.IMAGE_DIR)
    homography_tool = HomographyTool()
    ui = HomographyUI(root, image_manager, homography_tool)
    root.mainloop()

if __name__ == "__main__":
    main()