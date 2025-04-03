from dotenv import load_dotenv
import os
import google.generativeai as genai
load_dotenv(dotenv_path= "django4/.env")

class GenerativeModelClient:
    def __init__(self):
        # Load the API key from environment variables
        self.api_key = os.environ["DJ_Gem"]
        genai.configure(api_key=self.api_key)
        
        # Setup the generation configuration
        self.generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }

        # Initialize the generative model
        self.model = genai.GenerativeModel(
            model_name="gemini-2.0-flash-exp",
            generation_config=self.generation_config,
        )

    def get_response(self, user_input: str) -> str:
        # Start a chat session
        chat_session = self.model.start_chat()

        # Send the user input and get the response
        response = chat_session.send_message(user_input)

        # Return the response text
        return response.text
