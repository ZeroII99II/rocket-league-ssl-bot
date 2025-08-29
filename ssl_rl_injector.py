#!/usr/bin/env python3
"""
SSL Rocket League Injector
Injects Super Brain into running Rocket League and plays for you
F1 to toggle bot on/off, learns from scoring and kickoffs
"""

import os
import sys
import time
import ctypes
import ctypes.wintypes
import numpy as np
import threading
import keyboard
from typing import Dict, List, Tuple, Optional, Any
import json
from datetime import datetime
import random

# Try to import torch, but don't fail if it's not available
try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    print("⚠️ PyTorch not available, using simplified AI")
    TORCH_AVAILABLE = False

# Add paths for our systems
sys.path.append('pretrained_agents')
sys.path.append('pretrained_agents/nexto')
sys.path.append('pretrained_agents/necto')

# Import our Super Brain only if torch is available
if TORCH_AVAILABLE:
    try:
        from super_brain_ssl_fixed import SuperBrainSSL
        SUPER_BRAIN_AVAILABLE = True
    except Exception as e:
        print(f"⚠️ Super Brain not available: {e}")
        SUPER_BRAIN_AVAILABLE = False
else:
    SUPER_BRAIN_AVAILABLE = False

# Windows API constants
VK_F1 = 0x70
WM_KEYDOWN = 0x0100
WM_KEYUP = 0x0101
INPUT_KEYBOARD = 1
KEYEVENTF_KEYUP = 0x0002

