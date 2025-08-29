#!/usr/bin/env python3
"""
SSL Training Launcher
Launches the full real data training system for SSL achievement
Runs for 24 hours to reach SSL by tomorrow
"""

import subprocess
import time
import threading
import os
import sys
from datetime import datetime, timedelta

class SSLTrainingLauncher:
    """Launcher for SSL training system"""
    
    def __init__(self):
        self.processes = []
        self.start_time = time.time()
        self.target_time = 24 * 3600  # 24 hours
        
        print("🏆 SSL TRAINING LAUNCHER")
        print("=" * 60)
        print("🎯 Target: SSL by tomorrow (24 hours)")
        print("🚀 Launching full training system...")
    
    def launch_training_system(self):
        """Launch the complete SSL training system"""
        print("\n🚀 LAUNCHING SSL TRAINING SYSTEM")
        print("=" * 60)
        
        try:
            # Launch main real data trainer
            print("1. 🎮 Starting Real Data Multi-Mode Trainer...")
            trainer_process = subprocess.Popen([
                sys.executable, 'real_data_multi_trainer.py'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.processes.append(('Real Data Trainer', trainer_process))
            
            time.sleep(5)  # Wait for trainer to initialize
            
            # Launch SSL progress monitor
            print("2. 📊 Starting SSL Progress Monitor...")
            monitor_process = subprocess.Popen([
                sys.executable, 'ssl_progress_monitor.py'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.processes.append(('SSL Monitor', monitor_process))
            
            time.sleep(2)
            
            # Launch demo trainer for additional learning
            print("3. 🎯 Starting Demo Trainer for extra learning...")
            demo_process = subprocess.Popen([
                sys.executable, 'demo_real_data_trainer.py'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.processes.append(('Demo Trainer', demo_process))
            
            print("\n✅ ALL SSL TRAINING SYSTEMS LAUNCHED!")
            print("🎯 Training for SSL achievement...")
            print("📊 Monitoring progress...")
            print("⏰ Target: SSL by tomorrow")
            
            # Start monitoring
            self.monitor_system()
            
        except Exception as e:
            print(f"❌ Error launching training system: {e}")
            self.cleanup()
    
    def monitor_system(self):
        """Monitor the training system"""
        print("\n📊 MONITORING SSL TRAINING SYSTEM")
        print("=" * 60)
        
        while True:
            try:
                # Check if 24 hours is complete
                elapsed = time.time() - self.start_time
                remaining = self.target_time - elapsed
                
                if remaining <= 0:
                    print("\n🏆 24 HOURS COMPLETE!")
                    print("🎯 SSL training session finished!")
                    self.generate_final_ssl_report()
                    break
                
                # Show countdown
                hours = int(remaining // 3600)
                minutes = int((remaining % 3600) // 60)
                seconds = int(remaining % 60)
                
                print(f"\r⏰ SSL Training Time Remaining: {hours:02d}:{minutes:02d}:{seconds:02d} | "
                      f"Processes: {len(self.processes)}", 
                      end="", flush=True)
                
                # Check process health
                self.check_process_health()
                
                time.sleep(10)  # Check every 10 seconds
                
            except KeyboardInterrupt:
                print("\n⏹️ SSL training interrupted by user")
                break
            except Exception as e:
                print(f"\n❌ Monitoring error: {e}")
                time.sleep(10)
        
        self.cleanup()
    
    def check_process_health(self):
        """Check if all processes are still running"""
        try:
            for name, process in self.processes:
                if process.poll() is not None:
                    print(f"\n⚠️ {name} stopped unexpectedly")
                    # Restart the process
                    self.restart_process(name)
        except Exception as e:
            print(f"\n❌ Process health check error: {e}")
    
    def restart_process(self, process_name):
        """Restart a stopped process"""
        try:
            print(f"🔄 Restarting {process_name}...")
            
            if process_name == 'Real Data Trainer':
                new_process = subprocess.Popen([
                    sys.executable, 'real_data_multi_trainer.py'
                ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            elif process_name == 'SSL Monitor':
                new_process = subprocess.Popen([
                    sys.executable, 'ssl_progress_monitor.py'
                ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            elif process_name == 'Demo Trainer':
                new_process = subprocess.Popen([
                    sys.executable, 'demo_real_data_trainer.py'
                ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Update the process in the list
            for i, (name, process) in enumerate(self.processes):
                if name == process_name:
                    self.processes[i] = (name, new_process)
                    break
            
            print(f"✅ {process_name} restarted successfully")
            
        except Exception as e:
            print(f"❌ Error restarting {process_name}: {e}")
    
    def generate_final_ssl_report(self):
        """Generate final SSL achievement report"""
        print("\n\n🏆 FINAL SSL TRAINING REPORT")
        print("=" * 80)
        
        total_time = time.time() - self.start_time
        hours = total_time / 3600
        
        print(f"⏰ Total Training Time: {hours:.2f} hours")
        print(f"🎯 Target: SSL by tomorrow")
        print(f"📊 Processes Run: {len(self.processes)}")
        
        # Check final training data
        try:
            import glob
            import pickle
            
            files = glob.glob('real_data_training_*.pkl')
            if files:
                latest_file = max(files, key=lambda x: x.split('_')[-1].split('.')[0])
                
                with open(latest_file, 'rb') as f:
                    data = pickle.load(f)
                
                print(f"\n📊 FINAL TRAINING RESULTS:")
                print("-" * 40)
                print(f"🎮 Total Actions Learned: {data.get('total_actions', 0)}")
                print(f"📡 Real Data Points: {data.get('real_data_count', 0)}")
                print(f"🧠 Total Episodes: {data.get('total_episodes', 0)}")
                print(f"❌ Total Errors: {data.get('error_count', 0)}")
                
                # Check SSL readiness
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
                    print("🚀 Ready to dominate ranked matches!")
                else:
                    print(f"\n⚠️ SSL not yet achieved")
                    print("📈 Continue training for SSL readiness")
            
        except Exception as e:
            print(f"❌ Error generating final report: {e}")
        
        print("=" * 80)
    
    def cleanup(self):
        """Clean up all processes"""
        print("\n🧹 Cleaning up SSL training system...")
        
        for name, process in self.processes:
            try:
                process.terminate()
                process.wait(timeout=5)
                print(f"✅ {name} stopped")
            except:
                try:
                    process.kill()
                    print(f"🔨 {name} force stopped")
                except:
                    print(f"❌ Could not stop {name}")
        
        print("🧹 SSL training system cleanup complete")

def main():
    """Main function"""
    print("🏆 SSL TRAINING LAUNCHER")
    print("=" * 60)
    print("🎯 Target: SSL by tomorrow")
    print("🚀 Launching complete training system...")
    
    launcher = SSLTrainingLauncher()
    
    try:
        launcher.launch_training_system()
        
    except KeyboardInterrupt:
        print("\n⏹️ SSL training interrupted by user")
        launcher.cleanup()
    except Exception as e:
        print(f"\n❌ Critical Error: {e}")
        launcher.cleanup()

if __name__ == "__main__":
    main()
