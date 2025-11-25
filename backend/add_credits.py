import os
import sys
from dotenv import load_dotenv

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import db, User

# Load environment variables
load_dotenv()

app = create_app()

def add_credits():
    with app.app_context():
        users = User.query.all()
        print(f"Found {len(users)} users.")
        for user in users:
            print(f"User: {user.email}, Current Credits: {user.credits}")
            user.credits = 100
            print(f"-> Updated Credits to: {user.credits}")
        
        db.session.commit()
        print("✅ Successfully added 100 credits to all users.")

if __name__ == "__main__":
    add_credits()
