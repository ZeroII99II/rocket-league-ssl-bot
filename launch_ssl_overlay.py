#!/usr/bin/env python3
"""
SSL Overlay Launcher
Launches the SSL system with visual overlay on top of Rocket League
"""

import time
import threading
import sys
import os
from ssl_game_overlay import SSLGameOverlay
from working_ssl_controller import WorkingSSLController

class SSLOverlayLauncher:
    """Launcher that combines overlay and controller"""
    
    def __init__(self):
        self.overlay = None
        self.controller = None
        self.is_running = False
        
        print("🏆 SSL OVERLAY LAUNCHER")
        print("=" * 60)
        print("🎮 Visual overlay + Real game control")
        print("📊 See all game objects and XYZ data")
        print("⚡ Real inputs to real game")
        print("🚀 Ready to control your car with overlay!")
    
    def start_system(self):
        """Start the complete SSL system with overlay"""
        try:
            print("🚀 Starting SSL System with Overlay...")
            
            # Create controller
            self.controller = WorkingSSLController()
            
            # Connect to game
            if not self.controller.connect_to_game():
                print("❌ Failed to connect to Rocket League!")
                return False
            
            # Create overlay
            self.overlay = SSLGameOverlay()
            self.overlay.game_window = self.controller.game_window
            self.overlay.game_process = self.controller.game_process
            self.overlay.game_handle = self.controller.game_handle
            
            # Start overlay in separate thread
            overlay_thread = threading.Thread(target=self.overlay.start_overlay, daemon=True)
            overlay_thread.start()
            
            # Wait a moment for overlay to start
            time.sleep(2)
            
            print("✅ SSL System with Overlay started!")
            print("🎮 Overlay is displaying on top of Rocket League!")
            print("📊 You can see all game objects and XYZ data!")
            print("⚡ Bot is ready to control your car!")
            
            # Start practice
            print("\n🚀 Starting 30-minute free play practice with overlay...")
            self.controller.run_real_freeplay_practice(30)
            
            return True
            
        except Exception as e:
            print(f"❌ Error starting SSL system: {e}")
            return False
    
    def stop_system(self):
        """Stop the SSL system"""
        try:
            self.is_running = False
            
            if self.controller:
                self.controller.stop_control()
            
            if self.overlay:
                self.overlay.close_overlay()
            
            print("✅ SSL System stopped")
            
        except Exception as e:
            print(f"❌ Error stopping SSL system: {e}")

def main():
    """Main function"""
    print("🏆 SSL OVERLAY LAUNCHER")
    print("=" * 60)
    print("🎮 Visual overlay + Real game control")
    print("📊 See all game objects and XYZ data")
    print("⚡ Real inputs to real game")
    print("🚀 Ready to control your car with overlay!")
    
    launcher = SSLOverlayLauncher()
    
    try:
        # Start system
        launcher.start_system()
        
    except KeyboardInterrupt:
        print("\n⏹️ System interrupted by user")
        launcher.stop_system()
    except Exception as e:
        print(f"\n❌ Critical Error: {e}")
        launcher.stop_system()

if __name__ == "__main__":
    main()
