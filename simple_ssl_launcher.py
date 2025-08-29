#!/usr/bin/env python3
"""
Simple SSL Launcher
Automatically starts SSL learning without menu interruptions
"""

import time
import sys
import os
from real_ssl_controller import RealSSLController

def main():
    """Main launcher function - auto-starts SSL learning"""
    print("🏆 SIMPLE SSL LAUNCHER")
    print("=" * 60)
    print("🎯 Auto-starting SSL learning")
    print("🧠 Reading real game data from PC files")
    print("⚡ Real inputs to real game")
    print("🎮 Starting 30-minute free play practice")
    print("🚀 Ready to control your car!")
    
    try:
        # Create controller
        controller = RealSSLController()
        
        # Connect to the game
        print("\n🔌 Connecting to Rocket League...")
        if not controller.connect_to_game():
            print("❌ Failed to connect to Rocket League!")
            print("💡 Make sure Rocket League is running and in free play")
            return
        
        print("✅ Connected to Rocket League!")
        print("🎮 Ready to control your car!")
        
        # Auto-start 30-minute practice
        print("\n🚀 Auto-starting 30-minute free play practice...")
        print("🎯 The bot will now control your car and learn SSL mechanics!")
        print("⚡ Watch your car move and learn in real-time!")
        
        # Start practice
        controller.run_real_freeplay_practice(30)
        
    except KeyboardInterrupt:
        print("\n⏹️ Practice interrupted by user")
        if 'controller' in locals():
            controller.stop_control()
            controller.generate_real_learning_report()
    except Exception as e:
        print(f"\n❌ Critical Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n👋 SSL learning session complete!")

if __name__ == "__main__":
    main()
