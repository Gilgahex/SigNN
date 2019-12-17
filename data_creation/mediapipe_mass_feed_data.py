import os
import sys
import json

from PIL import Image, ImageOps
import cv2
import time


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
    if output:
        result = json.loads(output)
        return [x for x in result[1::2] if any(y for y in x)]
    return []

class TrainingImage():
    def __init__(self, path):
        assert isinstance(path, str)
        self.path = path
    def testBad(self, output_file, primer, mediapipeDirectory):
        testVideo = createVideoFromImages([self,], output_file, primer)
        result = runMediapipe(testVideo, mediapipeDirectory, output_file)
        if len(result) != 1:
            print("{} had {} hands in it".format(self.path, len(result)))
            self.destroy()
            return True
        return False
    def destroy(self):
        print("{} destroyed".format(self.path))
        os.remove(self.path)
        del self
        
         


def getImagesInFolder(absolutePath):
    assert isinstance(absolutePath, str)
    images = [TrainingImage(os.path.join(absolutePath, img)) for img in os.listdir(absolutePath) if img.endswith(".jpg") or img.endswith(".png")]
    [setResolution(img.path, BASE_RESOLUTION) for img in images]
    return images

def createVideoFromImages(images, output_name, primer=None):
    assert isinstance(images, list)
    assert all(isinstance(x, TrainingImage) for x in images)
    assert isinstance(output_name, str)
    assert primer is None or isinstance(primer, str)
    video = cv2.VideoWriter(output_name, 0, 1, BASE_RESOLUTION)
    for image in images:
        video.write(cv2.imread(primer))
        video.write(cv2.imread(image.path))
    cv2.destroyAllWindows()
    video.release()
    return output_name



def photoToJSON(absolutePath, word, mediapipeDirectory):
    ALL_IMAGES = getImagesInFolder(absolutePath)
    output_file = word + ".avi"
    output_file = os.path.join(absolutePath, output_file)
    original_image_count = len(ALL_IMAGES)

    primer = os.path.join(SCRIPT_PATH, "primer.jpg")
    video = createVideoFromImages(ALL_IMAGES, output_file, primer)
    result = runMediapipe(video, mediapipeDirectory, word)
    if len(ALL_IMAGES) != len(result):
        ALL_IMAGES = [x for x in ALL_IMAGES if not x.testBad(output_file, primer, mediapipeDirectory)]
        video = createVideoFromImages(ALL_IMAGES, output_file, primer)
        result = runMediapipe(video, mediapipeDirectory, word)
            
    if original_image_count != len(ALL_IMAGES):
        print("{} images used out of {}".format(len(ALL_IMAGES), original_image_count))

    return result

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
            # file_name = createVideosfromPhoto(full_path, file)
            # RESULTS[file] = runMediapipe(file_name, MEDIAPIPE_DIRECTORY, file)
            RESULTS[file] = photoToJSON(full_path, file, MEDIAPIPE_DIRECTORY)
            print("{} done".format(file))
            

    file = open(OUTPUT_FILE, "w+")
    json.dump(RESULTS, file)


if __name__ == "__main__":
    main()