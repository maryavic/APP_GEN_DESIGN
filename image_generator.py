import random
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
from PIL import Image
import io

class ImageGenerator:
    def __init__(self, stability_api_key):
        """
        Initialize Stability AI Stable Diffusion client
        
        Args:
            stability_api_key (str): Stability AI API key
        """
        self.stability_api = client.StabilityInference(
            key=stability_api_key,
            verbose=True,
            engine="stable-diffusion-xl-1024-v1-0"
        )

    def generate_prompt(self, keywords):
        """
        Generate a creative prompt dynamically from extracted keywords.
        
        Args:
            keywords (list): List of keywords extracted from the sketch.
        
        Returns:
            str: Generated creative prompt.
        """
        adjectives = [
            "photorealistic", "cinematic", "hyper-realistic", "lifelike", "natural", "detailed", 
            "vivid", "high-definition", "realistic", "stunning", "immersive", "dynamic"
        ]
        
        settings = [
            "with dramatic lighting", "in a beautiful natural environment", "with vibrant textures", 
            "captured in high-definition", "with soft natural light", "with intricate details"
        ]
        
        adjective = random.choice(adjectives)
        setting = random.choice(settings)
        
        prompt = f"A {adjective} depiction of {', '.join(keywords)}, {setting}. The image should emphasize realism, with a focus on lifelike textures, vivid colors, and realistic proportions."
        
        return prompt

    def generate_image(self, prompt, seed=None, cfg_scale=7, steps=50):
        """
        Generate an image based on the given prompt using Stability AI's Stable Diffusion.
        
        Args:
            prompt (str): Text prompt for image generation.
            seed (int, optional): Random seed for reproducibility.
            cfg_scale (int): Classifier-free guidance scale.
            steps (int): Number of diffusion steps.
        
        Returns:
            PIL.Image: Generated image.
        """
        seed = seed or random.randint(0, 2**32 - 1)
        
        answers = self.stability_api.generate(
            prompt=prompt,
            seed=seed,
            steps=steps,
            cfg_scale=cfg_scale,
            width=1024,
            height=1024,
            samples=1
        )
        
        for resp in answers:
            for artifact in resp.artifacts:
                if artifact.type == generation.ARTIFACT_IMAGE:
                    img = Image.open(io.BytesIO(artifact.binary))
                    return img
        return None
