from app import create_app
from flask_jwt_extended import create_access_token
import sys
import os

# Ensure we can import from current directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = create_app()
with app.app_context():
    # User ID 1 was seen in inspect_db output
    token = create_access_token(identity='1')
    print(token)
