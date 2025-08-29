#!/usr/bin/env python3
"""
Quick Setup Script for Integrated Learning System
Installs dependencies and sets up the system
"""

import os
import sys
import subprocess
import platform

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"STDOUT: {e.stdout}")
        if e.stderr:
            print(f"STDERR: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ required, found {version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def upgrade_pip():
    """Upgrade pip to latest version"""
    return run_command(f"{sys.executable} -m pip install --upgrade pip", "Upgrading pip")

def install_requirements():
    """Install requirements from requirements.txt"""
    if not os.path.exists("requirements.txt"):
        print("❌ requirements.txt not found")
        return False
    
    return run_command(f"{sys.executable} -m pip install -r requirements.txt", "Installing requirements")

def install_additional_packages():
    """Install additional packages that might be needed"""
    additional_packages = [
        "wheel",
        "setuptools",
        "cython"
    ]
    
    for package in additional_packages:
        run_command(f"{sys.executable} -m pip install {package}", f"Installing {package}")

def setup_directories():
    """Create necessary directories"""
    print("📁 Creating directories...")
    
    directories = [
        "models",
        "data", 
        "logs",
        "templates",
        "videos",
        "streams",
        "reports",
        "checkpoints"
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"   Created {directory}/")
        else:
            print(f"   {directory}/ already exists")
    
    print("✅ Directory setup complete")

def create_gitignore():
    """Create .gitignore file"""
    print("📝 Creating .gitignore...")
    
    gitignore_content = """
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Project specific
models/*.pth
models/*.pt
data/*.json
data/*.csv
logs/*.log
videos/*.mp4
streams/*.mp4
reports/*.html
reports/*.pdf
checkpoints/*.pth
checkpoints/*.pt

# Temporary files
temp_*
*.tmp
*.temp

# Configuration (if contains sensitive data)
config.json
secrets.json
.env
"""
    
    with open(".gitignore", "w") as f:
        f.write(gitignore_content)
    
    print("✅ .gitignore created")

def create_readme():
    """Create README.md file"""
    print("📖 Creating README.md...")
    
    readme_content = """# Integrated Learning System

A comprehensive AI system that learns to play Rocket League like professional players through:

1. **Imitation Learning** - Learning from jstn and GarettG's gameplay videos
2. **PPO Training** - Reinforcement learning to improve performance
3. **Online Testing** - Real-time testing against live streams

## Features

- 🎥 **Video Analysis** - Extracts controller inputs from YouTube videos
- 🔴 **Live Stream Analysis** - Real-time analysis of Twitch streams
- 🧠 **Imitation Learning** - Neural network learns from pro player patterns
- 🚀 **PPO Training** - Advanced reinforcement learning
- 🌐 **Online Testing** - Validation against live gameplay

## Quick Start

1. **Setup System:**
   ```bash
   python setup_integrated_system.py
   ```

2. **Launch Learning Pipeline:**
   ```bash
   python launch_integrated_learning.py
   ```

3. **Install Dependencies Only:**
   ```bash
   python launch_integrated_learning.py --install-deps
   ```

## System Requirements

- Python 3.8+
- 8GB+ RAM recommended
- Windows 10/11 (optimized for Windows)
- NVIDIA GPU (optional, for faster training)

## Training Pipeline

### Phase 1: Imitation Learning
- Analyzes pro player videos
- Extracts controller inputs
- Trains neural network to mimic pro behavior

### Phase 2: PPO Training
- Uses imitation learning as foundation
- Applies reinforcement learning
- Optimizes for game performance

### Phase 3: Online Testing
- Tests against live streams
- Validates in real game environment
- Generates performance reports

## Configuration

Edit `config.json` to customize:
- Training parameters
- Pro player video URLs
- Model architecture
- Learning rates

## Files

- `integrated_learning_system.py` - Main learning system
- `pro_player_analyzer.py` - Video/stream analysis
- `jstn_multi_mode_trainer.py` - PPO training
- `launch_integrated_learning.py` - System launcher
- `setup_integrated_system.py` - Setup script

## Support

For issues or questions, check the logs in the `logs/` directory.
"""
    
    with open("README.md", "w") as f:
        f.write(readme_content)
    
    print("✅ README.md created")

def test_imports():
    """Test if all required packages can be imported"""
    print("🧪 Testing imports...")
    
    test_packages = [
        ("torch", "PyTorch"),
        ("numpy", "NumPy"),
        ("cv2", "OpenCV"),
        ("yt_dlp", "yt-dlp"),
        ("requests", "Requests"),
        ("bs4", "BeautifulSoup"),
        ("rlgym", "RLGym"),
        ("stable_baselines3", "Stable Baselines3"),
        ("matplotlib", "Matplotlib")
    ]
    
    failed_imports = []
    
    for package, name in test_packages:
        try:
            __import__(package)
            print(f"   ✅ {name}")
        except ImportError:
            print(f"   ❌ {name}")
            failed_imports.append(name)
    
    if failed_imports:
        print(f"\n⚠️ Failed imports: {', '.join(failed_imports)}")
        print("Try running: python -m pip install -r requirements.txt")
        return False
    
    print("✅ All imports successful!")
    return True

def main():
    """Main setup function"""
    print("🚀 Integrated Learning System Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Upgrade pip
    if not upgrade_pip():
        print("⚠️ Pip upgrade failed, continuing...")
    
    # Install additional packages first
    install_additional_packages()
    
    # Install requirements
    if not install_requirements():
        print("❌ Requirements installation failed")
        return
    
    # Setup directories
    setup_directories()
    
    # Create files
    create_gitignore()
    create_readme()
    
    # Test imports
    if not test_imports():
        print("⚠️ Some packages failed to import")
        print("You may need to install them manually")
    
    print("\n🎉 Setup Complete!")
    print("\nNext steps:")
    print("1. Add pro player video URLs to config.json")
    print("2. Run: python launch_integrated_learning.py")
    print("3. Follow the interactive prompts")
    
    print(f"\nSystem Info:")
    print(f"   OS: {platform.system()} {platform.release()}")
    print(f"   Python: {sys.version}")
    print(f"   Architecture: {platform.architecture()[0]}")

if __name__ == "__main__":
    main()