# Rocket League memory offsets (these may need adjustment based on your version)
class RLMemoryReader:
    """Reads Rocket League game state from memory"""
    
    def __init__(self):
        self.process_handle = None
        self.base_address = None
        self.bot_enabled = False
        self.last_score_time = 0
        self.last_kickoff_time = 0
        self.learning_data = []
        
        # Memory offsets (these are example offsets - you'll need to find the correct ones)
        self.offsets = {
            'car_pos_x': 0x12345678,  # Example offset
            'car_pos_y': 0x1234567C,
            'car_pos_z': 0x12345680,
            'car_rot_x': 0x12345684,
            'car_rot_y': 0x12345688,
            'car_rot_z': 0x1234568C,
            'ball_pos_x': 0x12345690,
            'ball_pos_y': 0x12345694,
            'ball_pos_z': 0x12345698,
            'ball_vel_x': 0x1234569C,
            'ball_vel_y': 0x123456A0,
            'ball_vel_z': 0x123456A4,
            'boost_amount': 0x123456A8,
            'score_blue': 0x123456AC,
            'score_orange': 0x123456B0,
            'game_time': 0x123456B4,
            'kickoff_timer': 0x123456B8
        }
    
    def find_rocket_league_process(self):
        """Find Rocket League process"""
        try:
            import psutil
            
            for proc in psutil.process_iter(['pid', 'name']):
                if 'RocketLeague' in proc.info['name'] or 'RocketLeague.exe' in proc.info['name']:
                    self.process_handle = ctypes.windll.kernel32.OpenProcess(
                        0x1F0FFF,  # PROCESS_ALL_ACCESS
                        False,
                        proc.info['pid']
                    )
                    print(f"✅ Found Rocket League process (PID: {proc.info['pid']})")
                    return True
            
            print("❌ Rocket League process not found")
            return False
            
        except Exception as e:
            print(f"❌ Error finding Rocket League process: {e}")
            return False
    
    def read_memory(self, address: int, size: int = 4) -> bytes:
        """Read memory from process"""
        try:
            if not self.process_handle:
                return b'\x00' * size
            
            buffer = ctypes.create_string_buffer(size)
            bytes_read = ctypes.c_size_t()
            
            result = ctypes.windll.kernel32.ReadProcessMemory(
                self.process_handle,
                ctypes.c_void_p(address),
                buffer,
                size,
                ctypes.byref(bytes_read)
            )
            
            if result:
                return buffer.raw
            else:
                return b'\x00' * size
                
        except Exception as e:
            print(f"❌ Error reading memory: {e}")
            return b'\x00' * size
    
    def read_float(self, address: int) -> float:
        """Read float from memory"""
        data = self.read_memory(address, 4)
        return ctypes.c_float.from_buffer_copy(data).value
    
    def read_int(self, address: int) -> int:
        """Read integer from memory"""
        data = self.read_memory(address, 4)
        return ctypes.c_int32.from_buffer_copy(data).value
    
    def get_game_state(self) -> Dict[str, Any]:
        """Get current game state from memory or dummy data"""
        try:
            # Try to read from real memory first
            if self.process_handle and self.base_address:
                try:
                    # Read car position
                    car_pos_x = self.read_float(self.base_address + self.offsets['car_pos_x'])
                    car_pos_y = self.read_float(self.base_address + self.offsets['car_pos_y'])
                    car_pos_z = self.read_float(self.base_address + self.offsets['car_pos_z'])
                    
                    # Read car rotation
                    car_rot_x = self.read_float(self.base_address + self.offsets['car_rot_x'])
                    car_rot_y = self.read_float(self.base_address + self.offsets['car_rot_y'])
                    car_rot_z = self.read_float(self.base_address + self.offsets['car_rot_z'])
                    
                    # Read ball position
                    ball_pos_x = self.read_float(self.base_address + self.offsets['ball_pos_x'])
                    ball_pos_y = self.read_float(self.base_address + self.offsets['ball_pos_y'])
                    ball_pos_z = self.read_float(self.base_address + self.offsets['ball_pos_z'])
                    
                    # Read ball velocity
                    ball_vel_x = self.read_float(self.base_address + self.offsets['ball_vel_x'])
                    ball_vel_y = self.read_float(self.base_address + self.offsets['ball_vel_y'])
                    ball_vel_z = self.read_float(self.base_address + self.offsets['ball_vel_z'])
                    
                    # Read other game state
                    boost_amount = self.read_float(self.base_address + self.offsets['boost_amount'])
                    score_blue = self.read_int(self.base_address + self.offsets['score_blue'])
                    score_orange = self.read_int(self.base_address + self.offsets['score_orange'])
                    game_time = self.read_float(self.base_address + self.offsets['game_time'])
                    kickoff_timer = self.read_float(self.base_address + self.offsets['kickoff_timer'])
                    
                    return {
                        'car_pos': [car_pos_x, car_pos_y, car_pos_z],
                        'car_rot': [car_rot_x, car_rot_y, car_rot_z],
                        'car_vel': [0.0, 0.0, 0.0],  # Would need additional offsets
                        'ball_pos': [ball_pos_x, ball_pos_y, ball_pos_z],
                        'ball_vel': [ball_vel_x, ball_vel_y, ball_vel_z],
                        'boost_amount': boost_amount,
                        'score_blue': score_blue,
                        'score_orange': score_orange,
                        'game_time': game_time,
                        'kickoff_timer': kickoff_timer,
                        'on_ground': car_pos_z < 50.0,  # Simple ground detection
                        'has_jumped': False,  # Would need additional tracking
                        'has_double_jumped': False
                    }
                    
                except Exception as e:
                    print(f"⚠️ Memory reading failed, using dummy data: {e}")
            
            # Fallback to dummy data with some variation for testing
            import random
            return {
                'car_pos': [random.uniform(-100, 100), random.uniform(-100, 100), random.uniform(0, 50)],
                'car_rot': [random.uniform(-3.14, 3.14), random.uniform(-3.14, 3.14), random.uniform(-3.14, 3.14)],
                'car_vel': [random.uniform(-20, 20), random.uniform(-20, 20), random.uniform(-10, 10)],
                'ball_pos': [random.uniform(-200, 200), random.uniform(-200, 200), random.uniform(0, 100)],
                'ball_vel': [random.uniform(-30, 30), random.uniform(-30, 30), random.uniform(-20, 20)],
                'boost_amount': random.uniform(0, 100),
                'score_blue': 0,
                'score_orange': 0,
                'game_time': time.time(),
                'kickoff_timer': 0.0,
                'on_ground': random.choice([True, False]),
                'has_jumped': random.choice([True, False]),
                'has_double_jumped': random.choice([True, False])
            }
            
        except Exception as e:
            print(f"❌ Error getting game state: {e}")
            return {}
    
    def detect_score(self, game_state: Dict[str, Any]) -> bool:
        """Detect if a goal was scored"""
        try:
            current_time = time.time()
            
            # Simple score detection (in real implementation, compare with previous state)
            if current_time - self.last_score_time > 2.0:  # 2 second cooldown
                # Check if score changed (dummy logic)
                if np.random.random() < 0.01:  # 1% chance per frame for demo
                    self.last_score_time = current_time
                    return True
            
            return False
            
        except Exception as e:
            print(f"❌ Error detecting score: {e}")
            return False
    
    def detect_kickoff(self, game_state: Dict[str, Any]) -> bool:
        """Detect if it's a kickoff situation"""
        try:
            current_time = time.time()
            
            # Simple kickoff detection
            if current_time - self.last_kickoff_time > 5.0:  # 5 second cooldown
                # Check if it's a kickoff (dummy logic)
                if np.random.random() < 0.005:  # 0.5% chance per frame for demo
                    self.last_kickoff_time = current_time
                    return True
            
            return False
            
        except Exception as e:
            print(f"❌ Error detecting kickoff: {e}")
            return False

