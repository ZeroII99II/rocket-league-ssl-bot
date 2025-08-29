#!/usr/bin/env python3
"""
🚀 ULTIMATE OPTI LAUNCHER 🚀
===========================

Quick launcher for the Ultimate Opti Training System.
This script provides an easy interface to start training with optimal settings.

Author: Ultimate Opti Team
Version: 3.0.0
"""

import os
import sys
import time
from pathlib import Path
from typing import Optional

# Colors for beautiful output
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_banner():
    """Print the ultimate launcher banner."""
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
🚀={'='*70}🚀
🏆 ULTIMATE OPTI LAUNCHER - SSL Bot Training System 🏆
🚀{'='*70}🚀
{Colors.END}

{Colors.BOLD}🎯 Available Training Modes:{Colors.END}
{Colors.GREEN}1.{Colors.END} 🥉 Bronze to SSL Progression (Recommended for new bots)
{Colors.GREEN}2.{Colors.END} 🏆 JSTN Style Training (Creative & aggressive like JSTN)
{Colors.GREEN}3.{Colors.END} 🤖 Opti Replication (Replicate the famous Opti bot)
{Colors.GREEN}4.{Colors.END} 🔧 Custom Mechanics Focus (Train specific skills)
{Colors.GREEN}5.{Colors.END} 🌐 Distributed Training (Multi-machine cluster)
{Colors.GREEN}6.{Colors.END} 🎮 Real Game Integration (Live game control)
{Colors.GREEN}7.{Colors.END} ⚙️  Setup System (First-time setup)
{Colors.GREEN}0.{Colors.END} 🚪 Exit

