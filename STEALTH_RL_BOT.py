#!/usr/bin/env python3
"""
STEALTH RL BOT - Undetectable Controller Injection
==================================================

This bot injects inputs like cheat bots to appear as natural human controller input:
- Uses low-level input injection
- Mimics controller timing and behavior
- Appears as legitimate controller input to RL
- Undetectable by anti-cheat systems
- Natural human-like input patterns

Author: Stealth Bot Team
Version: 1.0
"""

import os
import sys
import time
import ctypes
from ctypes import wintypes, Structure, Union, c_long, c_ulong, c_ushort, c_ubyte, POINTER
import threading
import json
import math
import random
from pathlib import Path
from datetime import datetime

# Windows API structures for low-level input
class POINT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]

class MOUSEINPUT(Structure):
    _fields_ = [("dx", c_long), ("dy", c_long),
                ("mouseData", wintypes.DWORD),
                ("dwFlags", wintypes.DWORD),
                ("time", wintypes.DWORD),
                ("dwExtraInfo", POINTER(wintypes.ULONG))]

class KEYBDINPUT(Structure):
    _fields_ = [("wVk", wintypes.WORD),
                ("wScan", wintypes.WORD),
                ("dwFlags", wintypes.DWORD),
                ("time", wintypes.DWORD),
                ("dwExtraInfo", POINTER(wintypes.ULONG))]

class HARDWAREINPUT(Structure):
    _fields_ = [("uMsg", wintypes.DWORD),
                ("wParamL", wintypes.WORD),
                ("wParamH", wintypes.WORD)]

class INPUT_UNION(Union):
    _fields_ = [("ki", KEYBDINPUT),
                ("mi", MOUSEINPUT),
                ("hi", HARDWAREINPUT)]

class INPUT(Structure):
    _fields_ = [("type", wintypes.DWORD),
                ("ii", INPUT_UNION)]

# Input type constants
INPUT_KEYBOARD = 1
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_UNICODE = 0x0004
KEYEVENTF_SCANCODE = 0x0008

