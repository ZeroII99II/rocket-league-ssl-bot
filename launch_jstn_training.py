#!/usr/bin/env python3
"""
JSTN Training Launcher
Launches all workers and learners for JSTN-level training
"""

import os
import sys
import time
import subprocess
import threading
from pathlib import Path
import signal
import psutil

class JSTNTrainingLauncher:
    """Launches and manages all JSTN training processes"""
    
    def __init__(self):
        self.processes = {}
        self.worker_scripts = [
            'worker_selector.py',
            'worker_dtap.py', 
            'worker_flip_reset.py',
            'worker_aerial.py',
            'worker_flick.py',
            'worker_ceil_pinch.py',
            'worker_pinch.py',
            'worker_wall.py',
            'worker_walldash.py',
            'worker_recovery.py',
            'worker_demo.py',
            'worker_gp.py',
            'worker_half_flip.py',
            'worker_lix.py',
            'worker_kickoff.py'
        ]
        
        self.learner_scripts = [
            'learner_selector.py',
            'learner_dtap.py',
            'learner_flip_reset.py', 
            'learner_aerial.py',
            'learner_flick.py',
            'learner_ceil_pinch.py',
            'learner_pinch.py',
            'learner_wall.py',
            'learner_walldash.py',
            'learner_recovery.py',
            'learner_demo.py',
            'learner_gp.py',
            'learner_half_flip.py',
            'learner_lix.py',
            'learner_kickoff.py'
        ]
        
        print("🚀 JSTN Training Launcher initialized")
        print(f"📊 Workers: {len(self.worker_scripts)}")
        print(f"🧠 Learners: {len(self.learner_scripts)}")
    
    def start_workers(self):
        """Start all worker processes"""
        print("🚀 Starting all worker processes...")
        
        for worker_script in self.worker_scripts:
            if os.path.exists(worker_script):
                try:
                    # Start worker process
                    process = subprocess.Popen(
                        [sys.executable, worker_script],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True
                    )
                    
                    self.processes[f"worker_{worker_script}"] = process
                    print(f"✅ Started {worker_script} (PID: {process.pid})")
                    
                    # Small delay between starting workers
                    time.sleep(1)
                    
                except Exception as e:
                    print(f"❌ Failed to start {worker_script}: {e}")
            else:
                print(f"⚠️  Worker script not found: {worker_script}")
    
    def start_learners(self):
        """Start all learner processes"""
        print("🧠 Starting all learner processes...")
        
        for learner_script in self.learner_scripts:
            if os.path.exists(learner_script):
                try:
                    # Start learner process
                    process = subprocess.Popen(
                        [sys.executable, learner_script],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True
                    )
                    
                    self.processes[f"learner_{learner_script}"] = process
                    print(f"✅ Started {learner_script} (PID: {process.pid})")
                    
                    # Small delay between starting learners
                    time.sleep(1)
                    
                except Exception as e:
                    print(f"❌ Failed to start {learner_script}: {e}")
            else:
                print(f"⚠️  Learner script not found: {learner_script}")
    
    def start_main_trainer(self):
        """Start the main JSTN trainer"""
        print("🏆 Starting main JSTN trainer...")
        
        try:
            process = subprocess.Popen(
                [sys.executable, 'jstn_complete_trainer.py'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            self.processes['main_trainer'] = process
            print(f"✅ Started main JSTN trainer (PID: {process.pid})")
            
        except Exception as e:
            print(f"❌ Failed to start main JSTN trainer: {e}")
    
    def monitor_processes(self):
        """Monitor all processes and restart if needed"""
        print("👀 Monitoring all processes...")
        
        while True:
            for process_name, process in self.processes.items():
                if process.poll() is not None:  # Process has terminated
                    print(f"⚠️  Process {process_name} died, restarting...")
                    
                    try:
                        # Determine script name
                        if process_name == 'main_trainer':
                            script_name = 'jstn_complete_trainer.py'
                        elif process_name.startswith('worker_'):
                            script_name = process_name.replace('worker_', '')
                        elif process_name.startswith('learner_'):
                            script_name = process_name.replace('learner_', '')
                        else:
                            continue
                        
                        # Restart process
                        new_process = subprocess.Popen(
                            [sys.executable, script_name],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            text=True
                        )
                        
                        self.processes[process_name] = new_process
                        print(f"✅ Restarted {process_name} (PID: {new_process.pid})")
                        
                    except Exception as e:
                        print(f"❌ Failed to restart {process_name}: {e}")
            
            # Sleep before next check
            time.sleep(10)
    
    def cleanup(self):
        """Cleanup all processes"""
        print("🧹 Cleaning up all processes...")
        
        for process_name, process in self.processes.items():
            try:
                # Terminate process
                process.terminate()
                
                # Wait for graceful shutdown
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    # Force kill if needed
                    process.kill()
                    process.wait()
                
                print(f"✅ Terminated {process_name}")
                
            except Exception as e:
                print(f"❌ Failed to terminate {process_name}: {e}")
    
    def run(self):
        """Run the complete JSTN training system"""
        print("🏆 Starting JSTN Complete Training System...")
        print("🎯 This will train the ENTIRE bot to play like jstn (Justin)!")
        
        try:
            # Start all workers
            self.start_workers()
            
            # Wait a bit for workers to initialize
            time.sleep(5)
            
            # Start all learners
            self.start_learners()
            
            # Wait a bit for learners to initialize
            time.sleep(5)
            
            # Start main trainer
            self.start_main_trainer()
            
            print("✅ All processes started!")
            print("🎯 Training to play like jstn - the legendary pro!")
            print("📊 Press Ctrl+C to stop training")
            
            # Start monitoring thread
            monitor_thread = threading.Thread(target=self.monitor_processes, daemon=True)
            monitor_thread.start()
            
            # Wait for main trainer to complete
            if 'main_trainer' in self.processes:
                self.processes['main_trainer'].wait()
            
        except KeyboardInterrupt:
            print("\n⏹️  Training interrupted by user")
        except Exception as e:
            print(f"❌ Training error: {e}")
        finally:
            self.cleanup()
            print("✅ JSTN training completed!")

def signal_handler(signum, frame):
    """Handle interrupt signals"""
    print("\n⏹️  Received interrupt signal, shutting down...")
    sys.exit(0)

def main():
    """Main function"""
    print("🏆 JSTN Training Launcher")
    print("=" * 50)
    print("🎯 Launching complete JSTN training system!")
    print("🚀 This will start ALL workers and learners!")
    
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Create and run launcher
    launcher = JSTNTrainingLauncher()
    launcher.run()

if __name__ == "__main__":
    main()
