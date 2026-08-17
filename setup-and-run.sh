#!/bin/bash

# ==========================================================
# Car Price Prediction - Complete Setup & Run Script
# ==========================================================
# This script sets up and runs the entire application
# ==========================================================

set -e

PROJECT_DIR="/home/pavan/Documents/car-price-prediction"
FRONTEND_DIR="$PROJECT_DIR/frontend/vite-project"
BACKEND_DIR="$PROJECT_DIR"

echo "🚗 Car Price Prediction Dashboard - Setup & Run"
echo "=================================================="
echo ""

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Check prerequisites
echo "Checking prerequisites..."
echo ""

# Check Node.js
if ! command -v node &> /dev/null; then
    echo -e "${YELLOW}✗${NC} Node.js is not installed"
    echo "  Please install Node.js from: https://nodejs.org"
    exit 1
fi
NODE_VERSION=$(node --version)
print_status "Node.js found: $NODE_VERSION"

# Check npm
if ! command -v npm &> /dev/null; then
    echo -e "${YELLOW}✗${NC} npm is not installed"
    exit 1
fi
NPM_VERSION=$(npm --version)
print_status "npm found: $NPM_VERSION"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}✗${NC} Python 3 is not installed"
    echo "  Please install Python 3.8+ from: https://python.org"
    exit 1
fi
PYTHON_VERSION=$(python3 --version)
print_status "Python found: $PYTHON_VERSION"

echo ""
echo "=================================================="
echo "Setup Options:"
echo "=================================================="
echo ""
echo "1. Setup Backend Only"
echo "2. Setup Frontend Only"
echo "3. Setup Both (Recommended)"
echo "4. Run Backend (assumes setup complete)"
echo "5. Run Frontend (assumes setup complete)"
echo "6. Run Both Servers"
echo ""

read -p "Enter your choice (1-6): " choice

case $choice in
    1)
        echo ""
        echo "Installing Backend Dependencies..."
        print_info "Installing Python packages..."
        cd "$BACKEND_DIR"
        pip install -r backend/requirements.txt --break-system-packages -q
        print_status "Backend setup complete!"
        echo ""
        echo "To start the backend server, run:"
        echo "  cd $BACKEND_DIR"
        echo "  uvicorn backend.api.main:app --reload"
        ;;
    2)
        echo ""
        echo "Installing Frontend Dependencies..."
        cd "$FRONTEND_DIR"
        print_info "Installing npm packages..."
        npm install -q
        print_status "Frontend setup complete!"
        echo ""
        echo "To start the frontend dev server, run:"
        echo "  cd $FRONTEND_DIR"
        echo "  npm run dev"
        ;;
    3)
        echo ""
        echo "Installing Backend Dependencies..."
        cd "$BACKEND_DIR"
        print_info "Installing Python packages..."
        pip install -r backend/requirements.txt --break-system-packages -q
        print_status "Backend dependencies installed!"
        
        echo ""
        echo "Installing Frontend Dependencies..."
        cd "$FRONTEND_DIR"
        print_info "Installing npm packages..."
        npm install -q
        print_status "Frontend dependencies installed!"
        
        echo ""
        print_status "Full setup complete!"
        echo ""
        echo "To start the servers, open two terminals and run:"
        echo ""
        echo "Terminal 1 (Backend):"
        echo "  cd $BACKEND_DIR"
        echo "  uvicorn backend.api.main:app --reload"
        echo ""
        echo "Terminal 2 (Frontend):"
        echo "  cd $FRONTEND_DIR"
        echo "  npm run dev"
        echo ""
        echo "Then open: http://localhost:5173"
        ;;
    4)
        echo ""
        echo "Starting Backend Server..."
        cd "$BACKEND_DIR"
        print_info "Starting FastAPI on http://127.0.0.1:8000"
        print_info "Press Ctrl+C to stop"
        echo ""
        uvicorn backend.api.main:app --reload
        ;;
    5)
        echo ""
        echo "Starting Frontend Dev Server..."
        cd "$FRONTEND_DIR"
        print_info "Starting Vite on http://localhost:5173"
        print_info "Press Ctrl+C to stop"
        echo ""
        npm run dev
        ;;
    6)
        echo ""
        echo "Starting Both Servers..."
        echo ""
        print_warning "This will open two new terminals"
        echo ""
        
        # Try to open two terminals
        if command -v gnome-terminal &> /dev/null; then
            # GNOME Terminal
            gnome-terminal --new-window -- bash -c "cd '$BACKEND_DIR' && echo 'Starting Backend...' && uvicorn backend.api.main:app --reload"
            sleep 2
            gnome-terminal --new-window -- bash -c "cd '$FRONTEND_DIR' && echo 'Starting Frontend...' && npm run dev"
            echo ""
            print_status "Both servers starting!"
            print_info "Backend: http://127.0.0.1:8000"
            print_info "Frontend: http://localhost:5173"
        elif command -v xterm &> /dev/null; then
            # XTerm fallback
            xterm -e "cd '$BACKEND_DIR' && echo 'Starting Backend...' && uvicorn backend.api.main:app --reload" &
            sleep 2
            xterm -e "cd '$FRONTEND_DIR' && echo 'Starting Frontend...' && npm run dev" &
            echo ""
            print_status "Both servers starting!"
        else
            # Manual instructions
            echo -e "${YELLOW}!${NC} Could not auto-open terminals"
            echo ""
            echo "Please run these commands in separate terminals:"
            echo ""
            echo "Terminal 1 (Backend):"
            echo "  cd $BACKEND_DIR"
            echo "  uvicorn backend.api.main:app --reload"
            echo ""
            echo "Terminal 2 (Frontend):"
            echo "  cd $FRONTEND_DIR"
            echo "  npm run dev"
            echo ""
            echo "Then open: http://localhost:5173"
        fi
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "=================================================="
echo "For more information, see:"
echo "  - $PROJECT_DIR/SETUP.md"
echo "  - $PROJECT_DIR/FRONTEND_IMPLEMENTATION.md"
echo "=================================================="