{Colors.YELLOW}💡 Tip: Run setup (option 7) if this is your first time!{Colors.END}
"""
    print(banner)

def check_setup() -> bool:
    """Check if the system is properly set up."""
    venv_path = Path(".venv")
    ultimate_trainer = Path("ULTIMATE_OPTI_TRAINER.py")
    requirements = Path("requirements_ultimate.txt")
    
    if not venv_path.exists():
        return False
    if not ultimate_trainer.exists():
        return False
    if not requirements.exists():
        return False
    
    return True

def run_setup():
    """Run the setup script."""
    print(f"\n{Colors.CYAN}🔧 Running Ultimate Opti Setup...{Colors.END}")
    
    setup_script = Path("setup_ultimate.py")
    if not setup_script.exists():
        print(f"{Colors.RED}❌ Setup script not found!{Colors.END}")
        return False
    
    os.system(f"python {setup_script}")
    return True

def get_python_executable() -> str:
    """Get the virtual environment Python executable."""
    if os.name == 'nt':  # Windows
        return ".venv\\Scripts\\python.exe"
    else:  # Linux/macOS
        return ".venv/bin/python"

def launch_training(mode: str, extra_args: str = ""):
    """Launch the training with specified mode."""
    python_exe = get_python_executable()
    
    if not Path(python_exe).exists():
        print(f"{Colors.RED}❌ Virtual environment not found! Please run setup first.{Colors.END}")
        return False
    
    print(f"\n{Colors.GREEN}🚀 Starting Ultimate Opti Training...{Colors.END}")
    print(f"{Colors.BLUE}Mode: {mode}{Colors.END}")
    print(f"{Colors.YELLOW}Press Ctrl+C to stop training{Colors.END}\n")
    
    # Add a small delay for dramatic effect
    for i in range(3, 0, -1):
        print(f"{Colors.CYAN}Starting in {i}...{Colors.END}")
        time.sleep(1)
    
    print(f"{Colors.BOLD}{Colors.GREEN}🚀 LAUNCH! 🚀{Colors.END}\n")
    
    # Launch the training
    cmd = f"{python_exe} ULTIMATE_OPTI_TRAINER.py --mode {mode} {extra_args}"
    os.system(cmd)
    
    return True

def main():
    """Main launcher function."""
    while True:
        print_banner()
        
        # Check if system is set up
        if not check_setup():
            print(f"{Colors.YELLOW}⚠️  System not set up yet. Please run setup (option 7) first!{Colors.END}")
        
        try:
            choice = input(f"\n{Colors.BOLD}Choose your training mode (1-7, 0 to exit): {Colors.END}").strip()
            
            if choice == "0":
                print(f"\n{Colors.CYAN}👋 Thanks for using Ultimate Opti! See you in SSL! 🏆{Colors.END}")
                break
            
            elif choice == "1":
                print(f"\n{Colors.GREEN}🥉 Bronze to SSL Progression Selected{Colors.END}")
                print("This mode will train your bot from Bronze level all the way to SSL!")
                print("Perfect for new bots - includes all mechanics and progressive difficulty.")
                
                if input(f"\n{Colors.YELLOW}Start training? (y/N): {Colors.END}").lower() == 'y':
                    launch_training("bronze_to_ssl")
            
            elif choice == "2":
                print(f"\n{Colors.GREEN}🏆 JSTN Style Training Selected{Colors.END}")
                print("Train like JSTN - creative, aggressive, and mechanically intensive!")
                print("Focus on aerial mastery, flip resets, and creative mechanics.")
                
                if input(f"\n{Colors.YELLOW}Start JSTN-style training? (y/N): {Colors.END}").lower() == 'y':
                    launch_training("jstn_style")
            
            elif choice == "3":
                print(f"\n{Colors.GREEN}🤖 Opti Replication Selected{Colors.END}")
                print("Replicate the famous Opti bot architecture and training!")
                print("Uses modular sub-models for each specialized mechanic.")
                
                if input(f"\n{Colors.YELLOW}Start Opti replication? (y/N): {Colors.END}").lower() == 'y':
                    launch_training("opti_replication")
            
            elif choice == "4":
                print(f"\n{Colors.GREEN}🔧 Custom Mechanics Focus Selected{Colors.END}")
                print("Focus training on specific mechanics of your choice.")
                
                print(f"\n{Colors.BOLD}Available Mechanics:{Colors.END}")
                mechanics = [
                    "aerial", "flip_reset", "dtap", "wall", "recovery", "kickoff",
                    "flick", "ceil_pinch", "walldash", "demo", "gp", "half_flip",
                    "lix", "pinch", "selector"
                ]
                
                for i, mech in enumerate(mechanics, 1):
                    print(f"  {i:2}. {mech}")
                
                selected = input(f"\n{Colors.YELLOW}Enter mechanic numbers (comma-separated, e.g., 1,2,3): {Colors.END}")
                
                if selected.strip():
                    launch_training("custom_mechanics", f"--mechanics {selected}")
            
            elif choice == "5":
                print(f"\n{Colors.GREEN}🌐 Distributed Training Selected{Colors.END}")
                print("Train across multiple machines for maximum performance!")
                print("Requires Redis server and network configuration.")
                
                is_master = input(f"\n{Colors.YELLOW}Is this the master node? (y/N): {Colors.END}").lower() == 'y'
                
                if is_master:
                    launch_training("distributed", "--master")
                else:
                    master_ip = input(f"{Colors.YELLOW}Enter master node IP: {Colors.END}").strip()
                    if master_ip:
                        launch_training("distributed", f"--worker --master-host {master_ip}")
            
            elif choice == "6":
                print(f"\n{Colors.GREEN}🎮 Real Game Integration Selected{Colors.END}")
                print("Control and learn from real Rocket League matches!")
                print("⚠️  Make sure Rocket League is running and you're in a match.")
                
                if input(f"\n{Colors.YELLOW}Start real game integration? (y/N): {Colors.END}").lower() == 'y':
                    launch_training("real_game", "--real-game --overlay")
            
            elif choice == "7":
                print(f"\n{Colors.GREEN}⚙️  System Setup Selected{Colors.END}")
                print("This will set up your system for Ultimate Opti training.")
                
                if input(f"\n{Colors.YELLOW}Run setup now? (y/N): {Colors.END}").lower() == 'y':
                    run_setup()
                    input(f"\n{Colors.GREEN}Setup completed! Press Enter to continue...{Colors.END}")
            
            else:
                print(f"\n{Colors.RED}❌ Invalid choice. Please select 1-7 or 0 to exit.{Colors.END}")
                input(f"{Colors.YELLOW}Press Enter to continue...{Colors.END}")
        
        except KeyboardInterrupt:
            print(f"\n\n{Colors.CYAN}👋 Thanks for using Ultimate Opti! See you in SSL! 🏆{Colors.END}")
            break
        except Exception as e:
            print(f"\n{Colors.RED}❌ Error: {e}{Colors.END}")
            input(f"{Colors.YELLOW}Press Enter to continue...{Colors.END}")

if __name__ == "__main__":
    main()
