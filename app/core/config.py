"""Configuration management"""
import os
from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME")
API_BASE = os.getenv("API_BASE")
API_KEY = os.getenv("API_KEY")

if not all([MODEL_NAME, API_BASE, API_KEY]):
    raise ValueError("MODEL_NAME, API_BASE, and API_KEY must be set in .env file")
