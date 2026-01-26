#!/bin/bash
# =====================================================
# Setup and run Expense Tracker Backend on macOS
# =====================================================

# 1️⃣ Ensure Homebrew is installed
if ! command -v brew &> /dev/null; then
  echo "Installing Homebrew..."
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# 2️⃣ Install Rust (needed for pydantic-core)
if ! command -v rustc &> /dev/null; then
  echo "Installing Rust..."
  curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
  source $HOME/.cargo/env
fi

# 3️⃣ Install PostgreSQL headers
brew install postgresql

# 4️⃣ Create and activate virtual environment
if [ ! -d "venv" ]; then
  echo "Creating Python virtual environment..."
  python3 -m venv venv
fi
echo "Activating virtual environment..."
source venv/bin/activate

# 5️⃣ Upgrade pip, setuptools, wheel
echo "Upgrading pip, setuptools, wheel..."
pip install --upgrade pip setuptools wheel

# 6️⃣ Install maturin (needed for Rust wheels)
pip install maturin

# 7️⃣ Install Python requirements
echo "Installing project dependencies..."
pip install -r requirements.txt

# 8️⃣ Verify key packages
python -c "import pydantic, psycopg2, fastapi, uvicorn; print('✅ All key packages installed!')"

# 9️⃣ Run the backend server
echo "Starting backend server at http://127.0.0.1:8000 ..."
uvicorn main:app --reload
