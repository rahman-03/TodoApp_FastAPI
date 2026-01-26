import os
from dotenv import load_dotenv
load_dotenv()

FRONTEND_URL = os.getenv("FRONTEND_URL")
DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGO = os.getenv("ALGO")
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")