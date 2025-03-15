from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class Settings:
    PROJECT_ID: str = "helios-tech-interview-project"
    API_V1_STR: str = ""

    @classmethod
    def get_settings(cls):
        return cls()

settings = Settings.get_settings() 