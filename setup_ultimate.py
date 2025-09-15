#!/usr/bin/env python3
"""
🚀 Ultimate Opti Setup Script 🚀
===============================

Automated setup for the Ultimate Opti Training System.
This script will:
- Validate system requirements
- Install all dependencies
- Configure Redis for distributed training
- Set up directory structure
- Initialize configuration files
- Validate installation

Author: Ultimate Opti Team
Version: 3.0.0
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path
from typing import List, Tuple, Optional
import json
import time

class Colors:
    """ANSI color codes for beautiful terminal output."""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def print_banner():
    """Print the ultimate banner."""
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
🚀={'='*80}🚀
🏆 ULTIMATE OPTI SETUP - The Complete SSL Bot Training System 🏆
🚀{'='*80}🚀
{Colors.END}

{Colors.BOLD}✨ What this setup will do:{Colors.END}
   🔍 Validate system requirements (CPU, RAM, GPU, Python)
   📦 Install all required dependencies
   🌐 Configure Redis for distributed training
   📁 Create optimal directory structure
   ⚙️ Initialize configuration files
   🧪 Validate complete installation
   🚀 Prepare for SSL-level training

{Colors.YELLOW}⚡ Hardware Recommendations for Elite Performance:{Colors.END}
   🖥️  CPU: 16+ cores (Intel i7/i9, AMD Ryzen 7/9)
   🎮 GPU: RTX 3070+ / RTX 4060+ (8GB+ VRAM)
   💾 RAM: 32GB+ (16GB minimum)
   💿 Storage: NVMe SSD with 50GB+ free space
   🌐 Network: Stable internet for distributed training

{Colors.GREEN}Let's build the ultimate Rocket League AI! 🏆{Colors.END}
"""
    print(banner)

def print_success(text: str):
    """Print success message."""
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")

def print_warning(text: str):
    """Print warning message."""
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")

def print_error(text: str):
    """Print error message."""
    print(f"{Colors.RED}❌ {text}{Colors.END}")

def print_info(text: str):
    """Print info message."""
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.END}")

def print_step(text: str):
    """Print step header."""
    print(f"\n{Colors.BOLD}{Colors.CYAN}🔧 {text}{Colors.END}")
    print(f"{Colors.CYAN}{'─' * (len(text) + 4)}{Colors.END}")

def run_command(command: List[str], capture_output: bool = False, timeout: int = 300) -> Tuple[bool, str]:
    """Run a command with timeout and proper error handling."""
    try:
        if capture_output:
            result = subprocess.run(command, capture_output=True, text=True, check=True, timeout=timeout)
            return True, result.stdout.strip()
        else:
            subprocess.run(command, check=True, timeout=timeout)
            return True, ""
    except subprocess.TimeoutExpired:
        return False, "Command timed out"
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr if hasattr(e, 'stderr') and e.stderr else str(e)
        return False, error_msg
    except Exception as e:
        return False, str(e)

def check_system_requirements():
    """Check comprehensive system requirements."""
    print_step("SYSTEM REQUIREMENTS VALIDATION")
    
    # Check Python version
    version = sys.version_info
    if version.major == 3 and version.minor >= 10:
        print_success(f"Python {version.major}.{version.minor}.{version.micro} - Perfect!")
    elif version.major == 3 and version.minor >= 8:
        print_warning(f"Python {version.major}.{version.minor}.{version.micro} - Supported but 3.10+ recommended")
    else:
        print_error(f"Python {version.major}.{version.minor}.{version.micro} - Requires Python 3.8+")
        return False
    
    # Check system resources
    try:
        import psutil
        
        # CPU check
        cpu_count = psutil.cpu_count(logical=False)
        cpu_count_logical = psutil.cpu_count(logical=True)
        print_info(f"CPU: {cpu_count} physical cores, {cpu_count_logical} logical cores")
        
        if cpu_count >= 16:
            print_success("CPU: Excellent for elite training! 🚀")
        elif cpu_count >= 8:
            print_success("CPU: Great for training!")
        elif cpu_count >= 4:
            print_warning("CPU: Good for basic training (consider upgrading for elite performance)")
        else:
            print_error("CPU: Insufficient cores for optimal training")
        
        # Memory check
        memory = psutil.virtual_memory()
        memory_gb = memory.total / (1024**3)
        print_info(f"RAM: {memory_gb:.1f} GB available")
        
        if memory_gb >= 32:
            print_success("RAM: Perfect for elite training! 🏆")
        elif memory_gb >= 16:
            print_success("RAM: Great for training!")
        elif memory_gb >= 8:
            print_warning("RAM: Adequate (16GB+ recommended for elite training)")
        else:
            print_error("RAM: Insufficient for elite training (8GB minimum)")
            return False
        
        # Disk space check
        disk_usage = psutil.disk_usage('.')
        free_gb = disk_usage.free / (1024**3)
        print_info(f"Free disk space: {free_gb:.1f} GB")
        
        if free_gb >= 100:
            print_success("Storage: Plenty of space for training data!")
        elif free_gb >= 50:
            print_success("Storage: Good for training")
        elif free_gb >= 20:
            print_warning("Storage: Limited space (consider freeing up more)")
        else:
            print_error("Storage: Insufficient space (20GB minimum required)")
            return False
        
    except ImportError:
        print_warning("psutil not available - skipping detailed system check")
    
    # Check GPU availability
    print_info("Checking GPU availability...")
    try:
        import torch
        if torch.cuda.is_available():
            gpu_count = torch.cuda.device_count()
            for i in range(gpu_count):
                gpu_name = torch.cuda.get_device_name(i)
                gpu_memory = torch.cuda.get_device_properties(i).total_memory / (1024**3)
                print_success(f"GPU {i}: {gpu_name} ({gpu_memory:.1f} GB VRAM)")
            
            if "RTX" in gpu_name or "GTX" in gpu_name:
                print_success("GPU: Perfect for elite training! 🎮")
            else:
                print_info("GPU: Available (NVIDIA RTX recommended for best performance)")
        else:
            print_warning("No GPU detected - will use CPU training (much slower)")
    except ImportError:
        print_info("PyTorch not installed yet - GPU check will be performed after installation")
    
    return True

