# import cv2
# import os

# # Load class names from a file (one class per line)
# with open("classes.txt", "r") as f:
#     CLASSES = [line.strip() for line in f.readlines()]

# # Global variables
# points = []
# image = None
# selected_class = None

# # Define the image path
# IMAGE_PATH = r"C:\Users\Emma\Desktop\ESPBW\ESPBW\SelektovanePticeESP32\Test copy\American_Crow\American_Crow_0016_25112.jpg"
# BOX_FILE = "box.txt"  # File to store all annotations

# def click_event(event, x, y, flags, param):
#     """Handles mouse click events."""
#     global points, image

#     if event == cv2.EVENT_LBUTTONDOWN:
#         points.append((x, y))

#         if len(points) == 2:
#             # Draw rectangle
#             cv2.rectangle(image, points[0], points[1], (0, 255, 0), 2)
#             cv2.imshow("Image", image)


# def get_class():
#     """Asks the user to select a class for the image."""
#     print("\nSelect a class:")
#     for i, cls in enumerate(CLASSES):
#         print(f"{i}: {cls}")

#     while True:
#         try:
#             class_id = int(input("\nEnter class ID (0-19): "))
#             if 0 <= class_id < len(CLASSES):
#                 return class_id
#             else:
#                 print("Invalid ID. Please enter a number between 0 and 19.")
#         except ValueError:
#             print("Invalid input. Please enter a number.")


# def save_annotation(image_path, bbox, class_id):
#     """Saves the annotation in YOLO format to 'box.txt'."""
#     h, w, _ = image.shape
#     x_min, y_min = bbox[0]
#     x_max, y_max = bbox[1]

#     # Convert to YOLO format (normalized)
#     x_center = (x_min + x_max) / 2 / w
#     y_center = (y_min + y_max) / 2 / h
#     width = abs(x_max - x_min) / w
#     height = abs(y_max - y_min) / h

#     # Append to box.txt
#     with open(BOX_FILE, "a") as f:
#         f.write(f"{os.path.basename(image_path)} {class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")

#     print(f"Annotation saved to {BOX_FILE}")


# def main(image_path):
#     global image, points, selected_class

#     # Load image
#     image = cv2.imread(image_path)
#     if image is None:
#         print("Error: Could not load image.")
#         return

#     cv2.imshow("Image", image)
#     cv2.setMouseCallback("Image", click_event)

#     print("Click on two opposite corners of the bounding box.")
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

#     if len(points) != 2:
#         print("Bounding box not properly selected. Try again.")
#         return
#     else: 
#         print(points)

#     print("Type class num: ")
#     selected_class = get_class()
#     print("Class selected: ")
#     save_annotation(image_path, points, selected_class)

# if __name__ == "__main__":
#     main(IMAGE_PATH)

import cv2
import os
import glob


HARDCODED_CLASS_ID = 3  # Postaviti ovde odgovarajuci redni broj foldera (ID klase)

# Podesi putanju do foldera
IMAGE_FOLDER = r"C:\Users\Emma\Desktop\ESPBW\ESPBW\SelektovanePticeESP32\Test copy\American_Crow"
BOX_FILE = "box.txt"  # Ne menjati

points = []
image = None
current_image_path = None


def click_event(event, x, y, flags, param):
    """Handler for mouse click event"""
    global points, image

    if event == cv2.EVENT_LBUTTONDOWN:  # Ctrl + L je prelazak na sledecu sliku
        points.append((x, y))

        if len(points) == 2:
            cv2.rectangle(image, points[0], points[1], (0, 255, 0), 2)
            cv2.imshow("Image", image)


def save_annotation(image_path, bbox, class_id):
    """Save coords to specified txt file."""
    global image

    h, w, _ = image.shape
    x_min, y_min = bbox[0]
    x_max, y_max = bbox[1]

    x_center = (x_min + x_max) / 2 / w
    y_center = (y_min + y_max) / 2 / h
    width = abs(x_max - x_min) / w
    height = abs(y_max - y_min) / h

    with open(BOX_FILE, "a") as f:
        f.write(f"{os.path.basename(image_path)} {class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")

    print(f"Saved: {image_path}")


def annotate_image(image_path):
    """Open pic, annotate bb and save results."""
    global image, points, current_image_path

    points = []  
    current_image_path = image_path

    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Cannot load image {image_path}")
        return

    cv2.imshow("Image", image)
    cv2.setMouseCallback("Image", click_event)

    print(f"Annotate points on image {os.path.basename(image_path)}")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    if len(points) != 2:
        print(f"No valid bounding box found {os.path.basename(image_path)}. Skipping.")
        return

    save_annotation(image_path, points, HARDCODED_CLASS_ID)


def main():
    """Function for iteration through image folder."""
    image_paths = glob.glob(os.path.join(IMAGE_FOLDER, "*.jpg"))  

    if not image_paths:
        print("No images found in specified folder.")
        return

    for img_path in image_paths:
        annotate_image(img_path)

    print("Success. Done.")


if __name__ == "__main__":
    main()

