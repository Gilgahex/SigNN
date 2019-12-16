import os
import sys
import json

from PIL import Image, ImageOps
import cv2



# Instructions:
# 1. Make sure mediapipe_feed_data.py is in same directory
# 2. Put all images in folders in current directory, name folder after what image represents
# 3. run "python3 mediapipe_mass_feed_data.py"

OUTPUT_FILE = "training_data.json"
BASE_RESOLUTION = (1920, 1920)
SCRIPT_PATH = None

def setResolution(path, resolution):
    assert isinstance(path, str), "Is actually {} with value {}".format(type(path), path)
    assert isinstance(resolution, tuple)
    assert len(resolution) == 2
    im = Image.open(path)
    im = ImageOps.fit(im, resolution)
    im.save(path, dpi=resolution)

def runMediapipe(filename, mediapipe_directory, outputname):
    command = "python mediapipe_feed_data.py --input={} --mediapipe_directory={}".format(filename, mediapipe_directory)
    stream = os.popen(command)
    output = stream.read()
    result = json.loads(output)
    return [x for x in result[::3] if any(y for y in x)]

def createVideosfromPhoto(absolutePath, word):
    assert isinstance(absolutePath, str)
    output_file = word + ".avi"
    output_file = os.path.join(absolutePath, output_file)
    try:
        os.remove(output_file)
    except:
        pass
    primer = os.path.join(SCRIPT_PATH, "primer.jpg")


    images = [os.path.join(absolutePath, img) for img in os.listdir(absolutePath) if img.endswith(".jpg") or img.endswith(".png")]
    [setResolution(img, BASE_RESOLUTION) for img in images]
    setResolution(primer, BASE_RESOLUTION)

    video = cv2.VideoWriter(output_file, 0, 1, (1920, 1920))
    for image in images:
        video.write(cv2.imread(primer))
        video.write(cv2.imread(image))
        video.write(cv2.imread(image))

    cv2.destroyAllWindows()
    video.release()
    return output_file

def getMediapipeDirectory():
    MEDIAPIPE_DIRECTORY = None
    while MEDIAPIPE_DIRECTORY is None or not os.path.isdir(MEDIAPIPE_DIRECTORY):
        if MEDIAPIPE_DIRECTORY:
            print("Invalid directory!")
        MEDIAPIPE_DIRECTORY = input("Please enter mediapipe absolute directory:\n")  
        # if not os.path.isabs(MEDIAPIPE_DIRECTORY):
        #     MEDIAPIPE_DIRECTORY = None
        #     print("Must be an absolute path!")
        if MEDIAPIPE_DIRECTORY and MEDIAPIPE_DIRECTORY[-1] != "/":
            MEDIAPIPE_DIRECTORY += "/"      
    return MEDIAPIPE_DIRECTORY

def main():
    global SCRIPT_PATH
    pathname = os.path.dirname(sys.argv[0]) 
    SCRIPT_PATH = os.path.abspath(pathname)

    MEDIAPIPE_DIRECTORY = getMediapipeDirectory()
    
    CURRENT_PATH = os.getcwd()
    RESULTS = {}
    for file in os.listdir(CURRENT_PATH):
        full_path = os.path.join(CURRENT_PATH, file)
        if os.path.isdir(full_path):
            file_name = createVideosfromPhoto(full_path, file)
            RESULTS[file] = runMediapipe(file_name, MEDIAPIPE_DIRECTORY, file)
            print("{} done".format(file))
            

    file = open(OUTPUT_FILE, "w+")
    json.dump(RESULTS, file)


if __name__ == "__main__":
    main()