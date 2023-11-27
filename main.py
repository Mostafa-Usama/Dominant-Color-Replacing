import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox


def replace_color(image, target_color, replacement_color, tolerance=25):
  
    lower_bound = np.array([max(0, c - tolerance) for c in target_color])
    upper_bound = np.array([min(255, c + tolerance) for c in target_color])
    mask = cv.inRange(image, lower_bound, upper_bound)
    image[np.where(mask != 0)] = replacement_color
    return image

def extract_dominant_color(image):
    
    pixels = image.reshape((-1, 3))
    pixels = np.float32(pixels)
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 10, 0.1)
    _, _, center = cv.kmeans(pixels, 1, None, criteria, 10, cv.KMEANS_RANDOM_CENTERS)
    
    center = np.uint8(center)
    dominant_color = center[0]
    color = dominant_color[::-1]
    # print(color)
    plt.imshow([[color]])
    plt.title("Most Dominant Color")
    plt.show()
    return dominant_color

def browse_file():
    file_path = filedialog.askopenfilename()
    url.delete("1.0", tk.END )
    url.insert(tk.END, file_path)

def replace(file_path, red, green, blue):
    
    try:
        image = cv.imread(file_path)
        cv.imshow("Before", image)
        cv.waitKey(0)
        dominant_color = extract_dominant_color(image)
        try:
            red = int(red)
            blue = int(blue)
            green = int(green)
            if (red >= 0 and red <= 255) and (blue >= 0 and blue <= 255) and (green >= 0 and green <= 255):
                replacement = [red, green, blue]
                # print(dominant_color)
                output = replace_color(image, dominant_color, replacement)
                cv.imshow("After", output)
                cv.waitKey(0)
            else:
                messagebox.showerror("Error", "Make sure the values are between 0 and 255 inclusive")
        except:
            messagebox.showerror("Error", "Make sure you entered correct RGB value")
    except:
        messagebox.showerror("Error", "Wrong Image Fromat")


root = tk.Tk()
root.title("DCR")
root.geometry("500x500")
root.resizable(False, False)

primary = "#1E90FF"

title = tk.Label(root, text="Dominant Color Replacer", font=("Arial",16),fg=primary)
title.place(x=130, y=10)

hint = tk.Label(root, text="Please Select An Image from your computer", font=("Arial",13), fg=primary )
hint.place(x=80, y=200)
url = tk.Text(root,height=1, width=50)
url.place(x=40, y=250)
browse_button = tk.Button(root, text="Browse", command=browse_file, width=15, fg="white", bg=primary)
browse_button.place(x=190, y=300)


hint2 = tk.Label(root, text="Please Select The Values Of Red, Green, And Blue", font=("Arial",13), fg=primary )
hint2.place(x=60, y=350)

red = tk.Text(root,height=1, width=10)
green = tk.Text(root,height=1, width=10)
blue = tk.Text(root,height=1, width=10)

red.place(x=100, y=400)
green.place(x=200, y=400)
blue.place(x=300, y=400)

replace_button = tk.Button(root, text="Replace", command=lambda:replace(url.get("1.0", "end-1c"  ), blue.get("1.0", tk.END), green.get("1.0", tk.END), red.get("1.0", tk.END)), width=15, fg="white", bg=primary)
replace_button.place(x=190, y=450)


root.mainloop()