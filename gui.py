import os, cv2, face_recognition, subprocess
from tkinter import *
from tkinter import filedialog
import mttkinter

filename = ""

def takePic(name):
    video = cv2.VideoCapture(0)
    # Opens camera using opencv and saves a picture
    while True:
        check, frame = video.read()
        cv2.imshow("Capturing", frame)
        key = cv2.waitKey(1)
        if key % 256 == 32:  # Space button is pressed
            break

    cv2.imwrite("faces\\" + name + ".jpg", frame)
    video.release()
    cv2.destroyAllWindows()

def deletePic(name):
    os.remove("faces\\" + name + ".jpg")

def getEncodings(name):
    img = face_recognition.load_image_file("faces\\" + name + ".jpg")
    return face_recognition.face_encodings(img)

def faceFound(encodings1, encodings2):
    #Iterate through all the faces in the second image
    if True in face_recognition.compare_faces(encodings1[0], encodings2, tolerance=0.40):
        return True
    return False

def isLocked(path):
    check = "Everyone:(OI)(CI)(N)"
    result = str(subprocess.check_output(['icacls', path]))
    if check in result:
        return True
    return False

def makeFacesFolder():
    if not os.path.isdir("faces"):
        os.makedirs("faces")

def lockFolder():
    global filename
    makeFacesFolder()
    picName = filename.replace("/", " ").replace(":", "_")
    print(picName)
    encodings1 = []
    while len(encodings1) != 1:
        takePic(picName)
        encodings1 = getEncodings(picName)
        if len(encodings1) != 1:
            deletePic(picName)
            print("No face detected or too many faces")
    print("Face detected")

    os.system("echo y|cacls " + filename + " /P everyone:n")
    lock.destroy()
    global unlock
    unlock = Button(window, text="Unlock", command=unlockFolder)
    unlock.place(relx=0.5, rely=0.65, anchor=CENTER)

def unlockFolder():
    global filename, lock
    makeFacesFolder()
    picName = filename.replace("/", " ").replace(":", "_") + "(1)"
    encodings2 = []
    while len(encodings2) == 0:
        takePic(picName)
        encodings2 = getEncodings(picName)
        if len(encodings2) == 0:
            deletePic(picName)
            print("No face detected")
    print("Face detected")

    lockPic = filename.replace("/", " ").replace(":", "_")
    print(lockPic)
    encodings1 = getEncodings(lockPic)

    if faceFound(encodings1, encodings2):
        print("Faces match")
        os.system("echo y|cacls " + filename + " /P everyone:f")
        print(filename)
        unlock.destroy()
        lock = Button(window, text="Lock", command=lockFolder)
        lock.place(relx=0.5, rely=0.65, anchor=CENTER)
    else:
        print("Faces dont match")

# Function for opening the
# file explorer window
def browseFiles():
    global filename, lock, unlock
    filename = filedialog.askdirectory(initialdir="/", title="Select a Folder")
    label_file_explorer.configure(text="Folder Selected: " + filename)
    if isLocked(filename):
        lock.destroy()
        global unlock
        unlock = Button(window, text="Unlock", command=unlockFolder)
        unlock.place(relx=0.5, rely=0.65, anchor=CENTER)
    else:
        unlock.destroy()
        lock = Button(window, text="Lock", command=lockFolder)
        lock.place(relx=0.5, rely=0.65, anchor=CENTER)


window = Tk()
window.title('FaceLock')
window.geometry("400x200")
window.config(background="white")
label_file_explorer = Label(window,
                            text="File Explorer",
                            width=100, height=4,
                            fg="blue")

button_explore = Button(window,
                        text="Browse Files",
                        command=browseFiles)

lock = Button(window, text="Lock", command=lockFolder)
unlock = Button(window, text="Unlock", command=unlockFolder)

label_file_explorer.place(relx=0.5, rely=0.15, anchor=CENTER)
button_explore.place(relx=0.5, rely=0.5, anchor=CENTER)

# Let the window wait for any events
window.mainloop()