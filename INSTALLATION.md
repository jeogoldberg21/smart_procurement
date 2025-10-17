# 📦 Installation Guide - Smart Procurement System

## System Requirements

### Minimum Requirements
- **OS:** Windows 10/11, macOS 10.14+, or Linux
- **Python:** 3.8 or higher
- **RAM:** 4 GB minimum, 8 GB recommended
- **Disk Space:** 1 GB free space
- **Internet:** Required for initial package installation

### Recommended Setup
- **Python:** 3.9 or 3.10 (best compatibility with Prophet)
- **RAM:** 8 GB or more
- **CPU:** Multi-core processor for faster ML training

---

## Installation Methods

### Method 1: Automated Setup (Recommended for Windows)

```bash
# Run the setup script
setup.bat
```

This will:
1. Install all Python dependencies
2. Generate initial data files
3. Verify installation

### Method 2: Manual Installation (All Platforms)

#### Step 1: Verify Python Installation

```bash
python --version
```

Should show Python 3.8 or higher. If not installed:
- **Windows:** Download from [python.org](https://www.python.org/downloads/)
- **macOS:** `brew install python3`
- **Linux:** `sudo apt-get install python3 python3-pip`

#### Step 2: Navigate to Project Directory

```bash
cd d:/Hackathon/SRM/smart_procurement
```

#### Step 3: Create Virtual Environment (Optional but Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- Flask (backend framework)
- Streamlit (dashboard framework)
- Prophet (ML forecasting)
- Plotly (visualizations)
- Pandas, NumPy (data processing)
- And other supporting libraries

**Note:** Prophet installation may take 5-10 minutes as it compiles C++ extensions.

#### Step 5: Generate Initial Data

```bash
python -m utils.data_generator
```

You should see:
```
✓ Generated material_prices.csv with 90 records
✓ Generated inventory.json with 3 materials
✓ Generated vendors.json with vendor data
```

#### Step 6: Verify Installation

```bash
python test_system.py
```

All tests should pass.

---

## Troubleshooting Installation Issues

### Issue 1: Prophet Installation Fails

**Symptoms:**
```
ERROR: Failed building wheel for prophet
```

**Solutions:**

**Windows:**
```bash
# Install Visual C++ Build Tools first
# Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/

# Then install Prophet
pip install pystan==2.19.1.1
pip install prophet==1.1.5
```

**macOS:**
```bash
# Install Xcode Command Line Tools
xcode-select --install

# Install Prophet
pip install pystan
pip install prophet
```

**Linux:**
```bash
# Install build dependencies
sudo apt-get install build-essential python3-dev

# Install Prophet
pip install pystan
pip install prophet
```

**Alternative:** Use conda instead of pip:
```bash
conda install -c conda-forge prophet
```

### Issue 2: "No module named 'streamlit'"

**Solution:**
```bash
pip install streamlit
```

### Issue 3: "No module named 'plotly'"

**Solution:**
```bash
pip install plotly
```

### Issue 4: Permission Denied Errors

**Windows:**
```bash
# Run as Administrator or use --user flag
pip install --user -r requirements.txt
```

**macOS/Linux:**
```bash
# Use sudo or virtual environment
sudo pip3 install -r requirements.txt
# OR
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Issue 5: SSL Certificate Errors

**Solution:**
```bash
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
```

### Issue 6: Outdated pip

**Solution:**
```bash
python -m pip install --upgrade pip
```

### Issue 7: Port Already in Use

**Symptoms:**
```
Address already in use
```

**Solutions:**

**Check what's using the port:**

**Windows:**
```bash
netstat -ano | findstr :5000
netstat -ano | findstr :8501
```

**macOS/Linux:**
```bash
lsof -i :5000
lsof -i :8501
```

**Kill the process or change ports in config.py:**
```python
FLASK_PORT = 5001
STREAMLIT_PORT = 8502
```

---

## Platform-Specific Instructions

### Windows

1. **Install Python from python.org**
   - Download Python 3.9 or 3.10
   - Check "Add Python to PATH" during installation

2. **Open Command Prompt or PowerShell**
   ```bash
   cd d:\Hackathon\SRM\smart_procurement
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   # Option 1: Use batch files
   run_backend.bat
   run_dashboard.bat
   
   # Option 2: Manual
   python app.py
   streamlit run dashboard.py
   ```

### macOS

1. **Install Homebrew (if not installed)**
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Install Python**
   ```bash
   brew install python@3.9
   ```

3. **Navigate and install**
   ```bash
   cd ~/Hackathon/SRM/smart_procurement
   pip3 install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python3 app.py
   # In another terminal:
   streamlit run dashboard.py
   ```

### Linux (Ubuntu/Debian)

1. **Install Python and pip**
   ```bash
   sudo apt-get update
   sudo apt-get install python3 python3-pip python3-venv
   ```

2. **Navigate and install**
   ```bash
   cd ~/Hackathon/SRM/smart_procurement
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   # In another terminal:
   streamlit run dashboard.py
   ```

---

## Docker Installation (Advanced)

### Create Dockerfile

**Backend Dockerfile:**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

**Frontend Dockerfile:**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "dashboard.py"]
```

### Docker Compose

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    ports:
      - "5000:5000"
    volumes:
      - ./data:/app/data

  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    ports:
      - "8501:8501"
    depends_on:
      - backend
```

**Run with Docker:**
```bash
docker-compose up
```

---

## Verification Steps

### 1. Check Python Version
```bash
python --version
# Should show 3.8 or higher
```

### 2. Check Installed Packages
```bash
pip list
# Should show flask, streamlit, prophet, plotly, etc.
```

### 3. Verify Data Files
```bash
# Windows
dir data

# macOS/Linux
ls -la data
```

Should show:
- material_prices.csv
- inventory.json
- vendors.json

### 4. Test Backend
```bash
python app.py
# Should start without errors
# Visit http://localhost:5000/api/health
```

### 5. Test Dashboard
```bash
streamlit run dashboard.py
# Should open browser automatically
# Visit http://localhost:8501
```

### 6. Run Test Suite
```bash
python test_system.py
# All tests should pass
```

---

## Post-Installation Configuration

### 1. Environment Variables (Optional)

Create `.env` file:
```bash
cp .env.example .env
```

Edit `.env`:
```
FLASK_PORT=5000
STREAMLIT_PORT=8501
EMAIL_ALERTS=false
WHATSAPP_ALERTS=false
PRICE_DROP_THRESHOLD=5
INVENTORY_THRESHOLD=100
```

### 2. Customize Materials

Edit `config.py`:
```python
MATERIALS = ['Copper', 'Aluminum', 'Steel', 'Zinc']
```

Then regenerate data:
```bash
python -m utils.data_generator
```

### 3. Adjust Update Intervals

Edit `config.py`:
```python
PRICE_UPDATE_INTERVAL = 300      # 5 minutes
FORECAST_UPDATE_INTERVAL = 3600  # 1 hour
```

---

## Uninstallation

### Remove Virtual Environment
```bash
# Windows
rmdir /s venv

# macOS/Linux
rm -rf venv
```

### Remove Packages (if not using venv)
```bash
pip uninstall -r requirements.txt -y
```

### Remove Data Files
```bash
# Windows
rmdir /s data

# macOS/Linux
rm -rf data
```

---

## Getting Help

### Check Logs

**Flask logs:**
- Check console output where `python app.py` is running

**Streamlit logs:**
- Check console output where `streamlit run dashboard.py` is running
- Or check `~/.streamlit/logs/`

### Common Commands

**Check if Flask is running:**
```bash
curl http://localhost:5000/api/health
```

**Check if Streamlit is running:**
```bash
# Open browser to http://localhost:8501
```

**Restart services:**
```bash
# Press Ctrl+C to stop
# Then restart with python app.py or streamlit run dashboard.py
```

### Support Resources

1. **Documentation:**
   - README.md - Main documentation
   - QUICKSTART.md - Quick start guide
   - ARCHITECTURE.md - Technical details

2. **Test Suite:**
   ```bash
   python test_system.py
   ```

3. **Python Package Issues:**
   - Check [PyPI](https://pypi.org/) for package documentation
   - Check package GitHub issues

4. **Prophet Issues:**
   - [Prophet Documentation](https://facebook.github.io/prophet/)
   - [Prophet GitHub](https://github.com/facebook/prophet)

---

## Next Steps

After successful installation:

1. **Read QUICKSTART.md** for a 3-minute tutorial
2. **Run the test suite** to verify everything works
3. **Start the application** and explore the dashboard
4. **Review DEMO_GUIDE.md** for presentation tips

---

## Installation Checklist

- [ ] Python 3.8+ installed
- [ ] pip updated to latest version
- [ ] Virtual environment created (optional)
- [ ] All dependencies installed from requirements.txt
- [ ] Data files generated
- [ ] Test suite passes
- [ ] Flask backend starts successfully
- [ ] Streamlit dashboard opens in browser
- [ ] All dashboard pages load correctly
- [ ] Forecasts are generated
- [ ] API endpoints respond

---

**Installation complete! You're ready to use Smart Procurement System! 🚀**
