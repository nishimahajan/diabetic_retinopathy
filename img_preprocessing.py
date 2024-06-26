
# # Apply bilateral filtering for noise reduction
# bilateral_filtered_image = cv2.bilateralFilter(binary_image, d=9, sigmaColor=75, sigmaSpace=75)

# # Apply a top-hat transform for enhancing vessel-like structures
# kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
# tophat = cv2.morphologyEx(image, cv2.MORPH_TOPHAT, kernel)

# new code

import cv2
import numpy as np
from keras.preprocessing.image import ImageDataGenerator
import random
import os
from imutils import paths
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img

num_classes = 5
img_size = (224,224)  #depends on model
batch_size = 32 #depends on model
data = []
labels = []

# Data augmentation using ImageDataGenerator (optional)
train_data_gen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

test_data_gen = ImageDataGenerator(rescale=1./255)

train_generator = train_data_gen.flow_from_directory(
        'path',  # this is the target directory
        target_size= img_size,  # all images will be resized to 224x 224
        batch_size=batch_size,
        class_mode='categorical')  # for multi-class classification

validation_generator = test_data_gen.flow_from_directory(
        'path',
        target_size=img_size,
        batch_size=batch_size,
        class_mode='categorical')

imagePaths = sorted(list(paths.list_images("path")))

random.seed(42)
random.shuffle(imagePaths)

# loop over the input images
for imagePath in imagePaths:
    # load the image, pre-process it, and store it in the data list
    image = cv2.imread(imagePath)
    if image is None:
        continue
    # Load the retinal image
    image = cv2.imread('retinal_image.jpg', cv2.IMREAD_COLOR)  # Load in color

    # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    clahe_image = clahe.apply(image)

    # Apply Canny edge detection
    edges = cv2.Canny(clahe_image, 30, 150)  # Adjust thresholds as needed

    # Apply thresholding to segment retinal features
    _, binary_image = cv2.threshold(edges, 50, 255, cv2.THRESH_BINARY)

    # Apply morphological opening for noise reduction
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(binary_image, cv2.MORPH_OPEN, kernel)

    # Apply vessel segmentation using morphological operations
    kernel = np.ones((5, 5), np.uint8)
    vessel_segmentation = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    vessel_segmentation = cv2.morphologyEx(
    vessel_segmentation, cv2.MORPH_OPEN, kernel)

    # # Save the preprocessed image and vessel segmentation result
    # cv2.imwrite('preprocessed_retinal_image.jpg', vessel_segmentation)
    new_image = img_to_array(vessel_segmentation)
    data.append(new_image)

    label = imagePath.split(os.path.sep)[-2]
    labels.append(label)