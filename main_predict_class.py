import cv2
import numpy as np
from keras.models import load_model
from tkinter import filedialog
from tkinter import *
from header import alphabet
import os
import sys
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
def openImage(root):
    root.filename = filedialog.askopenfilename(initialdir="/test", title="Select file",filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
    return root.filename

def image_to_feature_vector(image, size=(32, 32)):
    # resize the image to a fixed size, then flatten the image into
	# a list of raw pixel intensities
	return cv2.resize(image, size).flatten()

# returns a compiled model
# identical to the previous one
print("[INFO] Load Model...")
model = load_model('model.h5')

print("[ASK] Do you want predict image? (Y/N)")
answer = input()

while answer:
    if answer == 'Y' or answer == 'y':
        root = Tk()
        imagePath = openImage(root)
        img = cv2.imread(imagePath)
        root.destroy()
        if img is not None:
            drive, path_and_file = os.path.splitdrive(imagePath)
            path, file = os.path.split(path_and_file)
            label = file.split(".")[0]

            data = []
            features = image_to_feature_vector(img)
            data.append(features)
            test = np.array(data) / 255.0

            #classes = model.predict_classes(test)
            probas = model.predict(test)
            classes = probas.argmax(axis=-1)

            #print(label, alphabet.Alphabet.printAlphabet(classes[0]))
            print("[PREDICT] Actual Class =", label, ", Predict Class =",alphabet.Alphabet.printAlphabet(classes))
        else:
            print("[INFO] Image can't be read")
    elif  answer == 'N' or answer == 'n':
        sys.exit()
    else:
        print("[INFO] Answer must Y/N!")
    print("\n[ASK] Do you want predict image again? (Y/N)")
    answer = input()


