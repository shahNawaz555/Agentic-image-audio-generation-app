import json
import os
from groq import Groq
import subprocess
import autogen as ag


class OrchestratorAgent(ag.Agent):
    def __init__(self):
        super().__init__()

        # Initialize the Groq client with your API key
        self.client = Groq(api_key="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")

    def process_story_with_groq(self, story):
        prompt = (
            #Include a narrator - foremost
            f"Analyze the following children's story with the steps below, and return only the requested information with no added commentary or explanations. It is crucial that you do not add any commentary, explanations, or additional information. Just specifically add these headings like **Major_Characters**, **Scenes**, **Character_Dialogues** and **Background_Scenery** wherever they get start. IT IS EXTREMELY CRUCIAL FOR THE HEADNGS TO BE EXACTLY THIS!!!\n\n"
            f"1. Identify all major characters. For each major character, provide a name and brief description in this format: 'Major_Character_name': 'description'.\n\n"
            f"2. Divide the story into short scenes, providing a brief description of each.\n\n"
            f"3. Extract all (major and side) character dialogues, prefixed with ONLY the (major and side) character's name. If there are no dialogues, generate suitable ones for each (major and side) character, prefixed with ONLY the (major and side) character's name.\n\n"
            f"4. For each scene, describe the background scenery. Do not mention any characters or scene names—only the setting details. I just want the background details. Strictly dont mention any story character, human-beings, animals, or any creatures of such sort in the background details and scenary.\n\n"
            f"**Story:** {story}"
        )

        completion = self.client.chat.completions.create(
            model="llama-3.2-90b-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=True,
            stop=None,
        )

        response_text = ""
        for chunk in completion:
            response_text += chunk.choices[0].delta.content or ""
        return response_text.strip()

    def save_response_to_file(self, response_text, filename):
        with open(filename, "w") as f:
            f.write(response_text)

    def parse_and_generate_json_files(self):
        # Read the groq_api_response.txt file
        with open('groq_api_response.txt', 'r') as file:
            lines = file.readlines()

        # Initialize data structures
        major_characters = {}
        background_scenery = []
        dialogues = {}

        # Flags to identify sections
        in_major_characters = False
        in_scenes = False
        in_character_dialogues = False
        in_background_scenery = False

        # Process the lines to extract information
        for line in lines:
            line = line.strip()
            if line == "**Major_Characters**":
                in_major_characters = True
                in_scenes = False
                in_character_dialogues = False
                in_background_scenery = False
            elif line == "**Scenes**":
                in_major_characters = False
                in_scenes = True
                in_character_dialogues = False
                in_background_scenery = False
            elif line == "**Character_Dialogues**":
                in_major_characters = False
                in_scenes = False
                in_character_dialogues = True
                in_background_scenery = False
            elif line == "**Background_Scenery**":
                in_major_characters = False
                in_scenes = False
                in_character_dialogues = False
                in_background_scenery = True
            elif in_major_characters:
                if line:
                    parts = line.split(":", 1)
                    character_name = parts[0].strip()
                    description = parts[1].strip()
                    major_characters[character_name] = description
            elif in_character_dialogues:
                if line:
                    parts = line.split(":", 1)
                    character_name = parts[0].strip()
                    dialogue = parts[1].strip()
                    if character_name in dialogues:
                        dialogues[character_name].append(dialogue)
                    else:
                        dialogues[character_name] = [dialogue]
            elif in_background_scenery:
                if line:
                    background_scenery.append(line)

        # Create the image_agent_data.json file
        image_agent_data = {
            "Major Characters": major_characters,
            "Background Scenery": background_scenery
        }
        with open('image_agent_data.json', 'w') as file:
            json.dump(image_agent_data, file, indent=4)

        # Create the audio_agent_data.json file
        audio_agent_data = {
            "dialogues": dialogues
        }
        with open('audio_agent_data.json', 'w') as file:
            json.dump(audio_agent_data, file, indent=4)

    def process_story(self, story):
        response_text = self.process_story_with_groq(story)
        print(f"Groq API Response: {response_text}")  # Debugging: Print the response from Groq API

        # Save the response to a text file
        self.save_response_to_file(response_text, "groq_api_response.txt")

        # Parse the text file and generate JSON files
        self.parse_and_generate_json_files()
    

if __name__ == "__main__":
    orchestrator = OrchestratorAgent()
    story = input("Please enter the children's story you want to process: ")
    orchestrator.process_story(story)
    
    # Ensure the working directory is set to the directory containing the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    result = subprocess.run(
        ["python", "image_agent.py"],
        cwd=script_dir,
        capture_output=True,
        text=True
    )
    
    # Print the output and error (if any) from the subprocess
    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)