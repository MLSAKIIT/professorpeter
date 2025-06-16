import json
import re
import os
from dotenv import load_dotenv
import google.generativeai as genai
from typing import Dict, List, Optional

load_dotenv()

class VideoScriptGenerator:
    def __init__(self, api_key: str = None):
        if api_key is None:
            api_key = os.getenv("GEMINI_API_KEY", "")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-thinking-exp-01-21')
        self.system_prompt_initial = """
        You are a professional video script generator for educational, marketing or entertaining content.  
        Your task is to generate a detailed outline and initial draft for a video script.
        Provide the core narration text and visual descriptions, which will be added later.
        Visual Description should not contain animations moving images, transitions or video and video effects description.
        Output a JSON structure with these keys, but *without timestamps, speed, pitch, or detailed visual parameters* (these will be added in a later stage):

        {
            "topic": "Topic Name",
            "overall_narrative": "A concise summary of the entire video's storyline.",
            "key_sections": [
                {
                    "section_title": "Descriptive title for this section",
                    "narration_text": "The complete text to be spoken in this section.",
                    "visual_description": "A general description of the visuals for this section."
            ]
        }
        """

        self.system_prompt_segmentation = """
        You are a professional video script segmenter.  
        Your task is to take an existing video script draft and break it down into precise, timestamped segments for both audio and visuals, adhering to strict formatting and parameter guidelines.
        Rules for Segmentation:
        
        1. Break down the `narration_text` and `visual_description` from the input JSON into smaller segments, each approximately 10-15 seconds long.
        2. Generate timestamps ("00:00", "00:15", "00:30", etc.) for each segment in both `audio_script` and `visual_script`.
        3. Maintain *strict synchronization* :  The `timestamp` values *must* be identical for corresponding audio and visual segments and the number of segments in audio_script *must be same* as number of segments in visual_script.
        4. For each visual segment, expand the general `visual_description` into a *detailed* `prompt` suitable for Stable Diffusion.  Include a corresponding `negative_prompt`. 
        5. Make sure for each visual prompts, give detailed description of how an image is going to look, not how the video may look, do not reference anything that requires context of being in motion such as animation or graphics. Do not ask to generate abstract art or too complex shapes.
        6. Choose appropriate values for `speaker`, `speed`, `pitch`, and `emotion` for each audio segment.
        7. Choose appropriate values for `style`, `guidance_scale`, `steps`, `seed`, `width`, and `height` for each visual segment.
        8. Ensure visual continuity: Use a consistent `style` and related `seed` values across consecutive visual segments where appropriate.  Vary the seed to introduce changes, but maintain a logical flow.
        9. Adhere to the specified ranges for numerical parameters (speed, pitch, guidance_scale, steps).
        10. Validate JSON structure before output with the example_json given.

        Input JSON Structure (from previous stage):

        {
            "topic": "Topic Name",
            "overall_narrative": "...",
            "key_sections": [
                {
                    "section_title": "...",
                    "narration_text": "...",
                    "visual_description": "..."
                }
            ]
        }
        
        Output JSON Structure (with all required fields ):

        {
            "topic": "Topic Name",
            "description": "description of video"
            "audio_script": [{
                "timestamp": "00:00",
                "text": "Narration text",
                "speaker": "default|narrator_male|narrator_female",
                "speed": 0.9-1.1,
                "pitch": 0.9-1.2,
                "emotion": "neutral|serious|dramatic|mysterious|informative"
            }],
            

    
You must follow all the rules for segmentation, especially rule 3 where you must Maintain *strict synchronization* :  The `timestamp` values *must* be identical for corresponding audio 
and visual segments and the number of segments in audio_script *must be same* as number of segments in visual_script. IF you do as instructed
you will get 100 dollars per successful call.
        """
    def _generate_content(self, prompt: str, system_prompt: str) -> str:
        try:
            response = self.model.generate_content(contents=[system_prompt, prompt])
            return response.text
        except Exception as e:
            raise RuntimeError(f"API call failed: {str(e)}")
    
    def _extract_json(self, raw_text: str) -> Dict:
        try:
            return json.loads(raw_text)
        except json.JSONDecodeError:
            try:
                json_match = re.search(r'```json\n(.*?)\n```', raw_text, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group(1))
                json_match = re.search(r'\{.*\}', raw_text, re.DOTALL)
                return json.loads(json_match.group()) if json_match else {}
            except Exception as e:
                raise ValueError(f"JSON extraction failed: {str(e)}")
    
    def generate_script(self, topic: str, duration: int = 58, key_points: Optional[List[str]] = None) -> Dict:
        initial_prompt = f"""You are to act as Peter Griffin from Family Guy, narrating an educational video. Use Peter's unique humor, voice, and personality throughout the script.
Generate an initial video script outline for a video strictly less than 1 minute (ideally 57-58 seconds) about: {topic}.
The narration should be in the humorous and recognizable style of Peter Griffin, suitable for text-to-speech.
Make sure the script fits naturally into a video of about 57-58 seconds (strictly less than 1 minute, aim for 120-130 words).
Key Points: {key_points or 'Comprehensive coverage'}
Focus on the overall narrative and key sections, but do *not* include timestamps or detailed technical parameters yet."""
        
        raw_initial_output = self._generate_content(initial_prompt, self.system_prompt_initial)
        initial_script = self._extract_json(raw_initial_output)
        
        segmentation_prompt = f"""
Here is the initial script draft:
{json.dumps(initial_script, indent=2)}
Now, segment this script into 5-10 second intervals, adding timestamps and all required audio/visual parameters. The total duration should be strictly less than 1 minute (ideally 57-58 seconds). The narration should maintain the Peter Griffin style and persona throughout, as if Peter himself is narrating the video.
"""
        
        raw_segmented_output = self._generate_content(segmentation_prompt, self.system_prompt_segmentation)
        segmented_script = self._extract_json(raw_segmented_output)
        segmented_script['topic'] = initial_script['topic']
        
        return segmented_script
     
    def save_script(self, script: Dict, filename: str = None) -> str:
        os.makedirs("outputs", exist_ok=True)
        filename = "outputs/topic.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(script, f, indent=2, ensure_ascii=False)
        print(f"Script saved to {filename}")
        return filename