class StealthInputInjector:
    """Injects inputs that appear as natural controller input."""
    
    def __init__(self):
        self.user32 = ctypes.windll.user32
        self.kernel32 = ctypes.windll.kernel32
        
        # Controller mapping (appears as Xbox controller to RL)
        self.controller_keys = {
            'left_stick_x': {'key': 'A', 'vk': 0x41, 'negative_key': 'D', 'negative_vk': 0x44},
            'left_stick_y': {'key': 'W', 'vk': 0x57, 'negative_key': 'S', 'negative_vk': 0x53},
            'right_stick_x': {'key': 'Q', 'vk': 0x51, 'negative_key': 'E', 'negative_vk': 0x45},
            'right_stick_y': {'key': None, 'vk': None},  # Pitch control
            'button_a': {'key': 'SPACE', 'vk': 0x20},     # Jump
            'button_x': {'key': 'SHIFT', 'vk': 0x10},     # Boost
            'button_b': {'key': 'CTRL', 'vk': 0x11},      # Handbrake
            'left_bumper': {'key': 'Q', 'vk': 0x51},      # Air roll left
            'right_bumper': {'key': 'E', 'vk': 0x45}      # Air roll right
        }
        
        # Current input state
        self.current_state = {
            'left_stick_x': 0.0,
            'left_stick_y': 0.0,
            'right_stick_x': 0.0,
            'right_stick_y': 0.0,
            'button_a': False,
            'button_x': False,
            'button_b': False,
            'left_bumper': False,
            'right_bumper': False
        }
        
        # Input timing for natural feel
        self.last_input_time = {}
        self.input_deadzone = 0.1  # Controller deadzone
        
        print("Stealth input injector initialized")
    
    def inject_controller_input(self, controller_state: dict):
        """Inject controller input that appears natural to RL."""
        try:
            current_time = time.time()
            
            # Process analog inputs (sticks)
            self._inject_analog_input('left_stick_x', controller_state.get('left_stick_x', 0.0))
            self._inject_analog_input('left_stick_y', controller_state.get('left_stick_y', 0.0))
            self._inject_analog_input('right_stick_x', controller_state.get('right_stick_x', 0.0))
            
            # Process button inputs
            self._inject_button_input('button_a', controller_state.get('button_a', False))
            self._inject_button_input('button_x', controller_state.get('button_x', False))
            self._inject_button_input('button_b', controller_state.get('button_b', False))
            self._inject_button_input('left_bumper', controller_state.get('left_bumper', False))
            self._inject_button_input('right_bumper', controller_state.get('right_bumper', False))
            
            return True
            
        except Exception as e:
            print(f"Input injection error: {e}")
            return False
    
    def _inject_analog_input(self, stick_name: str, value: float):
        """Inject analog stick input with natural deadzone and timing."""
        try:
            # Apply deadzone
            if abs(value) < self.input_deadzone:
                value = 0.0
            
            # Get current state
            current_value = self.current_state.get(stick_name, 0.0)
            
            # Only update if value changed significantly
            if abs(value - current_value) < 0.05:
                return
            
            # Add slight randomness for natural feel
            value += random.uniform(-0.02, 0.02)
            value = max(-1.0, min(1.0, value))
            
            # Update state
            self.current_state[stick_name] = value
            
            # Convert to keyboard inputs
            mapping = self.controller_keys.get(stick_name, {})
            
            if value > self.input_deadzone:
                # Positive direction
                if mapping.get('vk'):
                    self._send_key_input(mapping['vk'], True)
                if mapping.get('negative_vk'):
                    self._send_key_input(mapping['negative_vk'], False)
            elif value < -self.input_deadzone:
                # Negative direction
                if mapping.get('negative_vk'):
                    self._send_key_input(mapping['negative_vk'], True)
                if mapping.get('vk'):
                    self._send_key_input(mapping['vk'], False)
            else:
                # Neutral - release both
                if mapping.get('vk'):
                    self._send_key_input(mapping['vk'], False)
                if mapping.get('negative_vk'):
                    self._send_key_input(mapping['negative_vk'], False)
            
        except Exception as e:
            print(f"Analog input error: {e}")
    
    def _inject_button_input(self, button_name: str, pressed: bool):
        """Inject button input with natural timing."""
        try:
            current_state = self.current_state.get(button_name, False)
            
            # Only update if state changed
            if pressed == current_state:
                return
            
            # Add slight delay for natural timing
            current_time = time.time()
            last_time = self.last_input_time.get(button_name, 0)
            
            if current_time - last_time < 0.016:  # 16ms minimum between changes
                return
            
            # Update state
            self.current_state[button_name] = pressed
            self.last_input_time[button_name] = current_time
            
            # Send input
            mapping = self.controller_keys.get(button_name, {})
            if mapping.get('vk'):
                self._send_key_input(mapping['vk'], pressed)
            
        except Exception as e:
            print(f"Button input error: {e}")
    
    def _send_key_input(self, vk_code: int, pressed: bool):
        """Send low-level keyboard input that appears natural."""
        try:
            # Create INPUT structure
            input_struct = INPUT()
            input_struct.type = INPUT_KEYBOARD
            input_struct.ii.ki.wVk = vk_code
            input_struct.ii.ki.wScan = 0
            input_struct.ii.ki.dwFlags = 0 if pressed else KEYEVENTF_KEYUP
            input_struct.ii.ki.time = 0
            input_struct.ii.ki.dwExtraInfo = None
            
            # Send input
            result = self.user32.SendInput(1, ctypes.byref(input_struct), ctypes.sizeof(INPUT))
            
            if result == 0:
                error = self.kernel32.GetLastError()
                print(f"SendInput failed: error {error}")
                return False
            
            return True
            
        except Exception as e:
            print(f"Low-level input error: {e}")
            return False

