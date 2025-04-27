Agents Image and Audio Generation
This project consists of three main components: audio_agent.py, image_agent.py, and orchestrator.py. Each component has its own specific functionality and dependencies.

Requirements
The project dependencies are listed in the requirements.txt file. To install them, run:

pip install -r requirements.txt
Project Components
Audio Agent
File: audio_agent.py

Imports:
pydub: For audio processing
requests: For making HTTP requests
json: For JSON manipulation
os: For operating system interactions
base64: For encoding and decoding
requests.adapters.HTTPAdapter and urllib3.util.retry.Retry: For HTTP request retries
Description:
The audio_agent.py script uses Eleven Labs for audio generation. It processes audio files, makes HTTP requests to the Eleven Labs API, and handles retries for robust communication.

Image Agent
File: image_agent.py

Imports:
autogen: For automation
diffusers.StableDiffusionPipeline: For image generation
torch: For deep learning operations
os: For operating system interactions
json: For JSON manipulation
subprocess: For running subprocesses
Description:
The image_agent.py script uses the "CompVis/stable-diffusion-v1-4" model for image generation. It leverages the Stable Diffusion Pipeline to create images based on given prompts.

Orchestrator
File: orchestrator.py

Imports:
json: For JSON manipulation
os: For operating system interactions
groq: For Groq operations
subprocess: For running subprocesses
autogen: For automation
Description:
The orchestrator.py script uses the "llama-3.2-90b-vision-preview" model to analyze children's stories. It follows a specific prompt to extract:

Major characters
Scenes
Character dialogues
Background scenery
Usage
Install Dependencies
Ensure all required dependencies are installed by running:
pip install -r requirements.txt
License
This project is licensed under the MIT License.
