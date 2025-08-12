import google.generativeai as genai
import platform

# Configure Gemini API
genai.configure(api_key="")  # Replace with your API key

def ask_gemini(prompt):
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")  # Free tier friendly
        
        # --- MODIFICATION START ---
        generation_config = {
            "max_output_tokens": 70,  # Limits the response to 50 tokens
            "temperature": 0.3,       # Makes the response less random and more direct
            "stop_sequences": ["\n"] # Stops the response at the start of a new paragraph
        }
        
        # Pass the generation_config to the generate_content method
        response = model.generate_content(prompt, generation_config=generation_config)
        # --- MODIFICATION END ---
        
        return response.text
    except Exception as e:
        print("Gemini API Error:", e)
        return "Sorry, I couldn't process that request."