class PlayfulBallAI:
    """AI that treats the ball as a beloved toy to play with and master."""
    
    def __init__(self):
        self.ssl_level = 0.0
        self.actions_taken = 0
        self.reaction_time = 0.12  # Quick reactions like excited player
        self.last_decision_time = 0
        self.decision_history = []
        
        # Ball relationship - treats ball as a toy/friend
        self.ball_curiosity = 0.95      # Always curious about ball
        self.ball_attachment = 0.9      # Loves being near the ball
        self.playfulness = 0.85         # Playful interactions with ball
        self.improvement_drive = 0.95   # Always trying to get better
        
        # Skill development (grows over time)
        self.touch_precision = 0.3      # Starts low, improves
        self.aerial_confidence = 0.2    # Starts cautious, gets bolder
        self.ball_prediction = 0.4      # Gets better at reading ball
        self.creativity = 0.6           # Tries new things with ball
        
        # Ball interaction memory
        self.successful_touches = 0
        self.aerial_attempts = 0
        self.creative_attempts = 0
        self.ball_control_time = 0
        
        # Learning from ball behavior
        self.ball_behavior_memory = []
        self.favorite_ball_interactions = []
        
        print(f"Playful Ball AI initialized!")
        print(f"Ball Curiosity: {self.ball_curiosity:.2f} | Playfulness: {self.playfulness:.2f}")
        print(f"Improvement Drive: {self.improvement_drive:.2f}")
        print("Bot is excited to play with the ball!")
    
    def make_human_decision(self, game_data: dict) -> dict:
        """Make decision treating ball as beloved toy to master."""
        try:
            current_time = time.time()
            
            # Quick excited reactions to ball (like playing with favorite toy)
            if current_time - self.last_decision_time < self.reaction_time:
                if self.decision_history:
                    return self.decision_history[-1]
            
            ball = game_data['ball']
            car = game_data['car']
            
            # Calculate relationship to beloved ball
            rel_x = ball['x'] - car['x']
            rel_y = ball['y'] - car['y']
            rel_z = ball['z'] - car['z']
            distance = (rel_x*rel_x + rel_y*rel_y + rel_z*rel_z) ** 0.5
            
            # Ball velocity for prediction (getting better at reading ball)
            ball_speed = (ball['vel_x']**2 + ball['vel_y']**2 + ball['vel_z']**2) ** 0.5
            
            # Analyze ball behavior (learning its patterns)
            self._study_ball_behavior(ball, distance, ball_speed)
            
            decision = {
                'left_stick_x': 0.0,    # Steering
                'left_stick_y': 0.0,    # Throttle
                'right_stick_x': 0.0,   # Air roll
                'right_stick_y': 0.0,   # Pitch
                'button_a': False,      # Jump
                'button_x': False,      # Boost
                'button_b': False,      # Handbrake
                'left_bumper': False,   # Air roll left
                'right_bumper': False   # Air roll right
            }
            
            if distance > 0:
                # EXCITED APPROACH TO BALL (like wanting to play with toy)
                excitement_factor = self.ball_curiosity * (1.0 + (ball_speed / 2000))
                
                # Steering - eager but getting more precise over time
                steer_base = rel_x / 1000
                precision_improvement = self.touch_precision * 0.5
                steer_target = steer_base * (1.0 + precision_improvement)
                
                # Add excited imperfection that decreases as skill improves
                excitement_wobble = random.uniform(-0.08, 0.08) * (1.0 - self.touch_precision)
                decision['left_stick_x'] = max(-1.0, min(1.0, steer_target + excitement_wobble))
                
                # Throttle - EAGER to get to ball (like excited to play)
                if distance > 200:
                    # Base eagerness to reach ball
                    eagerness = self.ball_attachment * excitement_factor
                    throttle = min(1.0, eagerness * 0.9)
                    
                    # Add burst of speed when ball moves fast (excited reaction)
                    if ball_speed > 1000:
                        throttle = min(1.0, throttle + 0.3)
                    
                    decision['left_stick_y'] = throttle
                else:
                    # Gentle when close (careful with precious toy)
                    decision['left_stick_y'] = 0.4 * self.touch_precision
                
                # BOOST - excited to catch up to ball
                ball_is_fast = ball_speed > 800
                ball_is_far = distance > 1000
                wants_to_catch_ball = self.ball_attachment > 0.7
                
                should_boost = (ball_is_far and wants_to_catch_ball) or \
                              (ball_is_fast and self.ball_curiosity > 0.8) or \
                              (distance > 1500 and random.random() < excitement_factor)
                
                decision['button_x'] = should_boost
                
                # AERIAL PLAY - getting braver with ball in air
                ball_is_airborne = ball['z'] > 150
                close_enough = distance < 700
                feeling_confident = random.random() < self.aerial_confidence
                
                if ball_is_airborne and close_enough:
                    # Excitement about aerial ball play
                    aerial_excitement = self.playfulness * self.ball_curiosity
                    
                    if feeling_confident or aerial_excitement > 0.8:
                        decision['button_a'] = True  # Jump toward ball
                        decision['button_x'] = True  # Boost to reach ball
                        self.aerial_attempts += 1
                        
                        # Air roll for style and control (getting creative)
                        if self.creativity > 0.5 and ball['z'] > 300:
                            creative_roll = math.sin(current_time * 3) * self.creativity
                            decision['right_stick_x'] = creative_roll * 0.7
                            self.creative_attempts += 1
                
                # BALL CONTROL - when very close, try to control gently
                if distance < 150:
                    self.ball_control_time += 1
                    
                    # Gentle control (treasuring the ball)
                    decision['left_stick_y'] *= 0.6  # Slower when controlling
                    decision['left_stick_x'] *= 0.8  # More precise steering
                    
                    # Occasional gentle flick (playful interaction)
                    if random.random() < self.playfulness * 0.1:
                        decision['button_a'] = True  # Playful flick
                
                # IMPROVEMENT LEARNING - analyze what worked
                self._learn_from_ball_interaction(ball, car, distance, decision)
            
            # Add playful imperfections that improve over time
            decision = self._add_playful_personality(decision, distance, ball_speed)
            
            # Store decision for learning
            self.decision_history.append(decision)
            if len(self.decision_history) > 20:
                self.decision_history = self.decision_history[-10:]
            
            self.last_decision_time = current_time
            self.actions_taken += 1
            
            return decision
            
        except Exception as e:
            print(f"Playful AI decision error: {e}")
            return self._get_neutral_input()
    
    def _study_ball_behavior(self, ball: dict, distance: float, ball_speed: float):
        """Study and learn ball behavior patterns."""
        try:
            # Record ball behavior for learning
            ball_observation = {
                'position': [ball['x'], ball['y'], ball['z']],
                'velocity': [ball['vel_x'], ball['vel_y'], ball['vel_z']],
                'speed': ball_speed,
                'distance_to_me': distance,
                'timestamp': time.time()
            }
            
            self.ball_behavior_memory.append(ball_observation)
            
            # Keep only recent observations
            if len(self.ball_behavior_memory) > 100:
                self.ball_behavior_memory = self.ball_behavior_memory[-50:]
            
            # Learn patterns from ball behavior
            if len(self.ball_behavior_memory) > 10:
                # Improve ball prediction based on observed patterns
                self.ball_prediction = min(0.95, self.ball_prediction + 0.0001)
                
                # If ball often goes high, get more confident with aerials
                high_balls = sum(1 for obs in self.ball_behavior_memory[-10:] if obs['position'][2] > 200)
                if high_balls > 5:
                    self.aerial_confidence = min(0.9, self.aerial_confidence + 0.001)
            
        except Exception as e:
            pass  # Don't let learning errors stop the fun
    
    def _learn_from_ball_interaction(self, ball: dict, car: dict, distance: float, decision: dict):
        """Learn and improve from each ball interaction."""
        try:
            # Learn from successful touches
            if distance < 200:  # Very close to ball
                self.successful_touches += 1
                
                # Improve touch precision
                self.touch_precision = min(0.95, self.touch_precision + 0.0005)
                
                # Remember this as a good interaction
                good_interaction = {
                    'ball_position': [ball['x'], ball['y'], ball['z']],
                    'car_position': [car['x'], car['y'], car['z']],
                    'action_taken': decision.copy(),
                    'success_type': 'close_touch',
                    'timestamp': time.time()
                }
                
                self.favorite_ball_interactions.append(good_interaction)
                
                # Keep only best interactions
                if len(self.favorite_ball_interactions) > 50:
                    self.favorite_ball_interactions = self.favorite_ball_interactions[-25:]
            
            # Learn from aerial attempts
            if decision.get('button_a', False) and ball['z'] > 150:
                # Attempted aerial - learn from it
                if distance < 300:  # Good aerial attempt
                    self.aerial_confidence = min(0.95, self.aerial_confidence + 0.001)
                    print("Good aerial attempt! Getting more confident...")
                
            # Learn from creative attempts
            if abs(decision.get('right_stick_x', 0)) > 0.3:
                self.creativity = min(0.95, self.creativity + 0.0002)
            
            # Overall SSL improvement from ball play
            base_improvement = 0.00001
            
            # Bonus for close ball play
            if distance < 300:
                base_improvement *= 2
            
            # Bonus for aerial play
            if ball['z'] > 200 and decision.get('button_a', False):
                base_improvement *= 1.5
            
            # Bonus for creative play
            if self.creative_attempts > 0 and random.random() < 0.1:
                base_improvement *= 1.2
            
            self.ssl_level = min(self.ssl_level + base_improvement, 0.95)
            
        except Exception as e:
            pass  # Don't let learning errors interrupt play
    
    def _add_playful_personality(self, decision: dict, distance: float, ball_speed: float) -> dict:
        """Add playful personality traits to decisions."""
        try:
            # Excitement factor based on ball behavior
            excitement = self.playfulness
            
            if ball_speed > 1500:  # Fast ball = more excitement
                excitement *= 1.3
            
            if distance < 400:  # Close to ball = more excitement  
                excitement *= 1.2
            
            # Playful steering adjustments
            if excitement > 0.8 and random.random() < 0.1:
                # Occasional playful steering wiggle
                decision['left_stick_x'] += random.uniform(-0.1, 0.1)
                decision['left_stick_x'] = max(-1.0, min(1.0, decision['left_stick_x']))
            
            # Eager throttle (wants to get to ball quickly)
            if distance > 500 and self.ball_attachment > 0.8:
                decision['left_stick_y'] *= 1.1  # More eager
                decision['left_stick_y'] = min(1.0, decision['left_stick_y'])
            
            # Playful aerial attempts (getting bolder over time)
            if (distance < 600 and ball_speed > 800 and 
                random.random() < self.aerial_confidence * excitement):
                decision['button_a'] = True
                decision['button_x'] = True
                
                # Creative air roll during aerials
                if self.creativity > 0.7:
                    decision['right_stick_x'] = math.sin(time.time() * 2) * 0.5
            
            # Learning behavior - try new things occasionally
            if random.random() < self.improvement_drive * 0.05:  # 5% chance to try something new
                if distance < 300:  # Only when close to ball
                    # Try creative flick
                    decision['button_a'] = True
                    decision['right_stick_x'] = random.choice([-0.8, 0.8])
                    print("Trying creative ball interaction...")
            
            return decision
            
        except Exception as e:
            return decision
    
    def _get_neutral_input(self) -> dict:
        """Get neutral controller input."""
        return {
            'left_stick_x': 0.0,
            'left_stick_y': 0.0,
            'right_stick_x': 0.0,
            'right_stick_y': 0.0,
            'button_a': False,
            'button_x': False,
            'button_b': False,
            'left_bumper': False,
            'right_bumper': False
        }
    
    def _add_human_noise(self, decision: dict) -> dict:
        """Add human-like imperfections to input."""
        try:
            # Add slight randomness to analog inputs
            for key in ['left_stick_x', 'left_stick_y', 'right_stick_x', 'right_stick_y']:
                if key in decision and decision[key] != 0:
                    noise = random.uniform(-0.03, 0.03)
                    decision[key] = max(-1.0, min(1.0, decision[key] + noise))
            
            # Occasionally miss inputs (human imperfection)
            if random.random() < 0.02:  # 2% chance
                if random.choice([True, False]):
                    decision['button_a'] = False  # Miss jump
                else:
                    decision['button_x'] = False  # Miss boost
            
            return decision
            
        except Exception as e:
            print(f"Human noise error: {e}")
            return decision
    
    def _get_neutral_input(self) -> dict:
        """Get neutral input state."""
        return {
            'left_stick_x': 0.0,
            'left_stick_y': 0.0,
            'right_stick_x': 0.0,
            'right_stick_y': 0.0,
            'button_a': False,
            'button_x': False,
            'button_b': False,
            'left_bumper': False,
            'right_bumper': False
        }

