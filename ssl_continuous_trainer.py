#!/usr/bin/env python3
"""
SSL Continuous Trainer
Trains continuously until SSL is achieved
Runs 24/7 until all modes reach SSL level
"""

import subprocess
import time
import os
import sys
import pickle
import glob
from datetime import datetime
import json

class SSLContinuousTrainer:
    """Continuous trainer that runs until SSL is achieved"""
    
    def __init__(self):
        self.start_time = time.time()
        self.error_count = 0
        self.report_count = 0
        self.session_count = 0
        self.ssl_achieved = False
        
        # SSL Requirements
        self.ssl_requirements = {
            '1s': {'min_actions': 500, 'min_accuracy': 0.95, 'min_skills': 15},
            '2s': {'min_actions': 600, 'min_accuracy': 0.93, 'min_skills': 18},
            '3s': {'min_actions': 700, 'min_accuracy': 0.90, 'min_skills': 20}
        }
        
        print("🏆 SSL CONTINUOUS TRAINER")
        print("=" * 60)
        print("🎯 Target: SSL in ALL modes")
        print("⏰ Duration: Until SSL achieved")
        print("🔄 Continuous training: 24/7")
        print("🚀 Starting continuous SSL training...")
    
    def check_ssl_status(self):
        """Check if SSL has been achieved in all modes"""
        try:
            # Find latest training file
            files = glob.glob('real_data_training_*.pkl')
            if not files:
                return False, {}
            
            # Get the most recent file
            latest_file = max(files, key=os.path.getctime)
            
            # Fix file reading with proper error handling
            try:
                with open(latest_file, 'rb') as f:
                    data = pickle.load(f)
            except (pickle.UnpicklingError, EOFError, FileNotFoundError) as e:
                print(f"⚠️ Error reading {latest_file}: {e}")
                # Try to find an older file
                files = sorted(files, key=os.path.getctime, reverse=True)
                for file in files[1:]:  # Skip the corrupted one
                    try:
                        with open(file, 'rb') as f:
                            data = pickle.load(f)
                        print(f"✅ Using backup file: {file}")
                        break
                    except:
                        continue
                else:
                    return False, {}
            
            mode_performance = data.get('mode_performance', {})
            ssl_ready = True
            
            for mode, requirements in self.ssl_requirements.items():
                perf = mode_performance.get(mode, {})
                actions = perf.get('actions', 0)
                accuracy = perf.get('accuracy', 0.0)
                skills = len(perf.get('skills_learned', []))
                
                action_ready = actions >= requirements['min_actions']
                accuracy_ready = accuracy >= requirements['min_accuracy']
                skill_ready = skills >= requirements['min_skills']
                
                mode_ready = action_ready and accuracy_ready and skill_ready
                ssl_ready = ssl_ready and mode_ready
            
            return ssl_ready, data
            
        except Exception as e:
            print(f"❌ Error checking SSL status: {e}")
            return False, {}
    
    def launch_training_session(self):
        """Launch a new training session"""
        try:
            print(f"\n🚀 LAUNCHING TRAINING SESSION #{self.session_count + 1}")
            print("=" * 50)
            
            # Launch the real data trainer
            trainer_process = subprocess.Popen([
                sys.executable, 'real_data_multi_trainer.py'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            self.session_count += 1
            print(f"✅ Training session #{self.session_count} launched!")
            print("🎯 Training for SSL achievement...")
            
            return trainer_process
            
        except Exception as e:
            print(f"❌ Error launching training session: {e}")
            self.error_count += 1
            return None
    
    def monitor_training_session(self, trainer_process):
        """Monitor a training session"""
        session_start = time.time()
        last_report = time.time()
        report_interval = 300  # 5 minutes
        
        while True:
            try:
                # Check if trainer is still running
                is_running = trainer_process.poll() is None
                
                if not is_running:
                    print(f"\n⚠️ Training session #{self.session_count} stopped!")
                    self.error_count += 1
                    return False
                
                # Check SSL status
                ssl_achieved, data = self.check_ssl_status()
                
                if ssl_achieved:
                    print(f"\n🏆 SSL ACHIEVED IN ALL MODES!")
                    self.ssl_achieved = True
                    return True
                
                # Generate periodic reports
                if time.time() - last_report >= report_interval:
                    self.generate_ssl_report(data)
                    last_report = time.time()
                    self.report_count += 1
                
                # Show status
                elapsed = time.time() - session_start
                hours = int(elapsed // 3600)
                minutes = int((elapsed % 3600) // 60)
                
                print(f"\r⏰ Session #{self.session_count}: {hours:02d}:{minutes:02d} | "
                      f"SSL: {'✅' if ssl_achieved else '❌'} | "
                      f"Errors: {self.error_count} | "
                      f"Reports: {self.report_count}", 
                      end="", flush=True)
                
                time.sleep(30)  # Check every 30 seconds
                
            except KeyboardInterrupt:
                print("\n⏹️ Training interrupted by user")
                return False
            except Exception as e:
                print(f"\n❌ Monitoring error: {e}")
                self.error_count += 1
                time.sleep(30)
    
    def generate_ssl_report(self, data):
        """Generate SSL progress report"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        total_time = time.time() - self.start_time
        hours = total_time / 3600
        
        print(f"\n\n📊 SSL PROGRESS REPORT - {timestamp}")
        print("=" * 60)
        print(f"⏰ Total Training Time: {hours:.2f} hours")
        print(f"🔄 Training Sessions: {self.session_count}")
        print(f"❌ Total Errors: {self.error_count}")
        print(f"📊 Reports Generated: {self.report_count}")
        
        if data:
            print(f"\n📊 CURRENT TRAINING STATUS:")
            print("-" * 40)
            print(f"🎮 Total Actions: {data.get('total_actions', 0)}")
            print(f"📡 Real Data Points: {data.get('real_data_count', 0)}")
            print(f"🧠 Total Episodes: {data.get('total_episodes', 0)}")
            print(f"❌ Training Errors: {data.get('error_count', 0)}")
            
            # SSL readiness check
            mode_performance = data.get('mode_performance', {})
            
            print(f"\n🏆 SSL READINESS CHECK:")
            print("-" * 30)
            ssl_ready = True
            
            for mode, requirements in self.ssl_requirements.items():
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
                print(f"\n⚠️ SSL not yet achieved - continuing training...")
        
        print("=" * 60)
    
    def run_continuous_training(self):
        """Run continuous training until SSL is achieved"""
        print("\n🚀 STARTING CONTINUOUS SSL TRAINING")
        print("=" * 60)
        print("🎯 Training will continue until SSL is achieved in ALL modes")
        print("⏰ No time limit - runs until completion")
        print("🔄 Automatic session restarts if needed")
        print("📊 Reports every 5 minutes")
        
        while not self.ssl_achieved:
            try:
                # Launch new training session
                trainer_process = self.launch_training_session()
                
                if trainer_process is None:
                    print("❌ Failed to launch training session, retrying in 60 seconds...")
                    time.sleep(60)
                    continue
                
                # Monitor the session
                session_completed = self.monitor_training_session(trainer_process)
                
                if self.ssl_achieved:
                    break
                
                # Clean up the process
                try:
                    if trainer_process.poll() is None:
                        trainer_process.terminate()
                        trainer_process.wait(timeout=10)
                except:
                    pass
                
                # Brief pause before next session
                print(f"\n🔄 Starting new training session in 30 seconds...")
                time.sleep(30)
                
            except KeyboardInterrupt:
                print("\n⏹️ Continuous training interrupted by user")
                break
            except Exception as e:
                print(f"\n❌ Critical error in continuous training: {e}")
                self.error_count += 1
                time.sleep(60)  # Wait before retrying
        
        self.generate_final_ssl_report()
    
    def generate_final_ssl_report(self):
        """Generate final SSL achievement report"""
        print("\n\n🏆 FINAL SSL ACHIEVEMENT REPORT")
        print("=" * 70)
        
        total_time = time.time() - self.start_time
        hours = total_time / 3600
        
        print(f"⏰ Total Training Time: {hours:.2f} hours")
        print(f"🎯 Target: SSL in ALL modes")
        print(f"🔄 Training Sessions: {self.session_count}")
        print(f"📊 Total Reports: {self.report_count}")
        print(f"❌ Total Errors: {self.error_count}")
        
        if self.ssl_achieved:
            print(f"\n🏆 SSL ACHIEVEMENT UNLOCKED!")
            print("🎯 Bot is ready for SSL injection!")
            print("🚀 Ready to dominate ranked matches!")
        else:
            print(f"\n⚠️ Training stopped before SSL achievement")
        
        # Save final report
        report_data = {
            'total_training_time': hours,
            'training_sessions': self.session_count,
            'total_reports': self.report_count,
            'total_errors': self.error_count,
            'ssl_achieved': self.ssl_achieved,
            'timestamp': datetime.now().isoformat()
        }
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = f'ssl_continuous_training_report_{timestamp}.json'
        
        try:
            with open(report_file, 'w') as f:
                json.dump(report_data, f, indent=2)
            print(f"\n💾 Final report saved to: {report_file}")
        except Exception as e:
            print(f"\n⚠️ Could not save final report: {e}")
        
        print("=" * 70)

def main():
    """Main function"""
    print("🏆 SSL CONTINUOUS TRAINER")
    print("=" * 60)
    print("🎯 Target: SSL in ALL modes")
    print("⏰ Duration: Until SSL achieved")
    print("🔄 Continuous training: 24/7")
    print("🚀 Starting continuous SSL training...")
    
    trainer = SSLContinuousTrainer()
    
    try:
        trainer.run_continuous_training()
    except KeyboardInterrupt:
        print("\n⏹️ Continuous training interrupted by user")
    except Exception as e:
        print(f"\n❌ Critical Error: {e}")

if __name__ == "__main__":
    main()
