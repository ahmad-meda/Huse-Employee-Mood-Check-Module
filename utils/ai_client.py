from openai import OpenAI
import dotenv
import os

dotenv.load_dotenv()

# 
#  Initialize OpenAI client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)