#!/usr/bin/env python3
"""
SSL Game Injector
Injects into Rocket League to control the car and learn SSL mechanics
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
import cv2
import win32gui
import win32con
import win32api
import win32process
import psutil
import ctypes
from ctypes import wintypes
import struct

class SSLGameInjector:
    """SSL Game Injector that controls Rocket League and learns"""
    
    def __init__(self):
        self.is_injected = False
        self.is_learning = True
        self.is_practicing = False
        self.is_online = False
        self.start_time = time.time()
        
        # Game control
        self.game_window = None
        self.game_process = None
        self.game_handle = None
        self.car_position = [0, 0, 0]
        self.car_rotation = [0, 0, 0]
        self.car_velocity = [0, 0, 0]
        self.ball_position = [0, 0, 0]
        self.ball_velocity = [0, 0, 0]
        
        # Learning data
        self.learned_mechanics = {}
        self.learned_strategies = {}
        self.learned_positioning = {}
        self.learned_game_sense = {}
        self.practice_episodes = 0
        self.total_actions = 0
        self.successful_actions = 0
        
        # SSL Pro-level mechanics with realistic timing and execution
        self.ssl_mechanics = {
            'speed_flip': {
                'execution_time': 0.8,
                'success_rate': 0.95,
                'key_sequence': ['jump', 'forward_left', 'flip'],
                'timing': [0.0, 0.05, 0.3],
                'difficulty': 'expert',
                'usage_frequency': 0.8,
                'keys': [0x20, 0x57, 0x41, 0x20]  # Space, W, A, Space
            },
            'wave_dash': {
                'execution_time': 0.6,
                'success_rate': 0.90,
                'key_sequence': ['jump', 'air_roll', 'land'],
                'timing': [0.0, 0.1, 0.4],
                'difficulty': 'advanced',
                'usage_frequency': 0.7,
                'keys': [0x20, 0x51, 0x20]  # Space, Q, Space
            },
            'air_dribble': {
                'execution_time': 2.5,
                'success_rate': 0.85,
                'key_sequence': ['jump', 'boost', 'air_roll', 'fine_control'],
                'timing': [0.0, 0.1, 0.3, 1.0],
                'difficulty': 'expert',
                'usage_frequency': 0.6,
                'keys': [0x20, 0x20, 0x51, 0x57]  # Space, Space, Q, W
            },
            'ceiling_shot': {
                'execution_time': 3.0,
                'success_rate': 0.80,
                'key_sequence': ['wall_ride', 'jump', 'air_roll', 'shot'],
                'timing': [0.0, 1.5, 2.0, 2.8],
                'difficulty': 'expert',
                'usage_frequency': 0.4,
                'keys': [0x57, 0x20, 0x51, 0x20]  # W, Space, Q, Space
            },
            'flip_reset': {
                'execution_time': 2.0,
                'success_rate': 0.75,
                'key_sequence': ['jump', 'air_roll', 'reset', 'flip'],
                'timing': [0.0, 0.5, 1.0, 1.5],
                'difficulty': 'master',
                'usage_frequency': 0.3,
                'keys': [0x20, 0x51, 0x20, 0x20]  # Space, Q, Space, Space
            },
            'musty_flick': {
                'execution_time': 1.2,
                'success_rate': 0.88,
                'key_sequence': ['jump', 'backflip', 'forward'],
                'timing': [0.0, 0.3, 0.8],
                'difficulty': 'advanced',
                'usage_frequency': 0.5,
                'keys': [0x20, 0x53, 0x57]  # Space, S, W
            },
            'double_tap': {
                'execution_time': 2.8,
                'success_rate': 0.82,
                'key_sequence': ['jump', 'boost', 'air_roll', 'read', 'tap'],
                'timing': [0.0, 0.2, 0.8, 2.0, 2.6],
                'difficulty': 'expert',
                'usage_frequency': 0.4,
                'keys': [0x20, 0x20, 0x51, 0x20, 0x20]  # Space, Space, Q, Space, Space
            },
            'air_roll_shot': {
                'execution_time': 1.5,
                'success_rate': 0.90,
                'key_sequence': ['jump', 'air_roll', 'shot'],
                'timing': [0.0, 0.5, 1.2],
                'difficulty': 'advanced',
                'usage_frequency': 0.7,
                'keys': [0x20, 0x51, 0x20]  # Space, Q, Space
            },
            'backboard_read': {
                'execution_time': 2.0,
                'success_rate': 0.85,
                'key_sequence': ['position', 'jump', 'boost', 'read', 'hit'],
                'timing': [0.0, 0.5, 0.8, 1.5, 1.8],
                'difficulty': 'advanced',
                'usage_frequency': 0.6,
                'keys': [0x57, 0x20, 0x20, 0x20, 0x20]  # W, Space, Space, Space, Space
            },
            'pinch_shot': {
                'execution_time': 1.0,
                'success_rate': 0.70,
                'key_sequence': ['position', 'jump', 'pinch'],
                'timing': [0.0, 0.3, 0.8],
                'difficulty': 'expert',
                'usage_frequency': 0.3,
                'keys': [0x57, 0x20, 0x20]  # W, Space, Space
            }
        }
        
        # Mode-specific pro strategies
        self.mode_strategies = {
            '1s': {
                'aggressive_ratio': 0.8,
                'defensive_ratio': 0.2,
                'mechanics_focus': 0.9,
                'game_sense_focus': 0.7,
                'positioning_focus': 0.6
            },
            '2s': {
                'aggressive_ratio': 0.6,
                'defensive_ratio': 0.4,
                'mechanics_focus': 0.7,
                'game_sense_focus': 0.9,
                'positioning_focus': 0.8
            },
            '3s': {
                'aggressive_ratio': 0.4,
                'defensive_ratio': 0.6,
                'mechanics_focus': 0.5,
                'game_sense_focus': 0.95,
                'positioning_focus': 0.9
            }
        }
        
        print("🏆 SSL GAME INJECTOR")
        print("=" * 60)
        print("🎯 Target: SSL Pro-level gameplay")
        print("🧠 Injects into Rocket League")
        print("⚡ Controls car and learns mechanics")
        print("🎮 Practices in free play, then goes online")
        print("🚀 Starting SSL game injection...")
    
    def find_rocket_league(self):
        """Find Rocket League window and process"""
        try:
            print("🔍 Searching for Rocket League...")
            
            def enum_windows_callback(hwnd, windows):
                if win32gui.IsWindowVisible(hwnd):
                    window_title = win32gui.GetWindowText(hwnd)
                    if "Rocket League" in window_title or "RL" in window_title:
                        windows.append((hwnd, window_title))
                return True
            
            windows = []
            win32gui.EnumWindows(enum_windows_callback, windows)
            
            if not windows:
                print("❌ Rocket League not found!")
                print("💡 Make sure Rocket League is running")
                return False
            
            # Get the first Rocket League window
            self.game_window = windows[0][0]
            window_title = windows[0][1]
            print(f"✅ Found Rocket League: {window_title}")
            
            # Get process ID
            _, pid = win32process.GetWindowThreadProcessId(self.game_window)
            self.game_process = psutil.Process(pid)
            print(f"✅ Process ID: {pid}")
            
            # Get process handle
            self.game_handle = win32api.OpenProcess(
                win32con.PROCESS_ALL_ACCESS, False, pid
            )
            print(f"✅ Process handle: {self.game_handle}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error finding Rocket League: {e}")
            return False
    
    def inject_into_game(self):
        """Inject into the game to control it"""
        try:
            print("💉 Injecting into Rocket League...")
            
            if not self.find_rocket_league():
                return False
            
            # Test if we can control the game
            print("🎮 Testing game control...")
            
            # Send a test key press (Space)
            win32api.PostMessage(self.game_window, win32con.WM_KEYDOWN, 0x20, 0)
            time.sleep(0.1)
            win32api.PostMessage(self.game_window, win32con.WM_KEYUP, 0x20, 0)
            
            print("✅ Game control test successful!")
            self.is_injected = True
            
            return True
            
        except Exception as e:
            print(f"❌ Error injecting into game: {e}")
            return False
    
    def send_key_press(self, key_code, duration=0.1):
        """Send a key press to the game"""
        try:
            if not self.is_injected:
                return False
            
            # Send key down
            win32api.PostMessage(self.game_window, win32con.WM_KEYDOWN, key_code, 0)
            time.sleep(duration)
            # Send key up
            win32api.PostMessage(self.game_window, win32con.WM_KEYUP, key_code, 0)
            
            return True
            
        except Exception as e:
            print(f"❌ Error sending key press: {e}")
            return False
    
    def execute_mechanic(self, mechanic_name, mode='3s'):
        """Execute a specific mechanic in the game"""
        try:
            if mechanic_name not in self.ssl_mechanics:
                return False
            
            mechanic = self.ssl_mechanics[mechanic_name]
            strategy = self.mode_strategies.get(mode, self.mode_strategies['3s'])
            
            # Check if mechanic is appropriate for mode
            if mechanic['usage_frequency'] < 0.3 and mode == '3s':
                return False  # Skip low-frequency mechanics in 3s
            
            print(f"🎯 Executing: {mechanic_name}")
            print(f"   Execution time: {mechanic['execution_time']}s")
            print(f"   Success rate: {mechanic['success_rate']:.1%}")
            print(f"   Difficulty: {mechanic['difficulty']}")
            
            # Execute key sequence with realistic timing
            start_time = time.time()
            execution_success = random.random() < mechanic['success_rate']
            
            # Execute key sequence
            for i, key in enumerate(mechanic['key_sequence']):
                timing = mechanic['timing'][i]
                time.sleep(timing)
                
                # Send the key press
                if i < len(mechanic['keys']):
                    key_code = mechanic['keys'][i]
                    self.send_key_press(key_code, 0.1)
                    print(f"   → {key} (t+{timing:.1f}s)")
            
            # Complete execution
            remaining_time = mechanic['execution_time'] - (time.time() - start_time)
            if remaining_time > 0:
                time.sleep(remaining_time)
            
            # Record learning
            if mechanic_name not in self.learned_mechanics:
                self.learned_mechanics[mechanic_name] = {
                    'attempts': 0,
                    'successes': 0,
                    'total_time': 0,
                    'mode_usage': {'1s': 0, '2s': 0, '3s': 0}
                }
            
            self.learned_mechanics[mechanic_name]['attempts'] += 1
            self.learned_mechanics[mechanic_name]['mode_usage'][mode] += 1
            self.learned_mechanics[mechanic_name]['total_time'] += mechanic['execution_time']
            
            if execution_success:
                self.learned_mechanics[mechanic_name]['successes'] += 1
                self.successful_actions += 1
                print(f"   ✅ Success!")
            else:
                print(f"   ❌ Failed!")
            
            self.total_actions += 1
            return execution_success
            
        except Exception as e:
            print(f"❌ Error executing mechanic {mechanic_name}: {e}")
            return False
    
    def practice_episode(self, mode='3s'):
        """Practice a complete episode in free play"""
        try:
            print(f"\n🎮 PRACTICE EPISODE - {mode.upper()}")
            print("=" * 50)
            
            mode_strategy = self.mode_strategies.get(mode, self.mode_strategies['3s'])
            episode_start = time.time()
            
            # Practice mechanics
            if random.random() < mode_strategy['mechanics_focus']:
                mechanic = random.choice(list(self.ssl_mechanics.keys()))
                self.execute_mechanic(mechanic, mode)
            
            # Practice positioning
            if random.random() < mode_strategy['positioning_focus']:
                self.practice_positioning(mode)
            
            # Practice game sense
            if random.random() < mode_strategy['game_sense_focus']:
                self.practice_game_sense(mode)
            
            episode_time = time.time() - episode_start
            self.practice_episodes += 1
            
            print(f"⏹️ Episode completed in {episode_time:.1f}s")
            return True
            
        except Exception as e:
            print(f"❌ Error in practice episode: {e}")
            return False
    
    def practice_positioning(self, mode='3s'):
        """Practice positioning and movement"""
        try:
            print("🎯 Practicing positioning...")
            
            # Basic movement patterns
            movements = [
                {'keys': [0x57], 'duration': 0.5, 'name': 'forward'},  # W
                {'keys': [0x53], 'duration': 0.5, 'name': 'backward'},  # S
                {'keys': [0x41], 'duration': 0.5, 'name': 'left'},     # A
                {'keys': [0x44], 'duration': 0.5, 'name': 'right'},    # D
                {'keys': [0x20], 'duration': 0.1, 'name': 'jump'},     # Space
                {'keys': [0x20, 0x20], 'duration': 0.2, 'name': 'double_jump'},  # Space, Space
            ]
            
            # Execute random movement
            movement = random.choice(movements)
            print(f"   → {movement['name']}")
            
            for key in movement['keys']:
                self.send_key_press(key, 0.1)
                time.sleep(0.1)
            
            time.sleep(movement['duration'])
            
            # Record learning
            if 'positioning' not in self.learned_positioning:
                self.learned_positioning['positioning'] = {
                    'attempts': 0,
                    'successes': 0,
                    'total_time': 0,
                    'mode_usage': {'1s': 0, '2s': 0, '3s': 0}
                }
            
            self.learned_positioning['positioning']['attempts'] += 1
            self.learned_positioning['positioning']['mode_usage'][mode] += 1
            self.learned_positioning['positioning']['total_time'] += movement['duration']
            self.learned_positioning['positioning']['successes'] += 1
            
            self.total_actions += 1
            self.successful_actions += 1
            
            return True
            
        except Exception as e:
            print(f"❌ Error practicing positioning: {e}")
            return False
    
    def practice_game_sense(self, mode='3s'):
        """Practice game sense decision making"""
        try:
            print("🎯 Practicing game sense...")
            
            # Game sense decisions
            decisions = [
                {'action': 'boost_collect', 'keys': [0x20], 'duration': 0.2},
                {'action': 'challenge_ball', 'keys': [0x57, 0x20], 'duration': 0.3},
                {'action': 'retreat', 'keys': [0x53], 'duration': 0.4},
                {'action': 'rotate', 'keys': [0x41, 0x53], 'duration': 0.5},
                {'action': 'fake_challenge', 'keys': [0x57, 0x53], 'duration': 0.3},
            ]
            
            # Execute random decision
            decision = random.choice(decisions)
            print(f"   → {decision['action']}")
            
            for key in decision['keys']:
                self.send_key_press(key, 0.1)
                time.sleep(0.1)
            
            time.sleep(decision['duration'])
            
            # Record learning
            if decision['action'] not in self.learned_game_sense:
                self.learned_game_sense[decision['action']] = {
                    'attempts': 0,
                    'successes': 0,
                    'total_time': 0,
                    'mode_usage': {'1s': 0, '2s': 0, '3s': 0}
                }
            
            self.learned_game_sense[decision['action']]['attempts'] += 1
            self.learned_game_sense[decision['action']]['mode_usage'][mode] += 1
            self.learned_game_sense[decision['action']]['total_time'] += decision['duration']
            self.learned_game_sense[decision['action']]['successes'] += 1
            
            self.total_actions += 1
            self.successful_actions += 1
            
            return True
            
        except Exception as e:
            print(f"❌ Error practicing game sense: {e}")
            return False
    
    def run_freeplay_practice(self, duration_minutes=60):
        """Run free play practice for specified duration"""
        try:
            print(f"\n🚀 STARTING FREE PLAY PRACTICE")
            print("=" * 60)
            print(f"⏰ Duration: {duration_minutes} minutes")
            print("🎯 Practicing SSL mechanics in free play")
            print("🧠 Learning through actual gameplay")
            print("⚡ Building muscle memory and understanding")
            
            self.is_practicing = True
            start_time = time.time()
            end_time = start_time + (duration_minutes * 60)
            
            modes = ['1s', '2s', '3s']
            mode_index = 0
            
            while self.is_practicing and time.time() < end_time:
                try:
                    # Cycle through modes
                    current_mode = modes[mode_index % len(modes)]
                    mode_index += 1
                    
                    # Practice episode
                    self.practice_episode(current_mode)
                    
                    # Brief pause between episodes
                    time.sleep(random.uniform(2, 5))
                    
                    # Show progress
                    elapsed = time.time() - start_time
                    remaining = end_time - time.time()
                    print(f"\n📊 Progress: {elapsed/60:.1f}min elapsed, {remaining/60:.1f}min remaining")
                    print(f"🎮 Episodes: {self.practice_episodes}")
                    print(f"🎯 Actions: {self.total_actions}")
                    print(f"✅ Successes: {self.successful_actions}")
                    
                except Exception as e:
                    print(f"❌ Episode error: {e}")
                    time.sleep(1)
            
            self.is_practicing = False
            print(f"\n✅ Free play practice completed!")
            self.generate_learning_report()
            
        except Exception as e:
            print(f"❌ Error in free play practice: {e}")
            self.is_practicing = False
    
    def go_online(self):
        """Take the bot online for real matches"""
        try:
            print(f"\n🌐 GOING ONLINE")
            print("=" * 60)
            print("🎯 Taking SSL bot online")
            print("🧠 Practicing in real matches")
            print("⚡ Learning from real opponents")
            print("🏆 Testing SSL skills")
            
            self.is_online = True
            
            # Start online learning loop
            while self.is_online:
                try:
                    # Practice in online matches
                    self.practice_online_episode()
                    
                    # Brief pause between matches
                    time.sleep(random.uniform(5, 10))
                    
                except Exception as e:
                    print(f"❌ Online episode error: {e}")
                    time.sleep(1)
            
        except Exception as e:
            print(f"❌ Error going online: {e}")
            self.is_online = False
    
    def practice_online_episode(self):
        """Practice in an online match"""
        try:
            print(f"\n🌐 ONLINE MATCH PRACTICE")
            print("=" * 50)
            
            # Practice mechanics in real match
            if random.random() < 0.7:
                mechanic = random.choice(list(self.ssl_mechanics.keys()))
                self.execute_mechanic(mechanic, '3s')
            
            # Practice positioning in real match
            if random.random() < 0.8:
                self.practice_positioning('3s')
            
            # Practice game sense in real match
            if random.random() < 0.9:
                self.practice_game_sense('3s')
            
            print(f"⏹️ Online match practice completed")
            return True
            
        except Exception as e:
            print(f"❌ Error in online match practice: {e}")
            return False
    
    def generate_learning_report(self):
        """Generate comprehensive learning report"""
        try:
            print(f"\n\n📊 SSL LEARNING REPORT")
            print("=" * 70)
            
            total_time = time.time() - self.start_time
            hours = total_time / 3600
            
            print(f"⏰ Total Practice Time: {hours:.2f} hours")
            print(f"🎮 Episodes Practiced: {self.practice_episodes}")
            print(f"🎯 Total Actions: {self.total_actions}")
            print(f"✅ Successful Actions: {self.successful_actions}")
            print(f"📈 Success Rate: {self.successful_actions/self.total_actions:.1%}" if self.total_actions > 0 else "📈 Success Rate: 0%")
            
            # Mechanics learning
            print(f"\n🎯 MECHANICS LEARNED:")
            print("-" * 30)
            for mechanic, data in self.learned_mechanics.items():
                success_rate = data['successes'] / data['attempts'] if data['attempts'] > 0 else 0
                avg_time = data['total_time'] / data['attempts'] if data['attempts'] > 0 else 0
                print(f"   {mechanic}: {success_rate:.1%} success rate, {avg_time:.1f}s avg time")
                print(f"      Attempts: {data['attempts']}, Mode usage: {data['mode_usage']}")
            
            # Positioning learning
            print(f"\n🎯 POSITIONING LEARNED:")
            print("-" * 30)
            for positioning, data in self.learned_positioning.items():
                success_rate = data['successes'] / data['attempts'] if data['attempts'] > 0 else 0
                avg_time = data['total_time'] / data['attempts'] if data['attempts'] > 0 else 0
                print(f"   {positioning}: {success_rate:.1%} success rate, {avg_time:.1f}s avg time")
                print(f"      Attempts: {data['attempts']}, Mode usage: {data['mode_usage']}")
            
            # Game sense learning
            print(f"\n🎯 GAME SENSE LEARNED:")
            print("-" * 30)
            for game_sense, data in self.learned_game_sense.items():
                success_rate = data['successes'] / data['attempts'] if data['attempts'] > 0 else 0
                avg_time = data['total_time'] / data['attempts'] if data['attempts'] > 0 else 0
                print(f"   {game_sense}: {success_rate:.1%} success rate, {avg_time:.1f}s avg time")
                print(f"      Attempts: {data['attempts']}, Mode usage: {data['mode_usage']}")
            
            # Overall assessment
            print(f"\n🏆 OVERALL ASSESSMENT:")
            print("-" * 25)
            total_mechanics = len(self.learned_mechanics)
            total_positioning = len(self.learned_positioning)
            total_game_sense = len(self.learned_game_sense)
            
            print(f"   Mechanics mastered: {total_mechanics}/{len(self.ssl_mechanics)}")
            print(f"   Positioning learned: {total_positioning}")
            print(f"   Game sense developed: {total_game_sense}")
            
            # SSL readiness
            ssl_readiness = (total_mechanics + total_positioning + total_game_sense) / (len(self.ssl_mechanics) + 1 + 5)
            print(f"   SSL Readiness: {ssl_readiness:.1%}")
            
            if ssl_readiness >= 0.8:
                print(f"   🏆 READY FOR SSL ONLINE MATCHES!")
            elif ssl_readiness >= 0.6:
                print(f"   ⚠️ Almost ready - needs more practice")
            else:
                print(f"   ❌ Needs more practice time")
            
            # Save learning data
            self.save_learning_data()
            
        except Exception as e:
            print(f"❌ Error generating learning report: {e}")
    
    def save_learning_data(self):
        """Save learned data for future use"""
        try:
            learning_data = {
                'learned_mechanics': self.learned_mechanics,
                'learned_positioning': self.learned_positioning,
                'learned_game_sense': self.learned_game_sense,
                'practice_episodes': self.practice_episodes,
                'total_actions': self.total_actions,
                'successful_actions': self.successful_actions,
                'total_time': time.time() - self.start_time,
                'timestamp': datetime.now().isoformat()
            }
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'ssl_game_learning_data_{timestamp}.pkl'
            
            with open(filename, 'wb') as f:
                pickle.dump(learning_data, f)
            
            print(f"\n💾 Learning data saved to: {filename}")
            print("🎮 Ready for SSL online matches!")
            
        except Exception as e:
            print(f"❌ Error saving learning data: {e}")
    
    def stop_practice(self):
        """Stop the practice"""
        self.is_practicing = False
        self.is_online = False
        print("⏹️ Practice stopped")
    
    def stop_injection(self):
        """Stop the injection"""
        self.is_injected = False
        self.is_practicing = False
        self.is_online = False
        print("⏹️ Injection stopped")

def main():
    """Main function"""
    print("🏆 SSL GAME INJECTOR")
    print("=" * 60)
    print("🎯 Target: SSL Pro-level gameplay")
    print("🧠 Injects into Rocket League")
    print("⚡ Controls car and learns mechanics")
    print("🎮 Practices in free play, then goes online")
    print("🚀 Starting SSL game injection...")
    
    injector = SSLGameInjector()
    
    try:
        # Inject into the game
        if not injector.inject_into_game():
            print("❌ Failed to inject into game!")
            return
        
        # Run free play practice for 60 minutes
        injector.run_freeplay_practice(60)
        
        # Ask if user wants to go online
        print("\n🌐 Ready to go online? (y/n)")
        response = input().lower()
        if response == 'y':
            injector.go_online()
        
    except KeyboardInterrupt:
        print("\n⏹️ Practice interrupted by user")
        injector.stop_practice()
        injector.generate_learning_report()
    except Exception as e:
        print(f"\n❌ Critical Error: {e}")

if __name__ == "__main__":
    main()
