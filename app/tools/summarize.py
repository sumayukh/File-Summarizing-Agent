from openai import OpenAI
from app.config import OPENAI_API_KEY, GROQ_BASE_URL

class SummarizerService:
    def __init__(self, client=None):
        self.client = client or OpenAI(api_key=OPENAI_API_KEY, base_url=GROQ_BASE_URL)
    
    def summarize(self, text:str)->str:
        messages=[
            {
                "role": "system",
                "content": "You are an expert assistant that summarizes text exactly as directed."
            },
            {
                "role": "user",
                "content": f"Summarize the following text in 5-10 short sentences:\n\n{text}"
            }
        ]
        response = self.client.responses.create(
            model='openai/gpt-oss-20b',
            input=messages,
        )
        
        return response.output_text, response.usage.model_dump()