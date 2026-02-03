import os
from dotenv import load_dotenv
from fastapi.templating import Jinja2Templates

load_dotenv()

GROQ_API_KEY = os.environ["GROQ_API_KEY"]


VERCEL_URL = os.environ["VERCEL_URL"]


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


templates = Jinja2Templates(
    directory=os.path.join(BASE_DIR, "templates")
)
