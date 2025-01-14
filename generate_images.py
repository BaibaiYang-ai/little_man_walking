import pandas as pd
import cv2
import os

# which charactor to render

women_true = False
man_true = True

# Read the CSV file
# Assuming the CSV has columns: x, y, time
csv_file = "click_log_women1.csv"  # Replace with your CSV file
csv_file2 = "click_log_men1.csv"  # Replace with your CSV file
image_file = "supermarket.jpeg"  # Replace with your base image file
output_folder = "output_images_m1"  # Folder to save the images


# women   Read the CSV file
# Assuming the CSV has columns: x, y, and the third column is the time
image1_file_w = "icons/heel.png"  # Replace with your first symbol image file
image2_file_w = "icons/women1.PNG"  # Replace with your second symbol image file
image3_file_w = "icons/women2.PNG"  # Replace with your second symbol image file

### man 
image1_file = "icons/sneaker.png"  # Replace with your first symbol image file
image2_file = "icons/man1.PNG"  # Replace with your second symbol image file
image3_file = "icons/man2.PNG"  # Replace with your second symbol image file

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Load the data from the CSV
data = pd.read_csv(csv_file, header=None)  # No header assumed
data.columns = ["x", "y", "time"]  # Rename columns appropriately

data2 = pd.read_csv(csv_file2, header=None)  # No header assumed
data2.columns = ["x", "y", "time"]  # Rename columns appropriately

# Load the base image
base_image = cv2.imread(image_file)
if base_image is None:
    raise FileNotFoundError(f"Image file '{image_file}' not found.")

# Resize the base image to 618x1100
base_image = cv2.resize(base_image, (618, 1100))

# Load the symbol images
image1 = cv2.imread(image1_file, cv2.IMREAD_UNCHANGED)
image1 = cv2.resize(image1, (14, 14))
image2 = cv2.imread(image2_file, cv2.IMREAD_UNCHANGED)
image2 = cv2.resize(image2, (96, 120))
image3 = cv2.imread(image3_file, cv2.IMREAD_UNCHANGED)
image3 = cv2.resize(image3, (96, 120))
if image1 is None or image2 is None:
    raise FileNotFoundError("Symbol images not found.")


# Load the symbol images
image1_w = cv2.imread(image1_file_w, cv2.IMREAD_UNCHANGED)
image1_w = cv2.resize(image1_w, (14, 14))
image2_w = cv2.imread(image2_file_w, cv2.IMREAD_UNCHANGED)
image2_w = cv2.resize(image2_w, (96, 120))
image3_w = cv2.imread(image3_file_w, cv2.IMREAD_UNCHANGED)
image3_w = cv2.resize(image3_w, (96, 120))
if image1_w is None or image2_w is None:
    raise FileNotFoundError("Symbol images not found.")

# Ensure the data is sorted by time
data = data.sort_values(by="time")
data2 = data2.sort_values(by="time")

# Function to overlay an image
def overlay_image(background, overlay, x, y):
    h, w = overlay.shape[:2]
    
    # Calculate bounds for placing overlay centered at (x, y)
    y1, y2 = max(0, y - h // 2), min(background.shape[0], y + h // 2)
    x1, x2 = max(0, x - w // 2), min(background.shape[1], x + w // 2)

    # Calculate the region of the overlay to use
    overlay_y1, overlay_y2 = max(0, h // 2 - y), h - max(0, y + h // 2 - background.shape[0])
    overlay_x1, overlay_x2 = max(0, w // 2 - x), w - max(0, x + w // 2 - background.shape[1])

    # Calculate alpha blending
    alpha_s = overlay[overlay_y1:overlay_y2, overlay_x1:overlay_x2, 3] / 255.0
    alpha_l = 1.0 - alpha_s

    # Apply overlay on the background
    for c in range(0, 3):
        background[y1:y2, x1:x2, c] = (
            alpha_s * overlay[overlay_y1:overlay_y2, overlay_x1:overlay_x2, c]
            + alpha_l * background[y1:y2, x1:x2, c]
        )


# Copy the image for updating
current_image = base_image.copy()

if women_true == False and man_true == True:
    data =data2


# Iterate through the data row by row
for index, row in data.iterrows():
    x, y, time = int(row["x"]), int(row["y"]), row["time"]

    # Draw all previous points with symbol1
    for prev_index in range(index):
        if women_true:
            prev_x, prev_y = int(data.iloc[prev_index]["x"]), int(data.iloc[prev_index]["y"])
            overlay_image(current_image, image1_w, prev_x, prev_y)
        if man_true:
            prev_x_w, prev_y_w = int(data2.iloc[prev_index]["x"]), int(data2.iloc[prev_index]["y"])
            overlay_image(current_image, image1, prev_x_w, prev_y_w)

    # Draw the current point with symbol2

    if index%2 ==0: 
        if women_true:
            overlay_image(current_image, image2_w, x, y)
        if man_true:   
            overlay_image(current_image, image2, int(data2.iloc[index]["x"]), int(data2.iloc[index]["y"]))

    else:
        if women_true:
            overlay_image(current_image, image3_w, x, y)
        if man_true: 
            overlay_image(current_image, image3, int(data2.iloc[index]["x"]), int(data2.iloc[index]["y"]))


    # Save the updated image
    output_path = os.path.join(output_folder, f"frame_{index:04d}.png")
    cv2.imwrite(output_path, current_image)

    # Optional: Reset the image for the next frame
    current_image = base_image.copy()

print(f"Images saved in '{output_folder}' folder.")
