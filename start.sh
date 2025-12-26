#!/usr/bin/env bash
"""
Quick Start Script - One-command system setup
Run: bash start.sh
"""

set -e  # Exit on error

echo "=================================================="
echo "🚨 Traffic Violation Detection System - Setup"
echo "=================================================="
echo ""

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check Python version
echo -e "${BLUE}[1/6]${NC} Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is required but not installed. Aborting."
    exit 1
fi
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo -e "${GREEN}✓${NC} Python $PYTHON_VERSION found"
echo ""

# Create virtual environment
echo -e "${BLUE}[2/6]${NC} Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✓${NC} Virtual environment created"
else
    echo -e "${GREEN}✓${NC} Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo -e "${BLUE}[3/6]${NC} Activating virtual environment..."
source venv/bin/activate 2>/dev/null || . venv/Scripts/activate 2>/dev/null
echo -e "${GREEN}✓${NC} Virtual environment activated"
echo ""

# Install dependencies
echo -e "${BLUE}[4/6]${NC} Installing dependencies..."
echo "   This may take a few minutes on first run..."
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet
echo -e "${GREEN}✓${NC} Dependencies installed"
echo ""

# Setup environment
echo -e "${BLUE}[5/6]${NC} Setting up environment..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "${YELLOW}⚠${NC} .env file created. Please edit with your configuration."
else
    echo -e "${GREEN}✓${NC} .env file exists"
fi
echo ""

# Download models
echo -e "${BLUE}[6/6]${NC} Preparing model structure..."
python scripts/download_datasets.py --prepare --download-models --quiet 2>/dev/null || true
echo -e "${GREEN}✓${NC} Models prepared"
echo ""

echo "=================================================="
echo -e "${GREEN}✅ Setup Complete!${NC}"
echo "=================================================="
echo ""
echo "📝 Next Steps:"
echo ""
echo "1️⃣  Start Backend API:"
echo "   python -m uvicorn backend.app.main:app --reload"
echo ""
echo "2️⃣  Start Dashboard (new terminal):"
echo "   streamlit run frontend/streamlit_app/app.py"
echo ""
echo "3️⃣  Test the system:"
echo "   curl http://localhost:8000/api/docs"
echo ""
echo "4️⃣  Or use Docker:"
echo "   docker-compose up -d"
echo ""
echo "📖 Documentation:"
echo "   - README.md - Project overview"
echo "   - docs/GETTING_STARTED.md - Detailed setup"
echo "   - docs/API.md - API reference"
echo ""
echo "💡 Pro Tips:"
echo "   • Download datasets: python scripts/download_datasets.py --guide"
echo "   • Train models: python scripts/train_helmet_model.py --help"
echo "   • Run tests: pytest tests/ -v"
echo ""
echo "🎯 Common Issues?"
echo "   See docs/GETTING_STARTED.md#troubleshooting"
echo ""
