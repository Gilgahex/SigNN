import numpy as np
import tensorflow as tf

# Load TFLite model and allocate tensors.

hand_landmark = #"YOUR_PROJECT_PATH+/mediapipe/models/hand_landmark.tflite"
interpreter = tf.lite.Interpreter(model_path=hand_landmark_3D)
interpreter.allocate_tensors()

# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Test model on random input data.
input_shape = input_details[0]['shape']

print(input_shape)

input_data = np.array(np.random.random_sample(input_shape), dtype=np.float32)

interpreter.set_tensor(input_details[0]['index'], input_data)

interpreter.invoke()

# The function `get_tensor()` returns a copy of the tensor data.
# Use `tensor()` in order to get a pointer to the tensor.
output_data = interpreter.get_tensor(output_details[0]['index'])

print("Output Data:", output_data)
print("Output Len:", len(output_data[0]))