def create_virtual_environment():
    """Create and setup virtual environment."""
    print_step("VIRTUAL ENVIRONMENT SETUP")
    
    venv_path = Path(".venv")
    if venv_path.exists():
        print_warning("Virtual environment already exists")
        response = input(f"{Colors.YELLOW}Do you want to recreate it? (y/N): {Colors.END}").lower()
        if response == 'y':
            print_info("Removing existing virtual environment...")
            shutil.rmtree(venv_path)
        else:
            print_info("Using existing virtual environment")
            return True
    
    print_info("Creating virtual environment...")
    success, output = run_command([sys.executable, "-m", "venv", ".venv"])
    if success:
        print_success("Virtual environment created successfully!")
        return True
    else:
        print_error(f"Failed to create virtual environment: {output}")
        return False

def get_python_executable() -> str:
    """Get the correct Python executable for the virtual environment."""
    if platform.system() == "Windows":
        return ".venv\\Scripts\\python.exe"
    else:
        return ".venv/bin/python"

def install_dependencies():
    """Install all ultimate dependencies."""
    print_step("DEPENDENCY INSTALLATION")
    
    python_exe = get_python_executable()
    
    # Check if venv Python exists
    if not Path(python_exe).exists():
        print_error("Virtual environment Python not found!")
        return False
    
    # Upgrade pip, wheel, and setuptools
    print_info("Upgrading pip, wheel, and setuptools...")
    success, output = run_command([python_exe, "-m", "pip", "install", "-U", "pip", "wheel", "setuptools"], timeout=180)
    if not success:
        print_error(f"Failed to upgrade pip: {output}")
        return False
    print_success("Package management tools upgraded!")
    
    # Install PyTorch (with CUDA support if available)
    print_info("Installing PyTorch...")
    try:
        # Try to detect CUDA version
        success, cuda_version = run_command(["nvidia-smi"], capture_output=True)
        if success and "CUDA Version" in cuda_version:
            print_info("CUDA detected - installing PyTorch with GPU support")
            torch_cmd = [python_exe, "-m", "pip", "install", "torch", "torchvision", "torchaudio", 
                        "--index-url", "https://download.pytorch.org/whl/cu121"]
        else:
            print_info("No CUDA detected - installing PyTorch with CPU support")
            torch_cmd = [python_exe, "-m", "pip", "install", "torch", "torchvision", "torchaudio",
                        "--index-url", "https://download.pytorch.org/whl/cpu"]
        
        success, output = run_command(torch_cmd, timeout=600)  # 10 minutes timeout for PyTorch
        if not success:
            print_error(f"Failed to install PyTorch: {output}")
            return False
        print_success("PyTorch installed successfully!")
        
    except Exception as e:
        print_error(f"PyTorch installation failed: {e}")
        return False
    
    # Install ultimate requirements
    print_info("Installing ultimate requirements (this may take a while)...")
    req_file = "requirements_ultimate.txt"
    if not Path(req_file).exists():
        print_error(f"Requirements file {req_file} not found!")
        return False
    
    success, output = run_command([python_exe, "-m", "pip", "install", "-r", req_file], timeout=1800)  # 30 minutes
    if not success:
        print_error(f"Failed to install requirements: {output}")
        return False
    
    print_success("All ultimate requirements installed successfully! 🎉")
    return True

