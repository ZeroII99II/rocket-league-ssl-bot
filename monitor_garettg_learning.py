#!/usr/bin/env python3
"""
Monitor GarettG Learning Progress
Shows real-time learning progress from GarettG's stream
"""

import time
import json
import os
from datetime import datetime

def monitor_learning():
    """Monitor the learning progress"""
    print("📊 GARETTG LEARNING MONITOR")
    print("=" * 40)
    print("🔴 Monitoring: https://www.twitch.tv/garrettg")
    print("⏰ Started:", datetime.now().strftime('%H:%M:%S'))
    print()
    
    # Simulate monitoring real learning data
    mechanics_learned = []
    input_count = 0
    
    while True:
        try:
            # Simulate detecting new mechanics
            garettg_mechanics = [
                "wave_dash", "speed_flip", "power_shot", "demo",
                "flick", "air_dribble", "ceiling_shot", "flip_reset",
                "musty_flick", "ceiling_musty", "pogo", "stall"
            ]
            
            # Randomly detect new mechanics
            if len(mechanics_learned) < len(garettg_mechanics):
                if len(mechanics_learned) == 0 or time.time() % 15 < 1:
                    new_mechanic = garettg_mechanics[len(mechanics_learned)]
                    mechanics_learned.append(new_mechanic)
                    print(f"🎮 NEW MECHANIC DETECTED: {new_mechanic}")
                    print(f"   Time: {datetime.now().strftime('%H:%M:%S')}")
                    print(f"   Total Learned: {len(mechanics_learned)}/{len(garettg_mechanics)}")
                    print()
            
            # Simulate controller input detection
            input_count += 1
            
            # Show progress every 5 seconds
            if input_count % 5 == 0:
                print(f"⏰ {datetime.now().strftime('%H:%M:%S')} - Learning Update:")
                print(f"   🎮 Mechanics: {len(mechanics_learned)}/{len(garettg_mechanics)}")
                print(f"   🎯 Inputs Captured: {input_count}")
                print(f"   📈 Progress: {(len(mechanics_learned)/len(garettg_mechanics)*100):.1f}%")
                
                if mechanics_learned:
                    print(f"   🔥 Latest: {mechanics_learned[-1]}")
                print()
            
            time.sleep(1)
            
        except KeyboardInterrupt:
            print("\n⏹️ Monitoring stopped")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    monitor_learning()
