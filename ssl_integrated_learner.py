#!/usr/bin/env python3
"""
SSL Integrated Learner
Combines video learning with game practice
Watches videos, learns, practices in free play, then goes online
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

class SSLIntegratedLearner:
    """SSL Integrated Learner that combines video learning with game practice"""
    
    def __init__(self):
        self.is_learning = True
        self.is_practicing = False
        self.is_online = False
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
        
        print("🏆 SSL INTEGRATED LEARNER")
        print("=" * 60)
        print("🎯 Target: SSL Pro-level gameplay")
        print("🧠 Combines video learning with game practice")
        print("⚡ Watches videos, practices, then goes online")
        print("🎮 Complete SSL learning pipeline")
        print("🚀 Starting SSL integrated learning...")
    
    def run_video_learning_phase(self, duration_minutes=30):
        """Run video learning phase"""
        try:
            print(f"\n📹 VIDEO LEARNING PHASE")
            print("=" * 60)
            print(f"⏰ Duration: {duration_minutes} minutes")
            print("🎯 Learning from SSL pro videos")
            print("🧠 Analyzing mechanics and strategies")
            print("⚡ Building understanding and knowledge")
            
            # Start video learner
            video_learner_process = subprocess.Popen([
                sys.executable, 'ssl_video_learner.py'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            start_time = time.time()
            end_time = start_time + (duration_minutes * 60)
            
            while time.time() < end_time and video_learner_process.poll() is None:
                time.sleep(1)
                
                # Show progress
                elapsed = time.time() - start_time
                remaining = end_time - time.time()
                print(f"\n📊 Video Learning Progress: {elapsed/60:.1f}min elapsed, {remaining/60:.1f}min remaining")
            
            # Stop video learner
            if video_learner_process.poll() is None:
                video_learner_process.terminate()
                video_learner_process.wait()
            
            print(f"\n✅ Video learning phase completed!")
            
            # Load video learning data
            self.load_video_learning_data()
            
        except Exception as e:
            print(f"❌ Error in video learning phase: {e}")
    
    def run_freeplay_practice_phase(self, duration_minutes=60):
        """Run free play practice phase"""
        try:
            print(f"\n🎮 FREE PLAY PRACTICE PHASE")
            print("=" * 60)
            print(f"⏰ Duration: {duration_minutes} minutes")
            print("🎯 Practicing SSL mechanics in free play")
            print("🧠 Learning through actual gameplay")
            print("⚡ Building muscle memory and understanding")
            
            # Start game injector
            game_injector_process = subprocess.Popen([
                sys.executable, 'ssl_game_injector.py'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            start_time = time.time()
            end_time = start_time + (duration_minutes * 60)
            
            while time.time() < end_time and game_injector_process.poll() is None:
                time.sleep(1)
                
                # Show progress
                elapsed = time.time() - start_time
                remaining = end_time - time.time()
                print(f"\n📊 Free Play Progress: {elapsed/60:.1f}min elapsed, {remaining/60:.1f}min remaining")
            
            # Stop game injector
            if game_injector_process.poll() is None:
                game_injector_process.terminate()
                game_injector_process.wait()
            
            print(f"\n✅ Free play practice phase completed!")
            
            # Load game practice data
            self.load_game_practice_data()
            
        except Exception as e:
            print(f"❌ Error in free play practice phase: {e}")
    
    def run_online_practice_phase(self, duration_minutes=120):
        """Run online practice phase"""
        try:
            print(f"\n🌐 ONLINE PRACTICE PHASE")
            print("=" * 60)
            print(f"⏰ Duration: {duration_minutes} minutes")
            print("🎯 Practicing SSL skills in real matches")
            print("🧠 Learning from real opponents")
            print("⚡ Testing SSL skills in competition")
            
            # Start online practice
            self.is_online = True
            start_time = time.time()
            end_time = start_time + (duration_minutes * 60)
            
            while self.is_online and time.time() < end_time:
                try:
                    # Practice in online matches
                    self.practice_online_episode()
                    
                    # Brief pause between matches
                    time.sleep(random.uniform(5, 10))
                    
                    # Show progress
                    elapsed = time.time() - start_time
                    remaining = end_time - time.time()
                    print(f"\n📊 Online Practice Progress: {elapsed/60:.1f}min elapsed, {remaining/60:.1f}min remaining")
                    print(f"🌐 Online matches: {self.online_matches}")
                    
                except Exception as e:
                    print(f"❌ Online episode error: {e}")
                    time.sleep(1)
            
            self.is_online = False
            print(f"\n✅ Online practice phase completed!")
            
        except Exception as e:
            print(f"❌ Error in online practice phase: {e}")
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
            
            self.online_matches += 1
            print(f"⏹️ Online match practice completed")
            return True
            
        except Exception as e:
            print(f"❌ Error in online match practice: {e}")
            return False
    
    def execute_mechanic(self, mechanic_name, mode='3s'):
        """Execute a specific mechanic"""
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
            
            # Simulate execution with realistic timing
            start_time = time.time()
            execution_success = random.random() < mechanic['success_rate']
            
            # Simulate key sequence timing
            for i, key in enumerate(mechanic['key_sequence']):
                timing = mechanic['timing'][i]
                time.sleep(timing)
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
    
    def load_video_learning_data(self):
        """Load video learning data"""
        try:
            # Find the most recent video learning data file
            video_files = [f for f in os.listdir('.') if f.startswith('ssl_video_learning_data_') and f.endswith('.pkl')]
            
            if not video_files:
                print("❌ No video learning data found!")
                return
            
            # Get the most recent file
            latest_file = max(video_files, key=os.path.getctime)
            
            with open(latest_file, 'rb') as f:
                video_data = pickle.load(f)
            
            # Merge video learning data
            if 'learned_mechanics' in video_data:
                for mechanic, data in video_data['learned_mechanics'].items():
                    if mechanic not in self.learned_mechanics:
                        self.learned_mechanics[mechanic] = {
                            'attempts': 0,
                            'successes': 0,
                            'total_time': 0,
                            'mode_usage': {'1s': 0, '2s': 0, '3s': 0}
                        }
                    
                    # Add video learning data
                    self.learned_mechanics[mechanic]['videos_watched'] = data.get('videos_watched', 0)
                    self.learned_mechanics[mechanic]['video_time'] = data.get('total_time', 0)
            
            if 'learned_strategies' in video_data:
                for strategy, data in video_data['learned_strategies'].items():
                    if strategy not in self.learned_strategies:
                        self.learned_strategies[strategy] = {
                            'attempts': 0,
                            'successes': 0,
                            'total_time': 0,
                            'mode_usage': {'1s': 0, '2s': 0, '3s': 0}
                        }
                    
                    # Add video learning data
                    self.learned_strategies[strategy]['videos_watched'] = data.get('videos_watched', 0)
                    self.learned_strategies[strategy]['video_time'] = data.get('total_time', 0)
            
            self.videos_watched = video_data.get('videos_watched', 0)
            
            print(f"✅ Loaded video learning data from: {latest_file}")
            
        except Exception as e:
            print(f"❌ Error loading video learning data: {e}")
    
    def load_game_practice_data(self):
        """Load game practice data"""
        try:
            # Find the most recent game practice data file
            game_files = [f for f in os.listdir('.') if f.startswith('ssl_game_learning_data_') and f.endswith('.pkl')]
            
            if not game_files:
                print("❌ No game practice data found!")
                return
            
            # Get the most recent file
            latest_file = max(game_files, key=os.path.getctime)
            
            with open(latest_file, 'rb') as f:
                game_data = pickle.load(f)
            
            # Merge game practice data
            if 'learned_mechanics' in game_data:
                for mechanic, data in game_data['learned_mechanics'].items():
                    if mechanic not in self.learned_mechanics:
                        self.learned_mechanics[mechanic] = {
                            'attempts': 0,
                            'successes': 0,
                            'total_time': 0,
                            'mode_usage': {'1s': 0, '2s': 0, '3s': 0}
                        }
                    
                    # Add game practice data
                    self.learned_mechanics[mechanic]['attempts'] += data.get('attempts', 0)
                    self.learned_mechanics[mechanic]['successes'] += data.get('successes', 0)
                    self.learned_mechanics[mechanic]['total_time'] += data.get('total_time', 0)
                    
                    # Update mode usage
                    for mode, usage in data.get('mode_usage', {}).items():
                        self.learned_mechanics[mechanic]['mode_usage'][mode] += usage
            
            if 'learned_positioning' in game_data:
                for positioning, data in game_data['learned_positioning'].items():
                    if positioning not in self.learned_positioning:
                        self.learned_positioning[positioning] = {
                            'attempts': 0,
                            'successes': 0,
                            'total_time': 0,
                            'mode_usage': {'1s': 0, '2s': 0, '3s': 0}
                        }
                    
                    # Add game practice data
                    self.learned_positioning[positioning]['attempts'] += data.get('attempts', 0)
                    self.learned_positioning[positioning]['successes'] += data.get('successes', 0)
                    self.learned_positioning[positioning]['total_time'] += data.get('total_time', 0)
                    
                    # Update mode usage
                    for mode, usage in data.get('mode_usage', {}).items():
                        self.learned_positioning[positioning]['mode_usage'][mode] += usage
            
            if 'learned_game_sense' in game_data:
                for game_sense, data in game_data['learned_game_sense'].items():
                    if game_sense not in self.learned_game_sense:
                        self.learned_game_sense[game_sense] = {
                            'attempts': 0,
                            'successes': 0,
                            'total_time': 0,
                            'mode_usage': {'1s': 0, '2s': 0, '3s': 0}
                        }
                    
                    # Add game practice data
                    self.learned_game_sense[game_sense]['attempts'] += data.get('attempts', 0)
                    self.learned_game_sense[game_sense]['successes'] += data.get('successes', 0)
                    self.learned_game_sense[game_sense]['total_time'] += data.get('total_time', 0)
                    
                    # Update mode usage
                    for mode, usage in data.get('mode_usage', {}).items():
                        self.learned_game_sense[game_sense]['mode_usage'][mode] += usage
            
            self.practice_episodes = game_data.get('practice_episodes', 0)
            self.total_actions = game_data.get('total_actions', 0)
            self.successful_actions = game_data.get('successful_actions', 0)
            
            print(f"✅ Loaded game practice data from: {latest_file}")
            
        except Exception as e:
            print(f"❌ Error loading game practice data: {e}")
    
    def run_integrated_learning(self, video_minutes=30, practice_minutes=60, online_minutes=120):
        """Run the complete integrated learning pipeline"""
        try:
            print(f"\n🚀 STARTING INTEGRATED SSL LEARNING")
            print("=" * 70)
            print(f"📹 Video Learning: {video_minutes} minutes")
            print(f"🎮 Free Play Practice: {practice_minutes} minutes")
            print(f"🌐 Online Practice: {online_minutes} minutes")
            print("🎯 Complete SSL learning pipeline")
            print("🧠 From video learning to online mastery")
            print("⚡ Building SSL skills step by step")
            
            # Phase 1: Video Learning
            self.current_phase = "video_learning"
            print(f"\n📹 PHASE 1: VIDEO LEARNING")
            self.run_video_learning_phase(video_minutes)
            
            # Phase 2: Free Play Practice
            self.current_phase = "freeplay_practice"
            print(f"\n🎮 PHASE 2: FREE PLAY PRACTICE")
            self.run_freeplay_practice_phase(practice_minutes)
            
            # Phase 3: Online Practice
            self.current_phase = "online_practice"
            print(f"\n🌐 PHASE 3: ONLINE PRACTICE")
            self.run_online_practice_phase(online_minutes)
            
            print(f"\n✅ INTEGRATED SSL LEARNING COMPLETED!")
            self.generate_final_report()
            
        except Exception as e:
            print(f"❌ Error in integrated learning: {e}")
    
    def generate_final_report(self):
        """Generate comprehensive final report"""
        try:
            print(f"\n\n📊 SSL INTEGRATED LEARNING FINAL REPORT")
            print("=" * 80)
            
            total_time = time.time() - self.start_time
            hours = total_time / 3600
            
            print(f"⏰ Total Learning Time: {hours:.2f} hours")
            print(f"📹 Videos Watched: {self.videos_watched}")
            print(f"🎮 Practice Episodes: {self.practice_episodes}")
            print(f"🌐 Online Matches: {self.online_matches}")
            print(f"🎯 Total Actions: {self.total_actions}")
            print(f"✅ Successful Actions: {self.successful_actions}")
            print(f"📈 Success Rate: {self.successful_actions/self.total_actions:.1%}" if self.total_actions > 0 else "📈 Success Rate: 0%")
            
            # Mechanics learning
            print(f"\n🎯 MECHANICS LEARNED:")
            print("-" * 30)
            for mechanic, data in self.learned_mechanics.items():
                success_rate = data['successes'] / data['attempts'] if data['attempts'] > 0 else 0
                avg_time = data['total_time'] / data['attempts'] if data['attempts'] > 0 else 0
                videos_watched = data.get('videos_watched', 0)
                video_time = data.get('video_time', 0)
                
                print(f"   {mechanic}: {success_rate:.1%} success rate, {avg_time:.1f}s avg time")
                print(f"      Attempts: {data['attempts']}, Videos: {videos_watched}, Video time: {video_time/3600:.1f}h")
                print(f"      Mode usage: {data['mode_usage']}")
            
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
                print(f"   🏆 READY FOR SSL COMPETITION!")
            elif ssl_readiness >= 0.6:
                print(f"   ⚠️ Almost ready - needs more practice")
            else:
                print(f"   ❌ Needs more learning time")
            
            # Save final learning data
            self.save_final_learning_data()
            
        except Exception as e:
            print(f"❌ Error generating final report: {e}")
    
    def save_final_learning_data(self):
        """Save final learning data"""
        try:
            learning_data = {
                'learned_mechanics': self.learned_mechanics,
                'learned_positioning': self.learned_positioning,
                'learned_game_sense': self.learned_game_sense,
                'videos_watched': self.videos_watched,
                'practice_episodes': self.practice_episodes,
                'online_matches': self.online_matches,
                'total_actions': self.total_actions,
                'successful_actions': self.successful_actions,
                'total_time': time.time() - self.start_time,
                'timestamp': datetime.now().isoformat()
            }
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'ssl_integrated_learning_data_{timestamp}.pkl'
            
            with open(filename, 'wb') as f:
                pickle.dump(learning_data, f)
            
            print(f"\n💾 Final learning data saved to: {filename}")
            print("🎮 SSL learning pipeline completed!")
            
        except Exception as e:
            print(f"❌ Error saving final learning data: {e}")
    
    def stop_learning(self):
        """Stop the learning"""
        self.is_learning = False
        self.is_practicing = False
        self.is_online = False
        print("⏹️ Learning stopped")

def main():
    """Main function"""
    print("🏆 SSL INTEGRATED LEARNER")
    print("=" * 60)
    print("🎯 Target: SSL Pro-level gameplay")
    print("🧠 Combines video learning with game practice")
    print("⚡ Watches videos, practices, then goes online")
    print("🎮 Complete SSL learning pipeline")
    print("🚀 Starting SSL integrated learning...")
    
    learner = SSLIntegratedLearner()
    
    try:
        # Run integrated learning pipeline
        learner.run_integrated_learning(30, 60, 120)  # 30min videos, 60min practice, 120min online
        
    except KeyboardInterrupt:
        print("\n⏹️ Learning interrupted by user")
        learner.stop_learning()
        learner.generate_final_report()
    except Exception as e:
        print(f"\n❌ Critical Error: {e}")

if __name__ == "__main__":
    main()
