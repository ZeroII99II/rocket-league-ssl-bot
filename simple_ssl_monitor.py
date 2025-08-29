#!/usr/bin/env python3
"""
Simple SSL Training Monitor
Closes everything, restarts cleanly, and monitors for 1 hour
"""

import subprocess
import time
import os
import sys
from datetime import datetime
import json

class SimpleSSLMonitor:
    """Simple monitoring system for SSL training"""
    
    def __init__(self):
        self.start_time = time.time()
        self.monitor_duration = 3600  # 1 hour
        self.error_count = 0
        self.report_count = 0
        
        print("🏆 SIMPLE SSL TRAINING MONITOR")
        print("=" * 60)
        print("🎯 Target: SSL by tomorrow")
        print("⏰ Monitor Duration: 1 hour")
        print("🔍 Error Detection: Enabled")
        print("🚀 Starting simple system...")
    
    def kill_all_processes(self):
        """Kill all Python processes"""
        print("\n🧹 CLEANING UP ALL PROCESSES")
        print("=" * 40)
        
        try:
            # Use taskkill to stop all Python processes
            result = subprocess.run(['taskkill', '/f', '/im', 'python.exe'], 
                                  capture_output=True, text=True)
            print("✅ All Python processes stopped")
            time.sleep(3)
        except Exception as e:
            print(f"⚠️ Cleanup warning: {e}")
    
    def launch_single_trainer(self):
        """Launch a single reliable trainer"""
        print("\n🚀 LAUNCHING SIMPLE TRAINING SYSTEM")
        print("=" * 50)
        
        try:
            # Launch the real data trainer
            print("🎮 Starting Real Data Multi-Mode Trainer...")
            self.trainer_process = subprocess.Popen([
                sys.executable, 'real_data_multi_trainer.py'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            print("✅ Training system launched!")
            print("🎯 Training for SSL achievement...")
            print("📊 Monitoring for 1 hour...")
            
        except Exception as e:
            print(f"❌ Error launching system: {e}")
            self.error_count += 1
    
    def monitor_for_hour(self):
        """Monitor the system for 1 hour"""
        print("\n📊 MONITORING SSL TRAINING SYSTEM")
        print("=" * 60)
        
        last_report = time.time()
        report_interval = 300  # 5 minutes
        
        while True:
            try:
                # Check if 1 hour is complete
                elapsed = time.time() - self.start_time
                remaining = self.monitor_duration - elapsed
                
                if remaining <= 0:
                    print("\n🏆 1 HOUR MONITORING COMPLETE!")
                    self.generate_final_report()
                    break
                
                # Show countdown
                hours = int(remaining // 3600)
                minutes = int((remaining % 3600) // 60)
                seconds = int(remaining % 60)
                
                # Check if trainer is still running
                is_running = self.trainer_process.poll() is None
                status = "✅ RUNNING" if is_running else "❌ STOPPED"
                
                print(f"\r⏰ Time Remaining: {hours:02d}:{minutes:02d}:{seconds:02d} | "
                      f"Trainer: {status} | Errors: {self.error_count} | Reports: {self.report_count}", 
                      end="", flush=True)
                
                # Check trainer health
                if not is_running:
                    print(f"\n⚠️ Trainer stopped unexpectedly!")
                    self.error_count += 1
                    self.restart_trainer()
                
                # Generate periodic reports
                if time.time() - last_report >= report_interval:
                    self.generate_periodic_report()
                    last_report = time.time()
                    self.report_count += 1
                
                time.sleep(10)  # Check every 10 seconds
                
            except KeyboardInterrupt:
                print("\n⏹️ Monitoring interrupted by user")
                break
            except Exception as e:
                print(f"\n❌ Monitoring error: {e}")
                self.error_count += 1
                time.sleep(10)
        
        self.cleanup()
    
    def restart_trainer(self):
        """Restart the trainer"""
        try:
            print("\n🔄 Restarting trainer...")
            self.trainer_process = subprocess.Popen([
                sys.executable, 'real_data_multi_trainer.py'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print("✅ Trainer restarted!")
        except Exception as e:
            print(f"❌ Failed to restart trainer: {e}")
            self.error_count += 1
    
    def generate_periodic_report(self):
        """Generate a periodic report"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        elapsed_hours = (time.time() - self.start_time) / 3600
        
        print(f"\n\n📊 PERIODIC REPORT - {timestamp}")
        print("=" * 50)
        print(f"⏰ Elapsed Time: {elapsed_hours:.2f} hours")
        print(f"🎮 Trainer Status: {'RUNNING' if self.trainer_process.poll() is None else 'STOPPED'}")
        print(f"❌ Total Errors: {self.error_count}")
        print(f"📊 Reports Generated: {self.report_count}")
        
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
        
        print("=" * 50)
    
    def generate_final_report(self):
        """Generate final comprehensive report"""
        print("\n\n🏆 FINAL 1-HOUR MONITORING REPORT")
        print("=" * 70)
        
        total_time = time.time() - self.start_time
        hours = total_time / 3600
        
        print(f"⏰ Total Monitoring Time: {hours:.2f} hours")
        print(f"🎯 Target: SSL by tomorrow")
        print(f"📊 Total Reports Generated: {self.report_count}")
        print(f"❌ Total Errors Logged: {self.error_count}")
        
        # Final trainer status
        is_running = self.trainer_process.poll() is None
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
        if self.error_count > 5:
            print("1. 🔧 High error rate - investigate system stability")
        if not is_running:
            print("2. 🔄 Trainer stopped - restart training system")
        print("3. 🚀 Continue training for SSL achievement")
        print("4. 📊 Monitor for 24 hours to reach SSL by tomorrow")
        
        # Save report
        report_data = {
            'monitoring_duration': hours,
            'total_errors': self.error_count,
            'total_reports': self.report_count,
            'final_trainer_status': 'running' if is_running else 'stopped',
            'timestamp': datetime.now().isoformat()
        }
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = f'simple_ssl_monitor_report_{timestamp}.json'
        
        try:
            with open(report_file, 'w') as f:
                json.dump(report_data, f, indent=2)
            print(f"\n💾 Report saved to: {report_file}")
        except Exception as e:
            print(f"\n⚠️ Could not save report: {e}")
        
        print("=" * 70)
    
    def cleanup(self):
        """Clean up the trainer process"""
        print("\n🧹 CLEANING UP SYSTEM")
        print("=" * 30)
        
        try:
            if hasattr(self, 'trainer_process'):
                if self.trainer_process.poll() is None:
                    self.trainer_process.terminate()
                    self.trainer_process.wait(timeout=5)
                    print("✅ Trainer stopped")
        except Exception as e:
            print(f"⚠️ Cleanup warning: {e}")
        
        print("🧹 System cleanup complete")

def main():
    """Main function"""
    print("🏆 SIMPLE SSL TRAINING MONITOR")
    print("=" * 60)
    print("🎯 Target: SSL by tomorrow")
    print("⏰ Duration: 1 hour monitoring")
    print("🔍 Error Detection: Enabled")
    print("🚀 Starting simple system...")
    
    monitor = SimpleSSLMonitor()
    
    try:
        # Clean up first
        monitor.kill_all_processes()
        
        # Launch system
        monitor.launch_single_trainer()
        
        # Monitor for 1 hour
        monitor.monitor_for_hour()
        
    except KeyboardInterrupt:
        print("\n⏹️ Monitoring interrupted by user")
        monitor.cleanup()
    except Exception as e:
        print(f"\n❌ Critical Error: {e}")
        monitor.cleanup()

if __name__ == "__main__":
    main()