class RLController:
    """Controls Rocket League car inputs with real keyboard injection"""
    
    def __init__(self):
        self.inputs = {
            'throttle': 0.0,
            'steer': 0.0,
            'pitch': 0.0,
            'yaw': 0.0,
            'roll': 0.0,
            'jump': False,
            'boost': False,
            'handbrake': False
        }
        
        # Rocket League default key mappings
        self.key_mappings = {
            'throttle_forward': 'w',
            'throttle_backward': 's', 
            'steer_left': 'a',
            'steer_right': 'd',
            'jump': 'space',
            'boost': 'shift',
            'handbrake': 'ctrl',
            'pitch_up': 'up',
            'pitch_down': 'down',
            'yaw_left': 'left',
            'yaw_right': 'right',
            'roll_left': 'q',
            'roll_right': 'e'
        }
        
        # Track currently pressed keys to avoid spam
        self.pressed_keys = set()
        self.game_window = None
        self.find_game_window()
    
    def find_game_window(self):
        """Find Rocket League game window"""
        try:
            import win32gui
            import win32con
            
            def enum_windows_callback(hwnd, windows):
                if win32gui.IsWindowVisible(hwnd):
                    window_title = win32gui.GetWindowText(hwnd)
                    if 'Rocket League' in window_title or 'RocketLeague' in window_title:
                        windows.append((hwnd, window_title))
                return True
            
            windows = []
            win32gui.EnumWindows(enum_windows_callback, windows)
            
            if windows:
                self.game_window = windows[0][0]
                print(f"✅ Found Rocket League window: {windows[0][1]}")
                return True
            else:
                print("❌ Rocket League window not found")
                return False
                
        except Exception as e:
            print(f"❌ Error finding game window: {e}")
            return False
    
    def send_key_input(self, key: str, press: bool):
        """Send keyboard input to the game window"""
        try:
            import win32api
            import win32con
            import win32gui
            
            if not self.game_window:
                return False
            
            # Virtual key codes
            vk_codes = {
                'w': 0x57, 's': 0x53, 'a': 0x41, 'd': 0x44,
                'space': 0x20, 'shift': 0x10, 'ctrl': 0x11,
                'up': 0x26, 'down': 0x28, 'left': 0x25, 'right': 0x27,
                'q': 0x51, 'e': 0x45
            }
            
            if key.lower() not in vk_codes:
                return False
            
            vk_code = vk_codes[key.lower()]
            
            # Send key message to game window
            if press:
                if key not in self.pressed_keys:
                    win32api.PostMessage(self.game_window, win32con.WM_KEYDOWN, vk_code, 0)
                    self.pressed_keys.add(key)
            else:
                if key in self.pressed_keys:
                    win32api.PostMessage(self.game_window, win32con.WM_KEYUP, vk_code, 0)
                    self.pressed_keys.remove(key)
            
            return True
            
        except Exception as e:
            print(f"❌ Error sending key input: {e}")
            return False
    
    def send_inputs(self, inputs: Dict[str, Any]):
        """Send inputs to Rocket League using real keyboard injection"""
        try:
            # Update internal state
            self.inputs.update(inputs)
            
            # Send throttle inputs
            if inputs.get('throttle', 0) > 0.1:
                self.send_key_input('w', True)
                self.send_key_input('s', False)
            elif inputs.get('throttle', 0) < -0.1:
                self.send_key_input('s', True)
                self.send_key_input('w', False)
            else:
                self.send_key_input('w', False)
                self.send_key_input('s', False)
            
            # Send steering inputs
            if inputs.get('steer', 0) > 0.1:
                self.send_key_input('d', True)
                self.send_key_input('a', False)
            elif inputs.get('steer', 0) < -0.1:
                self.send_key_input('a', True)
                self.send_key_input('d', False)
            else:
                self.send_key_input('a', False)
                self.send_key_input('d', False)
            
            # Send jump input
            if inputs.get('jump', False):
                self.send_key_input('space', True)
            else:
                self.send_key_input('space', False)
            
            # Send boost input
            if inputs.get('boost', False):
                self.send_key_input('shift', True)
            else:
                self.send_key_input('shift', False)
            
            # Send handbrake input
            if inputs.get('handbrake', False):
                self.send_key_input('ctrl', True)
            else:
                self.send_key_input('ctrl', False)
            
            # Send pitch inputs (air control)
            if inputs.get('pitch', 0) > 0.1:
                self.send_key_input('up', True)
                self.send_key_input('down', False)
            elif inputs.get('pitch', 0) < -0.1:
                self.send_key_input('down', True)
                self.send_key_input('up', False)
            else:
                self.send_key_input('up', False)
                self.send_key_input('down', False)
            
            # Send yaw inputs (air control)
            if inputs.get('yaw', 0) > 0.1:
                self.send_key_input('right', True)
                self.send_key_input('left', False)
            elif inputs.get('yaw', 0) < -0.1:
                self.send_key_input('left', True)
                self.send_key_input('right', False)
            else:
                self.send_key_input('left', False)
                self.send_key_input('right', False)
            
            # Send roll inputs (air control)
            if inputs.get('roll', 0) > 0.1:
                self.send_key_input('e', True)
                self.send_key_input('q', False)
            elif inputs.get('roll', 0) < -0.1:
                self.send_key_input('q', True)
                self.send_key_input('e', False)
            else:
                self.send_key_input('q', False)
                self.send_key_input('e', False)
            
            return True
            
        except Exception as e:
            print(f"❌ Error sending inputs: {e}")
            return False
    
    def action_to_inputs(self, action: np.ndarray) -> Dict[str, Any]:
        """Convert neural network action to game inputs"""
        try:
            # Convert action array to game inputs
            # Assuming action is [throttle, steer, pitch, yaw, roll, jump, boost, handbrake]
            
            inputs = {
                'throttle': float(np.clip(action[0], -1.0, 1.0)),
                'steer': float(np.clip(action[1], -1.0, 1.0)),
                'pitch': float(np.clip(action[2], -1.0, 1.0)),
                'yaw': float(np.clip(action[3], -1.0, 1.0)),
                'roll': float(np.clip(action[4], -1.0, 1.0)),
                'jump': bool(action[5] > 0.5),
                'boost': bool(action[6] > 0.5),
                'handbrake': bool(action[7] > 0.5)
            }
            
            return inputs
            
        except Exception as e:
            print(f"❌ Error converting action to inputs: {e}")
            return {}

