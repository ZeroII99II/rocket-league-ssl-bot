#!/usr/bin/env python3
"""
Complete SSL Training Monitor
Closes everything, restarts cleanly, and monitors for 1 hour
Tracks errors, progress, and provides detailed reports
"""

import subprocess
import time
import threading
import os
import sys
import signal
import psutil
from datetime import datetime, timedelta
import json
import pickle

class CompleteSSLMonitor:
    """Complete monitoring system for SSL training"""
    
    def __init__(self):
        self.processes = {}
        self.start_time = time.time()
        self.monitor_duration = 3600  # 1 hour
        self.error_log = []
        self.progress_log = []
        self.report_interval = 300  # 5 minutes
        self.last_report_time = time.time()
        
        print("🏆 COMPLETE SSL TRAINING MONITOR")
        print("=" * 80)
        print("🎯 Target: SSL by tomorrow")
        print("⏰ Monitor Duration: 1 hour")
        print("🔍 Error Detection: Enabled")
        print("📊 Progress Tracking: Enabled")
        print("🚀 Starting complete system...")
    
    def kill_all_python_processes(self):
        """Kill all Python processes to ensure clean start"""
        print("\n🧹 CLEANING UP ALL PROCESSES")
        print("=" * 50)
        
        try:
            # Kill all Python processes
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    if proc.info['name'] and 'python' in proc.info['name'].lower():
                        if proc.info['cmdline'] and any('real_data' in str(cmd) or 'ssl' in str(cmd) or 'monitor' in str(cmd) for cmd in proc.info['cmdline']):
                            print(f"🔨 Killing process: {proc.info['pid']} - {proc.info['name']}")
                            proc.kill()
                            proc.wait(timeout=5)
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired):
                    pass
            
            time.sleep(3)  # Wait for cleanup
            print("✅ All processes cleaned up")
            
        except Exception as e:
            print(f"⚠️ Cleanup warning: {e}")
    
    def launch_training_system(self):
        """Launch the complete training system"""
        print("\n🚀 LAUNCHING COMPLETE TRAINING SYSTEM")
        print("=" * 60)
        
        try:
            # Launch main real data trainer
            print("1. 🎮 Starting Real Data Multi-Mode Trainer...")
            trainer_process = subprocess.Popen([
                sys.executable, 'real_data_multi_trainer.py'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            self.processes['trainer'] = {
                'process': trainer_process,
                'name': 'Real Data Trainer',
                'start_time': time.time(),
                'errors': 0,
                'restarts': 0
            }
            
            time.sleep(5)  # Wait for initialization
            
            # Launch SSL progress monitor
            print("2. 📊 Starting SSL Progress Monitor...")
            monitor_process = subprocess.Popen([
                sys.executable, 'ssl_progress_monitor.py'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            self.processes['monitor'] = {
                'process': monitor_process,
                'name': 'SSL Monitor',
                'start_time': time.time(),
                'errors': 0,
                'restarts': 0
            }
            
            time.sleep(3)
            
            # Launch demo trainer for additional learning
            print("3. 🎯 Starting Demo Trainer...")
            demo_process = subprocess.Popen([
                sys.executable, 'demo_real_data_trainer.py'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            self.processes['demo'] = {
                'process': demo_process,
                'name': 'Demo Trainer',
                'start_time': time.time(),
                'errors': 0,
                'restarts': 0
            }
            
            print("\n✅ ALL SYSTEMS LAUNCHED SUCCESSFULLY!")
            print("🎯 Training for SSL achievement...")
            print("📊 Monitoring progress and errors...")
            print("⏰ 1-hour monitoring session started")
            
        except Exception as e:
            self.log_error(f"Failed to launch training system: {e}")
            print(f"❌ Error launching system: {e}")
    
    def monitor_system(self):
        """Monitor the complete system for 1 hour"""
        print("\n📊 MONITORING COMPLETE SSL TRAINING SYSTEM")
        print("=" * 80)
        
        while True:
            try:
                # Check if 1 hour is complete
                elapsed = time.time() - self.start_time
                remaining = self.monitor_duration - elapsed
                
                if remaining <= 0:
                    print("\n🏆 1 HOUR MONITORING COMPLETE!")
                    self.generate_final_report()
                    break
                
                # Show countdown and status
                hours = int(remaining // 3600)
                minutes = int((remaining % 3600) // 60)
                seconds = int(remaining % 60)
                
                active_processes = sum(1 for p in self.processes.values() if p['process'].poll() is None)
                total_errors = sum(p['errors'] for p in self.processes.values())
                
                print(f"\r⏰ Time Remaining: {hours:02d}:{minutes:02d}:{seconds:02d} | "
                      f"Active: {active_processes}/{len(self.processes)} | "
                      f"Errors: {total_errors} | "
                      f"Reports: {len(self.progress_log)}", 
                      end="", flush=True)
                
                # Check process health
                self.check_process_health()
                
                # Generate periodic reports
                if time.time() - self.last_report_time >= self.report_interval:
                    self.generate_periodic_report()
                    self.last_report_time = time.time()
                
                time.sleep(10)  # Check every 10 seconds
                
            except KeyboardInterrupt:
                print("\n⏹️ Monitoring interrupted by user")
                break
            except Exception as e:
                self.log_error(f"Monitoring error: {e}")
                time.sleep(10)
        
        self.cleanup()
    
    def check_process_health(self):
        """Check health of all processes"""
        for name, proc_info in self.processes.items():
            process = proc_info['process']
            
            if process.poll() is not None:
                # Process has stopped
                proc_info['errors'] += 1
                self.log_error(f"{proc_info['name']} stopped unexpectedly")
                
                # Try to restart
                self.restart_process(name)
    
    def restart_process(self, process_name):
        """Restart a stopped process"""
        try:
            proc_info = self.processes[process_name]
            proc_info['restarts'] += 1
            
            print(f"\n🔄 Restarting {proc_info['name']} (attempt #{proc_info['restarts']})...")
            
            if process_name == 'trainer':
                new_process = subprocess.Popen([
                    sys.executable, 'real_data_multi_trainer.py'
                ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            elif process_name == 'monitor':
                new_process = subprocess.Popen([
                    sys.executable, 'ssl_progress_monitor.py'
                ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            elif process_name == 'demo':
                new_process = subprocess.Popen([
                    sys.executable, 'demo_real_data_trainer.py'
                ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            proc_info['process'] = new_process
            proc_info['start_time'] = time.time()
            
            print(f"✅ {proc_info['name']} restarted successfully")
            
        except Exception as e:
            self.log_error(f"Failed to restart {process_name}: {e}")
    
    def log_error(self, error_message):
        """Log an error with timestamp"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        error_entry = {
            'timestamp': timestamp,
            'error': error_message,
            'elapsed_time': time.time() - self.start_time
        }
        self.error_log.append(error_entry)
        print(f"\n❌ [{timestamp}] {error_message}")
    
    def generate_periodic_report(self):
        """Generate a periodic progress report"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        elapsed_hours = (time.time() - self.start_time) / 3600
        
        # Get training data if available
        training_data = self.get_latest_training_data()
        
        report = {
            'timestamp': timestamp,
            'elapsed_hours': elapsed_hours,
            'active_processes': sum(1 for p in self.processes.values() if p['process'].poll() is None),
            'total_errors': sum(p['errors'] for p in self.processes.values()),
            'total_restarts': sum(p['restarts'] for p in self.processes.values()),
            'training_data': training_data
        }
        
        self.progress_log.append(report)
        
        print(f"\n\n📊 PERIODIC REPORT - {timestamp}")
        print("=" * 60)
        print(f"⏰ Elapsed Time: {elapsed_hours:.2f} hours")
        print(f"🎮 Active Processes: {report['active_processes']}/{len(self.processes)}")
        print(f"❌ Total Errors: {report['total_errors']}")
        print(f"🔄 Total Restarts: {report['total_restarts']}")
        
        if training_data:
            print(f"📡 Real Data Points: {training_data.get('real_data_count', 0)}")
            print(f"🎯 Total Actions: {training_data.get('total_actions', 0)}")
            print(f"🧠 Episodes: {training_data.get('total_episodes', 0)}")
        
        # Show recent errors
        recent_errors = [e for e in self.error_log if time.time() - e['elapsed_time'] < 300]  # Last 5 minutes
        if recent_errors:
            print(f"\n⚠️ Recent Errors ({len(recent_errors)}):")
            for error in recent_errors[-3:]:  # Show last 3 errors
                print(f"   [{error['timestamp']}] {error['error']}")
        
        print("=" * 60)
    
    def get_latest_training_data(self):
        """Get the latest training data"""
        try:
            import glob
            files = glob.glob('real_data_training_*.pkl')
            if files:
                latest_file = max(files, key=os.path.getctime)
                with open(latest_file, 'rb') as f:
                    return pickle.load(f)
        except Exception:
            pass
        return None
    
    def generate_final_report(self):
        """Generate final comprehensive report"""
        print("\n\n🏆 FINAL 1-HOUR MONITORING REPORT")
        print("=" * 80)
        
        total_time = time.time() - self.start_time
        hours = total_time / 3600
        
        print(f"⏰ Total Monitoring Time: {hours:.2f} hours")
        print(f"🎯 Target: SSL by tomorrow")
        print(f"📊 Total Reports Generated: {len(self.progress_log)}")
        print(f"❌ Total Errors Logged: {len(self.error_log)}")
        
        # Process summary
        print(f"\n🎮 PROCESS SUMMARY:")
        print("-" * 40)
        for name, proc_info in self.processes.items():
            uptime = time.time() - proc_info['start_time']
            status = "✅ RUNNING" if proc_info['process'].poll() is None else "❌ STOPPED"
            print(f"   {proc_info['name']}: {status}")
            print(f"      Uptime: {uptime/3600:.2f}h")
            print(f"      Errors: {proc_info['errors']}")
            print(f"      Restarts: {proc_info['restarts']}")
        
        # Error analysis
        if self.error_log:
            print(f"\n❌ ERROR ANALYSIS:")
            print("-" * 30)
            error_types = {}
            for error in self.error_log:
                error_type = error['error'].split(':')[0] if ':' in error['error'] else 'Unknown'
                error_types[error_type] = error_types.get(error_type, 0) + 1
            
            for error_type, count in sorted(error_types.items(), key=lambda x: x[1], reverse=True):
                print(f"   {error_type}: {count} occurrences")
        
        # Training progress
        final_data = self.get_latest_training_data()
        if final_data:
            print(f"\n📊 FINAL TRAINING PROGRESS:")
            print("-" * 40)
            print(f"🎮 Total Actions: {final_data.get('total_actions', 0)}")
            print(f"📡 Real Data Points: {final_data.get('real_data_count', 0)}")
            print(f"🧠 Total Episodes: {final_data.get('total_episodes', 0)}")
            print(f"❌ Training Errors: {final_data.get('error_count', 0)}")
            
            # SSL readiness check
            mode_performance = final_data.get('mode_performance', {})
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
        
        # Recommendations
        print(f"\n💡 RECOMMENDATIONS:")
        print("-" * 25)
        if len(self.error_log) > 10:
            print("1. 🔧 High error rate - investigate system stability")
        if sum(p['restarts'] for p in self.processes.values()) > 5:
            print("2. 🔄 Frequent restarts - check process dependencies")
        if final_data and final_data.get('real_data_count', 0) < 100:
            print("3. 📡 Low real data collection - check stream connections")
        print("4. 🚀 Continue training for SSL achievement")
        print("5. 📊 Monitor for 24 hours to reach SSL by tomorrow")
        
        # Save report
        report_data = {
            'monitoring_duration': hours,
            'total_errors': len(self.error_log),
            'total_reports': len(self.progress_log),
            'process_summary': {name: {
                'errors': proc['errors'],
                'restarts': proc['restarts'],
                'uptime': time.time() - proc['start_time']
            } for name, proc in self.processes.items()},
            'error_log': self.error_log,
            'progress_log': self.progress_log,
            'final_training_data': final_data
        }
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = f'complete_ssl_monitor_report_{timestamp}.json'
        
        try:
            with open(report_file, 'w') as f:
                json.dump(report_data, f, indent=2, default=str)
            print(f"\n💾 Complete report saved to: {report_file}")
        except Exception as e:
            print(f"\n⚠️ Could not save report: {e}")
        
        print("=" * 80)
    
    def cleanup(self):
        """Clean up all processes"""
        print("\n🧹 CLEANING UP COMPLETE SYSTEM")
        print("=" * 50)
        
        for name, proc_info in self.processes.items():
            try:
                process = proc_info['process']
                if process.poll() is None:
                    process.terminate()
                    process.wait(timeout=5)
                    print(f"✅ {proc_info['name']} stopped")
            except:
                try:
                    process.kill()
                    print(f"🔨 {proc_info['name']} force stopped")
                except:
                    print(f"❌ Could not stop {proc_info['name']}")
        
        print("🧹 Complete system cleanup finished")

def main():
    """Main function"""
    print("🏆 COMPLETE SSL TRAINING MONITOR")
    print("=" * 80)
    print("🎯 Target: SSL by tomorrow")
    print("⏰ Duration: 1 hour monitoring")
    print("🔍 Error Detection: Enabled")
    print("📊 Progress Tracking: Enabled")
    print("🚀 Starting complete system...")
    
    monitor = CompleteSSLMonitor()
    
    try:
        # Clean up first
        monitor.kill_all_python_processes()
        
        # Launch system
        monitor.launch_training_system()
        
        # Monitor for 1 hour
        monitor.monitor_system()
        
    except KeyboardInterrupt:
        print("\n⏹️ Monitoring interrupted by user")
        monitor.cleanup()
    except Exception as e:
        print(f"\n❌ Critical Error: {e}")
        monitor.cleanup()

if __name__ == "__main__":
    main()
