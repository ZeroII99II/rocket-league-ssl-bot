#!/usr/bin/env python3
"""
Bronze to SSL Launcher
Combines GarettG learning with PPO controller emulator for fast ranking
"""

import time
import threading
from datetime import datetime

def main():
    """Main launcher function"""
    print("🎮 BRONZE → SSL FAST TRACK LAUNCHER")
    print("=" * 50)
    print("🔴 Step 1: Learn from GarettG's stream")
    print("🧠 Step 2: Train with PPO mimicry")
    print("🎯 Step 3: Rank up from Bronze to SSL")
    print("🚀 Starting complete training pipeline...")
    
    try:
        # Step 1: Start GarettG learning
        print("\n📺 STEP 1: LEARNING FROM GARETTG")
        print("=" * 40)
        
        from garettg_ppo_mimic import GarettGPPOMimic
        garettg_trainer = GarettGPPOMimic()
        
        # Start learning in background
        learning_thread = threading.Thread(target=garettg_trainer.start_ppo_mimic_training)
        learning_thread.daemon = True
        learning_thread.start()
        
        # Wait for some learning to happen
        print("⏳ Learning from GarettG for 30 seconds...")
        time.sleep(30)
        
        # Step 2: Start PPO controller emulator
        print("\n🎮 STEP 2: STARTING PPO CONTROLLER EMULATOR")
        print("=" * 40)
        
        from ppo_controller_emulator import PPOControllerEmulator
        ppo_emulator = PPOControllerEmulator()
        
        # Load any existing training data
        ppo_emulator.load_training_data("garettg_complete_training.pkl")
        
        # Step 3: Start rank grinding
        print("\n🏆 STEP 3: STARTING BRONZE → SSL RANK GRINDING")
        print("=" * 40)
        
        # Start rank grinding in background
        ranking_thread = threading.Thread(target=ppo_emulator.start_rank_grinding)
        ranking_thread.daemon = True
        ranking_thread.start()
        
        # Monitor both processes
        monitor_training(garettg_trainer, ppo_emulator)
        
    except KeyboardInterrupt:
        print("\n⏹️ Training interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")

def monitor_training(garettg_trainer, ppo_emulator):
    """Monitor both training processes"""
    print("\n📊 TRAINING MONITOR")
    print("=" * 30)
    
    start_time = time.time()
    
    while True:
        try:
            elapsed = time.time() - start_time
            
            print(f"\n⏰ {datetime.now().strftime('%H:%M:%S')} - Training Status:")
            
            # GarettG learning status
            if garettg_trainer:
                print(f"   📺 GarettG Actions: {len(garettg_trainer.garettg_actions)}")
                print(f"   🧠 PPO Episodes: {garettg_trainer.ppo_episodes}")
                print(f"   📈 Learning Rate: {garettg_trainer.learning_rate:.6f}")
            
            # PPO emulator status
            if ppo_emulator:
                status = ppo_emulator.get_current_status()
                print(f"   🏆 Current Rank: {status['current_rank'].upper()}")
                print(f"   🎮 Episodes: {status['episode_count']}")
                print(f"   🔥 Win Streak: {status['win_streak']}")
                print(f"   🎯 Actions Learned: {status['total_actions_learned']}")
            
            print(f"   ⏱️  Total Time: {elapsed:.1f}s")
            
            time.sleep(10)  # Update every 10 seconds
            
        except KeyboardInterrupt:
            print("\n⏹️ Monitoring stopped")
            break
        except Exception as e:
            print(f"❌ Monitor error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
