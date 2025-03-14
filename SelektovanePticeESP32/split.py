import os
import shutil
import random

test_dir = "Test"
validate_dir = "Validate"

os.makedirs(validate_dir, exist_ok=True)

for class_name in os.listdir(test_dir):
    class_path = os.path.join(test_dir, class_name)
    
    if not os.path.isdir(class_path):
        continue

    validate_class_path = os.path.join(validate_dir, class_name)
    os.makedirs(validate_class_path, exist_ok=True)

    images = [f for f in os.listdir(class_path) if f.lower().endswith(('.jpg', '.jpeg'))]
    
    random.shuffle(images)
    num_to_move = len(images) // 2  
    
    for img in images[:num_to_move]:
        src_path = os.path.join(class_path, img)
        dst_path = os.path.join(validate_class_path, img)
        shutil.move(src_path, dst_path)

print("Podela završena! Polovina slika prebačena u 'Validate' folder.")
