#!/usr/bin/env python3
"""
Integrated Learning System Launcher
Launches the complete learning pipeline: Imitation Learning -> PPO -> Online Testing
"""

import os
import sys
import subprocess
import time
from typing import List, Dict, Optional

class IntegratedLearningLauncher:
    """Launcher for the integrated learning system"""
    
    def __init__(self):
        self.required_packages = [
            'torch',
            'torchvision', 
            'numpy',
            'opencv-python',
            'pytesseract',
            'yt-dlp',
            'beautifulsoup4',
            'requests',
            'rlgym',
            'stable-baselines3',
            'gymnasium',
            'matplotlib',
            'tensorboard',
            'wandb'
        ]
        
        self.system_ready = False
        
    def check_system_requirements(self) -> bool:
        """Check if system meets requirements"""
        print("🔍 Checking system requirements...")
        
        # Check Python version
        if sys.version_info < (3, 8):
            print("❌ Python 3.8+ required")
            return False
        
        # Check if we're on Windows
        if os.name != 'nt':
            print("⚠️ This system is optimized for Windows")
        
        # Check available memory
        try:
            import psutil
            memory_gb = psutil.virtual_memory().total / (1024**3)
            if memory_gb < 8:
                print(f"⚠️ Low memory detected: {memory_gb:.1f}GB (8GB+ recommended)")
        except ImportError:
            print("⚠️ Cannot check memory (psutil not installed)")
        
        print("✅ System requirements check complete")
        return True
    
    def install_dependencies(self) -> bool:
        """Install required dependencies"""
        print("📦 Installing dependencies...")
        
        for package in self.required_packages:
            try:
                print(f"   Installing {package}...")
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
                print(f"   ✅ {package} installed")
            except subprocess.CalledProcessError as e:
                print(f"   ❌ Failed to install {package}: {e}")
                return False
        
        print("✅ All dependencies installed successfully!")
        return True
    
    def setup_directories(self):
        """Create necessary directories"""
        print("📁 Setting up directories...")
        
        directories = [
            'models',
            'data',
            'logs',
            'templates',
            'videos',
            'streams',
            'reports'
        ]
        
        for directory in directories:
            if not os.path.exists(directory):
                os.makedirs(directory)
                print(f"   Created {directory}/")
        
        print("✅ Directory setup complete!")
    
    def create_config_file(self):
        """Create configuration file"""
        print("⚙️ Creating configuration file...")
        
        config = {
            "learning_phases": {
                "imitation_learning": {
                    "episodes": 1000,
                    "learning_rate": 0.001,
                    "batch_size": 64
                },
                "ppo_training": {
                    "episodes": 5000,
                    "learning_rate": 0.0003,
                    "batch_size": 64
                },
                "online_testing": {
                    "episodes": 100,
                    "learning_rate": 0.0001
                }
            },
            "pro_players": {
                "jstn": {
                    "videos": [
                        "https://www.youtube.com/watch?v=jstn_example1",
                        "https://www.youtube.com/watch?v=jstn_example2"
                    ],
                    "streams": ["https://www.twitch.tv/jstn"]
                },
                "GarettG": {
                    "videos": [
                        "https://www.youtube.com/watch?v=garettg_example1",
                        "https://www.youtube.com/watch?v=garettg_example2"
                    ],
                    "streams": ["https://www.twitch.tv/garettg"]
                }
            },
            "model_settings": {
                "input_size": 10,
                "hidden_size": 512,
                "output_size": 8,
                "dropout": 0.2
            },
            "training_settings": {
                "save_interval": 100,
                "log_interval": 10,
                "eval_interval": 50
            }
        }
        
        import json
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=2)
        
        print("✅ Configuration file created!")
    
    def get_user_input(self) -> Dict:
        """Get user input for training configuration"""
        print("\n🎯 Training Configuration")
        print("=" * 40)
        
        config = {}
        
        # Get pro player video URLs
        print("\n📺 Pro Player Videos")
        print("Enter YouTube URLs for pro player videos (press Enter when done):")
        
        jstn_videos = []
        garettg_videos = []
        
        while True:
            url = input("jstn video URL (or Enter to finish): ").strip()
            if not url:
                break
            if 'jstn' in url.lower() or 'justin' in url.lower():
                jstn_videos.append(url)
            else:
                print("⚠️ URL doesn't appear to be jstn-related")
        
        while True:
            url = input("GarettG video URL (or Enter to finish): ").strip()
            if not url:
                break
            if 'garettg' in url.lower() or 'garett' in url.lower():
                garettg_videos.append(url)
            else:
                print("⚠️ URL doesn't appear to be GarettG-related")
        
        config['jstn_videos'] = jstn_videos
        config['garettg_videos'] = garettg_videos
        
        # Get training parameters
        print("\n⚙️ Training Parameters")
        
        try:
            imitation_episodes = int(input("Imitation learning episodes (default 1000): ") or "1000")
            ppo_episodes = int(input("PPO training episodes (default 5000): ") or "5000")
            online_episodes = int(input("Online testing episodes (default 100): ") or "100")
            
            config['imitation_episodes'] = imitation_episodes
            config['ppo_episodes'] = ppo_episodes
            config['online_episodes'] = online_episodes
            
        except ValueError:
            print("⚠️ Invalid input, using defaults")
            config['imitation_episodes'] = 1000
            config['ppo_episodes'] = 5000
            config['online_episodes'] = 100
        
        # Get live stream URLs
        print("\n🔴 Live Streams (optional)")
        print("Enter Twitch/YouTube stream URLs for live testing (press Enter when done):")
        
        live_streams = []
        while True:
            url = input("Stream URL (or Enter to finish): ").strip()
            if not url:
                break
            live_streams.append(url)
        
        config['live_streams'] = live_streams
        
        return config
    
    def launch_learning_pipeline(self, config: Dict):
        """Launch the integrated learning pipeline"""
        print("\n🚀 Launching Integrated Learning Pipeline")
        print("=" * 50)
        
        try:
            # Import the integrated learning system
            from integrated_learning_system import IntegratedLearningSystem
            
            # Initialize system
            learning_system = IntegratedLearningSystem()
            
            # Update training phases with user config
            learning_system.training_phases[0].duration = config.get('imitation_episodes', 1000)
            learning_system.training_phases[1].duration = config.get('ppo_episodes', 5000)
            learning_system.training_phases[2].duration = config.get('online_episodes', 100)
            
            # Prepare video URLs
            all_videos = config.get('jstn_videos', []) + config.get('garettg_videos', [])
            live_streams = config.get('live_streams', [])
            
            if not all_videos:
                print("⚠️ No videos provided, using example URLs")
                all_videos = [
                    "https://www.youtube.com/watch?v=jstn_example1",
                    "https://www.youtube.com/watch?v=garettg_example1"
                ]
            
            # Start the pipeline
            learning_system.start_learning_pipeline(all_videos, live_streams)
            
        except ImportError as e:
            print(f"❌ Import error: {e}")
            print("Make sure integrated_learning_system.py is in the same directory")
        except Exception as e:
            print(f"❌ Pipeline error: {e}")
    
    def run_system_check(self):
        """Run a quick system check"""
        print("\n🔍 Running System Check")
        print("=" * 30)
        
        # Check if all required files exist
        required_files = [
            'integrated_learning_system.py',
            'pro_player_analyzer.py',
            'jstn_multi_mode_trainer.py'
        ]
        
        missing_files = []
        for file in required_files:
            if not os.path.exists(file):
                missing_files.append(file)
        
        if missing_files:
            print(f"❌ Missing files: {', '.join(missing_files)}")
            return False
        
        # Check if dependencies are installed
        missing_packages = []
        for package in self.required_packages:
            try:
                __import__(package.replace('-', '_'))
            except ImportError:
                missing_packages.append(package)
        
        if missing_packages:
            print(f"⚠️ Missing packages: {', '.join(missing_packages)}")
            print("Run with --install-deps to install missing packages")
            return False
        
        print("✅ System check passed!")
        return True
    
    def show_help(self):
        """Show help information"""
        print("""
🚀 Integrated Learning System Launcher

USAGE:
    python launch_integrated_learning.py [OPTIONS]

OPTIONS:
    --install-deps     Install required dependencies
    --setup           Setup directories and config files
    --check           Run system check
    --help            Show this help message

EXAMPLES:
    python launch_integrated_learning.py --install-deps
    python launch_integrated_learning.py --setup
    python launch_integrated_learning.py --check
    python launch_integrated_learning.py

DESCRIPTION:
    This launcher sets up and runs the complete learning pipeline:
    1. Imitation Learning from pro player videos
    2. PPO Training with imitation learning foundation
    3. Online Testing against live streams

    The system will learn from jstn and GarettG's gameplay patterns
    and train a bot to play like the pros!
        """)