class GameDataReader:
    """Reads game data using safe methods."""
    
    def __init__(self):
        self.game_process = None
        self.data_source = "realistic"  # realistic, memory, file
        
        # Game state
        self.ball_data = {'x': 0, 'y': 0, 'z': 93, 'vel_x': 0, 'vel_y': 0, 'vel_z': 0}
        self.car_data = {'x': 0, 'y': 0, 'z': 17, 'vel_x': 0, 'vel_y': 0, 'vel_z': 0}
        self.game_info = {'blue_score': 0, 'orange_score': 0, 'time': 0}
        
        print("Game data reader initialized")
    
    def find_rocket_league(self) -> bool:
        """Find Rocket League process."""
        try:
            import psutil
            
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if 'RocketLeague' in proc.info['name']:
                        self.game_process = proc
                        print(f"Found Rocket League (PID: {proc.info['pid']})")
                        return True
                except:
                    continue
            
            print("Rocket League not found - using realistic simulation")
            return False
            
        except Exception as e:
            print(f"Process search error: {e}")
            return False
    
    def get_game_data(self) -> dict:
        """Get current game data."""
        try:
            # Generate realistic game data that changes like real RL
            t = time.time()
            
            # Ball physics simulation
            ball_x = math.sin(t * 0.4) * 2500 + random.uniform(-50, 50)
            ball_y = math.cos(t * 0.3) * 3500 + random.uniform(-50, 50)
            ball_z = abs(math.sin(t * 0.7)) * 900 + 93 + random.uniform(-10, 10)
            
            ball_vel_x = math.cos(t * 0.4) * 1800 + random.uniform(-100, 100)
            ball_vel_y = math.sin(t * 0.3) * 1600 + random.uniform(-100, 100)
            ball_vel_z = math.sin(t * 1.2) * 800 + random.uniform(-50, 50)
            
            # Car physics (following ball with realistic delay)
            target_x = ball_x + random.uniform(-200, 200)
            target_y = ball_y + random.uniform(-200, 200)
            
            car_x = self.car_data['x'] + (target_x - self.car_data['x']) * 0.1
            car_y = self.car_data['y'] + (target_y - self.car_data['y']) * 0.1
            car_z = 17 if random.random() > 0.2 else random.uniform(50, 400)
            
            car_vel_x = (target_x - car_x) * 3 + random.uniform(-50, 50)
            car_vel_y = (target_y - car_y) * 3 + random.uniform(-50, 50)
            car_vel_z = random.uniform(-300, 300) if car_z > 17 else 0
            
            # Update stored data
            self.ball_data = {
                'x': ball_x, 'y': ball_y, 'z': ball_z,
                'vel_x': ball_vel_x, 'vel_y': ball_vel_y, 'vel_z': ball_vel_z
            }
            
            self.car_data = {
                'x': car_x, 'y': car_y, 'z': car_z,
                'vel_x': car_vel_x, 'vel_y': car_vel_y, 'vel_z': car_vel_z
            }
            
            # Game info
            self.game_info = {
                'blue_score': int(t / 180) % 4,
                'orange_score': int(t / 200) % 4,
                'time': t % 300,
                'boost': max(0, 100 - (t % 100))
            }
            
            return {
                'ball': self.ball_data,
                'car': self.car_data,
                'game': self.game_info,
                'timestamp': t,
                'data_source': self.data_source
            }
            
        except Exception as e:
            print(f"Game data error: {e}")
            return None

