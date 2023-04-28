import cv2
import tkinter as tk
import imutils
import tkinter.filedialog
import pytesseract
import numpy as np
from PIL import Image, ImageTk

class ANPR_GUI:
    def __init__(self, window):
        self.window = window
        self.window.title("ANPR System")
        
        # Create a file input button
        self.input_button = tk.Button(self.window, text="Select Image", command=self.load_image)
        self.input_button.pack(padx=10, pady=10)

        # Create a canvas to display the image
        self.canvas = tk.Canvas(self.window, width=500, height=500)
        self.canvas.pack(padx=10, pady=10)

        # Create a button to perform ANPR
        self.anpr_button = tk.Button(self.window, text="Perform ANPR", command=self.perform_anpr)
        self.anpr_button.pack(padx=10, pady=10)

    def load_image(self):
        # Load the image from file
        self.filename = str(tk.filedialog.askopenfilenames(initialdir="./", title="Select Image", filetypes=(("jpeg files", "*.jpg"), ("png files", "*.png"), ("all files", "*.*"))))
        self.image = cv2.imread(self.filename)
        self.image = imutils.resize(self.image, width=500)
        self.display_image()

    def display_image(self):
        # Convert the image to a PhotoImage and display on the canvas
        self.photo = cv2.cvtColor(self.image,cv2.COLOR_BGR2GRAY)
        self.photo = imutils.resize(self.photo, width=500)
        self.photo = Image.fromarray(self.photo)
        self.photo = ImageTk.PhotoImage(self.photo)
        self.canvas.create_image(0, 0, anchor="nw", image=self.photo)

    def perform_anpr(self):
        # Perform ANPR on the loaded image and display the result
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 2)
        contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        for c in contours:
            if cv2.contourArea(c) < 500:
                continue
            (x, y, w, h) = cv2.boundingRect(c)
            if w / h > 5 or h / w > 5:
                continue
            cv2.rectangle(self.image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        self.display_image()

if __name__ == "__main__":
    window = tk.Tk()
    gui = ANPR_GUI(window)
    window.mainloop()
