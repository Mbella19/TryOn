# Try On - Virtual Fitting Room

## Setup Instructions

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Edit `.env` and add your actual API keys:
     - `GOOGLE_API_KEY`: Your Google Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
     - `SECRET_KEY`: A random secret key for Flask sessions
     - `JWT_SECRET_KEY`: A random secret key for JWT tokens

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

### Running the Application

From the project root directory:

```bash
bash start-app.sh
```

This will start both backend (port 5001) and frontend (port 3000).

Access the app at: **http://localhost:3000**

## Environment Variables

All sensitive configuration is stored in `backend/.env` (not tracked by git).

See `backend/.env.example` for required variables.

## Security Notes

- **Never commit `.env` files** - They contain sensitive API keys
- The `.env` file is already in `.gitignore`
- Use `.env.example` as a template for new setups