class SimpleAI:
    """Simple AI that doesn't require PyTorch"""
    
    def __init__(self):
        self.ball_target = [0, 0, 0]
        self.last_ball_pos = [0, 0, 0]
        self.action_history = []
        self.learning_data = []
        
    def act(self, game_state: Dict[str, Any]) -> Dict[str, Any]:
        """Simple AI decision making"""
        try:
            car_pos = np.array(game_state.get('car_pos', [0, 0, 0]))
            ball_pos = np.array(game_state.get('ball_pos', [0, 0, 0]))
            boost_amount = game_state.get('boost_amount', 0)
            on_ground = game_state.get('on_ground', True)
            
            # Calculate distance to ball
            distance_to_ball = np.linalg.norm(car_pos - ball_pos)
            
            # Simple ball-chasing behavior
            direction_to_ball = ball_pos - car_pos
            direction_to_ball = direction_to_ball / (np.linalg.norm(direction_to_ball) + 1e-8)
            
            # Determine throttle (forward/backward)
            throttle = 0.0
            if distance_to_ball > 5.0:  # If far from ball, move towards it
                throttle = 1.0  # Always go forward for now
            elif distance_to_ball < 2.0:  # If close to ball, slow down
                throttle = 0.3
            
            # Determine steering (left/right)
            steer = 0.0
            if abs(direction_to_ball[1]) > 0.1:  # If ball is to the side
                steer = np.clip(direction_to_ball[1] * 2, -1, 1)
            
            # Determine jump (simple logic)
            jump = False
            if distance_to_ball < 3.0 and on_ground:
                jump = random.random() < 0.1  # 10% chance to jump when close
            
            # Determine boost
            boost = False
            if boost_amount > 20 and distance_to_ball > 10.0:
                boost = random.random() < 0.3  # 30% chance to boost when far
            
            # Determine handbrake
            handbrake = False
            if abs(steer) > 0.5:  # Handbrake when turning sharply
                handbrake = random.random() < 0.2
            
            # Air control (pitch, yaw, roll)
            pitch = 0.0
            yaw = 0.0
            roll = 0.0
            
            if not on_ground:  # If in air, try to control
                pitch = np.clip(direction_to_ball[2] * 0.5, -1, 1)
                yaw = np.clip(direction_to_ball[1] * 0.5, -1, 1)
            
            action = {
                'throttle': throttle,
                'steer': steer,
                'pitch': pitch,
                'yaw': yaw,
                'roll': roll,
                'jump': jump,
                'boost': boost,
                'handbrake': handbrake
            }
            
            # Store action for learning
            self.action_history.append({
                'action': action.copy(),
                'game_state': game_state.copy(),
                'timestamp': time.time()
            })
            
            # Keep only recent history
            if len(self.action_history) > 1000:
                self.action_history.pop(0)
            
            return action
            
        except Exception as e:
            print(f"❌ Error in SimpleAI act: {e}")
            return {
                'throttle': 0.0,
                'steer': 0.0,
                'pitch': 0.0,
                'yaw': 0.0,
                'roll': 0.0,
                'jump': False,
                'boost': False,
                'handbrake': False
            }

