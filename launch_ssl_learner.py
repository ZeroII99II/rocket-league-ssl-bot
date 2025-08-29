#!/usr/bin/env python3
"""
SSL Learner Launcher
Launches the complete SSL learning system
Watches videos, practices in free play, then goes online
"""

import time
import threading
import random
import numpy as np
from datetime import datetime
import json
import os
import sys
import pickle
import subprocess
import signal

class SSLLearnerLauncher:
    """SSL Learner Launcher that manages the complete learning system"""
    
    def __init__(self):
        self.is_running = False
        self.start_time = time.time()
        
        # Learning phases
        self.current_phase = "video_learning"
        self.phases = ["video_learning", "freeplay_practice", "online_practice"]
        self.phase_index = 0
        
        # Learning data
        self.learned_mechanics = {}
        self.learned_strategies = {}
        self.learned_positioning = {}
        self.learned_game_sense = {}
        self.videos_watched = 0
        self.practice_episodes = 0
        self.online_matches = 0
        self.total_actions = 0
        self.successful_actions = 0
        
        print("🏆 SSL LEARNER LAUNCHER")
        print("=" * 60)
        print("🎯 Target: SSL Pro-level gameplay")
        print("🧠 Complete learning system")
        print("⚡ Watches videos, practices, then goes online")
        print("🎮 Ready to launch SSL learning!")
        print("🚀 Starting SSL learner launcher...")
    
    def show_menu(self):
        """Show the main menu"""
        print(f"\n📋 SSL LEARNER MENU")
        print("=" * 40)
        print("1. 🎮 Quick Start (30min videos + 60min practice)")
        print("2. 📹 Video Learning Only (60 minutes)")
        print("3. 🎮 Free Play Practice Only (60 minutes)")
        print("4. 🌐 Online Practice Only (120 minutes)")
        print("5. 🚀 Full Pipeline (30min videos + 60min practice + 120min online)")
        print("6. ⚙️ Custom Configuration")
        print("7. 📊 View Learning Progress")
        print("8. 🛑 Exit")
        print("=" * 40)
    
    def get_user_choice(self):
        """Get user choice from menu"""
        try:
            choice = input("\n🎯 Enter your choice (1-8): ").strip()
            return choice
        except KeyboardInterrupt:
            print("\n⏹️ Exiting...")
            return "8"
        except Exception as e:
            print(f"❌ Error getting user choice: {e}")
            return "8"
    
    def run_quick_start(self):
        """Run quick start learning"""
        try:
            print(f"\n🚀 QUICK START LEARNING")
            print("=" * 60)
            print("📹 30 minutes of video learning")
            print("🎮 60 minutes of free play practice")
            print("🎯 Perfect for getting started!")
            
            # Start integrated learner
            process = subprocess.Popen([
                sys.executable, 'ssl_integrated_learner.py'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Wait for completion
            process.wait()
            
            print(f"\n✅ Quick start learning completed!")
            
        except Exception as e:
            print(f"❌ Error in quick start: {e}")
    
    def run_video_learning_only(self):
        """Run video learning only"""
        try:
            print(f"\n📹 VIDEO LEARNING ONLY")
            print("=" * 60)
            print("🎯 Learning from SSL pro videos")
            print("🧠 Analyzing mechanics and strategies")
            print("⚡ Building understanding and knowledge")
            
            # Start video learner
            process = subprocess.Popen([
                sys.executable, 'ssl_video_learner.py'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Wait for completion
            process.wait()
            
            print(f"\n✅ Video learning completed!")
            
        except Exception as e:
            print(f"❌ Error in video learning: {e}")
    
    def run_freeplay_practice_only(self):
        """Run free play practice only"""
        try:
            print(f"\n🎮 FREE PLAY PRACTICE ONLY")
            print("=" * 60)
            print("🎯 Practicing SSL mechanics in free play")
            print("🧠 Learning through actual gameplay")
            print("⚡ Building muscle memory and understanding")
            
            # Start game injector
            process = subprocess.Popen([
                sys.executable, 'ssl_game_injector.py'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Wait for completion
            process.wait()
            
            print(f"\n✅ Free play practice completed!")
            
        except Exception as e:
            print(f"❌ Error in free play practice: {e}")
    
    def run_online_practice_only(self):
        """Run online practice only"""
        try:
            print(f"\n🌐 ONLINE PRACTICE ONLY")
            print("=" * 60)
            print("🎯 Practicing SSL skills in real matches")
            print("🧠 Learning from real opponents")
            print("⚡ Testing SSL skills in competition")
            
            # Start online practice
            process = subprocess.Popen([
                sys.executable, 'ssl_integrated_learner.py'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Wait for completion
            process.wait()
            
            print(f"\n✅ Online practice completed!")
            
        except Exception as e:
            print(f"❌ Error in online practice: {e}")
    
    def run_full_pipeline(self):
        """Run full learning pipeline"""
        try:
            print(f"\n🚀 FULL LEARNING PIPELINE")
            print("=" * 60)
            print("📹 30 minutes of video learning")
            print("🎮 60 minutes of free play practice")
            print("🌐 120 minutes of online practice")
            print("🎯 Complete SSL learning experience!")
            
            # Start integrated learner
            process = subprocess.Popen([
                sys.executable, 'ssl_integrated_learner.py'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Wait for completion
            process.wait()
            
            print(f"\n✅ Full pipeline completed!")
            
        except Exception as e:
            print(f"❌ Error in full pipeline: {e}")
    
    def run_custom_configuration(self):
        """Run custom configuration"""
        try:
            print(f"\n⚙️ CUSTOM CONFIGURATION")
            print("=" * 60)
            print("🎯 Configure your own learning schedule")
            print("🧠 Set video learning time")
            print("🎮 Set free play practice time")
            print("🌐 Set online practice time")
            
            # Get video learning time
            try:
                video_minutes = int(input("\n📹 Video learning time (minutes): "))
            except ValueError:
                video_minutes = 30
                print(f"⚠️ Invalid input, using default: {video_minutes} minutes")
            
            # Get free play practice time
            try:
                practice_minutes = int(input("🎮 Free play practice time (minutes): "))
            except ValueError:
                practice_minutes = 60
                print(f"⚠️ Invalid input, using default: {practice_minutes} minutes")
            
            # Get online practice time
            try:
                online_minutes = int(input("🌐 Online practice time (minutes): "))
            except ValueError:
                online_minutes = 120
                print(f"⚠️ Invalid input, using default: {online_minutes} minutes")
            
            print(f"\n🚀 Starting custom learning:")
            print(f"   📹 Video learning: {video_minutes} minutes")
            print(f"   🎮 Free play practice: {practice_minutes} minutes")
            print(f"   🌐 Online practice: {online_minutes} minutes")
            
            # Start integrated learner with custom times
            process = subprocess.Popen([
                sys.executable, 'ssl_integrated_learner.py'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Wait for completion
            process.wait()
            
            print(f"\n✅ Custom learning completed!")
            
        except Exception as e:
            print(f"❌ Error in custom configuration: {e}")
    
    def view_learning_progress(self):
        """View learning progress"""
        try:
            print(f"\n📊 LEARNING PROGRESS")
            print("=" * 60)
            
            # Find learning data files
            video_files = [f for f in os.listdir('.') if f.startswith('ssl_video_learning_data_') and f.endswith('.pkl')]
            game_files = [f for f in os.listdir('.') if f.startswith('ssl_game_learning_data_') and f.endswith('.pkl')]
            integrated_files = [f for f in os.listdir('.') if f.startswith('ssl_integrated_learning_data_') and f.endswith('.pkl')]
            
            print(f"📹 Video learning files: {len(video_files)}")
            print(f"🎮 Game practice files: {len(game_files)}")
            print(f"🚀 Integrated learning files: {len(integrated_files)}")
            
            if integrated_files:
                # Show most recent integrated learning data
                latest_file = max(integrated_files, key=os.path.getctime)
                print(f"\n📊 Most recent learning data: {latest_file}")
                
                with open(latest_file, 'rb') as f:
                    data = pickle.load(f)
                
                print(f"   📹 Videos watched: {data.get('videos_watched', 0)}")
                print(f"   🎮 Practice episodes: {data.get('practice_episodes', 0)}")
                print(f"   🌐 Online matches: {data.get('online_matches', 0)}")
                print(f"   🎯 Total actions: {data.get('total_actions', 0)}")
                print(f"   ✅ Successful actions: {data.get('successful_actions', 0)}")
                
                if data.get('total_actions', 0) > 0:
                    success_rate = data.get('successful_actions', 0) / data.get('total_actions', 1)
                    print(f"   📈 Success rate: {success_rate:.1%}")
                
                total_time = data.get('total_time', 0)
                print(f"   ⏰ Total time: {total_time/3600:.2f} hours")
                
                # Show mechanics learned
                mechanics = data.get('learned_mechanics', {})
                print(f"   🎯 Mechanics learned: {len(mechanics)}/{10}")
                
                for mechanic, info in mechanics.items():
                    attempts = info.get('attempts', 0)
                    successes = info.get('successes', 0)
                    success_rate = successes / attempts if attempts > 0 else 0
                    print(f"      {mechanic}: {success_rate:.1%} success rate ({attempts} attempts)")
            
            else:
                print("❌ No learning data found!")
                print("💡 Run some learning sessions first")
            
        except Exception as e:
            print(f"❌ Error viewing learning progress: {e}")
    
    def run_launcher(self):
        """Run the main launcher loop"""
        try:
            self.is_running = True
            
            while self.is_running:
                try:
                    # Show menu
                    self.show_menu()
                    
                    # Get user choice
                    choice = self.get_user_choice()
                    
                    # Handle choice
                    if choice == "1":
                        self.run_quick_start()
                    elif choice == "2":
                        self.run_video_learning_only()
                    elif choice == "3":
                        self.run_freeplay_practice_only()
                    elif choice == "4":
                        self.run_online_practice_only()
                    elif choice == "5":
                        self.run_full_pipeline()
                    elif choice == "6":
                        self.run_custom_configuration()
                    elif choice == "7":
                        self.view_learning_progress()
                    elif choice == "8":
                        print("\n👋 Goodbye! Thanks for using SSL Learner!")
                        self.is_running = False
                    else:
                        print("❌ Invalid choice! Please enter 1-8.")
                    
                    # Brief pause before showing menu again
                    if self.is_running:
                        time.sleep(2)
                    
                except KeyboardInterrupt:
                    print("\n⏹️ Exiting...")
                    self.is_running = False
                except Exception as e:
                    print(f"❌ Error in launcher: {e}")
                    time.sleep(1)
            
        except Exception as e:
            print(f"❌ Critical error in launcher: {e}")
    
    def stop_launcher(self):
        """Stop the launcher"""
        self.is_running = False
        print("⏹️ Launcher stopped")

def main():
    """Main function"""
    print("🏆 SSL LEARNER LAUNCHER")
    print("=" * 60)
    print("🎯 Target: SSL Pro-level gameplay")
    print("🧠 Complete learning system")
    print("⚡ Watches videos, practices, then goes online")
    print("🎮 Ready to launch SSL learning!")
    print("🚀 Starting SSL learner launcher...")
    
    launcher = SSLLearnerLauncher()
    
    try:
        # Run the launcher
        launcher.run_launcher()
        
    except KeyboardInterrupt:
        print("\n⏹️ Launcher interrupted by user")
        launcher.stop_launcher()
    except Exception as e:
        print(f"\n❌ Critical Error: {e}")

if __name__ == "__main__":
    main()
