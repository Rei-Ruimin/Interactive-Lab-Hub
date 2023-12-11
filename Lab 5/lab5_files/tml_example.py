from collections import deque
import random
from teachable_machine_lite import TeachableMachineLite
import cv2 as cv
import pygame  # Import the pygame library

# Initialize Pygame's mixer module
pygame.mixer.init()

# Dictionary of sounds for each result ID
sounds_for_id = {
    1: ['path_to_sound1_for_id_1.mp3', 'path_to_sound2_for_id_1.mp3', 'path_to_sound3_for_id_1.mp3'],
    2: ['path_to_sound1_for_id_2.mp3', 'path_to_sound2_for_id_2.mp3', 'path_to_sound3_for_id_2.mp3'],
    3: ['path_to_sound1_for_id_3.mp3', 'path_to_sound2_for_id_3.mp3', 'path_to_sound3_for_id_3.mp3']
}

# Stability check parameters
stability_threshold = 5  # Number of frames to consider the result stable
result_history = deque(maxlen=stability_threshold)

cap = cv.VideoCapture(0)

model_path = 'water_bottle.tflite'
image_file_name = "frame.jpg"
labels_path = "labels.txt"

tm_model = TeachableMachineLite(model_path=model_path, labels_file_path=labels_path)

previous_id = None

while True:
    ret, frame = cap.read()
    cv.imshow('Cam', frame)
    cv.imwrite(image_file_name, frame)
    
    results = tm_model.classify_frame(image_file_name)
    print("results:", results)
    
    current_id = results['id']
    result_history.append(current_id)
    
    # Check if the result is stable
    if (len(result_history) == stability_threshold and
        len(set(result_history)) == 1 and
        current_id in [1, 2, 3] and
        current_id != previous_id):
        sound_path = random.choice(sounds_for_id[current_id])
        sound = pygame.mixer.Sound(sound_path)
        sound.play()
        previous_id = current_id
    
    k = cv.waitKey(1)
    if k % 256 == 27:
        # press ESC to close camera view.
        break

cap.release()
cv.destroyAllWindows()
