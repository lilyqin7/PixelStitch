# import tkinter as tk
# from cmu_graphics import *

# def onAppStart(app):
# # Create the tkinter window
#     root = tk.Tk()
#     root.title("Scrollable CMU Graphics")
#     root.geometry('800x500')

# # Create a tkinter frame and canvas
#     frame = tk.Frame(root)
#     frame.pack(fill=tk.BOTH, expand=True)

#     canvas = tk.Canvas(root, width = 800, height = 500, bg = 'white')
#     canvas.pack()

# # Add scrollbar to the canvas
#     scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
#     scrollbar.pack(side=tk.RIGHT, fill="y")

#     canvas.config(yscrollcommand=scrollbar.set)

# # Create a frame that will be used to embed CMU Graphics into the tkinter canvas
#     cmu_frame = tk.Frame(canvas)

# # Create a window inside tkinter canvas to hold the CMU Graphics content
#     canvas.create_window((0, 0), window=cmu_frame, anchor="nw")

#     root.mainloop()

# def redrawAll(app):
#     drawCircle(5, 5, 40)

# def main():
#     runApp(width=800, height=500)

# main()


import tkinter as tk
from PIL import Image, ImageTk

# Create a tkinter window
root = tk.Tk()
root.title("Background Image with Scrollbar")

# Create a canvas and a vertical scrollbar
canvas = tk.Canvas(root)
canvas.pack(side="left", fill="both", expand=True)

scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")

canvas.config(yscrollcommand=scrollbar.set)

# Load the background image using PIL (Pillow)
bg_image = Image.open("background.jpg")  # Replace with your image file path
bg_photo = ImageTk.PhotoImage(bg_image)

# Place the background image on the canvas
background = canvas.create_image(0, 0, anchor="nw", image=bg_photo)

# Set the scroll region of the canvas to match the size of the image
canvas.config(scrollregion=canvas.bbox("all"))

# Add some content over the image (optional)
canvas.create_text(300, 200, text="Scroll with the image!", font=("Arial", 24), fill="white")

# Main tkinter loop
root.mainloop()