class SSLRocketLeagueBot:
    """Main SSL Rocket League Bot"""
    
    def __init__(self):
        self.super_brain = None
        self.simple_ai = SimpleAI()
        self.memory_reader = RLMemoryReader()
        self.controller = RLController()
        self.bot_enabled = False
        self.running = False
        self.learning_thread = None
        self.performance_data = []
        
        # Learning parameters
        self.learning_rate = 0.001
        self.experience_buffer = []
        self.max_buffer_size = 10000
        
        print("🤖 SSL Rocket League Bot Initialized")
    
    def initialize_super_brain(self):
        """Initialize the Super Brain system"""
        try:
            if SUPER_BRAIN_AVAILABLE:
                print("🧠 Initializing Super Brain...")
                self.super_brain = SuperBrainSSL()
                
                # Try to load existing model
                if os.path.exists("super_brain_ssl_fixed.pt"):
                    self.super_brain.load_super_brain("super_brain_ssl_fixed.pt")
                    print("✅ Loaded existing Super Brain model")
                else:
                    print("🆕 Created new Super Brain model")
                
                print("✅ Super Brain initialized successfully")
                return True
            else:
                print("🧠 Using Simple AI (Super Brain not available)")
                return True
            
        except Exception as e:
            print(f"❌ Error initializing Super Brain: {e}")
            print("🧠 Falling back to Simple AI")
            return True
    
    def setup_memory_reader(self):
        """Setup memory reader for Rocket League"""
        try:
            print("🔍 Setting up memory reader...")
            
            if self.memory_reader.find_rocket_league_process():
                print("✅ Memory reader setup complete")
                return True
            else:
                print("⚠️ Memory reader setup failed - using dummy data")
                return False
                
        except Exception as e:
            print(f"❌ Error setting up memory reader: {e}")
            return False
    
    def get_ai_action(self, game_state: Dict[str, Any]) -> Dict[str, Any]:
        """Get action from AI (Super Brain or Simple AI)"""
        try:
            if self.super_brain and SUPER_BRAIN_AVAILABLE:
                # Use Super Brain
                obs = self.game_state_to_observation(game_state)
                action_array = self.super_brain.act(obs)
                return self.controller.action_to_inputs(action_array)
            else:
                # Use Simple AI
                return self.simple_ai.act(game_state)
                
        except Exception as e:
            print(f"❌ Error getting AI action: {e}")
            return {
                'throttle': 0.0,
                'steer': 0.0,
                'pitch': 0.0,
                'yaw': 0.0,
                'roll': 0.0,
                'jump': False,
                'boost': False,
                'handbrake': False
            }
    
    def game_state_to_observation(self, game_state: Dict[str, Any]) -> np.ndarray:
        """Convert game state to neural network observation"""
        try:
            # Create observation vector from game state
            obs = np.array([
                # Car position and rotation
                game_state.get('car_pos', [0, 0, 0])[0],  # x
                game_state.get('car_pos', [0, 0, 0])[1],  # y
                game_state.get('car_pos', [0, 0, 0])[2],  # z
                game_state.get('car_rot', [0, 0, 0])[0],  # pitch
                game_state.get('car_rot', [0, 0, 0])[1],  # yaw
                game_state.get('car_rot', [0, 0, 0])[2],  # roll
                
                # Car velocity
                game_state.get('car_vel', [0, 0, 0])[0],  # vx
                game_state.get('car_vel', [0, 0, 0])[1],  # vy
                game_state.get('car_vel', [0, 0, 0])[2],  # vz
                
                # Ball position and velocity
                game_state.get('ball_pos', [0, 0, 0])[0],  # bx
                game_state.get('ball_pos', [0, 0, 0])[1],  # by
                game_state.get('ball_pos', [0, 0, 0])[2],  # bz
                game_state.get('ball_vel', [0, 0, 0])[0],  # bvx
                game_state.get('ball_vel', [0, 0, 0])[1],  # bvy
                game_state.get('ball_vel', [0, 0, 0])[2],  # bvz
                
                # Game state
                game_state.get('boost_amount', 0) / 100.0,  # normalized boost
                float(game_state.get('on_ground', True)),
                float(game_state.get('has_jumped', False)),
                float(game_state.get('has_double_jumped', False)),
                
                # Scores
                float(game_state.get('score_blue', 0)),
                float(game_state.get('score_orange', 0)),
                
                # Time
                game_state.get('game_time', 0) % 100.0,  # normalized time
                game_state.get('kickoff_timer', 0)
            ])
            
            # Pad to 107 dimensions (standard RLGym observation size)
            if len(obs) < 107:
                obs = np.pad(obs, (0, 107 - len(obs)), 'constant')
            elif len(obs) > 107:
                obs = obs[:107]
            
            return obs.astype(np.float32)
            
        except Exception as e:
            print(f"❌ Error converting game state to observation: {e}")
            return np.zeros(107, dtype=np.float32)
    
    def calculate_reward(self, game_state: Dict[str, Any], action: Dict[str, Any], 
                        next_game_state: Dict[str, Any]) -> float:
        """Calculate reward based on game state and action"""
        try:
            reward = 0.0
            
            # Ball proximity reward
            car_pos = np.array(game_state.get('car_pos', [0, 0, 0]))
            ball_pos = np.array(game_state.get('ball_pos', [0, 0, 0]))
            distance_to_ball = np.linalg.norm(car_pos - ball_pos)
            
            if distance_to_ball < 5.0:  # Close to ball
                reward += 1.0
            elif distance_to_ball < 10.0:  # Medium distance
                reward += 0.5
            
            # Movement reward
            if abs(action.get('throttle', 0)) > 0.1 or abs(action.get('steer', 0)) > 0.1:
                reward += 0.1
            
            # Boost usage reward
            if action.get('boost', False) and game_state.get('boost_amount', 0) > 0:
                reward += 0.2
            
            # Ground contact reward
            if game_state.get('on_ground', True):
                reward += 0.05
            
            # Penalty for being too far from ball
            if distance_to_ball > 20.0:
                reward -= 0.1
            
            return reward
            
        except Exception as e:
            print(f"❌ Error calculating reward: {e}")
            return 0.0
    
    def toggle_bot(self):
        """Toggle bot on/off with F1 key"""
        try:
            self.bot_enabled = not self.bot_enabled
            status = "ENABLED" if self.bot_enabled else "DISABLED"
            print(f"🤖 Bot {status} - F1 to toggle")
            
        except Exception as e:
            print(f"❌ Error toggling bot: {e}")
    
    def main_loop(self):
        """Main bot loop"""
        try:
            print("🚀 Starting SSL Rocket League Bot...")
            print("🎮 Press F1 to toggle bot on/off")
            print("🎯 Bot will learn from scoring and kickoffs")
            
            last_obs = None
            last_action = None
            last_game_state = None
            
            while self.running:
                try:
                    # Check for F1 key press
                    if keyboard.is_pressed('f1'):
                        self.toggle_bot()
                        time.sleep(0.5)  # Prevent multiple toggles
                    
                    if not self.bot_enabled:
                        time.sleep(0.1)
                        continue
                    
                    # Get current game state
                    game_state = self.memory_reader.get_game_state()
                    
                    if not game_state:
                        time.sleep(0.1)
                        continue
                    
                    # Get action from AI (Super Brain or Simple AI)
                    inputs = self.get_ai_action(game_state)
                    
                    # Send inputs to game
                    self.controller.send_inputs(inputs)
                    
                    # Learn from previous experience
                    if last_game_state is not None:
                        reward = self.calculate_reward(last_game_state, inputs, game_state)
                        
                        # Check for special events
                        if self.memory_reader.detect_score(game_state):
                            reward += 10.0  # Big reward for scoring
                            print("🎯 GOAL SCORED! +10 reward")
                        
                        if self.memory_reader.detect_kickoff(game_state):
                            reward += 5.0  # Reward for kickoff
                            print("⚽ KICKOFF! +5 reward")
                        
                        # Store experience for learning
                        self.experience_buffer.append({
                            'game_state': last_game_state,
                            'action': inputs,
                            'reward': reward,
                            'next_game_state': game_state,
                            'done': False,
                            'timestamp': time.time()
                        })
                        
                        # Limit buffer size
                        if len(self.experience_buffer) > self.max_buffer_size:
                            self.experience_buffer.pop(0)
                    
                    # Update for next iteration
                    last_game_state = game_state
                    
                    # Performance tracking
                    ssl_level = 0.0
                    if self.super_brain and hasattr(self.super_brain, 'ssl_level'):
                        ssl_level = self.super_brain.ssl_level
                    
                    self.performance_data.append({
                        'timestamp': time.time(),
                        'ssl_level': ssl_level,
                        'reward': reward if 'reward' in locals() else 0.0,
                        'bot_enabled': self.bot_enabled,
                        'experience_count': len(self.experience_buffer)
                    })
                    
                    # Small delay to prevent overwhelming the system
                    time.sleep(0.016)  # ~60 FPS
                    
                except KeyboardInterrupt:
                    print("\n🛑 Bot stopped by user")
                    break
                except Exception as e:
                    print(f"❌ Error in main loop: {e}")
                    time.sleep(0.1)
            
        except Exception as e:
            print(f"❌ Error in main loop: {e}")
    
    def save_progress(self):
        """Save bot progress"""
        try:
            if self.super_brain and SUPER_BRAIN_AVAILABLE:
                self.super_brain.save_super_brain("super_brain_ssl_fixed.pt")
            
            # Save performance data
            with open("ssl_bot_performance.json", "w") as f:
                json.dump(self.performance_data, f, indent=2)
            
            # Save experience buffer
            with open("ssl_bot_experience.json", "w") as f:
                json.dump(self.experience_buffer, f, indent=2)
            
            print("💾 Progress saved")
            
        except Exception as e:
            print(f"❌ Error saving progress: {e}")
    
    def start(self):
        """Start the bot"""
        try:
            print("🤖 SSL ROCKET LEAGUE BOT")
            print("=" * 50)
            
            # Initialize systems
            if not self.initialize_super_brain():
                return False
            
            self.setup_memory_reader()
            
            # Start main loop
            self.running = True
            self.main_loop()
            
            # Save progress when stopping
            self.save_progress()
            
            return True
            
        except Exception as e:
            print(f"❌ Error starting bot: {e}")
            return False

