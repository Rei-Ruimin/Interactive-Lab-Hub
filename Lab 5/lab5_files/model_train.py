from teachable_machine_lite import TeachableMachineLite

print("SURVIVED 5")

model_path = 'models/model.tflite'
image_file_name = "frame.jpg"
labels_path = "models/labels.txt"

tm_model = TeachableMachineLite(model_path=model_path, labels_file_path=labels_path)

print("SURVIVED 6")
