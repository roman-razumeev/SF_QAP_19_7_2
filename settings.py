import os
from dotenv import load_dotenv

load_dotenv()

valid_email = os.getenv('valid_email')
valid_password = os.getenv('valid_password')
invalid_email = os.getenv('invalid_email')
invalid_password = os.getenv('invalid_password')
# valid_email = "raycom4@1secmail.com"
# valid_password = "123456"
