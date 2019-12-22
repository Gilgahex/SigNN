import os
import sys
import getopt
import json

def processMediapipeData(data):
    processed = []
    
    for frame in data:
        if not frame:
            continue
        for hand in frame:
            processed.append(hand)
    
    return processed

def runMediapipe(filename, mediapipe_directory):
    assert isinstance(filename, str)
    assert isinstance(mediapipe_directory, str)

    command = ""
    if mediapipe_directory:
        command = "cd {}; ".format(mediapipe_directory)
    command += "sudo GLOG_logtostderr=0 bazel-bin/mediapipe/examples/desktop/multi_hand_tracking/multi_hand_tracking_cpu --calculator_graph_config_file=mediapipe/graphs/hand_tracking/multi_hand_tracking_desktop_console_logger.pbtxt --input_video_path={}".format(filename)

    stream = os.popen(command)
    output = stream.read()
    if output:
        return json.loads(output)
    return []



def main():
    fullCmdArguments = sys.argv
    argumentList = fullCmdArguments[1:]
    args = getopt.getopt(argumentList,'', ("input=", "mediapipe_directory=", "output="))[0]
    INPUT_FILE = ""
    OUTPUT_FILE = ""
    MEDIAPIPE_DIRECTORY = ""

    for arg in args:
        if len(arg) > 1:
            value = arg[1]
            arg = arg[0]
        else:
            value = None

        if arg == "--input":
            INPUT_FILE = value
        elif arg == "--mediapipe_directory":
            MEDIAPIPE_DIRECTORY = value
        elif arg == "--output":
            assert value.split(".")[-1] == "json", "Output file must be json"
            OUTPUT_FILE = value
        else:
            raise Exception("{} is not a valid argument!".format(arg))

    assert INPUT_FILE, "--input= argument required"
    assert MEDIAPIPE_DIRECTORY, "--mediapipe_directory= argument required"
    # assert os.path.isdir(MEDIAPIPE_DIRECTORY), "{} is not a valid directory".format(MEDIAPIPE_DIRECTORY)

    if OUTPUT_FILE:
        file = open(OUTPUT_FILE, "w+")
    result = processMediapipeData(runMediapipe(INPUT_FILE, MEDIAPIPE_DIRECTORY))
    if OUTPUT_FILE:
        # file.write(result)
        json.dump(result, file)
        file.close()
    else:
        print(result)
    return 1



if __name__ == "__main__":
    main()