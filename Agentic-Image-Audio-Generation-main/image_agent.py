import autogen as ag
from diffusers import StableDiffusionPipeline
import torch
import os
import json
import subprocess

class ImageGenerationAgent(ag.Agent):
    def __init__(self):
        super().__init__()
        self.model_id = "CompVis/stable-diffusion-v1-4"
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.pipeline = StableDiffusionPipeline.from_pretrained(self.model_id)
        self.pipeline.to(self.device)

    def generate_image(self, prompt, output_dir, filename):
        # Generate the image based on the prompt
        image = self.pipeline(prompt).images[0]
        
        # Ensure the output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Save the image
        image_path = os.path.join(output_dir, filename)
        image.save(image_path)
        print(f"Image saved to {image_path}")

    def generate_images_from_json(self, json_file, output_dir):
        # Read the JSON file
        with open(json_file, 'r') as file:
            data = json.load(file)
        
        # Generate images for major characters
        for character, description in data["Major Characters"].items():
            prompt = f"{character}: {description}"
            filename = f"{character}.png"
            self.generate_image(prompt, output_dir, filename)
        
        # Generate images for background scenery
        for i, scene in enumerate(data["Background Scenery"], start=1):
            prompt = scene
            filename = f"Scene_{i}.png"
            self.generate_image(prompt, output_dir, filename)

if __name__ == "__main__":
    agent = ImageGenerationAgent()
    json_file = "image_agent_data.json"
    output_dir = r"E:\agent_storage\images"
    agent.generate_images_from_json(json_file, output_dir)
    # Call audio_agent.py after image generation completes
    subprocess.run(["python", "audio_agent.py"])