def main():
    """Main function"""
    launcher = IntegratedLearningLauncher()
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        if '--help' in sys.argv or '-h' in sys.argv:
            launcher.show_help()
            return
        
        if '--install-deps' in sys.argv:
            if not launcher.check_system_requirements():
                return
            if not launcher.install_dependencies():
                return
            print("✅ Dependencies installed successfully!")
            return
        
        if '--setup' in sys.argv:
            launcher.setup_directories()
            launcher.create_config_file()
            print("✅ Setup complete!")
            return
        
        if '--check' in sys.argv:
            launcher.run_system_check()
            return
    
    # Interactive mode
    print("🚀 Integrated Learning System Launcher")
    print("=" * 50)
    
    # Check system
    if not launcher.check_system_requirements():
        print("❌ System requirements not met")
        return
    
    # Check if system is ready
    if not launcher.run_system_check():
        print("\n🔧 System not ready. Options:")
        print("1. Install dependencies: python launch_integrated_learning.py --install-deps")
        print("2. Setup system: python launch_integrated_learning.py --setup")
        print("3. Run system check: python launch_integrated_learning.py --check")
        return
    
    # Setup if needed
    if not os.path.exists('config.json'):
        print("\n⚙️ Setting up system...")
        launcher.setup_directories()
        launcher.create_config_file()
    
    # Get user configuration
    config = launcher.get_user_input()
    
    # Confirm launch
    print(f"\n🎯 Ready to launch with:")
    print(f"   jstn videos: {len(config.get('jstn_videos', []))}")
    print(f"   GarettG videos: {len(config.get('garettg_videos', []))}")
    print(f"   Live streams: {len(config.get('live_streams', []))}")
    print(f"   Imitation episodes: {config.get('imitation_episodes', 1000)}")
    print(f"   PPO episodes: {config.get('ppo_episodes', 5000)}")
    print(f"   Online episodes: {config.get('online_episodes', 100)}")
    
    confirm = input("\n🚀 Launch learning pipeline? (y/N): ").strip().lower()
    if confirm in ['y', 'yes']:
        launcher.launch_learning_pipeline(config)
    else:
        print("❌ Launch cancelled")

if __name__ == "__main__":
    main()
