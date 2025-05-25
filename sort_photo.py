import os
import shutil
import torch
import clip
from PIL import Image

# Load the model
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

# Define meme categories
categories = ["Anime","Breaking Bad", "Furry", "Dark Humor", "Gaming", "Computer Science", "Animals", "Pope", "Alcohol", "Politics", "University", "Wholesome", "Woke"]

# Folder paths
input_folder = "A"
output_folder = "B"

# Create output folders if they don't exist
for category in categories:
    os.makedirs(os.path.join(output_folder, category), exist_ok=True)

# Process each meme
for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
        image_path = os.path.join(input_folder, filename)
        image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)

        with torch.no_grad():
            image_features = model.encode_image(image)

            # Prepare text features
            text = clip.tokenize(categories).to(device)
            text_features = model.encode_text(text)

            # Find the best matching category
            similarities = (image_features @ text_features.T).squeeze(0)
            best_category_idx = similarities.argmax().item()
            best_category = categories[best_category_idx]

        # Move meme to the correct folder
        shutil.move(image_path, os.path.join(output_folder, best_category, filename))
        print(f"Moved {filename} to {best_category}")

print("Done sorting memes!")
