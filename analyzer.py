import cv2
import numpy as np
import json
import os
import pandas as pd
from google import genai
from dotenv import load_dotenv
from PIL import Image

# Configuration
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_ID = "gemini-2.5-flash"

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found. Check your .env file.")

client = genai.Client(api_key=API_KEY)

def extract_visual_features(img_pil):
    """Extracts basic color and brightness features."""
    img_rgb = img_pil.convert("RGB")
    img_np = np.array(img_rgb)
    avg_color = img_np.mean(axis=(0, 1)).astype(int).tolist()
    gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
    brightness = float(gray.mean() / 255)

    return {
        "avg_color_rgb": avg_color,
        "brightness": round(brightness, 3)
    }

def build_prompt(features):
    """Constructs the analysis prompt."""
    return f"""
        You are a fashion market analyst.
        Data: RGB {features['avg_color_rgb']}, Brightness {features['brightness']}

        Respond ONLY in valid JSON:
        {{
        "category": "",
        "color": "",
        "material": "",
        "vibe": "",
        "season": ""
        }}
        """

def analyze_folder(folder_path):
    results = []
    abs_folder_path = os.path.abspath(folder_path)
    
    if not os.path.exists(abs_folder_path):
        print(f"Error: Folder {abs_folder_path} not found.")
        return None

    images = [f for f in os.listdir(abs_folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    print(f"Starting analysis for {len(images)} images using {MODEL_ID}...")

    for filename in images:
        path = os.path.join(abs_folder_path, filename)
        
        try:
            with Image.open(path) as img:
                img.load()
                features = extract_visual_features(img)
                prompt_text = build_prompt(features)
                
                try:
                    response = client.models.generate_content(
                        model=MODEL_ID,
                        contents=[prompt_text, img]
                    )
                    
                    # FIX: Handle cases where the API returns no text (NoneType error fix)
                    if response.text is None:
                        print(f"Warning: No text returned for {filename}. Checking safety filters...")
                        ai_data = {"category": "Blocked", "color": "N/A", "material": "N/A", "vibe": "N/A", "season": "N/A"}
                    else:
                        # Clean and parse JSON
                        clean_text = response.text.replace("```json", "").replace("```", "").strip()
                        ai_data = json.loads(clean_text)

                except Exception as api_err:
                    print(f"Response Error on {filename}: {api_err}")
                    ai_data = {"category": "Error", "color": "Error", "material": "Error", "vibe": "Error", "season": "Error"}

                results.append({
                    "image": filename,
                    "avg_color": features["avg_color_rgb"],
                    "brightness": features["brightness"],
                    **ai_data
                })
                print(f"Processed: {filename}")

        except Exception as e:
            print(f"Failed to process {filename}: {str(e)}")
            continue

    if not results:
        return None

    df = pd.DataFrame(results)
    output_name = f"analysis_{os.path.basename(abs_folder_path)}.csv"
    df.to_csv(output_name, index=False)
    print(f"Analysis complete. CSV saved: {output_name}")
    return output_name