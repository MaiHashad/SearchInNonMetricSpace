from tkinter import Tk, Canvas
from PIL import ImageTk, Image

def pic_choice(pic1,pic2):
    

    root = Tk()

    #Create a canvas
    canvas = Canvas(root, width=600, height=300)
    canvas.pack()

    # Load the image file
    im = Image.open(pic1 + '.jpg')
    im2 = Image.open(pic2 + '.jpg')
    im = im.resize((250,250), Image.ANTIALIAS)
    im2 = im2.resize((250,250), Image.ANTIALIAS)
    # Put the image into a canvas compatible class, and stick in an
    # arbitrary variable to the garbage collector doesn't destroy it
    canvas.image = ImageTk.PhotoImage(im)
    canvas.image2 = ImageTk.PhotoImage(im2)

    # Add the image to the canvas, and set the anchor to the top left / north west corner
    canvas.create_image(0, 0, image=canvas.image, anchor='nw')
    canvas.create_image(270, 0, image=canvas.image2, anchor='nw')
    #canvas.move(canvas.image2, 960, 0)
    root.mainloop()
    choice = input("Do you think picture 1 or 2 is closer to query picture")
    while choice != '1' and choice != '2':
        choice = input("Do you think picture 1 or 2 is closer to query picture")
    if choice == '1':
        return pic1
    
    return pic2

print(pic_choice('0','1'))