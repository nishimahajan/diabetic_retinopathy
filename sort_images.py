import pandas as pd
import shutil
import os

# Load the dataset CSV file (replace 'dataset.csv' with your dataset file)
dataset_file = "C:\\Users\\Nishi Mahajan\\Desktop\\python\\ML\\ML\\DR 2.0\\trainLabels.csv\\trainLabels.csv"
df = pd.read_csv(dataset_file)
labels_column = 'level'

image_path_column = 'image'
output_folder = "C:\\Users\\Nishi Mahajan\\Desktop\\python\\ML\\ML\\DR 2.0\\train\\"
os.makedirs(output_folder, exist_ok=True)
missing_images=[]
for index, row in df.iterrows():
    level = row[labels_column]
    image = "C:\\Users\\Nishi Mahajan\\Desktop\\python\\ML\\ML\\DR 2.0\\train\\train\\"+row[image_path_column]+".jpeg"
    # Create a subfolder for each label (0 to 4)
    label_folder = os.path.join(output_folder, str(level))
    os.makedirs(label_folder, exist_ok=True)
    filename = os.path.basename(image)

    # Move the image to the corresponding label folder
    destination_path = os.path.join(label_folder, row[image_path_column] + ".jpeg")
    if not os.path.exists(image):
        missing_images.append(image)
        continue
    shutil.copy(image, destination_path)

print("Data sorted and organized into folders.")





# import pandas as pd
# import shutil
# import os

# missing_images=[]
# # Define the path to the CSV file and output folder
# csv_file = "C:\\Users\\Nishi Mahajan\\Desktop\\python\\ML\\ML\\DR 2.0\\trainLabels.csv\\trainLabels.csv"
# output_folder = "C:\\Users\\Nishi Mahajan\\Desktop\\python\\ML\\ML\\DR 2.0\\train"

# # Read the CSV file into a Pandas DataFrame
# df = pd.read_csv(csv_file)

# # Iterate through the DataFrame and organize the images
# for index, row in df.iterrows():
#     image_name = row['image']  # Replace 'image_filename' with the actual column name for image names
#     label = row['level']  # Replace 'label' with the actual column name for labels
    
#     # Create a folder for the label if it doesn't exist
#     label_folder = os.path.join(output_folder, str(label))
#     os.makedirs(label_folder, exist_ok=True)
    
#     # Define the source and destination paths for the image
#     source_path = os.path.join("C:\\Users\\Nishi Mahajan\\Desktop\\python\\ML\\ML\\DR 2.0\\train\\train", image_name) 
#     destination_path = os.path.join(label_folder, image_name)
    
#     # Check if the image file exists and move it to the corresponding folder
#     if os.path.exists(source_path):
#         shutil.copy(source_path, destination_path)
#     else:
#         missing_images.append(image_name)

# print("Data sorted and organized into folders.")
