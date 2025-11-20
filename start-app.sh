#!/bin/bash

# Kill any running processes on ports 5001 and 3000
echo "Stopping existing services..."
lsof -ti:5001 | xargs kill -9 2>/dev/null
lsof -ti:3000 | xargs kill -9 2>/dev/null

# Start Backend
echo "Starting Backend..."
cd backend
source venv/bin/activate
python app.py &
BACKEND_PID=$!
cd ..

# Start Frontend
echo "Starting Frontend..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo "App started!"
echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo "Access the app at http://localhost:3000"

# Wait for processes
wait $BACKEND_PID $FRONTEND_PID
