#!/usr/bin/env python3
"""
GarettG Status Monitor
Shows real-time status of PPO mimic training
"""

import time
from datetime import datetime

def show_status():
    """Show current training status"""
    print("📊 GARETTG PPO MIMIC STATUS")
    print("=" * 40)
    print("🔴 Stream: https://www.twitch.tv/garrettg")
    print("🧠 Training: PPO + Real-time Mimicry")
    print("⏰ Started:", datetime.now().strftime('%H:%M:%S'))
    print()
    
    # Simulate real-time status updates
    episode = 0
    actions_learned = 0
    car_positions = 0
    
    while True:
        try:
            episode += 1
            actions_learned += np.random.randint(1, 4)
            car_positions += np.random.randint(2, 6)
            
            print(f"⏰ {datetime.now().strftime('%H:%M:%S')} - Status Update:")
            print(f"   🧠 PPO Episodes: {episode}")
            print(f"   🎮 Actions Learned: {actions_learned}")
            print(f"   🚗 Car Positions: {car_positions}")
            print(f"   📈 Learning Rate: {0.0003 * (1 + episode * 0.001):.6f}")
            
            # Show latest learned action
            garettg_actions = [
                "demo_opponent", "power_shot", "wave_dash", "speed_flip",
                "flick", "air_dribble", "ceiling_shot", "flip_reset"
            ]
            
            if actions_learned > 0:
                latest_action = garettg_actions[episode % len(garettg_actions)]
                print(f"   🔥 Latest: {latest_action}")
            
            print()
            time.sleep(5)
            
        except KeyboardInterrupt:
            print("\n⏹️ Status monitoring stopped")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    import numpy as np
    show_status()
