import os
import tkinter as tk
from tkinter import Label, Button
import cv2
from PIL import Image, ImageTk

class HomographyUI:
    """GUI for selecting points and computing homography."""

    def __init__(self, root, image_manager, homography_tool):
        self.root = root
        self.image_manager = image_manager
        self.homography_tool = homography_tool

        self.canvas_width = 1008
        self.canvas_height = 756
        self.scale_x = 1.0
        self.scale_y = 1.0

        self.image_label = Label(root)
        self.image_label.place(x=0, y=30)
        self.label_text = Label(root, font=("Courier", 14))
        self.label_text.pack()

        self.init_buttons()
        self.bind_events()
        self.update_display()

    def init_buttons(self):
        """Initialize UI buttons."""
        Button(self.root, text=" < ", command=self.prev_image, bg="white").pack(
            side="left", padx=10
        )
        Button(self.root, text=" > ", command=self.next_image, bg="white").pack(
            side="right", padx=10
        )
        Button(
            self.root,
            text="Generate Homography",
            command=self.generate_homography,
            bg="white",
        ).pack(side="bottom", pady=10)
        Button(
            self.root, text="Save", command=self.save_homography, bg="white"
        ).place(relx=0.01, rely=0.005, anchor="nw")
        Button(
            self.root, text="Refresh", command=self.refresh, bg="white"
        ).place(relx=0.99, rely=0.005, anchor="ne")

    def bind_events(self):
        """Bind mouse and keyboard events."""
        self.root.bind("<Button-1>", self.add_point)
        self.root.bind("<BackSpace>", lambda event: self.clear_points())

    def update_display(self):
        """Display the current image with any selected points."""
        img = self.image_manager.current_image()
        if img is not None:
            self.scale_x = img.shape[1] / self.canvas_width
            self.scale_y = img.shape[0] / self.canvas_height
            img_resized = cv2.resize(img, (self.canvas_width, self.canvas_height))

            for pt in self.homography_tool.points:
                cv2.circle(img_resized, (int(pt[0]), int(pt[1])), 5, (0, 0, 255), -1)

            self.to_tk_image(img_resized)
        self.update_label()

    def to_tk_image(self, img):
        """Convert OpenCV image to ImageTk for display."""
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(img_rgb)
        photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=photo)
        self.image_label.image = photo

    def add_point(self, event):
        """Add a point to the list if in image region."""
        if event.y > 15:
            self.homography_tool.add_point(event.x, event.y)
            self.update_display()

    def clear_points(self):
        """Clear selected points."""
        self.homography_tool.clear_points()
        self.update_display()

    def generate_homography(self):
        """Compute the homography using selected points."""
        try:
            src_img = self.image_manager.current_image()
            self.homography_tool.compute_homography(
                src_img, self.scale_x, self.scale_y
            )
            print("Homography generated.")
        except Exception as error:
            print("Error generating homography:", error)

    def save_homography(self):
        """Save the computed homography image."""
        try:
            img_name = self.image_manager.current_image_name()
            output_path = os.path.join(
                "images", "outputs", f"Homography_{img_name}"
            )
            self.homography_tool.save_homography(output_path)
            self.image_manager.remove_current_image()
            self.update_display()
        except Exception as error:
            print("Error saving homography:", error)

    def next_image(self):
        """Display the next image."""
        self.image_manager.next_image()
        self.homography_tool.clear_points()
        self.update_display()

    def prev_image(self):
        """Display the previous image."""
        self.image_manager.prev_image()
        self.homography_tool.clear_points()
        self.update_display()

    def refresh(self):
        """Reload image list from directory."""
        self.image_manager.reload()
        self.update_display()

    def update_label(self):
        """Update the status label with current image info."""
        if self.image_manager.has_images():
            self.label_text.config(
                text=(
                    f"Image: {self.image_manager.current_image_name()}; "
                    f"Unprocessed: {len(self.image_manager.images)}"
                )
            )
        else:
            self.label_text.config(
                text="List empty: Add images to /images/jpg and click refresh"
            )