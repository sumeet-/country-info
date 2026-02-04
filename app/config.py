import logging
import os
import sys

from dotenv import load_dotenv
from fastapi.templating import Jinja2Templates

load_dotenv()


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)


GROQ_API_KEY = os.environ["GROQ_API_KEY"]
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]

# For Vercel deployment, available as an environment variable on Vercel
VERCEL_URL = os.environ["VERCEL_URL"]


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


templates = Jinja2Templates(
    directory=os.path.join(BASE_DIR, "templates")
)
