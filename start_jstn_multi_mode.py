#!/usr/bin/env python3
"""
JSTN Multi-Mode Training Launcher
Starts the complete JSTN multi-mode training system
"""

import subprocess
import sys
import time
import os

def main():
    print("🏆 JSTN Multi-Mode Training Launcher")
    print("🎯 Starting JSTN multi-mode training...")
    print("🚀 This will train the bot to play like jstn across 1s, 2s, and 3s!")
    
    # Start multi-mode trainer
    print("🧠 Starting JSTN multi-mode trainer...")
    trainer_process = subprocess.Popen([sys.executable, 'jstn_multi_mode_trainer.py'])
    
    print("✅ JSTN multi-mode training started!")
    print("📊 Training across 1s → 2s → 3s → repeat!")
    print("🎯 Press Ctrl+C to stop")
    
    try:
        # Wait for process
        trainer_process.wait()
    except KeyboardInterrupt:
        print("\n⏹️  Stopping training...")
        trainer_process.terminate()
        print("✅ Training stopped")

if __name__ == "__main__":
    main()
