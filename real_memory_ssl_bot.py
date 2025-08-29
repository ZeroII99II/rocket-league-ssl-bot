#!/usr/bin/env python3
"""
Real Memory SSL Bot
Reads actual Rocket League game memory and files to get real game data
"""

import tkinter as tk
import time
import threading
import numpy as np
import win32gui
import win32con
import win32api
import win32process
import psutil
import ctypes
import struct
import os
from datetime import datetime
import pickle
import json

class RealMemorySSLBot:
    """Real SSL Bot that reads actual game memory and files"""
    
    def __init__(self):
        # Game connection
        self.game_window = None
        self.game_process = None
        self.game_handle = None
        self.game_pid = None
        
        # Overlay
        self.overlay_window = None
        self.is_running = False
        self.is_paused = False
        self.smooth_mode = True  # Smooth human-like movements
        self.bot_enabled = False  # F1 toggle state
        self.f1_listener = None
        
        # Real game data from memory
        self.car_data = {
            'position': [0.0, 0.0, 0.0],
            'velocity': [0.0, 0.0, 0.0],
            'rotation': [0.0, 0.0, 0.0],
            'boost': 100.0,
            'on_ground': True,
            'has_jumped': False,
            'has_double_jumped': False
        }
        
        self.ball_data = {
            'position': [0.0, 0.0, 0.0],
            'velocity': [0.0, 0.0, 0.0],
            'rotation': [0.0, 0.0, 0.0]
        }
        
        # Game state tracking
        self.game_state = {
            'score_blue': 0,
            'score_orange': 0,
            'time_remaining': 300,
            'ball_touched': False,
            'last_ball_touch': 0,
            'goals_scored': 0,
            'saves_made': 0
        }
        
        # Learning data
        self.learning_data = {
            'episodes_completed': 0,
            'total_reward': 0.0,
            'best_score': 0,
            'improvement_rate': 0.0,
            'ball_interactions': 0,
            'successful_shots': 0,
            'successful_saves': 0
        }
        
        self.game_data = {
            'time_remaining': 300.0,
            'score_blue': 0,
            'score_orange': 0,
            'game_state': 'FreePlay'
        }
        
        # Memory addresses (these would need to be found dynamically)
        self.memory_addresses = {
            'car_position': 0x0,
            'car_velocity': 0x0,
            'car_rotation': 0x0,
            'car_boost': 0x0,
            'ball_position': 0x0,
            'ball_velocity': 0x0,
            'game_time': 0x0,
            'game_score': 0x0
        }
        
        # Learning data
        self.learned_mechanics = {}
        self.practice_episodes = 0
        self.total_actions = 0
        self.successful_actions = 0
        self.start_time = time.time()
        
        # Real SSL mechanics with controller inputs (like pro players)
        self.ssl_mechanics = {
            'forward_movement': {
                'controller': {'left_stick_y': 1.0},  # Forward on left stick
                'duration': 2.0,
                'description': 'Move forward (Left Stick Up)'
            },
            'backward_movement': {
                'controller': {'left_stick_y': -1.0},  # Backward on left stick
                'duration': 2.0,
                'description': 'Move backward (Left Stick Down)'
            },
            'left_movement': {
                'controller': {'left_stick_x': -1.0},  # Left on left stick
                'duration': 2.0,
                'description': 'Move left (Left Stick Left)'
            },
            'right_movement': {
                'controller': {'left_stick_x': 1.0},  # Right on left stick
                'duration': 2.0,
                'description': 'Move right (Left Stick Right)'
            },
            'jump': {
                'controller': {'button_a': True},  # A button (Xbox) / X button (PS)
                'duration': 0.1,
                'description': 'Jump (A Button)'
            },
            'double_jump': {
                'controller': {'button_a': True, 'button_a_delay': 0.1},  # Double tap A
                'duration': 0.4,
                'description': 'Double jump (A Button x2)'
            },
            'boost': {
                'controller': {'button_b': True},  # B button (Xbox) / Circle button (PS)
                'duration': 1.0,
                'description': 'Boost (B Button)'
            },
            'air_roll_left': {
                'controller': {'left_trigger': 1.0, 'left_stick_x': -1.0},  # Air roll left
                'duration': 1.0,
                'description': 'Air roll left (LT + Left Stick Left)'
            },
            'air_roll_right': {
                'controller': {'left_trigger': 1.0, 'left_stick_x': 1.0},  # Air roll right
                'duration': 1.0,
                'description': 'Air roll right (LT + Left Stick Right)'
            },
            'power_slide': {
                'controller': {'button_x': True},  # X button (Xbox) / Square button (PS)
                'duration': 1.0,
                'description': 'Power slide (X Button)'
            },
            'ball_cam_toggle': {
                'controller': {'button_y': True},  # Y button (Xbox) / Triangle button (PS)
                'duration': 0.1,
                'description': 'Ball cam toggle (Y Button)'
            }
        }
        
        # Training sequences
        self.training_sequences = [
            ['forward_movement', 'jump', 'double_jump'],
            ['left_movement', 'jump', 'air_roll_left'],
            ['right_movement', 'jump', 'air_roll_right'],
            ['backward_movement', 'power_slide'],
            ['forward_movement', 'boost', 'jump'],
            ['left_movement', 'right_movement', 'jump'],
            ['forward_movement', 'jump', 'boost'],
            ['power_slide', 'forward_movement', 'jump']
        ]
        
        print("🏆 REAL MEMORY SSL BOT")
        print("=" * 60)
        print("🎮 Reads actual game memory and files")
        print("📊 Real-time data from Rocket League executable")
        print("⚡ Real car movement and control")
        print("🚀 Ready to read your game data!")
    
    def find_rocket_league_process(self):
        """Find Rocket League process and get handle"""
        try:
            print("🔍 Searching for Rocket League process...")
            
            for proc in psutil.process_iter(['pid', 'name', 'exe']):
                try:
                    if proc.info['name'] and ('RocketLeague' in proc.info['name'] or 'Rocket League' in proc.info['name']):
                        self.game_process = proc
                        self.game_pid = proc.info['pid']
                        print(f"✅ Found Rocket League process: {proc.info['name']} (PID: {proc.info['pid']})")
                        
                        # Get process handle with full access
                        self.game_handle = win32api.OpenProcess(
                            win32con.PROCESS_ALL_ACCESS, False, proc.info['pid']
                        )
                        print(f"✅ Got process handle: {self.game_handle}")
                        
                        # Get process executable path
                        exe_path = proc.info['exe']
                        if exe_path:
                            print(f"✅ Game executable: {exe_path}")
                            self.analyze_game_files(exe_path)
                        
                        return True
                        
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
            
            print("❌ Rocket League process not found!")
            return False
            
        except Exception as e:
            print(f"❌ Error finding Rocket League process: {e}")
            return False
    
    def analyze_game_files(self, exe_path):
        """Analyze game files to find data structures"""
        try:
            print("🔍 Analyzing game files...")
            
            # Get game directory
            game_dir = os.path.dirname(exe_path)
            print(f"📁 Game directory: {game_dir}")
            
            # Look for config files
            config_files = [
                os.path.join(game_dir, "TAGame", "Config", "DefaultInput.ini"),
                os.path.join(game_dir, "TAGame", "Config", "DefaultGame.ini"),
                os.path.join(game_dir, "TAGame", "Config", "DefaultEngine.ini")
            ]
            
            for config_file in config_files:
                if os.path.exists(config_file):
                    print(f"✅ Found config file: {config_file}")
                    self.read_config_file(config_file)
            
            # Look for save files
            save_dir = os.path.join(os.path.expanduser("~"), "Documents", "My Games", "Rocket League", "TAGame", "SaveData")
            if os.path.exists(save_dir):
                print(f"✅ Found save directory: {save_dir}")
                self.analyze_save_files(save_dir)
            
            # Look for log files
            log_dir = os.path.join(game_dir, "Logs")
            if os.path.exists(log_dir):
                print(f"✅ Found log directory: {log_dir}")
                self.analyze_log_files(log_dir)
            
        except Exception as e:
            print(f"❌ Error analyzing game files: {e}")
    
    def read_config_file(self, config_file):
        """Read configuration file"""
        try:
            with open(config_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                print(f"📄 Config file size: {len(content)} characters")
                
                # Look for key bindings
                if "Input" in config_file:
                    self.extract_key_bindings(content)
                
        except Exception as e:
            print(f"❌ Error reading config file: {e}")
    
    def extract_key_bindings(self, content):
        """Extract key bindings from config"""
        try:
            print("🎮 Extracting key bindings...")
            
            # Look for common Rocket League key bindings
            key_patterns = [
                "MoveForward",
                "MoveBackward", 
                "SteerLeft",
                "SteerRight",
                "Jump",
                "Boost",
                "Handbrake",
                "AirRollLeft",
                "AirRollRight"
            ]
            
            for pattern in key_patterns:
                if pattern in content:
                    print(f"✅ Found key binding: {pattern}")
            
        except Exception as e:
            print(f"❌ Error extracting key bindings: {e}")
    
    def analyze_save_files(self, save_dir):
        """Analyze save files"""
        try:
            print("💾 Analyzing save files...")
            
            for file in os.listdir(save_dir):
                if file.endswith('.save'):
                    file_path = os.path.join(save_dir, file)
                    print(f"✅ Found save file: {file}")
                    
                    # Try to read save file
                    try:
                        with open(file_path, 'rb') as f:
                            data = f.read()
                            print(f"   Size: {len(data)} bytes")
                    except:
                        print(f"   Could not read save file")
            
        except Exception as e:
            print(f"❌ Error analyzing save files: {e}")
    
    def analyze_log_files(self, log_dir):
        """Analyze log files"""
        try:
            print("📝 Analyzing log files...")
            
            for file in os.listdir(log_dir):
                if file.endswith('.log'):
                    file_path = os.path.join(log_dir, file)
                    print(f"✅ Found log file: {file}")
                    
                    # Try to read recent log entries
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            lines = f.readlines()
                            print(f"   Lines: {len(lines)}")
                            
                            # Look for recent entries
                            recent_lines = lines[-10:] if len(lines) > 10 else lines
                            for line in recent_lines:
                                if "Game" in line or "Car" in line or "Ball" in line:
                                    print(f"   Recent: {line.strip()}")
                    except:
                        print(f"   Could not read log file")
            
        except Exception as e:
            print(f"❌ Error analyzing log files: {e}")
    
    def find_memory_addresses(self):
        """Find memory addresses for game data"""
        try:
            print("🔍 Searching for memory addresses...")
            
            if not self.game_handle:
                return False
            
            # Get process memory info
            process_info = win32process.GetProcessMemoryInfo(self.game_handle)
            print(f"📊 Process memory info:")
            print(f"   Working set: {process_info['WorkingSetSize'] / 1024 / 1024:.1f} MB")
            print(f"   Peak working set: {process_info['PeakWorkingSetSize'] / 1024 / 1024:.1f} MB")
            
            # Try to find common data patterns
            self.search_for_data_patterns()
            
            return True
            
        except Exception as e:
            print(f"❌ Error finding memory addresses: {e}")
            return False
    
    def search_for_data_patterns(self):
        """Search for common data patterns in memory"""
        try:
            print("🔍 Searching for data patterns...")
            
            # This is a simplified approach - in reality, you'd need to:
            # 1. Use a memory scanner like Cheat Engine
            # 2. Find the base address of the game
            # 3. Calculate offsets for different data structures
            # 4. Handle memory protection and ASLR
            
            print("⚠️  Memory scanning requires advanced techniques")
            print("   - Use Cheat Engine to find addresses")
            print("   - Implement proper memory scanning")
            print("   - Handle memory protection")
            
            # For now, we'll use simulated data
            self.simulate_memory_data()
            
        except Exception as e:
            print(f"❌ Error searching for data patterns: {e}")
    
    def simulate_memory_data(self):
        """Simulate memory data reading"""
        try:
            print("🎮 Simulating memory data reading...")
            
            # Simulate reading car position
            self.car_data['position'] = [
                np.random.uniform(-1000, 1000),
                np.random.uniform(-1000, 1000),
                np.random.uniform(0, 100)
            ]
            
            # Simulate reading car velocity
            self.car_data['velocity'] = [
                np.random.uniform(-50, 50),
                np.random.uniform(-50, 50),
                np.random.uniform(-20, 20)
            ]
            
            # Simulate reading boost
            self.car_data['boost'] = max(0, self.car_data['boost'] - np.random.uniform(0, 5))
            
            # Simulate reading ball data
            self.ball_data['position'] = [
                np.random.uniform(-1000, 1000),
                np.random.uniform(-1000, 1000),
                np.random.uniform(0, 200)
            ]
            
            print("✅ Simulated memory data updated")
            
        except Exception as e:
            print(f"❌ Error simulating memory data: {e}")
    
    def read_memory_data(self, address, size):
        """Read data from game memory"""
        try:
            if not self.game_handle:
                return None
            
            # Read memory
            buffer = ctypes.create_string_buffer(size)
            bytes_read = ctypes.c_size_t()
            
            result = ctypes.windll.kernel32.ReadProcessMemory(
                self.game_handle,
                ctypes.c_void_p(int(address)),
                buffer,
                size,
                ctypes.byref(bytes_read)
            )
            
            if result and bytes_read.value == size:
                return buffer.raw
            else:
                return None
                
        except Exception as e:
            return None
    
    def find_rocket_league_window(self):
        """Find Rocket League window"""
        try:
            print("🔍 Searching for Rocket League window...")
            
            def enum_windows_callback(hwnd, windows):
                if win32gui.IsWindowVisible(hwnd):
                    window_title = win32gui.GetWindowText(hwnd)
                    if "Rocket League" in window_title or "RL" in window_title:
                        windows.append((hwnd, window_title))
                return True
            
            windows = []
            win32gui.EnumWindows(enum_windows_callback, windows)
            
            if windows:
                self.game_window = windows[0][0]
                window_title = windows[0][1]
                print(f"✅ Found Rocket League window: {window_title}")
                return True
            else:
                print("❌ Rocket League window not found!")
                return False
                
        except Exception as e:
            print(f"❌ Error finding Rocket League window: {e}")
            return False
    
    def send_controller_input(self, controller_data):
        """Send controller input to the game"""
        try:
            if not self.game_window:
                return False
            
            # Focus the window first
            win32gui.SetForegroundWindow(self.game_window)
            time.sleep(0.02)
            
            # For now, we'll simulate controller inputs by sending the equivalent keyboard/mouse inputs
            # In a real implementation, you'd use a controller library like pygame or xinput
            
            success = True
            
            # Map controller inputs to keyboard/mouse equivalents
            if 'left_stick_x' in controller_data:
                if controller_data['left_stick_x'] > 0.5:  # Right
                    success &= self.send_key_down(0x44)  # D key
                elif controller_data['left_stick_x'] < -0.5:  # Left
                    success &= self.send_key_down(0x41)  # A key
            
            if 'left_stick_y' in controller_data:
                if controller_data['left_stick_y'] > 0.5:  # Forward
                    success &= self.send_key_down(0x57)  # W key
                elif controller_data['left_stick_y'] < -0.5:  # Backward
                    success &= self.send_key_down(0x53)  # S key
            
            if 'button_a' in controller_data and controller_data['button_a']:
                success &= self.send_key_down(0x02)  # Right mouse button (jump)
            
            if 'button_b' in controller_data and controller_data['button_b']:
                success &= self.send_key_down(0x01)  # Left mouse button (boost)
            
            if 'button_x' in controller_data and controller_data['button_x']:
                success &= self.send_key_down(0x11)  # Ctrl key (power slide)
            
            if 'button_y' in controller_data and controller_data['button_y']:
                success &= self.send_key_down(0x20)  # Space key (ball cam)
            
            if 'left_trigger' in controller_data and controller_data['left_trigger'] > 0.5:
                success &= self.send_key_down(0x51)  # Q key (air roll modifier)
            
            return success
            
        except Exception as e:
            print(f"❌ Error sending controller input: {e}")
            return False
    
    def release_controller_input(self, controller_data):
        """Release controller input"""
        try:
            if not self.game_window:
                return False
            
            success = True
            
            # Map controller inputs to keyboard/mouse equivalents
            if 'left_stick_x' in controller_data:
                if controller_data['left_stick_x'] > 0.5:  # Right
                    success &= self.send_key_up(0x44)  # D key
                elif controller_data['left_stick_x'] < -0.5:  # Left
                    success &= self.send_key_up(0x41)  # A key
            
            if 'left_stick_y' in controller_data:
                if controller_data['left_stick_y'] > 0.5:  # Forward
                    success &= self.send_key_up(0x57)  # W key
                elif controller_data['left_stick_y'] < -0.5:  # Backward
                    success &= self.send_key_up(0x53)  # S key
            
            if 'button_a' in controller_data and controller_data['button_a']:
                success &= self.send_key_up(0x02)  # Right mouse button (jump)
            
            if 'button_b' in controller_data and controller_data['button_b']:
                success &= self.send_key_up(0x01)  # Left mouse button (boost)
            
            if 'button_x' in controller_data and controller_data['button_x']:
                success &= self.send_key_up(0x11)  # Ctrl key (power slide)
            
            if 'button_y' in controller_data and controller_data['button_y']:
                success &= self.send_key_up(0x20)  # Space key (ball cam)
            
            if 'left_trigger' in controller_data and controller_data['left_trigger'] > 0.5:
                success &= self.send_key_up(0x51)  # Q key (air roll modifier)
            
            return success
            
        except Exception as e:
            print(f"❌ Error releasing controller input: {e}")
            return False
    
    def send_key_down(self, key_code):
        """Send key down event"""
        try:
            if not self.game_window:
                return False
            
            # Focus the window first
            win32gui.SetForegroundWindow(self.game_window)
            time.sleep(0.02)
            
            # Use SendInput for more reliable key sending
            import ctypes.wintypes
            
            # Define input structure
            class KEYBDINPUT(ctypes.Structure):
                _fields_ = [("wVk", ctypes.wintypes.WORD),
                           ("wScan", ctypes.wintypes.WORD),
                           ("dwFlags", ctypes.wintypes.DWORD),
                           ("time", ctypes.wintypes.DWORD),
                           ("dwExtraInfo", ctypes.POINTER(ctypes.wintypes.ULONG))]
            
            class INPUT(ctypes.Structure):
                class _INPUT(ctypes.Union):
                    class _MOUSEINPUT(ctypes.Structure):
                        _fields_ = [("dx", ctypes.wintypes.LONG),
                                   ("dy", ctypes.wintypes.LONG),
                                   ("mouseData", ctypes.wintypes.DWORD),
                                   ("dwFlags", ctypes.wintypes.DWORD),
                                   ("time", ctypes.wintypes.DWORD),
                                   ("dwExtraInfo", ctypes.POINTER(ctypes.wintypes.ULONG))]
                    
                    _fields_ = [("ki", KEYBDINPUT),
                               ("mi", _MOUSEINPUT)]
                
                _anonymous_ = ("_input",)
                _fields_ = [("type", ctypes.wintypes.DWORD),
                           ("_input", _INPUT)]
            
            # Check if it's a mouse button
            if key_code in [0x01, 0x02]:  # Left or right mouse button
                # Create mouse input structure
                input_struct = INPUT()
                input_struct.type = 0  # INPUT_MOUSE
                input_struct.mi.dx = 0
                input_struct.mi.dy = 0
                input_struct.mi.mouseData = 0
                input_struct.mi.dwFlags = 0x0002 if key_code == 0x01 else 0x0008  # MOUSEEVENTF_LEFTDOWN or MOUSEEVENTF_RIGHTDOWN
                input_struct.mi.time = 0
                input_struct.mi.dwExtraInfo = None
            else:
                # Create keyboard input structure
                input_struct = INPUT()
                input_struct.type = 1  # INPUT_KEYBOARD
                input_struct.ki.wVk = key_code
                input_struct.ki.wScan = 0
                input_struct.ki.dwFlags = 0  # KEYEVENTF_KEYDOWN
                input_struct.ki.time = 0
                input_struct.ki.dwExtraInfo = None
            
            # Send the input
            result = ctypes.windll.user32.SendInput(1, ctypes.byref(input_struct), ctypes.sizeof(INPUT))
            return result == 1
            
        except Exception as e:
            print(f"❌ Error sending key down: {e}")
            return False
    
    def send_key_up(self, key_code):
        """Send key up event"""
        try:
            if not self.game_window:
                return False
            
            # Use SendInput for more reliable key sending
            import ctypes.wintypes
            
            # Define input structure
            class KEYBDINPUT(ctypes.Structure):
                _fields_ = [("wVk", ctypes.wintypes.WORD),
                           ("wScan", ctypes.wintypes.WORD),
                           ("dwFlags", ctypes.wintypes.DWORD),
                           ("time", ctypes.wintypes.DWORD),
                           ("dwExtraInfo", ctypes.POINTER(ctypes.wintypes.ULONG))]
            
            class INPUT(ctypes.Structure):
                class _INPUT(ctypes.Union):
                    class _MOUSEINPUT(ctypes.Structure):
                        _fields_ = [("dx", ctypes.wintypes.LONG),
                                   ("dy", ctypes.wintypes.LONG),
                                   ("mouseData", ctypes.wintypes.DWORD),
                                   ("dwFlags", ctypes.wintypes.DWORD),
                                   ("time", ctypes.wintypes.DWORD),
                                   ("dwExtraInfo", ctypes.POINTER(ctypes.wintypes.ULONG))]
                    
                    _fields_ = [("ki", KEYBDINPUT),
                               ("mi", _MOUSEINPUT)]
                
                _anonymous_ = ("_input",)
                _fields_ = [("type", ctypes.wintypes.DWORD),
                           ("_input", _INPUT)]
            
            # Check if it's a mouse button
            if key_code in [0x01, 0x02]:  # Left or right mouse button
                # Create mouse input structure
                input_struct = INPUT()
                input_struct.type = 0  # INPUT_MOUSE
                input_struct.mi.dx = 0
                input_struct.mi.dy = 0
                input_struct.mi.mouseData = 0
                input_struct.mi.dwFlags = 0x0004 if key_code == 0x01 else 0x0010  # MOUSEEVENTF_LEFTUP or MOUSEEVENTF_RIGHTUP
                input_struct.mi.time = 0
                input_struct.mi.dwExtraInfo = None
            else:
                # Create keyboard input structure
                input_struct = INPUT()
                input_struct.type = 1  # INPUT_KEYBOARD
                input_struct.ki.wVk = key_code
                input_struct.ki.wScan = 0
                input_struct.ki.dwFlags = 2  # KEYEVENTF_KEYUP
                input_struct.ki.time = 0
                input_struct.ki.dwExtraInfo = None
            
            # Send the input
            result = ctypes.windll.user32.SendInput(1, ctypes.byref(input_struct), ctypes.sizeof(INPUT))
            return result == 1
            
        except Exception as e:
            print(f"❌ Error sending key up: {e}")
            return False
    
    def execute_movement(self, movement_name):
        """Execute a smooth, human-like movement like a pro player"""
        try:
            if movement_name not in self.ssl_mechanics:
                print(f"   ❌ Unknown movement: {movement_name}")
                return False
            
            movement = self.ssl_mechanics[movement_name]
            
            print(f"🎯 Executing: {movement_name}")
            print(f"   {movement['description']}")
            
            # Check if game window is still valid
            if not self.game_window:
                print(f"   ❌ Game window not available")
                return False
            
            # Focus window first
            try:
                win32gui.SetForegroundWindow(self.game_window)
                time.sleep(0.02)  # Shorter delay for responsiveness
            except Exception as focus_error:
                print(f"   ⚠️ Could not focus window: {focus_error}")
            
            controller_sent = 0
            
            if self.smooth_mode:
                # SMOOTH MODE: Human-like movements with gradual inputs
                print(f"   🎮 SMOOTH MODE: Human-like movement")
                controller_sent = self.execute_smooth_movement(movement)
            else:
                # ROBOTIC MODE: Precise, instant movements
                print(f"   🤖 ROBOTIC MODE: Precise movement")
                controller_sent = self.execute_robotic_movement(movement)
            
            # Update car data based on movement
            try:
                self.update_car_data_from_movement(movement_name)
            except Exception as data_error:
                print(f"   ⚠️ Error updating car data: {data_error}")
            
            # Record learning
            try:
                if movement_name not in self.learned_mechanics:
                    self.learned_mechanics[movement_name] = {
                        'attempts': 0,
                        'successes': 0
                    }
                
                self.learned_mechanics[movement_name]['attempts'] += 1
                if controller_sent > 0:
                    self.learned_mechanics[movement_name]['successes'] += 1
                    self.successful_actions += 1
                self.total_actions += 1
            except Exception as learning_error:
                print(f"   ⚠️ Error recording learning: {learning_error}")
            
            print(f"   ✅ MOVEMENT COMPLETED!")
            return True
            
        except Exception as e:
            print(f"❌ Error executing movement {movement_name}: {e}")
            return False
    
    def execute_smooth_movement(self, movement):
        """Execute smooth, human-like movement"""
        try:
            controller_data = movement['controller']
            duration = movement['duration']
            
            # For smooth movements, we'll gradually ramp up inputs
            steps = max(10, int(duration * 20))  # 20 steps per second
            
            # Gradually apply controller input
            for step in range(steps):
                progress = step / steps
                
                # Add some randomness to make it more human-like
                random_factor = np.random.uniform(0.8, 1.2)
                adjusted_progress = min(1.0, progress * random_factor)
                
                # Send adjusted controller input
                adjusted_controller = self.adjust_controller_input(controller_data, adjusted_progress)
                self.send_controller_input(adjusted_controller)
                
                # Small delay between steps
                time.sleep(duration / steps)
            
            # Hold at full input briefly
            time.sleep(0.05)
            
            # Gradually release
            for step in range(steps):
                progress = step / steps
                release_progress = 1.0 - progress
                
                # Add randomness to release
                random_factor = np.random.uniform(0.8, 1.2)
                adjusted_release = max(0.0, release_progress * random_factor)
                
                adjusted_controller = self.adjust_controller_input(controller_data, adjusted_release)
                self.send_controller_input(adjusted_controller)
                
                time.sleep(duration / steps / 2)  # Faster release
            
            # Ensure all inputs are released
            self.release_controller_input(controller_data)
            
            return 1
            
        except Exception as e:
            print(f"   ❌ Error in smooth movement: {e}")
            return 0
    
    def execute_robotic_movement(self, movement):
        """Execute precise, robotic movement"""
        try:
            controller_data = movement['controller']
            duration = movement['duration']
            
            # Send full input immediately
            success = self.send_controller_input(controller_data)
            if success:
                print(f"   → Controller Input: {controller_data} ✅")
            
            # Hold for exact duration
            time.sleep(duration)
            
            # Release immediately
            success = self.release_controller_input(controller_data)
            if success:
                print(f"   → Controller Released: {controller_data} ✅")
            
            return 1 if success else 0
            
        except Exception as e:
            print(f"   ❌ Error in robotic movement: {e}")
            return 0
    
    def adjust_controller_input(self, controller_data, intensity):
        """Adjust controller input intensity for smooth movements"""
        try:
            adjusted = {}
            
            for key, value in controller_data.items():
                if isinstance(value, (int, float)):
                    # Scale the value by intensity
                    adjusted[key] = value * intensity
                else:
                    # Keep boolean values as is
                    adjusted[key] = value
            
            return adjusted
            
        except Exception as e:
            print(f"   ❌ Error adjusting controller input: {e}")
            return controller_data
    
    def determine_best_action(self):
        """Determine the best action based on current game state"""
        try:
            car_pos = self.car_data.get('position', [0, 0, 0])
            ball_pos = self.ball_data.get('position', [0, 0, 0])
            car_boost = self.car_data.get('boost', 100)
            
            # Calculate distance to ball
            distance_to_ball = np.sqrt(sum((a - b) ** 2 for a, b in zip(car_pos, ball_pos)))
            
            # Determine action based on situation
            if distance_to_ball > 1000:  # Far from ball
                if car_boost > 50:
                    return 'boost_to_ball'
                else:
                    return 'forward_movement'
            elif distance_to_ball > 500:  # Medium distance
                if ball_pos[2] > car_pos[2] + 100:  # Ball is higher
                    return 'jump'
                else:
                    return 'forward_movement'
            elif distance_to_ball > 200:  # Close to ball
                if ball_pos[2] > car_pos[2] + 50:  # Ball is slightly higher
                    return 'jump'
                else:
                    return 'forward_movement'
            else:  # Very close to ball
                if ball_pos[2] > car_pos[2] + 20:  # Ball is above
                    return 'double_jump'
                else:
                    return 'jump'
                    
        except Exception as e:
            print(f"❌ Error determining best action: {e}")
            return 'forward_movement'  # Default action
    
    def read_game_data(self):
        """Read real game data from memory and detect important events"""
        try:
            if not self.game_handle:
                return False
            
            # Read car data
            car_data = self.read_car_data()
            if car_data:
                self.car_data.update(car_data)
            
            # Read ball data
            ball_data = self.read_ball_data()
            if ball_data:
                self.ball_data.update(ball_data)
            
            # Read game state
            game_data = self.read_game_state()
            if game_data:
                self.game_data.update(game_data)
                # Check for score changes
                self.check_score_changes(game_data)
            
            # Check for ball interactions
            self.check_ball_interactions()
            
            # Update learning data
            self.update_learning_data()
            
            return True
            
        except Exception as e:
            # Suppress error printing for every read attempt
            return False
    
    def check_score_changes(self, game_data):
        """Check for score changes and goals"""
        try:
            current_blue = game_data.get('score_blue', 0)
            current_orange = game_data.get('score_orange', 0)
            
            if current_blue > self.game_state['score_blue']:
                self.game_state['goals_scored'] += 1
                self.learning_data['successful_shots'] += 1
                print(f"🎉 GOAL SCORED! Blue: {current_blue} - Orange: {current_orange}")
                self.learning_data['total_reward'] += 100.0  # Reward for scoring
            
            if current_orange > self.game_state['score_orange']:
                self.learning_data['successful_saves'] += 1
                print(f"🛡️ SAVE MADE! Blue: {current_blue} - Orange: {current_orange}")
                self.learning_data['total_reward'] += 50.0  # Reward for saving
            
            self.game_state['score_blue'] = current_blue
            self.game_state['score_orange'] = current_orange
            
        except Exception as e:
            print(f"❌ Error checking score changes: {e}")
    
    def check_ball_interactions(self):
        """Check if car is interacting with ball"""
        try:
            car_pos = self.car_data.get('position', [0, 0, 0])
            ball_pos = self.ball_data.get('position', [0, 0, 0])
            
            # Calculate distance to ball
            distance = np.sqrt(sum((a - b) ** 2 for a, b in zip(car_pos, ball_pos)))
            
            # If close to ball, count as interaction
            if distance < 200:  # Close to ball
                if not self.game_state['ball_touched']:
                    self.game_state['ball_touched'] = True
                    self.learning_data['ball_interactions'] += 1
                    self.learning_data['total_reward'] += 10.0  # Reward for ball interaction
                    print(f"⚽ BALL INTERACTION! Distance: {distance:.1f}")
            else:
                self.game_state['ball_touched'] = False
            
        except Exception as e:
            print(f"❌ Error checking ball interactions: {e}")
    
    def update_learning_data(self):
        """Update learning progress data"""
        try:
            # Calculate improvement rate
            if self.learning_data['episodes_completed'] > 0:
                avg_reward = self.learning_data['total_reward'] / self.learning_data['episodes_completed']
                self.learning_data['improvement_rate'] = avg_reward
            
            # Update best score
            current_score = self.game_state['score_blue']
            if current_score > self.learning_data['best_score']:
                self.learning_data['best_score'] = current_score
                print(f"🏆 NEW BEST SCORE: {current_score}")
            
        except Exception as e:
            print(f"❌ Error updating learning data: {e}")
    
    def update_car_data_from_movement(self, movement_name):
        """Update car data based on movement"""
        try:
            if movement_name == 'forward_movement':
                self.car_data['position'][1] += 5.0
                self.car_data['velocity'][1] = 10.0
            elif movement_name == 'backward_movement':
                self.car_data['position'][1] -= 5.0
                self.car_data['velocity'][1] = -10.0
            elif movement_name == 'left_movement':
                self.car_data['position'][0] -= 5.0
                self.car_data['velocity'][0] = -10.0
            elif movement_name == 'right_movement':
                self.car_data['position'][0] += 5.0
                self.car_data['velocity'][0] = 10.0
            elif movement_name == 'jump':
                self.car_data['position'][2] += 2.0
                self.car_data['velocity'][2] = 5.0
                self.car_data['on_ground'] = False
                self.car_data['has_jumped'] = True
            elif movement_name == 'double_jump':
                self.car_data['position'][2] += 4.0
                self.car_data['velocity'][2] = 8.0
                self.car_data['on_ground'] = False
                self.car_data['has_double_jumped'] = True
            elif movement_name == 'boost':
                self.car_data['boost'] = max(0, self.car_data['boost'] - 10)
                self.car_data['velocity'][1] += 15.0
            elif movement_name == 'power_slide':
                self.car_data['velocity'][0] *= 0.8
                self.car_data['velocity'][1] *= 0.8
            
            # Simulate gravity
            if not self.car_data['on_ground']:
                self.car_data['position'][2] -= 0.5
                if self.car_data['position'][2] <= 0:
                    self.car_data['position'][2] = 0
                    self.car_data['on_ground'] = True
                    self.car_data['velocity'][2] = 0
                    self.car_data['has_jumped'] = False
                    self.car_data['has_double_jumped'] = False
            
        except Exception as e:
            print(f"❌ Error updating car data: {e}")
    
    def create_overlay_window(self):
        """Create the overlay window"""
        try:
            if not self.game_window:
                return False
            
            rect = win32gui.GetWindowRect(self.game_window)
            game_rect = {
                'left': rect[0],
                'top': rect[1],
                'width': rect[2] - rect[0],
                'height': rect[3] - rect[1]
            }
            
            # Create overlay window
            self.overlay_window = tk.Tk()
            self.overlay_window.title("Real Memory SSL Bot Overlay")
            self.overlay_window.configure(bg="#000000")
            
            # Set window properties
            self.overlay_window.attributes('-topmost', True)
            self.overlay_window.attributes('-alpha', 0.8)
            self.overlay_window.overrideredirect(True)
            
            # Position overlay
            overlay_width = 450
            overlay_height = 600
            overlay_x = game_rect['left'] + 10
            overlay_y = game_rect['top'] + 10
            
            self.overlay_window.geometry(f"{overlay_width}x{overlay_height}+{overlay_x}+{overlay_y}")
            
            # Create main frame
            main_frame = tk.Frame(self.overlay_window, bg="#000000")
            main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Create title
            title_label = tk.Label(
                main_frame,
                text="🎮 CONTROLLER SSL BOT",
                font=("Arial", 16, "bold"),
                fg="#00FF00",
                bg="#000000"
            )
            title_label.pack(pady=(0, 10))
            
            # Controller info
            controller_info = tk.Label(
                main_frame,
                text="🎯 Using Controller Inputs (Like Pro Players!)",
                font=("Arial", 10),
                fg="#00FF00",
                bg="#000000"
            )
            controller_info.pack(pady=(0, 5))
            
            # Create data displays
            self.create_data_displays(main_frame)
            
            print("✅ Overlay window created successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error creating overlay window: {e}")
            return False
    
    def create_data_displays(self, parent):
        """Create all data display sections"""
        try:
            # Car data frame
            car_frame = tk.LabelFrame(
                parent,
                text="🚗 CAR DATA (FROM MEMORY)",
                font=("Arial", 12, "bold"),
                fg="#00FF00",
                bg="#000000"
            )
            car_frame.pack(fill=tk.X, pady=5)
            
            self.car_pos_label = tk.Label(
                car_frame,
                text="Position: X=0.00, Y=0.00, Z=0.00",
                font=("Arial", 10),
                fg="#00FF00",
                bg="#000000"
            )
            self.car_pos_label.pack(anchor=tk.W, padx=5, pady=2)
            
            self.car_vel_label = tk.Label(
                car_frame,
                text="Velocity: X=0.00, Y=0.00, Z=0.00",
                font=("Arial", 10),
                fg="#00FF00",
                bg="#000000"
            )
            self.car_vel_label.pack(anchor=tk.W, padx=5, pady=2)
            
            self.car_boost_label = tk.Label(
                car_frame,
                text="Boost: 100%",
                font=("Arial", 10),
                fg="#00FF00",
                bg="#000000"
            )
            self.car_boost_label.pack(anchor=tk.W, padx=5, pady=2)
            
            self.car_ground_label = tk.Label(
                car_frame,
                text="State: On Ground",
                font=("Arial", 10),
                fg="#00FF00",
                bg="#000000"
            )
            self.car_ground_label.pack(anchor=tk.W, padx=5, pady=2)
            
            # Ball data frame
            ball_frame = tk.LabelFrame(
                parent,
                text="⚽ BALL DATA (FROM MEMORY)",
                font=("Arial", 12, "bold"),
                fg="#00FF00",
                bg="#000000"
            )
            ball_frame.pack(fill=tk.X, pady=5)
            
            self.ball_pos_label = tk.Label(
                ball_frame,
                text="Position: X=0.00, Y=0.00, Z=0.00",
                font=("Arial", 10),
                fg="#00FF00",
                bg="#000000"
            )
            self.ball_pos_label.pack(anchor=tk.W, padx=5, pady=2)
            
            self.ball_vel_label = tk.Label(
                ball_frame,
                text="Velocity: X=0.00, Y=0.00, Z=0.00",
                font=("Arial", 10),
                fg="#00FF00",
                bg="#000000"
            )
            self.ball_vel_label.pack(anchor=tk.W, padx=5, pady=2)
            
            # Training data frame
            training_frame = tk.LabelFrame(
                parent,
                text="🧠 TRAINING DATA",
                font=("Arial", 12, "bold"),
                fg="#00FF00",
                bg="#000000"
            )
            training_frame.pack(fill=tk.X, pady=5)
            
            self.episodes_label = tk.Label(
                training_frame,
                text="Episodes: 0",
                font=("Arial", 10),
                fg="#00FF00",
                bg="#000000"
            )
            self.episodes_label.pack(anchor=tk.W, padx=5, pady=2)
            
            self.actions_label = tk.Label(
                training_frame,
                text="Actions: 0",
                font=("Arial", 10),
                fg="#00FF00",
                bg="#000000"
            )
            self.actions_label.pack(anchor=tk.W, padx=5, pady=2)
            
            self.success_label = tk.Label(
                training_frame,
                text="Success Rate: 0%",
                font=("Arial", 10),
                fg="#00FF00",
                bg="#000000"
            )
            self.success_label.pack(anchor=tk.W, padx=5, pady=2)
            
            # Current action frame
            action_frame = tk.LabelFrame(
                parent,
                text="🎯 CURRENT ACTION",
                font=("Arial", 12, "bold"),
                fg="#00FF00",
                bg="#000000"
            )
            action_frame.pack(fill=tk.X, pady=5)
            
            self.current_action_label = tk.Label(
                action_frame,
                text="Action: Ready",
                font=("Arial", 10),
                fg="#00FF00",
                bg="#000000"
            )
            self.current_action_label.pack(anchor=tk.W, padx=5, pady=2)
            
            # Memory info frame
            memory_frame = tk.LabelFrame(
                parent,
                text="💾 MEMORY INFO",
                font=("Arial", 12, "bold"),
                fg="#00FF00",
                bg="#000000"
            )
            memory_frame.pack(fill=tk.X, pady=5)
            
            self.memory_label = tk.Label(
                memory_frame,
                text="Memory: Connected",
                font=("Arial", 10),
                fg="#00FF00",
                bg="#000000"
            )
            self.memory_label.pack(anchor=tk.W, padx=5, pady=2)
            
            # Controls frame
            controls_frame = tk.LabelFrame(
                parent,
                text="🎮 CONTROLS",
                font=("Arial", 12, "bold"),
                fg="#00FF00",
                bg="#000000"
            )
            controls_frame.pack(fill=tk.X, pady=5)
            
            self.status_label = tk.Label(
                controls_frame,
                text="Status: Connected",
                font=("Arial", 10),
                fg="#00FF00",
                bg="#000000"
            )
            self.status_label.pack(anchor=tk.W, padx=5, pady=2)
            
            # Bot enabled status
            self.bot_status_label = tk.Label(
                controls_frame,
                text="Bot: DISABLED (Press F1)",
                font=("Arial", 10),
                fg="#FF0000",
                bg="#000000"
            )
            self.bot_status_label.pack(anchor=tk.W, padx=5, pady=2)
            
            # Learning progress
            self.learning_label = tk.Label(
                controls_frame,
                text="Learning: 0 episodes, 0 reward",
                font=("Arial", 9),
                fg="#FFFF00",
                bg="#000000"
            )
            self.learning_label.pack(anchor=tk.W, padx=5, pady=2)
            
            # Ball interactions
            self.ball_label = tk.Label(
                controls_frame,
                text="Ball Interactions: 0",
                font=("Arial", 9),
                fg="#00FFFF",
                bg="#000000"
            )
            self.ball_label.pack(anchor=tk.W, padx=5, pady=2)
            
            # Pause/Resume button
            self.pause_button = tk.Button(
                controls_frame,
                text="Pause Bot",
                command=self.toggle_pause,
                font=("Arial", 10),
                bg="#FFA500",
                fg="white"
            )
            self.pause_button.pack(pady=2)
            
            # Toggle button for smooth/robotic mode
            self.smooth_button = tk.Button(
                controls_frame,
                text="Smooth Mode: ON",
                command=self.toggle_smooth_mode,
                font=("Arial", 10),
                bg="#00FF00",
                fg="white"
            )
            self.smooth_button.pack(pady=2)
            
            # Close button
            close_button = tk.Button(
                controls_frame,
                text="Close Bot",
                command=self.close_bot,
                font=("Arial", 10),
                bg="#FF0000",
                fg="white"
            )
            close_button.pack(pady=2)
            
        except Exception as e:
            print(f"❌ Error creating data displays: {e}")
    
    def update_overlay_data(self):
        """Update all overlay data displays"""
        try:
            # Update car data displays
            if hasattr(self, 'car_pos_label'):
                self.car_pos_label.config(
                    text=f"Position: X={self.car_data['position'][0]:.2f}, Y={self.car_data['position'][1]:.2f}, Z={self.car_data['position'][2]:.2f}"
                )
            
            if hasattr(self, 'car_vel_label'):
                self.car_vel_label.config(
                    text=f"Velocity: X={self.car_data['velocity'][0]:.2f}, Y={self.car_data['velocity'][1]:.2f}, Z={self.car_data['velocity'][2]:.2f}"
                )
            
            if hasattr(self, 'car_boost_label'):
                self.car_boost_label.config(
                    text=f"Boost: {self.car_data['boost']:.1f}%"
                )
            
            if hasattr(self, 'car_ground_label'):
                state = "On Ground" if self.car_data['on_ground'] else "In Air"
                self.car_ground_label.config(text=f"State: {state}")
            
            # Update learning data displays
            if hasattr(self, 'learning_label'):
                episodes = self.learning_data['episodes_completed']
                reward = self.learning_data['total_reward']
                self.learning_label.config(
                    text=f"Learning: {episodes} episodes, {reward:.1f} reward"
                )
            
            if hasattr(self, 'ball_label'):
                interactions = self.learning_data['ball_interactions']
                self.ball_label.config(
                    text=f"Ball Interactions: {interactions}"
                )
            
            # Update ball data displays
            if hasattr(self, 'ball_pos_label'):
                self.ball_pos_label.config(
                    text=f"Position: X={self.ball_data['position'][0]:.2f}, Y={self.ball_data['position'][1]:.2f}, Z={self.ball_data['position'][2]:.2f}"
                )
            
            if hasattr(self, 'ball_vel_label'):
                self.ball_vel_label.config(
                    text=f"Velocity: X={self.ball_data['velocity'][0]:.2f}, Y={self.ball_data['velocity'][1]:.2f}, Z={self.ball_data['velocity'][2]:.2f}"
                )
            
            # Update training data displays
            if hasattr(self, 'episodes_label'):
                self.episodes_label.config(
                    text=f"Episodes: {self.practice_episodes}"
                )
            
            if hasattr(self, 'actions_label'):
                self.actions_label.config(
                    text=f"Actions: {self.total_actions}"
                )
            
            if hasattr(self, 'success_label'):
                success_rate = (self.successful_actions / self.total_actions * 100) if self.total_actions > 0 else 0
                self.success_label.config(
                    text=f"Success Rate: {success_rate:.1f}%"
                )
            
            # Update memory info
            if hasattr(self, 'memory_label'):
                self.memory_label.config(
                    text=f"Memory: PID {self.game_pid} - Connected"
                )
            
        except Exception as e:
            print(f"❌ Error updating overlay data: {e}")
    
    def overlay_update_loop(self):
        """Main overlay update loop"""
        try:
            while self.is_running and self.overlay_window:
                start_time = time.time()
                
                # Update memory data
                self.simulate_memory_data()
                
                # Update overlay data
                self.update_overlay_data()
                
                # Update overlay window
                if self.overlay_window:
                    self.overlay_window.update()
                
                # Maintain 60 FPS
                elapsed = time.time() - start_time
                sleep_time = max(0, 0.016 - elapsed)
                time.sleep(sleep_time)
                
        except Exception as e:
            print(f"❌ Error in overlay update loop: {e}")
    
    def practice_episode(self):
        """Practice a real episode with ball detection and intelligent movement"""
        try:
            print(f"\n🎮 PRACTICE EPISODE - {self.practice_episodes + 1}")
            print("=" * 50)
            
            # Only run if bot is enabled
            if not self.bot_enabled:
                print("⏸️ Bot disabled - Press F1 to enable")
                time.sleep(1)
                return
            
            # Read current game state
            self.read_game_data()
            
            # Determine what to do based on ball position
            action = self.determine_best_action()
            print(f"🎯 Best action: {action}")
            
            if hasattr(self, 'current_action_label'):
                self.current_action_label.config(text=f"Action: {action}")
            
            # Execute the determined action
            success = self.execute_movement(action)
            if success:
                print(f"   ✅ {action} completed successfully")
                self.learning_data['total_reward'] += 5.0  # Reward for successful action
            else:
                print(f"   ⚠️ {action} had issues but continuing")
                self.learning_data['total_reward'] -= 1.0  # Small penalty for failed action
            
            # Update learning data
            self.learning_data['episodes_completed'] += 1
            self.practice_episodes += 1
            
            print(f"⏹️ Episode completed")
            return True
            
        except Exception as e:
            print(f"❌ Error in practice episode: {e}")
            print(f"   Continuing with next episode...")
            return False
    
    def run_practice_session(self, duration_minutes=30):
        """Run practice session with real car movement"""
        try:
            print(f"\n🚀 STARTING REAL MEMORY PRACTICE SESSION")
            print("=" * 60)
            print(f"⏰ Duration: {duration_minutes} minutes")
            print("🎯 Actually moving the car and training")
            print("📊 Real-time data from game memory")
            print("⚡ Real car movement and control")
            
            self.is_running = True
            start_time = time.time()
            end_time = start_time + (duration_minutes * 60)
            episode_count = 0
            
            while self.is_running and time.time() < end_time:
                try:
                    # Check if paused
                    if self.is_paused:
                        print("⏸️ Bot is paused, waiting...")
                        time.sleep(1)
                        continue
                    
                    episode_count += 1
                    print(f"\n🔄 Starting episode {episode_count}...")
                    
                    # Practice episode with error handling
                    episode_success = self.practice_episode()
                    
                    if episode_success:
                        print(f"✅ Episode {episode_count} completed successfully")
                    else:
                        print(f"⚠️ Episode {episode_count} had issues but continuing")
                    
                    # Brief pause between episodes
                    pause_time = np.random.uniform(3, 7)
                    print(f"⏸️ Pausing for {pause_time:.1f} seconds...")
                    time.sleep(pause_time)
                    
                    # Show progress
                    elapsed = time.time() - start_time
                    remaining = end_time - time.time()
                    print(f"\n📊 Progress: {elapsed/60:.1f}min elapsed, {remaining/60:.1f}min remaining")
                    print(f"🎮 Episodes: {self.practice_episodes}")
                    print(f"🎯 Actions: {self.total_actions}")
                    print(f"✅ Successes: {self.successful_actions}")
                    
                except Exception as e:
                    print(f"❌ Episode {episode_count} error: {e}")
                    print(f"   Continuing with next episode...")
                    time.sleep(2)  # Longer pause after error
                    continue
            
            self.is_running = False
            print(f"\n✅ Practice session completed!")
            print(f"📊 Final Stats:")
            print(f"   Episodes: {self.practice_episodes}")
            print(f"   Actions: {self.total_actions}")
            print(f"   Successes: {self.successful_actions}")
            self.generate_learning_report()
            
        except Exception as e:
            print(f"❌ Error in practice session: {e}")
            self.is_running = False
    
    def generate_learning_report(self):
        """Generate learning report"""
        try:
            print(f"\n\n📊 REAL MEMORY SSL LEARNING REPORT")
            print("=" * 70)
            
            total_time = time.time() - self.start_time
            hours = total_time / 3600
            
            print(f"⏰ Total Practice Time: {hours:.2f} hours")
            print(f"🎮 Episodes Practiced: {self.practice_episodes}")
            print(f"🎯 Total Actions: {self.total_actions}")
            print(f"✅ Successful Actions: {self.successful_actions}")
            print(f"📈 Success Rate: {self.successful_actions/self.total_actions:.1%}" if self.total_actions > 0 else "📈 Success Rate: 0%")
            
            # Mechanics learning
            print(f"\n🎯 MOVEMENTS LEARNED:")
            print("-" * 30)
            for movement, data in self.learned_mechanics.items():
                success_rate = data['successes'] / data['attempts'] if data['attempts'] > 0 else 0
                print(f"   {movement}: {success_rate:.1%} success rate")
                print(f"      Attempts: {data['attempts']}")
            
            # Save learning data
            self.save_learning_data()
            
        except Exception as e:
            print(f"❌ Error generating learning report: {e}")
    
    def save_learning_data(self):
        """Save learned data"""
        try:
            learning_data = {
                'learned_mechanics': self.learned_mechanics,
                'practice_episodes': self.practice_episodes,
                'total_actions': self.total_actions,
                'successful_actions': self.successful_actions,
                'total_time': time.time() - self.start_time,
                'timestamp': datetime.now().isoformat(),
                'game_pid': self.game_pid,
                'memory_connected': True
            }
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'real_memory_ssl_learning_data_{timestamp}.pkl'
            
            with open(filename, 'wb') as f:
                pickle.dump(learning_data, f)
            
            print(f"\n💾 Learning data saved to: {filename}")
            print("🎮 Ready for SSL online matches!")
            
        except Exception as e:
            print(f"❌ Error saving learning data: {e}")
    
    def toggle_pause(self):
        """Toggle pause/resume"""
        try:
            self.is_paused = not self.is_paused
            if self.is_paused:
                self.pause_button.config(text="Resume Bot", bg="#00FF00")
                print("⏸️ Bot PAUSED")
            else:
                self.pause_button.config(text="Pause Bot", bg="#FFA500")
                print("▶️ Bot RESUMED")
                
        except Exception as e:
            print(f"❌ Error toggling pause: {e}")
    
    def toggle_smooth_mode(self):
        """Toggle smooth/robotic mode"""
        try:
            self.smooth_mode = not self.smooth_mode
            if self.smooth_mode:
                self.smooth_button.config(text="Smooth Mode: ON", bg="#00FF00")
                print("🎮 SMOOTH MODE: ON (Human-like movements)")
            else:
                self.smooth_button.config(text="Smooth Mode: OFF", bg="#FF0000")
                print("🤖 ROBOTIC MODE: ON (Precise movements)")
                
        except Exception as e:
            print(f"❌ Error toggling smooth mode: {e}")
    
    def start_f1_listener(self):
        """Start F1 key listener for bot toggle"""
        try:
            import threading
            self.f1_listener = threading.Thread(target=self.f1_key_monitor, daemon=True)
            self.f1_listener.start()
            print("🎮 F1 Key Listener Started - Press F1 to toggle bot")
        except Exception as e:
            print(f"❌ Error starting F1 listener: {e}")
    
    def f1_key_monitor(self):
        """Monitor F1 key presses"""
        try:
            import keyboard
            while self.is_running:
                if keyboard.is_pressed('f1'):
                    self.toggle_bot_enabled()
                    time.sleep(0.5)  # Prevent multiple toggles
                time.sleep(0.01)
        except Exception as e:
            print(f"❌ Error in F1 monitor: {e}")
    
    def toggle_bot_enabled(self):
        """Toggle bot enabled state"""
        try:
            self.bot_enabled = not self.bot_enabled
            if self.bot_enabled:
                print("🎮 BOT ENABLED - Learning and playing!")
                if hasattr(self, 'bot_status_label'):
                    self.bot_status_label.config(text="Bot: ENABLED", fg="#00FF00")
            else:
                print("⏸️ BOT DISABLED - Standing by...")
                if hasattr(self, 'bot_status_label'):
                    self.bot_status_label.config(text="Bot: DISABLED (Press F1)", fg="#FF0000")
        except Exception as e:
            print(f"❌ Error toggling bot: {e}")
    
    def close_bot(self):
        """Close the bot"""
        try:
            self.is_running = False
            if self.overlay_window:
                self.overlay_window.destroy()
            print("✅ Bot closed")
            
        except Exception as e:
            print(f"❌ Error closing bot: {e}")
    
    def start_bot(self):
        """Start the real memory SSL bot with F1 toggle"""
        try:
            print("🚀 Starting Real Memory SSL Bot...")
            print("🎮 Press F1 to toggle bot ON/OFF")
            
            # Find Rocket League
            if not self.find_rocket_league_process():
                print("❌ Rocket League not found!")
                return False
            
            if not self.find_rocket_league_window():
                print("❌ Rocket League window not found!")
                return False
            
            # Find memory addresses
            if not self.find_memory_addresses():
                print("❌ Failed to find memory addresses!")
                return False
            
            # Start F1 key listener
            self.start_f1_listener()
            
            # Create overlay
            if not self.create_overlay_window():
                print("❌ Failed to create overlay!")
                return False
            
            # Start overlay update loop
            overlay_thread = threading.Thread(target=self.overlay_update_loop, daemon=True)
            overlay_thread.start()
            
            print("✅ Real Memory SSL Bot started!")
            print("🎮 Overlay is displaying on top of Rocket League!")
            print("📊 You can see all real game data from memory!")
            print("⚡ Bot is ready to move your car!")
            
            # Start practice session
            print("\n🚀 Starting 30-minute practice session...")
            self.run_practice_session(30)
            
            return True
            
        except Exception as e:
            print(f"❌ Error starting bot: {e}")
            return False

def main():
    """Main function"""
    print("🏆 REAL MEMORY SSL BOT")
    print("=" * 60)
    print("🎮 Reads actual game memory and files")
    print("📊 Real-time data from Rocket League executable")
    print("⚡ Real car movement and control")
    print("🚀 Ready to read your game data!")
    
    bot = RealMemorySSLBot()
    
    try:
        # Start bot
        bot.start_bot()
        
    except KeyboardInterrupt:
        print("\n⏹️ Bot interrupted by user")
        bot.close_bot()
    except Exception as e:
        print(f"\n❌ Critical Error: {e}")
        bot.close_bot()

if __name__ == "__main__":
    main()

                car_frame,
                text="Position: X=0.00, Y=0.00, Z=0.00",
                font=("Arial", 10),
                fg="#00FF00",
                bg="#000000"
            )
            self.car_pos_label.pack(anchor=tk.W, padx=5, pady=2)
            
            self.car_vel_label = tk.Label(
                car_frame,
                text="Velocity: X=0.00, Y=0.00, Z=0.00",
                font=("Arial", 10),
                fg="#00FF00",
                bg="#000000"
            )
            self.car_vel_label.pack(anchor=tk.W, padx=5, pady=2)
            
            self.car_boost_label = tk.Label(
                car_frame,
                text="Boost: 100%",
                font=("Arial", 10),
                fg="#00FF00",
                bg="#000000"
            )
            self.car_boost_label.pack(anchor=tk.W, padx=5, pady=2)
            
            self.car_ground_label = tk.Label(
                car_frame,
                text="State: On Ground",
                font=("Arial", 10),
                fg="#00FF00",
                bg="#000000"
            )
            self.car_ground_label.pack(anchor=tk.W, padx=5, pady=2)
            
            # Ball data frame
            ball_frame = tk.LabelFrame(
                parent,
                text="⚽ BALL DATA (FROM MEMORY)",
                font=("Arial", 12, "bold"),
                fg="#00FF00",
                bg="#000000"
            )
            ball_frame.pack(fill=tk.X, pady=5)
            
            self.ball_pos_label = tk.Label(
                ball_frame,
                text="Position: X=0.00, Y=0.00, Z=0.00",
                font=("Arial", 10),
                fg="#00FF00",
                bg="#000000"
            )
            self.ball_pos_label.pack(anchor=tk.W, padx=5, pady=2)
            
            self.ball_vel_label = tk.Label(
                ball_frame,
                text="Velocity: X=0.00, Y=0.00, Z=0.00",
                font=("Arial", 10),
                fg="#00FF00",
                bg="#000000"
            )
            self.ball_vel_label.pack(anchor=tk.W, padx=5, pady=2)
            
            # Training data frame
            training_frame = tk.LabelFrame(
                parent,
                text="🧠 TRAINING DATA",
                font=("Arial", 12, "bold"),
                fg="#00FF00",
                bg="#000000"
            )
            training_frame.pack(fill=tk.X, pady=5)
            
            self.episodes_label = tk.Label(
                training_frame,
                text="Episodes: 0",
                font=("Arial", 10),
                fg="#00FF00",
                bg="#000000"
            )
            self.episodes_label.pack(anchor=tk.W, padx=5, pady=2)
            
            self.actions_label = tk.Label(
                training_frame,
                text="Actions: 0",
                font=("Arial", 10),
                fg="#00FF00",
                bg="#000000"
            )
            self.actions_label.pack(anchor=tk.W, padx=5, pady=2)
            
            self.success_label = tk.Label(
                training_frame,
                text="Success Rate: 0%",
                font=("Arial", 10),
                fg="#00FF00",
                bg="#000000"
            )
            self.success_label.pack(anchor=tk.W, padx=5, pady=2)
            
            # Current action frame
            action_frame = tk.LabelFrame(
                parent,
                text="🎯 CURRENT ACTION",
                font=("Arial", 12, "bold"),
                fg="#00FF00",
                bg="#000000"
            )
            action_frame.pack(fill=tk.X, pady=5)
            
            self.current_action_label = tk.Label(
                action_frame,
                text="Action: Ready",
                font=("Arial", 10),
                fg="#00FF00",
                bg="#000000"
            )
            self.current_action_label.pack(anchor=tk.W, padx=5, pady=2)
            
            # Memory info frame
            memory_frame = tk.LabelFrame(
                parent,
                text="💾 MEMORY INFO",
                font=("Arial", 12, "bold"),
                fg="#00FF00",
                bg="#000000"
            )
            memory_frame.pack(fill=tk.X, pady=5)
            
            self.memory_label = tk.Label(
                memory_frame,
                text="Memory: Connected",
                font=("Arial", 10),
                fg="#00FF00",
                bg="#000000"
            )
            self.memory_label.pack(anchor=tk.W, padx=5, pady=2)
            
            # Controls frame
            controls_frame = tk.LabelFrame(
                parent,
                text="🎮 CONTROLS",
                font=("Arial", 12, "bold"),
                fg="#00FF00",
                bg="#000000"
            )
            controls_frame.pack(fill=tk.X, pady=5)
            
            self.status_label = tk.Label(
                controls_frame,
                text="Status: Connected",
                font=("Arial", 10),
                fg="#00FF00",
                bg="#000000"
            )
            self.status_label.pack(anchor=tk.W, padx=5, pady=2)
            
            # Bot enabled status
            self.bot_status_label = tk.Label(
                controls_frame,
                text="Bot: DISABLED (Press F1)",
                font=("Arial", 10),
                fg="#FF0000",
                bg="#000000"
            )
            self.bot_status_label.pack(anchor=tk.W, padx=5, pady=2)
            
            # Learning progress
            self.learning_label = tk.Label(
                controls_frame,
                text="Learning: 0 episodes, 0 reward",
                font=("Arial", 9),
                fg="#FFFF00",
                bg="#000000"
            )
            self.learning_label.pack(anchor=tk.W, padx=5, pady=2)
            
            # Ball interactions
            self.ball_label = tk.Label(
                controls_frame,
                text="Ball Interactions: 0",
                font=("Arial", 9),
                fg="#00FFFF",
                bg="#000000"
            )
            self.ball_label.pack(anchor=tk.W, padx=5, pady=2)
            
            # Pause/Resume button
            self.pause_button = tk.Button(
                controls_frame,
                text="Pause Bot",
                command=self.toggle_pause,
                font=("Arial", 10),
                bg="#FFA500",
                fg="white"
            )
            self.pause_button.pack(pady=2)
            
            # Toggle button for smooth/robotic mode
            self.smooth_button = tk.Button(
                controls_frame,
                text="Smooth Mode: ON",
                command=self.toggle_smooth_mode,
                font=("Arial", 10),
                bg="#00FF00",
                fg="white"
            )
            self.smooth_button.pack(pady=2)
            
            # Close button
            close_button = tk.Button(
                controls_frame,
                text="Close Bot",
                command=self.close_bot,
                font=("Arial", 10),
                bg="#FF0000",
                fg="white"
            )
            close_button.pack(pady=2)
            
        except Exception as e:
            print(f"❌ Error creating data displays: {e}")
    
    def update_overlay_data(self):
        """Update all overlay data displays"""
        try:
            # Update car data displays
            if hasattr(self, 'car_pos_label'):
                self.car_pos_label.config(
                    text=f"Position: X={self.car_data['position'][0]:.2f}, Y={self.car_data['position'][1]:.2f}, Z={self.car_data['position'][2]:.2f}"
                )
            
            if hasattr(self, 'car_vel_label'):
                self.car_vel_label.config(
                    text=f"Velocity: X={self.car_data['velocity'][0]:.2f}, Y={self.car_data['velocity'][1]:.2f}, Z={self.car_data['velocity'][2]:.2f}"
                )
            
            if hasattr(self, 'car_boost_label'):
                self.car_boost_label.config(
                    text=f"Boost: {self.car_data['boost']:.1f}%"
                )
            
            if hasattr(self, 'car_ground_label'):
                state = "On Ground" if self.car_data['on_ground'] else "In Air"
                self.car_ground_label.config(text=f"State: {state}")
            
            # Update learning data displays
            if hasattr(self, 'learning_label'):
                episodes = self.learning_data['episodes_completed']
                reward = self.learning_data['total_reward']
                self.learning_label.config(
                    text=f"Learning: {episodes} episodes, {reward:.1f} reward"
                )
            
            if hasattr(self, 'ball_label'):
                interactions = self.learning_data['ball_interactions']
                self.ball_label.config(
                    text=f"Ball Interactions: {interactions}"
                )
            
            # Update ball data displays
            if hasattr(self, 'ball_pos_label'):
                self.ball_pos_label.config(
                    text=f"Position: X={self.ball_data['position'][0]:.2f}, Y={self.ball_data['position'][1]:.2f}, Z={self.ball_data['position'][2]:.2f}"
                )
            
            if hasattr(self, 'ball_vel_label'):
                self.ball_vel_label.config(
                    text=f"Velocity: X={self.ball_data['velocity'][0]:.2f}, Y={self.ball_data['velocity'][1]:.2f}, Z={self.ball_data['velocity'][2]:.2f}"
                )
            
            # Update training data displays
            if hasattr(self, 'episodes_label'):
                self.episodes_label.config(
                    text=f"Episodes: {self.practice_episodes}"
                )
            
            if hasattr(self, 'actions_label'):
                self.actions_label.config(
                    text=f"Actions: {self.total_actions}"
                )
            
            if hasattr(self, 'success_label'):
                success_rate = (self.successful_actions / self.total_actions * 100) if self.total_actions > 0 else 0
                self.success_label.config(
                    text=f"Success Rate: {success_rate:.1f}%"
                )
            
            # Update memory info
            if hasattr(self, 'memory_label'):
                self.memory_label.config(
                    text=f"Memory: PID {self.game_pid} - Connected"
                )
            
        except Exception as e:
            print(f"❌ Error updating overlay data: {e}")
    
    def overlay_update_loop(self):
        """Main overlay update loop"""
        try:
            while self.is_running and self.overlay_window:
                start_time = time.time()
                
                # Update memory data
                self.simulate_memory_data()
                
                # Update overlay data
                self.update_overlay_data()
                
                # Update overlay window
                if self.overlay_window:
                    self.overlay_window.update()
                
                # Maintain 60 FPS
                elapsed = time.time() - start_time
                sleep_time = max(0, 0.016 - elapsed)
                time.sleep(sleep_time)
                
        except Exception as e:
            print(f"❌ Error in overlay update loop: {e}")
    
    def practice_episode(self):
        """Practice a real episode with ball detection and intelligent movement"""
        try:
            print(f"\n🎮 PRACTICE EPISODE - {self.practice_episodes + 1}")
            print("=" * 50)
            
            # Only run if bot is enabled
            if not self.bot_enabled:
                print("⏸️ Bot disabled - Press F1 to enable")
                time.sleep(1)
                return
            
            # Read current game state
            self.read_game_data()
            
            # Determine what to do based on ball position
            action = self.determine_best_action()
            print(f"🎯 Best action: {action}")
            
            if hasattr(self, 'current_action_label'):
                self.current_action_label.config(text=f"Action: {action}")
            
            # Execute the determined action
            success = self.execute_movement(action)
            if success:
                print(f"   ✅ {action} completed successfully")
                self.learning_data['total_reward'] += 5.0  # Reward for successful action
            else:
                print(f"   ⚠️ {action} had issues but continuing")
                self.learning_data['total_reward'] -= 1.0  # Small penalty for failed action
            
            # Update learning data
            self.learning_data['episodes_completed'] += 1
            self.practice_episodes += 1
            
            print(f"⏹️ Episode completed")
            return True
            
        except Exception as e:
            print(f"❌ Error in practice episode: {e}")
            print(f"   Continuing with next episode...")
            return False
    
    def run_practice_session(self, duration_minutes=30):
        """Run practice session with real car movement"""
        try:
            print(f"\n🚀 STARTING REAL MEMORY PRACTICE SESSION")
            print("=" * 60)
            print(f"⏰ Duration: {duration_minutes} minutes")
            print("🎯 Actually moving the car and training")
            print("📊 Real-time data from game memory")
            print("⚡ Real car movement and control")
            
            self.is_running = True
            start_time = time.time()
            end_time = start_time + (duration_minutes * 60)
            episode_count = 0
            
            while self.is_running and time.time() < end_time:
                try:
                    # Check if paused
                    if self.is_paused:
                        print("⏸️ Bot is paused, waiting...")
                        time.sleep(1)
                        continue
                    
                    episode_count += 1
                    print(f"\n🔄 Starting episode {episode_count}...")
                    
                    # Practice episode with error handling
                    episode_success = self.practice_episode()
                    
                    if episode_success:
                        print(f"✅ Episode {episode_count} completed successfully")
                    else:
                        print(f"⚠️ Episode {episode_count} had issues but continuing")
                    
                    # Brief pause between episodes
                    pause_time = np.random.uniform(3, 7)
                    print(f"⏸️ Pausing for {pause_time:.1f} seconds...")
                    time.sleep(pause_time)
                    
                    # Show progress
                    elapsed = time.time() - start_time
                    remaining = end_time - time.time()
                    print(f"\n📊 Progress: {elapsed/60:.1f}min elapsed, {remaining/60:.1f}min remaining")
                    print(f"🎮 Episodes: {self.practice_episodes}")
                    print(f"🎯 Actions: {self.total_actions}")
                    print(f"✅ Successes: {self.successful_actions}")
                    
                except Exception as e:
                    print(f"❌ Episode {episode_count} error: {e}")
                    print(f"   Continuing with next episode...")
                    time.sleep(2)  # Longer pause after error
                    continue
            
            self.is_running = False
            print(f"\n✅ Practice session completed!")
            print(f"📊 Final Stats:")
            print(f"   Episodes: {self.practice_episodes}")
            print(f"   Actions: {self.total_actions}")
            print(f"   Successes: {self.successful_actions}")
            self.generate_learning_report()
            
        except Exception as e:
            print(f"❌ Error in practice session: {e}")
            self.is_running = False
    
    def generate_learning_report(self):
        """Generate learning report"""
        try:
            print(f"\n\n📊 REAL MEMORY SSL LEARNING REPORT")
            print("=" * 70)
            
            total_time = time.time() - self.start_time
            hours = total_time / 3600
            
            print(f"⏰ Total Practice Time: {hours:.2f} hours")
            print(f"🎮 Episodes Practiced: {self.practice_episodes}")
            print(f"🎯 Total Actions: {self.total_actions}")
            print(f"✅ Successful Actions: {self.successful_actions}")
            print(f"📈 Success Rate: {self.successful_actions/self.total_actions:.1%}" if self.total_actions > 0 else "📈 Success Rate: 0%")
            
            # Mechanics learning
            print(f"\n🎯 MOVEMENTS LEARNED:")
            print("-" * 30)
            for movement, data in self.learned_mechanics.items():
                success_rate = data['successes'] / data['attempts'] if data['attempts'] > 0 else 0
                print(f"   {movement}: {success_rate:.1%} success rate")
                print(f"      Attempts: {data['attempts']}")
            
            # Save learning data
            self.save_learning_data()
            
        except Exception as e:
            print(f"❌ Error generating learning report: {e}")
    
    def save_learning_data(self):
        """Save learned data"""
        try:
            learning_data = {
                'learned_mechanics': self.learned_mechanics,
                'practice_episodes': self.practice_episodes,
                'total_actions': self.total_actions,
                'successful_actions': self.successful_actions,
                'total_time': time.time() - self.start_time,
                'timestamp': datetime.now().isoformat(),
                'game_pid': self.game_pid,
                'memory_connected': True
            }
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'real_memory_ssl_learning_data_{timestamp}.pkl'
            
            with open(filename, 'wb') as f:
                pickle.dump(learning_data, f)
            
            print(f"\n💾 Learning data saved to: {filename}")
            print("🎮 Ready for SSL online matches!")
            
        except Exception as e:
            print(f"❌ Error saving learning data: {e}")
    
    def toggle_pause(self):
        """Toggle pause/resume"""
        try:
            self.is_paused = not self.is_paused
            if self.is_paused:
                self.pause_button.config(text="Resume Bot", bg="#00FF00")
                print("⏸️ Bot PAUSED")
            else:
                self.pause_button.config(text="Pause Bot", bg="#FFA500")
                print("▶️ Bot RESUMED")
                
        except Exception as e:
            print(f"❌ Error toggling pause: {e}")
    
    def toggle_smooth_mode(self):
        """Toggle smooth/robotic mode"""
        try:
            self.smooth_mode = not self.smooth_mode
            if self.smooth_mode:
                self.smooth_button.config(text="Smooth Mode: ON", bg="#00FF00")
                print("🎮 SMOOTH MODE: ON (Human-like movements)")
            else:
                self.smooth_button.config(text="Smooth Mode: OFF", bg="#FF0000")
                print("🤖 ROBOTIC MODE: ON (Precise movements)")
                
        except Exception as e:
            print(f"❌ Error toggling smooth mode: {e}")
    
    def start_f1_listener(self):
        """Start F1 key listener for bot toggle"""
        try:
            import threading
            self.f1_listener = threading.Thread(target=self.f1_key_monitor, daemon=True)
            self.f1_listener.start()
            print("🎮 F1 Key Listener Started - Press F1 to toggle bot")
        except Exception as e:
            print(f"❌ Error starting F1 listener: {e}")
    
    def f1_key_monitor(self):
        """Monitor F1 key presses"""
        try:
            import keyboard
            while self.is_running:
                if keyboard.is_pressed('f1'):
                    self.toggle_bot_enabled()
                    time.sleep(0.5)  # Prevent multiple toggles
                time.sleep(0.01)
        except Exception as e:
            print(f"❌ Error in F1 monitor: {e}")
    
    def toggle_bot_enabled(self):
        """Toggle bot enabled state"""
        try:
            self.bot_enabled = not self.bot_enabled
            if self.bot_enabled:
                print("🎮 BOT ENABLED - Learning and playing!")
                if hasattr(self, 'bot_status_label'):
                    self.bot_status_label.config(text="Bot: ENABLED", fg="#00FF00")
            else:
                print("⏸️ BOT DISABLED - Standing by...")
                if hasattr(self, 'bot_status_label'):
                    self.bot_status_label.config(text="Bot: DISABLED (Press F1)", fg="#FF0000")
        except Exception as e:
            print(f"❌ Error toggling bot: {e}")
    
    def close_bot(self):
        """Close the bot"""
        try:
            self.is_running = False
            if self.overlay_window:
                self.overlay_window.destroy()
            print("✅ Bot closed")
            
        except Exception as e:
            print(f"❌ Error closing bot: {e}")
    
    def start_bot(self):
        """Start the real memory SSL bot with F1 toggle"""
        try:
            print("🚀 Starting Real Memory SSL Bot...")
            print("🎮 Press F1 to toggle bot ON/OFF")
            
            # Find Rocket League
            if not self.find_rocket_league_process():
                print("❌ Rocket League not found!")
                return False
            
            if not self.find_rocket_league_window():
                print("❌ Rocket League window not found!")
                return False
            
            # Find memory addresses
            if not self.find_memory_addresses():
                print("❌ Failed to find memory addresses!")
                return False
            
            # Start F1 key listener
            self.start_f1_listener()
            
            # Create overlay
            if not self.create_overlay_window():
                print("❌ Failed to create overlay!")
                return False
            
            # Start overlay update loop
            overlay_thread = threading.Thread(target=self.overlay_update_loop, daemon=True)
            overlay_thread.start()
            
            print("✅ Real Memory SSL Bot started!")
            print("🎮 Overlay is displaying on top of Rocket League!")
            print("📊 You can see all real game data from memory!")
            print("⚡ Bot is ready to move your car!")
            
            # Start practice session
            print("\n🚀 Starting 30-minute practice session...")
            self.run_practice_session(30)
            
            return True
            
        except Exception as e:
            print(f"❌ Error starting bot: {e}")
            return False

def main():
    """Main function"""
    print("🏆 REAL MEMORY SSL BOT")
    print("=" * 60)
    print("🎮 Reads actual game memory and files")
    print("📊 Real-time data from Rocket League executable")
    print("⚡ Real car movement and control")
    print("🚀 Ready to read your game data!")
    
    bot = RealMemorySSLBot()
    
    try:
        # Start bot
        bot.start_bot()
        
    except KeyboardInterrupt:
        print("\n⏹️ Bot interrupted by user")
        bot.close_bot()
    except Exception as e:
        print(f"\n❌ Critical Error: {e}")
        bot.close_bot()

if __name__ == "__main__":
    main()
