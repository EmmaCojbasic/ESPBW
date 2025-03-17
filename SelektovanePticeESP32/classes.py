import os

def extract_classes(train_dir="Train", output_file="classes.txt"):
    # Ensure the Train directory exists
    if not os.path.exists(train_dir):
        print(f"Error: The directory '{train_dir}' does not exist.")
        return
    
    # Get class names from folder names
    class_names = sorted([name for name in os.listdir(train_dir) if os.path.isdir(os.path.join(train_dir, name))])

    if not class_names:
        print("No class folders found in the Train directory.")
        return

    # Save to classes.txt
    with open(output_file, "w") as f:
        for class_name in class_names:
            f.write(class_name + "\n")

    print(f"Class names saved to {output_file}. Found {len(class_names)} classes.")

if __name__ == "__main__":
    extract_classes()
