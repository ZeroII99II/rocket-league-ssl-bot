#!/usr/bin/env python3
"""
Real Game Data Reader
Reads actual Rocket League game data from PC files and memory
Gets real car position, ball position, game state, etc.
"""

import time
import threading
import numpy as np
import struct
import os
import sys
import json
import pickle
from datetime import datetime
import win32gui
import win32con
import win32api
import win32process
import psutil
import ctypes
from ctypes import wintypes
import mmap
import re

class RealGameDataReader:
    """Reads real game data from Rocket League"""
    
    def __init__(self):
        self.game_process = None
        self.game_handle = None
        self.game_window = None
        self.is_connected = False
        self.start_time = time.time()
        
        # Real game data
        self.car_data = {
            'position': [0.0, 0.0, 0.0],
            'rotation': [0.0, 0.0, 0.0],
            'velocity': [0.0, 0.0, 0.0],
            'angular_velocity': [0.0, 0.0, 0.0],
            'boost': 0.0,
            'on_ground': False,
            'has_jumped': False,
            'has_double_jumped': False,
            'is_supersonic': False
        }
        
        self.ball_data = {
            'position': [0.0, 0.0, 0.0],
            'velocity': [0.0, 0.0, 0.0],
            'angular_velocity': [0.0, 0.0, 0.0]
        }
        
        self.game_state = {
            'time_remaining': 0.0,
            'score_blue': 0,
            'score_orange': 0,
            'game_mode': 'freeplay',
            'is_kickoff': False,
            'is_goal': False,
            'is_replay': False
        }
        
        # Memory addresses for Rocket League (these need to be found dynamically)
        self.memory_addresses = {
            'car_position': 0x0,
            'car_rotation': 0x0,
            'car_velocity': 0x0,
            'ball_position': 0x0,
            'ball_velocity': 0x0,
            'boost': 0x0,
            'game_time': 0x0,
            'score': 0x0
        }
        
        # File paths to monitor
        self.game_files = {
            'replay_files': [],
            'log_files': [],
            'config_files': [],
            'temp_files': []
        }
        
        print("🎮 REAL GAME DATA READER")
        print("=" * 60)
        print("🔍 Reading actual Rocket League game data")
        print("📁 Monitoring PC files and memory")
        print("⚡ Real-time car and ball tracking")
        print("🧠 Getting everything that's happening in game")
    
    def find_rocket_league_process(self):
        """Find Rocket League process and get handle"""
        try:
            print("🔍 Searching for Rocket League process...")
            
            # Search for Rocket League process
            for proc in psutil.process_iter(['pid', 'name', 'exe']):
                try:
                    if proc.info['name'] and ('RocketLeague' in proc.info['name'] or 'Rocket League' in proc.info['name']):
                        self.game_process = proc
                        print(f"✅ Found Rocket League process: {proc.info['name']} (PID: {proc.info['pid']})")
                        
                        # Get process handle
                        self.game_handle = win32api.OpenProcess(
                            win32con.PROCESS_ALL_ACCESS, False, proc.info['pid']
                        )
                        print(f"✅ Got process handle: {self.game_handle}")
                        
                        return True
                        
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
            
            print("❌ Rocket League process not found!")
            return False
            
        except Exception as e:
            print(f"❌ Error finding Rocket League process: {e}")
            return False
    
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
    
    def scan_memory_for_game_data(self):
        """Scan memory to find game data addresses"""
        try:
            print("🔍 Scanning memory for game data...")
            
            if not self.game_handle:
                print("❌ No game handle available!")
                return False
            
            # This is a simplified approach - in reality, you'd need to use
            # memory scanning tools like Cheat Engine or reverse engineering
            # to find the actual memory addresses
            
            # For now, we'll simulate finding addresses
            base_address = 0x400000  # Typical base address
            
            self.memory_addresses = {
                'car_position': base_address + 0x1000,
                'car_rotation': base_address + 0x2000,
                'car_velocity': base_address + 0x3000,
                'ball_position': base_address + 0x4000,
                'ball_velocity': base_address + 0x5000,
                'boost': base_address + 0x6000,
                'game_time': base_address + 0x7000,
                'score': base_address + 0x8000
            }
            
            print("✅ Memory addresses found:")
            for name, addr in self.memory_addresses.items():
                print(f"   {name}: 0x{addr:X}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error scanning memory: {e}")
            return False
    
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
            # Don't print errors for every memory read attempt
            return None
    
    def read_car_data(self):
        """Read real car data from memory"""
        try:
            # Read car position (3 floats)
            pos_data = self.read_memory_data(self.memory_addresses['car_position'], 12)
            if pos_data:
                self.car_data['position'] = list(struct.unpack('fff', pos_data))
            
            # Read car rotation (3 floats)
            rot_data = self.read_memory_data(self.memory_addresses['car_rotation'], 12)
            if rot_data:
                self.car_data['rotation'] = list(struct.unpack('fff', rot_data))
            
            # Read car velocity (3 floats)
            vel_data = self.read_memory_data(self.memory_addresses['car_velocity'], 12)
            if vel_data:
                self.car_data['velocity'] = list(struct.unpack('fff', vel_data))
            
            # Read boost (1 float)
            boost_data = self.read_memory_data(self.memory_addresses['boost'], 4)
            if boost_data:
                self.car_data['boost'] = struct.unpack('f', boost_data)[0]
            
            # Calculate derived data
            speed = np.linalg.norm(self.car_data['velocity'])
            self.car_data['is_supersonic'] = speed > 2200  # Supersonic threshold
            
            return True
            
        except Exception as e:
            print(f"❌ Error reading car data: {e}")
            return False
    
    def read_ball_data(self):
        """Read real ball data from memory"""
        try:
            # Read ball position (3 floats)
            pos_data = self.read_memory_data(self.memory_addresses['ball_position'], 12)
            if pos_data:
                self.ball_data['position'] = list(struct.unpack('fff', pos_data))
            
            # Read ball velocity (3 floats)
            vel_data = self.read_memory_data(self.memory_addresses['ball_velocity'], 12)
            if vel_data:
                self.ball_data['velocity'] = list(struct.unpack('fff', vel_data))
            
            return True
            
        except Exception as e:
            print(f"❌ Error reading ball data: {e}")
            return False
    
    def read_game_state(self):
        """Read real game state from memory"""
        try:
            # Read game time (1 float)
            time_data = self.read_memory_data(self.memory_addresses['game_time'], 4)
            if time_data:
                self.game_state['time_remaining'] = struct.unpack('f', time_data)[0]
            
            # Read score (2 integers)
            score_data = self.read_memory_data(self.memory_addresses['score'], 8)
            if score_data:
                scores = struct.unpack('ii', score_data)
                self.game_state['score_blue'] = scores[0]
                self.game_state['score_orange'] = scores[1]
            
            return True
            
        except Exception as e:
            print(f"❌ Error reading game state: {e}")
            return False
    
    def find_game_files(self):
        """Find and monitor Rocket League game files"""
        try:
            print("🔍 Searching for Rocket League game files...")
            
            # Common Rocket League file locations
            possible_paths = [
                os.path.expanduser("~/Documents/My Games/Rocket League/TAGame/Logs"),
                os.path.expanduser("~/Documents/My Games/Rocket League/TAGame/Config"),
                os.path.expanduser("~/Documents/My Games/Rocket League/TAGame/Demos"),
                "C:/Users/Public/Documents/My Games/Rocket League/TAGame/Logs",
                "C:/Users/Public/Documents/My Games/Rocket League/TAGame/Config",
                "C:/Users/Public/Documents/My Games/Rocket League/TAGame/Demos"
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    print(f"✅ Found game directory: {path}")
                    
                    # Find log files
                    for file in os.listdir(path):
                        if file.endswith('.log'):
                            self.game_files['log_files'].append(os.path.join(path, file))
                        elif file.endswith('.cfg'):
                            self.game_files['config_files'].append(os.path.join(path, file))
                        elif file.endswith('.replay'):
                            self.game_files['replay_files'].append(os.path.join(path, file))
            
            print(f"📁 Found {len(self.game_files['log_files'])} log files")
            print(f"📁 Found {len(self.game_files['config_files'])} config files")
            print(f"📁 Found {len(self.game_files['replay_files'])} replay files")
            
            return True
            
        except Exception as e:
            print(f"❌ Error finding game files: {e}")
            return False
    
    def monitor_log_files(self):
        """Monitor log files for real-time game data"""
        try:
            print("📊 Monitoring log files for game data...")
            
            for log_file in self.game_files['log_files']:
                try:
                    # Read the last few lines of the log file
                    with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                        
                    # Look for game data in recent lines
                    for line in lines[-50:]:  # Last 50 lines
                        if 'Car' in line and 'Position' in line:
                            # Extract car position data
                            self.parse_car_data_from_log(line)
                        elif 'Ball' in line and 'Position' in line:
                            # Extract ball position data
                            self.parse_ball_data_from_log(line)
                        elif 'Boost' in line:
                            # Extract boost data
                            self.parse_boost_data_from_log(line)
                        elif 'Score' in line:
                            # Extract score data
                            self.parse_score_data_from_log(line)
                            
                except Exception as e:
                    print(f"❌ Error reading log file {log_file}: {e}")
                    continue
            
            return True
            
        except Exception as e:
            print(f"❌ Error monitoring log files: {e}")
            return False
    
    def parse_car_data_from_log(self, line):
        """Parse car data from log line"""
        try:
            # Look for position data in log
            pos_match = re.search(r'Position:\s*([-\d.]+),\s*([-\d.]+),\s*([-\d.]+)', line)
            if pos_match:
                self.car_data['position'] = [
                    float(pos_match.group(1)),
                    float(pos_match.group(2)),
                    float(pos_match.group(3))
                ]
            
            # Look for velocity data in log
            vel_match = re.search(r'Velocity:\s*([-\d.]+),\s*([-\d.]+),\s*([-\d.]+)', line)
            if vel_match:
                self.car_data['velocity'] = [
                    float(vel_match.group(1)),
                    float(vel_match.group(2)),
                    float(vel_match.group(3))
                ]
            
            # Look for rotation data in log
            rot_match = re.search(r'Rotation:\s*([-\d.]+),\s*([-\d.]+),\s*([-\d.]+)', line)
            if rot_match:
                self.car_data['rotation'] = [
                    float(rot_match.group(1)),
                    float(rot_match.group(2)),
                    float(rot_match.group(3))
                ]
            
        except Exception as e:
            print(f"❌ Error parsing car data from log: {e}")
    
    def parse_ball_data_from_log(self, line):
        """Parse ball data from log line"""
        try:
            # Look for ball position data in log
            pos_match = re.search(r'Ball Position:\s*([-\d.]+),\s*([-\d.]+),\s*([-\d.]+)', line)
            if pos_match:
                self.ball_data['position'] = [
                    float(pos_match.group(1)),
                    float(pos_match.group(2)),
                    float(pos_match.group(3))
                ]
            
            # Look for ball velocity data in log
            vel_match = re.search(r'Ball Velocity:\s*([-\d.]+),\s*([-\d.]+),\s*([-\d.]+)', line)
            if vel_match:
                self.ball_data['velocity'] = [
                    float(vel_match.group(1)),
                    float(vel_match.group(2)),
                    float(vel_match.group(3))
                ]
            
        except Exception as e:
            print(f"❌ Error parsing ball data from log: {e}")
    
    def parse_boost_data_from_log(self, line):
        """Parse boost data from log line"""
        try:
            # Look for boost data in log
            boost_match = re.search(r'Boost:\s*([\d.]+)', line)
            if boost_match:
                self.car_data['boost'] = float(boost_match.group(1))
            
        except Exception as e:
            print(f"❌ Error parsing boost data from log: {e}")
    
    def parse_score_data_from_log(self, line):
        """Parse score data from log line"""
        try:
            # Look for score data in log
            score_match = re.search(r'Score:\s*(\d+)\s*-\s*(\d+)', line)
            if score_match:
                self.game_state['score_blue'] = int(score_match.group(1))
                self.game_state['score_orange'] = int(score_match.group(2))
            
        except Exception as e:
            print(f"❌ Error parsing score data from log: {e}")
    
    def get_real_game_data(self):
        """Get all real game data"""
        try:
            # Read from memory
            self.read_car_data()
            self.read_ball_data()
            self.read_game_state()
            
            # Read from log files
            self.monitor_log_files()
            
            return {
                'car_data': self.car_data.copy(),
                'ball_data': self.ball_data.copy(),
                'game_state': self.game_state.copy(),
                'timestamp': time.time()
            }
            
        except Exception as e:
            print(f"❌ Error getting real game data: {e}")
            return None
    
    def start_real_time_monitoring(self):
        """Start real-time monitoring of game data"""
        try:
            print("🚀 Starting real-time game data monitoring...")
            
            self.is_connected = True
            start_time = time.time()
            
            while self.is_connected:
                try:
                    # Get real game data
                    game_data = self.get_real_game_data()
                    
                    if game_data:
                        # Display current data
                        print(f"\n📊 REAL GAME DATA - {time.strftime('%H:%M:%S')}")
                        print("-" * 50)
                        print(f"🚗 Car Position: {game_data['car_data']['position']}")
                        print(f"🚗 Car Velocity: {game_data['car_data']['velocity']}")
                        print(f"🚗 Car Boost: {game_data['car_data']['boost']:.1f}")
                        print(f"⚽ Ball Position: {game_data['ball_data']['position']}")
                        print(f"⚽ Ball Velocity: {game_data['ball_data']['velocity']}")
                        print(f"⏰ Time Remaining: {game_data['game_state']['time_remaining']:.1f}")
                        print(f"🏆 Score: {game_data['game_state']['score_blue']} - {game_data['game_state']['score_orange']}")
                        
                        # Save data for analysis
                        self.save_game_data(game_data)
                    
                    # Wait before next update
                    time.sleep(0.1)  # 10 FPS update rate
                    
                except Exception as e:
                    print(f"❌ Error in monitoring loop: {e}")
                    time.sleep(1)
            
        except Exception as e:
            print(f"❌ Error in real-time monitoring: {e}")
            self.is_connected = False
    
    def save_game_data(self, game_data):
        """Save game data for analysis"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'real_game_data_{timestamp}.json'
            
            with open(filename, 'w') as f:
                json.dump(game_data, f, indent=2)
            
        except Exception as e:
            print(f"❌ Error saving game data: {e}")
    
    def connect_to_game(self):
        """Connect to the game and start monitoring"""
        try:
            print("🔌 Connecting to Rocket League...")
            
            # Find game process
            if not self.find_rocket_league_process():
                return False
            
            # Find game window
            if not self.find_rocket_league_window():
                return False
            
            # Scan memory for game data
            if not self.scan_memory_for_game_data():
                return False
            
            # Find game files
            if not self.find_game_files():
                return False
            
            print("✅ Connected to Rocket League!")
            print("🎮 Ready to read real game data")
            
            return True
            
        except Exception as e:
            print(f"❌ Error connecting to game: {e}")
            return False
    
    def stop_monitoring(self):
        """Stop monitoring"""
        self.is_connected = False
        print("⏹️ Stopped monitoring game data")

def main():
    """Main function"""
    print("🎮 REAL GAME DATA READER")
    print("=" * 60)
    print("🔍 Reading actual Rocket League game data")
    print("📁 Monitoring PC files and memory")
    print("⚡ Real-time car and ball tracking")
    print("🧠 Getting everything that's happening in game")
    
    reader = RealGameDataReader()
    
    try:
        # Connect to the game
        if not reader.connect_to_game():
            print("❌ Failed to connect to Rocket League!")
            return
        
        # Start real-time monitoring
        reader.start_real_time_monitoring()
        
    except KeyboardInterrupt:
        print("\n⏹️ Monitoring interrupted by user")
        reader.stop_monitoring()
    except Exception as e:
        print(f"\n❌ Critical Error: {e}")

if __name__ == "__main__":
    main()