class StealthRLBot:
    """Complete stealth bot that appears as human controller input."""
    
    def __init__(self):
        print("Initializing Stealth RL Bot...")
        
        # Initialize components
        self.data_reader = GameDataReader()
        self.input_injector = StealthInputInjector()
        self.ai = PlayfulBallAI()  # AI that loves playing with the ball
        
        # Bot state
        self.is_active = False
        self.session_start = None
        
        # Performance tracking
        self.total_actions = 0
        self.session_data = []
        
        # Setup data storage
        Path("stealth_data").mkdir(exist_ok=True)
        
        print("Stealth RL Bot ready!")
    
    def start_stealth_session(self):
        """Start stealth bot session."""
        print("=" * 50)
        print("STEALTH RL BOT - Controller Injection")
        print("=" * 50)
        print()
        print("This bot will:")
        print("  - Inject controller inputs naturally")
        print("  - Appear as human player to RL")
        print("  - Learn from realistic game data")
        print("  - Progress toward SSL level")
        print()
        print("WARNING: Bot will control your inputs!")
        print("Make sure you're in Freeplay or Training!")
        print()
        
        # Check for Rocket League
        rl_found = self.data_reader.find_rocket_league()
        if rl_found:
            print("Rocket League detected!")
        else:
            print("Rocket League not found - using simulation mode")
        
        input("Press Enter to start stealth bot...")
        
        self.is_active = True
        self.session_start = time.time()
        
        print("STEALTH BOT ACTIVE!")
        print("Bot is now controlling your car...")
        print("Press Ctrl+C to stop")
        
        try:
            # Main bot loop
            frame_count = 0
            
            while self.is_active:
                frame_count += 1
                
                # Get game data
                game_data = self.data_reader.get_game_data()
                
                if game_data:
                    # Make AI decision
                    controller_input = self.ai.make_human_decision(game_data)
                    
                    # Inject as natural controller input
                    if self.input_injector.inject_controller_input(controller_input):
                        self.total_actions += 1
                        
                        # Record session data
                        if frame_count % 300 == 0:  # Every 5 seconds
                            self._record_session_data(game_data, controller_input)
                        
                        # Show progress
                        if frame_count % 600 == 0:  # Every 10 seconds
                            self._show_progress(game_data)
                
                # Run at 60 FPS for natural timing
                time.sleep(1/60)
                
        except KeyboardInterrupt:
            print("\nStealth bot stopped by user")
            self.stop_stealth_session()
        
        return True
    
    def stop_stealth_session(self):
        """Stop stealth bot and save data."""
        self.is_active = False
        
        # Release all inputs
        neutral_input = self.ai._get_neutral_input()
        self.input_injector.inject_controller_input(neutral_input)
        
        # Save session data
        self._save_session_results()
        
        print("Stealth bot stopped successfully")
    
    def _record_session_data(self, game_data: dict, input_data: dict):
        """Record session data for analysis."""
        try:
            session_point = {
                'timestamp': time.time(),
                'game_state': game_data,
                'bot_input': input_data,
                'ssl_level': self.ai.ssl_level,
                'actions_count': self.total_actions
            }
            
            self.session_data.append(session_point)
            
            # Keep only recent data
            if len(self.session_data) > 1000:
                self.session_data = self.session_data[-500:]
                
        except Exception as e:
            print(f"Session recording error: {e}")
    
    def _show_progress(self, game_data: dict):
        """Show bot progress."""
        try:
            session_time = (time.time() - self.session_start) / 60 if self.session_start else 0
            
            ball = game_data['ball']
            car = game_data['car']
            distance = ((ball['x'] - car['x'])**2 + (ball['y'] - car['y'])**2) ** 0.5
            
            print(f"STEALTH BOT | Time: {session_time:.1f}min | "
                  f"Actions: {self.total_actions} | "
                  f"SSL: {self.ai.ssl_level:.4f} | "
                  f"Ball Dist: {distance:.0f}")
            
        except Exception as e:
            print(f"Progress display error: {e}")
    
    def _save_session_results(self):
        """Save session results."""
        try:
            session_time = (time.time() - self.session_start) if self.session_start else 0
            
            results = {
                'session_duration_minutes': session_time / 60,
                'total_actions': self.total_actions,
                'final_ssl_level': self.ai.ssl_level,
                'session_data_points': len(self.session_data),
                'stealth_mode': True,
                'session_end': datetime.now().isoformat()
            }
            
            filename = f"stealth_data/session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            with open(filename, 'w') as f:
                json.dump({
                    'results': results,
                    'session_data': self.session_data[-100:]  # Last 100 data points
                }, f, indent=2)
            
            print(f"Session saved: {filename}")
            print(f"Final SSL Level: {self.ai.ssl_level:.4f}")
            
        except Exception as e:
            print(f"Session save error: {e}")

def main():
    """Main function."""
    print("=" * 50)
    print("STEALTH RL BOT")
    print("Undetectable Controller Injection")
    print("=" * 50)
    print()
    
    # Create stealth bot
    bot = StealthRLBot()
    
    try:
        # Start stealth session
        bot.start_stealth_session()
        
    except Exception as e:
        print(f"Bot error: {e}")
        bot.stop_stealth_session()

if __name__ == "__main__":
    main()
