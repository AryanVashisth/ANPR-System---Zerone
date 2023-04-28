import cv2
import tkinter as tk
import tkinter.filedialog
import pytesseract
import numpy as np
from PIL import Image, ImageTk

class ANPR_GUI:
    def __init__(self, window, title):
        self.window = window
        self.window.title(title)
        
        # Create a canvas to display the image
        self.canvas = tk.Canvas(self.window, width=400, height=400)
        self.canvas.pack()
        
        # Create a button to open an image file
        self.open_button = tk.Button(self.window, text="Open Image", command=self.open_image)
        self.open_button.pack(side=tk.LEFT)
        
        # Create a button to perform ANPR on the image
        self.anpr_button = tk.Button(self.window, text="ANPR", command=self.anpr)
        self.anpr_button.pack(side=tk.LEFT)
        
        # Create a button to quit the program
        self.quit_button = tk.Button(self.window, text="Quit", command=self.window.quit)
        self.quit_button.pack(side=tk.LEFT)
        
        # Initialize image and filename
        self.img = None
        self.filename = None
    
    def open_image(self):
        # Open a file dialog to choose an image file
        self.filename = tk.filedialog.askopenfilenames(initialdir="/", title="Select File", filetypes=(("jpg files", "*.jpg"),))
        # Load the image and display it on the canvas
        self.img = cv2.imread(self.filename)
       
        img = cv2.cvtColor(self.img,cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(img)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=img)
        self.canvas.image = img
    
    def anpr(self):
        if self.img is not None:
           pytesseract.pytesseract.tesseract_cmd = r'C:\Tesseract-OCR\tesseract.exe'     
cascade = cv2.CascadeClassifier("haarcascade_russian_plate_number.xml")
 
def extract_num(img_name):
    global read
    img   = cv2.imread(img_name)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    nplate = cascade.detectMultiScale(gray,1.1,4)
    
    for(x,y,w,h) in nplate: 
        #CROPPING NUMBER PLATE
        a,b =(int(0.02*img.shape[0]), int(0.025*img.shape[1]))
        plate = img[y+a:y+h-a, x+b:x+w-b, :]
        
        #IMAGE PROCESSING USING THRESHOLD TECHNIQUE
        kernel= np.ones((1,1), np.uint8)
        plate = cv2.dilate(plate, kernel, iterations=1 )
        plate = cv2.erode(plate, kernel, iterations=1)
        plate_gray= cv2.cvtColor(plate,cv2.COLOR_RGB2GRAY)
        (thresh, plate) = cv2.threshold(plate_gray, 127, 255, cv2.THRESH_BINARY_INV)
        
        read= pytesseract.image_to_string(plate)
        read = ''.join(e for e in read if e.isalnum())  #only alphanumeric character will print alnum=alphanumeric
        print(read)
        
        cv2.rectangle(img, (x,y), (x+w, y+h), (51,51,255), 2)
        cv2.rectangle(img, (x, y - 40), (x+w, y), (51,51,255), -1)
        fontScale= 1
        color= (255,255,255) #white color
        thickness= 2
        cv2.putText(img, read, (x,y-10), cv2.FONT_HERSHEY_SIMPLEX, fontScale, color, thickness, cv2.LINE_AA, False)
        
        #cv2.imshow('Scanned Plate',plate)
    
    #cv2.imshow("Result", img) 
    #cv2.imwrite('result.jpg',img)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
        
#extract_num()

# Create the GUI window
window = tk.Tk()

# Create the ANPR GUI object
anpr_gui = ANPR_GUI(window, "ANPR System")

# Start the main event loop
window.mainloop()