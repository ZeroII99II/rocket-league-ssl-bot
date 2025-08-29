#!/usr/bin/env python3
"""
Launch Opti UDP Training System
Starts both the UDP visualizer and the JSTN training system
"""

import subprocess
import time
import sys
import os
from pathlib import Path

def main():
    """Launch the complete Opti UDP training system"""
    print("🚀 Launching Opti UDP Training System...")
    print("   🤖 JSTN Bot Training with UDP Visualizer")
    print("   📡 Real-time 3D visualization via UDP packets")
    print("   🎮 Multi-panel view with bot thoughts and actions")
    print()
    
    # Check if required files exist
    required_files = [
        "opti_udp_visualizer.py",
        "udp_packet_sender.py", 
        "jstn_multi_mode_trainer.py"
    ]
    
    for file in required_files:
        if not Path(file).exists():
            print(f"❌ Required file not found: {file}")
            return
    
    print("✅ All required files found!")
    print()
    
    try:
        # Start the UDP visualizer first
        print("🎮 Starting UDP Visualizer...")
        visualizer_process = subprocess.Popen([
            sys.executable, "opti_udp_visualizer.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Give the visualizer time to start
        print("   ⏳ Waiting for visualizer to initialize...")
        time.sleep(3)
        
        # Check if visualizer is still running
        if visualizer_process.poll() is not None:
            print("❌ UDP Visualizer failed to start!")
            stdout, stderr = visualizer_process.communicate()
            print(f"Error: {stderr.decode()}")
            return
        
        print("✅ UDP Visualizer started successfully!")
        print("   📺 You should see a 3D game window open on your desktop!")
        print("   🎯 The window shows real-time bot training with multiple panels!")
        print()
        
        # Start the training system
        print("🤖 Starting JSTN Multi-Mode Training...")
        training_process = subprocess.Popen([
            sys.executable, "jstn_multi_mode_trainer.py"
        ])
        
        print("✅ Training system started!")
        print()
        print("🎮 System Status:")
        print("   📡 UDP Visualizer: Running")
        print("   🤖 JSTN Training: Running")
        print("   📊 Multi-mode training: 1s, 2s, 3s rotation")
        print("   🧠 Real-time bot thoughts and actions displayed")
        print()
        print("🎯 Controls:")
        print("   ESC - Toggle visualizer menu")
        print("   1-8 - Focus on different cars")
        print("   9 - Director camera")
        print("   0 - Free camera")
        print("   WASD - Move camera")
        print("   Space/Ctrl - Up/Down")
        print("   P - Pause/Play")
        print("   +/- - Speed up/down")
        print("   R - Reset ball to goal")
        print()
        print("⚠️  Press Ctrl+C to stop both systems")
        
        # Wait for processes
        try:
            training_process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Stopping systems...")
            training_process.terminate()
            visualizer_process.terminate()
            
            # Wait for processes to terminate
            training_process.wait()
            visualizer_process.wait()
            
            print("✅ Systems stopped successfully!")
    
    except Exception as e:
        print(f"❌ Error launching system: {e}")
        
        # Clean up processes
        try:
            if 'visualizer_process' in locals():
                visualizer_process.terminate()
            if 'training_process' in locals():
                training_process.terminate()
        except:
            pass

if __name__ == "__main__":
    main()

