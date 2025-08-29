#!/usr/bin/env python3
"""
RLViser Launcher - Creates a proper game window using rlviser-py
This will open the actual RLViser window that looks like Rocket League
"""

import rlviser_py
import time
import threading
import sys

def launch_rlviser():
    """Launch RLViser with proper settings"""
    try:
        print("🎮 Launching RLViser...")
        print("   📺 This should open a proper Rocket League-style window!")
        
        # Launch RLViser
        rlviser_py.launch()
        
        print("✅ RLViser launched successfully!")
        print("   🎯 You should see a Rocket League-style window open")
        print("   🖱️  You can move it around your desktop")
        print("   ⌨️  Press ESC in the window to close it")
        
        # Keep the process alive
        while True:
            time.sleep(1)
            
    except Exception as e:
        print(f"❌ Failed to launch RLViser: {e}")
        print("   🔧 Trying alternative method...")
        
        # Alternative: try to launch with different settings
        try:
            # Set some basic settings
            rlviser_py.set_boost_pad_locations([])
            rlviser_py.launch()
            print("✅ RLViser launched with alternative method!")
        except Exception as e2:
            print(f"❌ Alternative method also failed: {e2}")
            print("   💡 RLViser may need to be built from source")
            return False
    
    return True

if __name__ == "__main__":
    print("🚀 RLViser Launcher")
    print("=" * 50)
    launch_rlviser()

