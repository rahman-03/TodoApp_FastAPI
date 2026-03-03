import os
from dotenv import load_dotenv
load_dotenv()

def get_env_var(name : str):
    value = os.getenv(name)
    if not value:
        raise ValueError(f"{name} is not set")
    return value


FRONTEND_URL = get_env_var("FRONTEND_URL")
DATABASE_URL = get_env_var("DATABASE_URL")
ACCESS_SECRET_KEY = get_env_var("ACCESS_SECRET_KEY")
REFREST_SECRET_KEY = get_env_var("REFREST_SECRET_KEY")
ALGO = get_env_var("ALGO")