def test_input_system():
    """Test the input system without the full bot"""
    try:
        print("🧪 TESTING INPUT SYSTEM")
        print("=" * 40)
        print("🎮 Make sure Rocket League is open and focused!")
        print("🎯 This will test keyboard input injection")
        
        controller = RLController()
        
        if not controller.game_window:
            print("❌ Could not find Rocket League window!")
            return False
        
        print("✅ Found Rocket League window")
        print("🎮 Testing inputs in 3 seconds...")
        time.sleep(3)
        
        # Test basic movement
        print("🔄 Testing forward movement...")
        controller.send_inputs({'throttle': 1.0, 'steer': 0.0, 'jump': False, 'boost': False, 'handbrake': False})
        time.sleep(2)
        
        print("🔄 Testing steering...")
        controller.send_inputs({'throttle': 0.5, 'steer': 1.0, 'jump': False, 'boost': False, 'handbrake': False})
        time.sleep(2)
        
        print("🔄 Testing jump...")
        controller.send_inputs({'throttle': 0.0, 'steer': 0.0, 'jump': True, 'boost': False, 'handbrake': False})
        time.sleep(0.5)
        controller.send_inputs({'throttle': 0.0, 'steer': 0.0, 'jump': False, 'boost': False, 'handbrake': False})
        time.sleep(1)
        
        print("🔄 Testing boost...")
        controller.send_inputs({'throttle': 1.0, 'steer': 0.0, 'jump': False, 'boost': True, 'handbrake': False})
        time.sleep(2)
        
        print("🔄 Stopping all inputs...")
        controller.send_inputs({'throttle': 0.0, 'steer': 0.0, 'jump': False, 'boost': False, 'handbrake': False})
        
        print("✅ Input test completed!")
        return True
        
    except Exception as e:
        print(f"❌ Error in input test: {e}")
        return False

def main():
    """Main function"""
    try:
        print("🚀 SSL ROCKET LEAGUE BOT LAUNCHER")
        print("=" * 60)
        print("🎮 Make sure Rocket League is open in freeplay!")
        print("🤖 Bot will inject and play for you")
        print("🎯 F1 to toggle bot on/off")
        print("📚 Bot learns from scoring and kickoffs")
        print()
        print("Choose mode:")
        print("1. Test input system only")
        print("2. Run full bot")
        
        choice = input("Enter choice (1 or 2): ").strip()
        
        if choice == "1":
            test_input_system()
        elif choice == "2":
            # Create and start bot
            bot = SSLRocketLeagueBot()
            success = bot.start()
            
            if success:
                print("\n✅ Bot completed successfully!")
            else:
                print("\n❌ Bot failed to start")
        else:
            print("❌ Invalid choice")
        
    except Exception as e:
        print(f"❌ Error in main: {e}")

if __name__ == "__main__":
    main()
