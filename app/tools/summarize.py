from openai import OpenAI
from app.config import OPENAI_API_KEY

class SummarizerService:
    def __init__(self, client=None):
        self.client = client or OpenAI(api_key=OPENAI_API_KEY)
    
    def summarize(self, text:str)->str:
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert assistant that summarizes text exactly as directed."
                },
                {
                    "role": "user",
                    "content": f"Summarize the following text in 5-10 short sentences:\n\n{text}"
                }
            ],
        )
        
        return response.choices[0].message.content.strip()