def setup_redis():
    """Set up Redis for distributed training."""
    print_step("REDIS SETUP FOR DISTRIBUTED TRAINING")
    
    # Check if Redis is already running
    try:
        import redis
        client = redis.Redis(host='localhost', port=6379, db=0)
        client.ping()
        print_success("Redis is already running and accessible!")
        return True
    except:
        pass
    
    # Try to install and start Redis
    if platform.system() == "Windows":
        print_info("On Windows, please install Redis manually:")
        print_info("1. Download Redis from: https://github.com/microsoftarchive/redis/releases")
        print_info("2. Extract and run redis-server.exe")
        print_info("3. Or use Docker: docker run -d -p 6379:6379 redis:alpine")
    else:
        print_info("Attempting to install Redis...")
        
        # Try different package managers
        for cmd in [["sudo", "apt-get", "install", "-y", "redis-server"], 
                   ["sudo", "yum", "install", "-y", "redis"], 
                   ["brew", "install", "redis"]]:
            try:
                success, output = run_command(cmd, timeout=300)
                if success:
                    print_success("Redis installed successfully!")
                    # Try to start Redis
                    subprocess.Popen(["redis-server", "--daemonize", "yes"])
                    time.sleep(2)  # Wait for Redis to start
                    return True
            except:
                continue
        
        print_warning("Could not auto-install Redis. Please install manually:")
        print_info("Ubuntu/Debian: sudo apt-get install redis-server")
        print_info("CentOS/RHEL: sudo yum install redis")
        print_info("macOS: brew install redis")
    
    return False  # Redis not available, but training can continue without it

def create_directory_structure():
    """Create the complete directory structure."""
    print_step("DIRECTORY STRUCTURE CREATION")
    
    directories = [
        "models",           # Trained models
        "checkpoints",      # Training checkpoints
        "logs",            # Training logs
        "configs",         # Configuration files
        "data",            # Training data
        "evaluations",     # Evaluation results
        "pretrained_agents", # Pretrained agent models
        "submodels",       # Specialized sub-models
        "scripts",         # Helper scripts
        "utils",           # Utility modules
        "tests",           # Test files
        "docs",            # Documentation
        "results",         # Training results
        "visualizations"   # Data visualizations
    ]
    
    created_count = 0
    for directory in directories:
        dir_path = Path(directory)
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
            created_count += 1
    
    print_success(f"Directory structure created ({created_count} new directories)")
    
    # Create .gitignore for the project
    gitignore_content = """
# Virtual environments
.venv/
venv/
env/

# Python cache
__pycache__/
*.py[cod]
*.so

# Training outputs
checkpoints/
models/
logs/
*.log
*.pkl
*.pth
*.pt

# Data files
data/
*.csv
*.json
*.npy

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Weights & Biases
wandb/

# Redis
dump.rdb

# Temporary files
temp/
tmp/
*.tmp
"""
    
    with open(".gitignore", "w") as f:
        f.write(gitignore_content.strip())
    
    print_success("Project .gitignore created")

def create_default_configs():
    """Create default configuration files."""
    print_step("DEFAULT CONFIGURATION CREATION")
    
    # Create default training config
    default_config = {
        "training_mode": "bronze_to_ssl",
        "n_proc": min(os.cpu_count() or 4, 16),
        "use_gpu": True,
        "distributed_training": True,
        "team_size": 3,
        "learning_rate": 0.0003,
        "batch_size": 100000,
        "use_wandb": True,
        "wandb_project": "ultimate-opti-ssl",
        "ssl_target_level": 0.8
    }
    
    config_path = Path("configs/default_config.json")
    config_path.parent.mkdir(exist_ok=True)
    
    with open(config_path, "w") as f:
        json.dump(default_config, f, indent=2)
    
    print_success("Default configuration created")
    
    # Create launch scripts
    if platform.system() == "Windows":
        launch_script = """@echo off
echo 🚀 Starting Ultimate Opti Training...
call .venv\\Scripts\\activate
python ULTIMATE_OPTI_TRAINER.py
pause
"""
        with open("scripts/launch_training.bat", "w") as f:
            f.write(launch_script)
        print_success("Windows launch script created")
    else:
        launch_script = """#!/bin/bash
echo "🚀 Starting Ultimate Opti Training..."
source .venv/bin/activate
python ULTIMATE_OPTI_TRAINER.py
"""
        script_path = Path("scripts/launch_training.sh")
        with open(script_path, "w") as f:
            f.write(launch_script)
        script_path.chmod(0o755)  # Make executable
        print_success("Linux/macOS launch script created")

