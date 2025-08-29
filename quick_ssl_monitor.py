#!/usr/bin/env python3
"""
Quick SSL Training Monitor
Simple monitoring for 1 hour with error tracking
"""

import subprocess
import time
import os
import sys
from datetime import datetime

def main():
    """Main monitoring function"""
    print("🏆 QUICK SSL TRAINING MONITOR")
    print("=" * 50)
    print("🎯 Target: SSL by tomorrow")
    print("⏰ Duration: 1 hour monitoring")
    print("🚀 Starting quick system...")
    
    start_time = time.time()
    monitor_duration = 3600  # 1 hour
    error_count = 0
    report_count = 0
    
    # Launch the trainer
    print("\n🎮 Starting Real Data Multi-Mode Trainer...")
    try:
        trainer_process = subprocess.Popen([
            sys.executable, 'real_data_multi_trainer.py'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print("✅ Trainer launched successfully!")
    except Exception as e:
        print(f"❌ Error launching trainer: {e}")
        return
    
    print("\n📊 MONITORING SSL TRAINING SYSTEM")
    print("=" * 50)
    
    last_report = time.time()
    report_interval = 300  # 5 minutes
    
    try:
        while True:
            # Check if 1 hour is complete
            elapsed = time.time() - start_time
            remaining = monitor_duration - elapsed
            
            if remaining <= 0:
                print("\n🏆 1 HOUR MONITORING COMPLETE!")
                break
            
            # Show countdown
            hours = int(remaining // 3600)
            minutes = int((remaining % 3600) // 60)
            seconds = int(remaining % 60)
            
            # Check if trainer is still running
            is_running = trainer_process.poll() is None
            status = "✅ RUNNING" if is_running else "❌ STOPPED"
            
            print(f"\r⏰ Time Remaining: {hours:02d}:{minutes:02d}:{seconds:02d} | "
                  f"Trainer: {status} | Errors: {error_count} | Reports: {report_count}", 
                  end="", flush=True)
            
            # Check trainer health
            if not is_running:
                print(f"\n⚠️ Trainer stopped unexpectedly!")
                error_count += 1
                try:
                    print("🔄 Restarting trainer...")
                    trainer_process = subprocess.Popen([
                        sys.executable, 'real_data_multi_trainer.py'
                    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    print("✅ Trainer restarted!")
                except Exception as e:
                    print(f"❌ Failed to restart trainer: {e}")
                    error_count += 1
            
            # Generate periodic reports
            if time.time() - last_report >= report_interval:
                timestamp = datetime.now().strftime('%H:%M:%S')
                elapsed_hours = elapsed / 3600
                
                print(f"\n\n📊 PERIODIC REPORT - {timestamp}")
                print("=" * 40)
                print(f"⏰ Elapsed Time: {elapsed_hours:.2f} hours")
                print(f"🎮 Trainer Status: {'RUNNING' if is_running else 'STOPPED'}")
                print(f"❌ Total Errors: {error_count}")
                print(f"📊 Reports Generated: {report_count}")
                
                # Check for training data
                try:
                    import glob
                    import pickle
                    files = glob.glob('real_data_training_*.pkl')
                    if files:
                        latest_file = max(files, key=os.path.getctime)
                        with open(latest_file, 'rb') as f:
                            data = pickle.load(f)
                        
                        print(f"📡 Real Data Points: {data.get('real_data_count', 0)}")
                        print(f"🎯 Total Actions: {data.get('total_actions', 0)}")
                        print(f"🧠 Episodes: {data.get('total_episodes', 0)}")
                        print(f"❌ Training Errors: {data.get('error_count', 0)}")
                except Exception as e:
                    print(f"⚠️ Could not read training data: {e}")
                
                print("=" * 40)
                
                last_report = time.time()
                report_count += 1
            
            time.sleep(10)  # Check every 10 seconds
            
    except KeyboardInterrupt:
        print("\n⏹️ Monitoring interrupted by user")
    
    # Final report
    print("\n\n🏆 FINAL 1-HOUR MONITORING REPORT")
    print("=" * 60)
    
    total_time = time.time() - start_time
    hours = total_time / 3600
    
    print(f"⏰ Total Monitoring Time: {hours:.2f} hours")
    print(f"🎯 Target: SSL by tomorrow")
    print(f"📊 Total Reports Generated: {report_count}")
    print(f"❌ Total Errors Logged: {error_count}")
    
    # Final trainer status
    is_running = trainer_process.poll() is None
    print(f"🎮 Final Trainer Status: {'✅ RUNNING' if is_running else '❌ STOPPED'}")
    
    # Training progress
    try:
        import glob
        import pickle
        files = glob.glob('real_data_training_*.pkl')
        if files:
            latest_file = max(files, key=os.path.getctime)
            with open(latest_file, 'rb') as f:
                data = pickle.load(f)
            
            print(f"\n📊 FINAL TRAINING PROGRESS:")
            print("-" * 40)
            print(f"🎮 Total Actions: {data.get('total_actions', 0)}")
            print(f"📡 Real Data Points: {data.get('real_data_count', 0)}")
            print(f"🧠 Total Episodes: {data.get('total_episodes', 0)}")
            print(f"❌ Training Errors: {data.get('error_count', 0)}")
            
            # SSL readiness check
            mode_performance = data.get('mode_performance', {})
            ssl_requirements = {
                '1s': {'min_actions': 500, 'min_accuracy': 0.95, 'min_skills': 15},
                '2s': {'min_actions': 600, 'min_accuracy': 0.93, 'min_skills': 18},
                '3s': {'min_actions': 700, 'min_accuracy': 0.90, 'min_skills': 20}
            }
            
            print(f"\n🏆 SSL READINESS CHECK:")
            print("-" * 30)
            ssl_ready = True
            for mode, requirements in ssl_requirements.items():
                perf = mode_performance.get(mode, {})
                actions = perf.get('actions', 0)
                accuracy = perf.get('accuracy', 0.0)
                skills = len(perf.get('skills_learned', []))
                
                action_ready = actions >= requirements['min_actions']
                accuracy_ready = accuracy >= requirements['min_accuracy']
                skill_ready = skills >= requirements['min_skills']
                
                mode_ready = action_ready and accuracy_ready and skill_ready
                ssl_ready = ssl_ready and mode_ready
                
                status = "✅ READY" if mode_ready else "❌ NOT READY"
                print(f"   {mode.upper()}: {status}")
                print(f"      Actions: {actions}/{requirements['min_actions']}")
                print(f"      Accuracy: {accuracy:.1%}/{requirements['min_accuracy']:.1%}")
                print(f"      Skills: {skills}/{requirements['min_skills']}")
            
            if ssl_ready:
                print(f"\n🏆 SSL ACHIEVEMENT UNLOCKED!")
                print("🎯 Bot is ready for SSL injection!")
            else:
                print(f"\n⚠️ SSL not yet achieved - continue training")
    except Exception as e:
        print(f"⚠️ Could not read final training data: {e}")
    
    # Recommendations
    print(f"\n💡 RECOMMENDATIONS:")
    print("-" * 25)
    if error_count > 5:
        print("1. 🔧 High error rate - investigate system stability")
    if not is_running:
        print("2. 🔄 Trainer stopped - restart training system")
    print("3. 🚀 Continue training for SSL achievement")
    print("4. 📊 Monitor for 24 hours to reach SSL by tomorrow")
    
    print("=" * 60)
    
    # Cleanup
    print("\n🧹 CLEANING UP SYSTEM")
    print("=" * 30)
    try:
        if trainer_process.poll() is None:
            trainer_process.terminate()
            trainer_process.wait(timeout=5)
            print("✅ Trainer stopped")
    except Exception as e:
        print(f"⚠️ Cleanup warning: {e}")
    
    print("🧹 System cleanup complete")

if __name__ == "__main__":
    main()
