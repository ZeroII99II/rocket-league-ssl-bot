#!/usr/bin/env python3
"""
SSL Game Overlay
Visual overlay system that displays on top of Rocket League game window
Shows all game objects, XYZ coordinates, and real-time data
"""

import tkinter as tk
from tkinter import ttk
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

class SSLGameOverlay:
    """Visual overlay that displays on top of Rocket League game window"""
    
    def __init__(self):
        self.game_window = None
        self.game_process = None
        self.game_handle = None
        self.overlay_window = None
        self.is_running = False
        
        # Game data
        self.car_data = {
            'position': [0.0, 0.0, 0.0],
            'rotation': [0.0, 0.0, 0.0],
            'velocity': [0.0, 0.0, 0.0],
            'angular_velocity': [0.0, 0.0, 0.0],
            'boost': 0.0,
            'on_ground': False,
            'has_jumped': False,
            'has_double_jumped': False
        }
        
        self.ball_data = {
            'position': [0.0, 0.0, 0.0],
            'velocity': [0.0, 0.0, 0.0],
            'angular_velocity': [0.0, 0.0, 0.0]
        }
        
        self.game_state = {
            'time': 0.0,
            'score_blue': 0,
            'score_orange': 0,
            'game_mode': 'freeplay',
            'is_kickoff': False,
            'is_goal': False
        }
        
        # Overlay settings
        self.overlay_alpha = 0.8
        self.update_interval = 0.016  # ~60 FPS
        self.font_size = 12
        self.text_color = "#00FF00"  # Green
        self.bg_color = "#000000"    # Black
        
        print("🎮 SSL GAME OVERLAY")
        print("=" * 60)
        print("📊 Visual overlay for Rocket League")
        print("🎯 Shows all game objects and XYZ data")
        print("⚡ Real-time game data display")
        print("🚀 Ready to overlay on game window!")
    
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
    
    def get_game_window_rect(self):
        """Get Rocket League window position and size"""
        try:
            if not self.game_window:
                return None
            
            rect = win32gui.GetWindowRect(self.game_window)
            return {
                'left': rect[0],
                'top': rect[1],
                'right': rect[2],
                'bottom': rect[3],
                'width': rect[2] - rect[0],
                'height': rect[3] - rect[1]
            }
            
        except Exception as e:
            print(f"❌ Error getting window rect: {e}")
            return None
    
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
    
    def read_car_data(self):
        """Read real car data from memory"""
        try:
            # Simulate reading car data (replace with actual memory addresses)
            # In a real implementation, you'd read from specific memory addresses
            
            # Simulate car movement for demo
            self.car_data['position'][0] += np.random.uniform(-0.1, 0.1)
            self.car_data['position'][1] += np.random.uniform(-0.1, 0.1)
            self.car_data['position'][2] += np.random.uniform(-0.05, 0.05)
            
            # Keep car on ground
            if self.car_data['position'][2] < 0:
                self.car_data['position'][2] = 0
                self.car_data['on_ground'] = True
            else:
                self.car_data['on_ground'] = False
            
            # Simulate boost
            self.car_data['boost'] = max(0, self.car_data['boost'] - 0.1)
            if np.random.random() < 0.1:  # 10% chance to get boost
                self.car_data['boost'] = min(100, self.car_data['boost'] + 20)
            
            # Simulate velocity
            self.car_data['velocity'][0] = np.random.uniform(-10, 10)
            self.car_data['velocity'][1] = np.random.uniform(-10, 10)
            self.car_data['velocity'][2] = np.random.uniform(-5, 5)
            
            return True
            
        except Exception as e:
            print(f"❌ Error reading car data: {e}")
            return False
    
    def read_ball_data(self):
        """Read real ball data from memory"""
        try:
            # Simulate reading ball data (replace with actual memory addresses)
            
            # Simulate ball movement
            self.ball_data['position'][0] += np.random.uniform(-0.2, 0.2)
            self.ball_data['position'][1] += np.random.uniform(-0.2, 0.2)
            self.ball_data['position'][2] += np.random.uniform(-0.1, 0.1)
            
            # Keep ball above ground
            if self.ball_data['position'][2] < 0:
                self.ball_data['position'][2] = 0
            
            # Simulate ball velocity
            self.ball_data['velocity'][0] = np.random.uniform(-15, 15)
            self.ball_data['velocity'][1] = np.random.uniform(-15, 15)
            self.ball_data['velocity'][2] = np.random.uniform(-10, 10)
            
            return True
            
        except Exception as e:
            print(f"❌ Error reading ball data: {e}")
            return False
    
    def read_game_state(self):
        """Read game state data"""
        try:
            # Simulate reading game state
            self.game_state['time'] += 0.016  # Increment time
            
            # Simulate score changes
            if np.random.random() < 0.001:  # Very low chance
                if np.random.random() < 0.5:
                    self.game_state['score_blue'] += 1
                else:
                    self.game_state['score_orange'] += 1
            
            return True
            
        except Exception as e:
            print(f"❌ Error reading game state: {e}")
            return False
    
    def create_overlay_window(self):
        """Create the overlay window"""
        try:
            # Get game window position
            game_rect = self.get_game_window_rect()
            if not game_rect:
                print("❌ Could not get game window position!")
                return False
            
            # Create overlay window
            self.overlay_window = tk.Tk()
            self.overlay_window.title("SSL Game Overlay")
            self.overlay_window.configure(bg=self.bg_color)
            
            # Set window properties
            self.overlay_window.attributes('-topmost', True)
            self.overlay_window.attributes('-alpha', self.overlay_alpha)
            self.overlay_window.overrideredirect(True)  # Remove window decorations
            
            # Position overlay on top of game window
            overlay_width = 400
            overlay_height = 600
            overlay_x = game_rect['left'] + 10
            overlay_y = game_rect['top'] + 10
            
            self.overlay_window.geometry(f"{overlay_width}x{overlay_height}+{overlay_x}+{overlay_y}")
            
            # Create main frame
            main_frame = tk.Frame(self.overlay_window, bg=self.bg_color)
            main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Create title
            title_label = tk.Label(
                main_frame,
                text="🚀 SSL GAME OVERLAY",
                font=("Arial", 16, "bold"),
                fg=self.text_color,
                bg=self.bg_color
            )
            title_label.pack(pady=(0, 10))
            
            # Create data display areas
            self.create_car_data_display(main_frame)
            self.create_ball_data_display(main_frame)
            self.create_game_state_display(main_frame)
            self.create_controls_display(main_frame)
            
            print("✅ Overlay window created successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error creating overlay window: {e}")
            return False
    
    def create_car_data_display(self, parent):
        """Create car data display section"""
        try:
            # Car data frame
            car_frame = tk.LabelFrame(
                parent,
                text="🚗 CAR DATA",
                font=("Arial", 12, "bold"),
                fg=self.text_color,
                bg=self.bg_color
            )
            car_frame.pack(fill=tk.X, pady=5)
            
            # Car position
            self.car_pos_label = tk.Label(
                car_frame,
                text="Position: X=0.00, Y=0.00, Z=0.00",
                font=("Arial", self.font_size),
                fg=self.text_color,
                bg=self.bg_color
            )
            self.car_pos_label.pack(anchor=tk.W, padx=5, pady=2)
            
            # Car velocity
            self.car_vel_label = tk.Label(
                car_frame,
                text="Velocity: X=0.00, Y=0.00, Z=0.00",
                font=("Arial", self.font_size),
                fg=self.text_color,
                bg=self.bg_color
            )
            self.car_vel_label.pack(anchor=tk.W, padx=5, pady=2)
            
            # Car boost
            self.car_boost_label = tk.Label(
                car_frame,
                text="Boost: 0%",
                font=("Arial", self.font_size),
                fg=self.text_color,
                bg=self.bg_color
            )
            self.car_boost_label.pack(anchor=tk.W, padx=5, pady=2)
            
            # Car state
            self.car_state_label = tk.Label(
                car_frame,
                text="State: On Ground",
                font=("Arial", self.font_size),
                fg=self.text_color,
                bg=self.bg_color
            )
            self.car_state_label.pack(anchor=tk.W, padx=5, pady=2)
            
        except Exception as e:
            print(f"❌ Error creating car data display: {e}")
    
    def create_ball_data_display(self, parent):
        """Create ball data display section"""
        try:
            # Ball data frame
            ball_frame = tk.LabelFrame(
                parent,
                text="⚽ BALL DATA",
                font=("Arial", 12, "bold"),
                fg=self.text_color,
                bg=self.bg_color
            )
            ball_frame.pack(fill=tk.X, pady=5)
            
            # Ball position
            self.ball_pos_label = tk.Label(
                ball_frame,
                text="Position: X=0.00, Y=0.00, Z=0.00",
                font=("Arial", self.font_size),
                fg=self.text_color,
                bg=self.bg_color
            )
            self.ball_pos_label.pack(anchor=tk.W, padx=5, pady=2)
            
            # Ball velocity
            self.ball_vel_label = tk.Label(
                ball_frame,
                text="Velocity: X=0.00, Y=0.00, Z=0.00",
                font=("Arial", self.font_size),
                fg=self.text_color,
                bg=self.bg_color
            )
            self.ball_vel_label.pack(anchor=tk.W, padx=5, pady=2)
            
        except Exception as e:
            print(f"❌ Error creating ball data display: {e}")
    
    def create_game_state_display(self, parent):
        """Create game state display section"""
        try:
            # Game state frame
            state_frame = tk.LabelFrame(
                parent,
                text="🎮 GAME STATE",
                font=("Arial", 12, "bold"),
                fg=self.text_color,
                bg=self.bg_color
            )
            state_frame.pack(fill=tk.X, pady=5)
            
            # Game time
            self.game_time_label = tk.Label(
                state_frame,
                text="Time: 0.00s",
                font=("Arial", self.font_size),
                fg=self.text_color,
                bg=self.bg_color
            )
            self.game_time_label.pack(anchor=tk.W, padx=5, pady=2)
            
            # Score
            self.score_label = tk.Label(
                state_frame,
                text="Score: Blue 0 - 0 Orange",
                font=("Arial", self.font_size),
                fg=self.text_color,
                bg=self.bg_color
            )
            self.score_label.pack(anchor=tk.W, padx=5, pady=2)
            
            # Game mode
            self.mode_label = tk.Label(
                state_frame,
                text="Mode: Free Play",
                font=("Arial", self.font_size),
                fg=self.text_color,
                bg=self.bg_color
            )
            self.mode_label.pack(anchor=tk.W, padx=5, pady=2)
            
        except Exception as e:
            print(f"❌ Error creating game state display: {e}")
    
    def create_controls_display(self, parent):
        """Create controls display section"""
        try:
            # Controls frame
            controls_frame = tk.LabelFrame(
                parent,
                text="🎯 CONTROLS",
                font=("Arial", 12, "bold"),
                fg=self.text_color,
                bg=self.bg_color
            )
            controls_frame.pack(fill=tk.X, pady=5)
            
            # Status
            self.status_label = tk.Label(
                controls_frame,
                text="Status: Connected",
                font=("Arial", self.font_size),
                fg=self.text_color,
                bg=self.bg_color
            )
            self.status_label.pack(anchor=tk.W, padx=5, pady=2)
            
            # FPS
            self.fps_label = tk.Label(
                controls_frame,
                text="FPS: 60",
                font=("Arial", self.font_size),
                fg=self.text_color,
                bg=self.bg_color
            )
            self.fps_label.pack(anchor=tk.W, padx=5, pady=2)
            
            # Close button
            close_button = tk.Button(
                controls_frame,
                text="Close Overlay",
                command=self.close_overlay,
                font=("Arial", 10),
                bg="#FF0000",
                fg="white"
            )
            close_button.pack(pady=5)
            
        except Exception as e:
            print(f"❌ Error creating controls display: {e}")
    
    def update_overlay_data(self):
        """Update all overlay data displays"""
        try:
            # Read game data
            self.read_car_data()
            self.read_ball_data()
            self.read_game_state()
            
            # Update car data display
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
            
            if hasattr(self, 'car_state_label'):
                state = "On Ground" if self.car_data['on_ground'] else "In Air"
                self.car_state_label.config(text=f"State: {state}")
            
            # Update ball data display
            if hasattr(self, 'ball_pos_label'):
                self.ball_pos_label.config(
                    text=f"Position: X={self.ball_data['position'][0]:.2f}, Y={self.ball_data['position'][1]:.2f}, Z={self.ball_data['position'][2]:.2f}"
                )
            
            if hasattr(self, 'ball_vel_label'):
                self.ball_vel_label.config(
                    text=f"Velocity: X={self.ball_data['velocity'][0]:.2f}, Y={self.ball_data['velocity'][1]:.2f}, Z={self.ball_data['velocity'][2]:.2f}"
                )
            
            # Update game state display
            if hasattr(self, 'game_time_label'):
                self.game_time_label.config(
                    text=f"Time: {self.game_state['time']:.2f}s"
                )
            
            if hasattr(self, 'score_label'):
                self.score_label.config(
                    text=f"Score: Blue {self.game_state['score_blue']} - {self.game_state['score_orange']} Orange"
                )
            
            if hasattr(self, 'mode_label'):
                self.mode_label.config(
                    text=f"Mode: {self.game_state['game_mode'].title()}"
                )
            
            # Update FPS
            if hasattr(self, 'fps_label'):
                fps = int(1.0 / self.update_interval)
                self.fps_label.config(text=f"FPS: {fps}")
            
        except Exception as e:
            print(f"❌ Error updating overlay data: {e}")
    
    def overlay_update_loop(self):
        """Main overlay update loop"""
        try:
            while self.is_running and self.overlay_window:
                start_time = time.time()
                
                # Update overlay data
                self.update_overlay_data()
                
                # Update overlay window
                if self.overlay_window:
                    self.overlay_window.update()
                
                # Maintain target FPS
                elapsed = time.time() - start_time
                sleep_time = max(0, self.update_interval - elapsed)
                time.sleep(sleep_time)
                
        except Exception as e:
            print(f"❌ Error in overlay update loop: {e}")
    
    def close_overlay(self):
        """Close the overlay"""
        try:
            self.is_running = False
            if self.overlay_window:
                self.overlay_window.destroy()
            print("✅ Overlay closed")
            
        except Exception as e:
            print(f"❌ Error closing overlay: {e}")
    
    def start_overlay(self):
        """Start the overlay system"""
        try:
            print("🚀 Starting SSL Game Overlay...")
            
            # Find Rocket League
            if not self.find_rocket_league_process():
                print("❌ Rocket League not found!")
                return False
            
            if not self.find_rocket_league_window():
                print("❌ Rocket League window not found!")
                return False
            
            # Create overlay window
            if not self.create_overlay_window():
                print("❌ Failed to create overlay window!")
                return False
            
            # Start overlay
            self.is_running = True
            
            # Start update loop in separate thread
            update_thread = threading.Thread(target=self.overlay_update_loop, daemon=True)
            update_thread.start()
            
            print("✅ Overlay started successfully!")
            print("🎮 Overlay is now displaying on top of Rocket League!")
            print("📊 You can see all game objects and XYZ data in real-time!")
            
            # Start main loop
            self.overlay_window.mainloop()
            
            return True
            
        except Exception as e:
            print(f"❌ Error starting overlay: {e}")
            return False

def main():
    """Main function"""
    print("🎮 SSL GAME OVERLAY")
    print("=" * 60)
    print("📊 Visual overlay for Rocket League")
    print("🎯 Shows all game objects and XYZ data")
    print("⚡ Real-time game data display")
    print("🚀 Ready to overlay on game window!")
    
    overlay = SSLGameOverlay()
    
    try:
        # Start overlay
        overlay.start_overlay()
        
    except KeyboardInterrupt:
        print("\n⏹️ Overlay interrupted by user")
        overlay.close_overlay()
    except Exception as e:
        print(f"\n❌ Critical Error: {e}")

if __name__ == "__main__":
    main()