def validate_installation():
    """Validate the complete installation."""
    print_step("INSTALLATION VALIDATION")
    
    python_exe = get_python_executable()
    
    # Test script to validate all components
    test_script = '''
import sys
print("🧪 Testing Ultimate Opti Installation...")

# Test core dependencies
try:
    import torch
    print(f"✅ PyTorch {torch.__version__}")
    if torch.cuda.is_available():
        print(f"✅ CUDA available: {torch.cuda.get_device_name(0)}")
    else:
        print("ℹ️  CPU training mode (no GPU detected)")
except ImportError as e:
    print(f"❌ PyTorch import failed: {e}")
    sys.exit(1)

try:
    import numpy as np
    print(f"✅ NumPy {np.__version__}")
except ImportError as e:
    print(f"❌ NumPy import failed: {e}")
    sys.exit(1)

try:
    import redis
    client = redis.Redis(host='localhost', port=6379, db=0)
    client.ping()
    print("✅ Redis connection successful")
except:
    print("⚠️  Redis not available (distributed training disabled)")

try:
    import wandb
    print(f"✅ Weights & Biases available")
except ImportError:
    print("⚠️  W&B not available (logging disabled)")

# Test RLGym components
try:
    import rlgym
    print(f"✅ RLGym available")
except ImportError:
    print("⚠️  RLGym not available (using fallback training)")

try:
    import rlgym_ppo
    print(f"✅ RLGym-PPO available")
except ImportError:
    print("⚠️  RLGym-PPO not available (using fallback training)")

print("\\n🎉 Installation validation completed!")
print("🚀 Ready to train the ultimate SSL bot!")
'''
    
    # Write and run test script
    test_file = Path("_test_installation.py")
    test_file.write_text(test_script)
    
    try:
        success, output = run_command([python_exe, str(test_file)], capture_output=True, timeout=60)
        if success:
            print(output)
            print_success("Installation validation passed! 🎉")
            return True
        else:
            print_error(f"Validation failed: {output}")
            return False
    finally:
        # Clean up test file
        if test_file.exists():
            test_file.unlink()

def print_next_steps():
    """Print next steps for the user."""
    print_step("🏆 SETUP COMPLETE - NEXT STEPS")
    
    activation_cmd = ".venv\\Scripts\\Activate.ps1" if platform.system() == "Windows" else "source .venv/bin/activate"
    
    next_steps = f"""
{Colors.BOLD}🚀 Your Ultimate Opti Training System is ready! 🚀{Colors.END}

{Colors.BOLD}Quick Start:{Colors.END}
1️⃣  Activate virtual environment:
   {Colors.GREEN}{activation_cmd}{Colors.END}

2️⃣  Start training:
   {Colors.GREEN}python ULTIMATE_OPTI_TRAINER.py{Colors.END}

{Colors.BOLD}🎯 Training Features Available:{Colors.END}
   ✨ All specialized mechanics (aerial, flip_reset, dtap, etc.)
   🧠 Modern transformer-based neural architecture  
   🏆 JSTN-style creative and aggressive training
   📈 SSL-level progression system (Bronze → SSL)
   🌐 Distributed training with Redis
   📊 Professional monitoring with W&B
   🎮 Real game integration capabilities
   🔧 Modular sub-model architecture

{Colors.BOLD}⚙️ Optional Enhancements:{Colors.END}
   🔐 W&B Login: {Colors.CYAN}wandb login{Colors.END}
   🌐 Redis Setup: Start Redis server for distributed training
   🎮 GPU Optimization: Install CUDA-enabled PyTorch for maximum performance

{Colors.BOLD}📁 Important Files:{Colors.END}
   🚀 ULTIMATE_OPTI_TRAINER.py - Main training system
   ⚙️  configs/default_config.json - Training configuration
   📋 requirements_ultimate.txt - All dependencies
   🚀 scripts/launch_training.* - Quick launch scripts

{Colors.BOLD}{Colors.MAGENTA}🏆 Ready to reach Supersonic Legend! Good luck! 🏆{Colors.END}
"""
    
    print(next_steps)

def main():
    """Main setup function."""
    print_banner()
    
    # System validation
    if not check_system_requirements():
        print_error("System requirements not met. Please upgrade your system.")
        sys.exit(1)
    
    # Virtual environment setup
    if not create_virtual_environment():
        print_error("Failed to create virtual environment.")
        sys.exit(1)
    
    # Dependency installation
    if not install_dependencies():
        print_error("Failed to install dependencies.")
        sys.exit(1)
    
    # Redis setup (optional)
    setup_redis()
    
    # Directory structure
    create_directory_structure()
    
    # Configuration files
    create_default_configs()
    
    # Validation
    if not validate_installation():
        print_error("Installation validation failed.")
        sys.exit(1)
    
    # Success!
    print_next_steps()

if __name__ == "__main__":
    main()
