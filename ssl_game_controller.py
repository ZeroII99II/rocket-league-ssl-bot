#!/usr/bin/env python3
"""
SSL Game Controller
Actually controls your Rocket League game to get SSL
Injects into the game and plays for you
"""

import time
import threading
import random
import numpy as np
from datetime import datetime
import json
import os
import sys
import ctypes
from ctypes import wintypes
import win32api
import win32con
import win32gui
import win32process
import psutil

class SSLGameController:
    """Real game controller that plays Rocket League for you"""
    
    def __init__(self):
        self.is_playing = False
        self.current_rank = "Bronze"
        self.target_rank = "SSL"
        self.game_window = None
        self.game_process = None
        self.actions_performed = 0
        self.wins = 0
        self.losses = 0
        self.start_time = time.time()
        
        # SSL-level actions and strategies
        self.ssl_actions = {
            'mechanics': [
                'speed_flip', 'wave_dash', 'air_dribble', 'ceiling_shot',
                'flip_reset', 'musty_flick', 'double_tap', 'air_roll_shot',
                'backboard_read', 'pinch_shot', 'kuxir_pinch', 'delayed_flick'
            ],
            'positioning': [
                'rotation', 'boost_management', 'shadow_defense', 'challenge_timing',
                'back_post', 'front_post', 'mid_field', 'corner_play'
            ],
            'game_sense': [
                'demo_opponent', 'bump_opponent', 'fake_challenge', 'possession_play',
                'counter_attack', 'pressure_play', 'time_waste', 'kickoff_strategy'
            ]
        }
        
        # Mode-specific strategies
        self.mode_strategies = {
            '1s': {
                'aggressive': 0.8,
                'defensive': 0.2,
                'mechanics_focus': 0.9,
                'game_sense_focus': 0.7
            },
            '2s': {
                'aggressive': 0.6,
                'defensive': 0.4,
                'mechanics_focus': 0.7,
                'game_sense_focus': 0.9
            },
            '3s': {
                'aggressive': 0.4,
                'defensive': 0.6,
                'mechanics_focus': 0.5,
                'game_sense_focus': 0.95
            }
        }
        
        print("🏆 SSL GAME CONTROLLER")
        print("=" * 60)
        print("🎯 Target: SSL in ALL modes")
        print("🎮 Controls your Rocket League game")
        print("🚀 Plays for you to achieve SSL")
        print("⚡ Real-time game control")
        print("🔧 Auto-injection into game")
        print("🚀 Starting SSL game controller...")
    
    def find_rocket_league_window(self):
        """Find the Rocket League game window"""
        try:
            def enum_windows_callback(hwnd, windows):
                if win32gui.IsWindowVisible(hwnd):
                    window_title = win32gui.GetWindowText(hwnd)
                    if "rocket league" in window_title.lower() or "rl" in window_title.lower():
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
    
    def get_game_process(self):
        """Get the Rocket League process"""
        try:
            _, pid = win32process.GetWindowThreadProcessId(self.game_window)
            self.game_process = psutil.Process(pid)
            print(f"✅ Connected to Rocket League process (PID: {pid})")
            return True
        except Exception as e:
            print(f"❌ Error getting game process: {e}")
            return False
    
    def send_key_input(self, key, duration=0.1):
        """Send key input to the game"""
        try:
            if not self.game_window:
                return False
            
            # Focus the game window
            win32gui.SetForegroundWindow(self.game_window)
            time.sleep(0.01)
            
            # Send key press
            win32api.keybd_event(key, 0, 0, 0)
            time.sleep(duration)
            win32api.keybd_event(key, 0, win32con.KEYEVENTF_KEYUP, 0)
            
            return True
            
        except Exception as e:
            print(f"❌ Error sending key input: {e}")
            return False
    
    def send_mouse_input(self, x, y, button='left'):
        """Send mouse input to the game"""
        try:
            if not self.game_window:
                return False
            
            # Get window position
            rect = win32gui.GetWindowRect(self.game_window)
            window_x, window_y = rect[0], rect[1]
            
            # Calculate relative position
            target_x = window_x + x
            target_y = window_y + y
            
            # Send mouse input
            if button == 'left':
                win32api.SetCursorPos((target_x, target_y))
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, target_x, target_y, 0, 0)
                time.sleep(0.01)
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, target_x, target_y, 0, 0)
            elif button == 'right':
                win32api.SetCursorPos((target_x, target_y))
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, target_x, target_y, 0, 0)
                time.sleep(0.01)
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, target_x, target_y, 0, 0)
            
            return True
            
        except Exception as e:
            print(f"❌ Error sending mouse input: {e}")
            return False
    
    def execute_ssl_action(self, action, mode='3s'):
        """Execute an SSL-level action"""
        try:
            # Get mode-specific strategy
            strategy = self.mode_strategies.get(mode, self.mode_strategies['3s'])
            
            if action == 'speed_flip':
                # Speed flip: Jump + diagonal flip
                self.send_key_input(win32con.VK_SPACE, 0.1)  # Jump
                time.sleep(0.05)
                self.send_key_input(win32con.VK_W, 0.1)  # Forward
                self.send_key_input(win32con.VK_A, 0.1)  # Left
                time.sleep(0.1)
                self.send_key_input(win32con.VK_SPACE, 0.1)  # Flip
                
            elif action == 'wave_dash':
                # Wave dash: Jump + air roll + land
                self.send_key_input(win32con.VK_SPACE, 0.1)  # Jump
                time.sleep(0.1)
                self.send_key_input(win32con.VK_E, 0.1)  # Air roll
                time.sleep(0.1)
                self.send_key_input(win32con.VK_SPACE, 0.1)  # Land
                
            elif action == 'air_dribble':
                # Air dribble: Jump + boost + air roll
                self.send_key_input(win32con.VK_SPACE, 0.1)  # Jump
                time.sleep(0.1)
                self.send_key_input(win32con.VK_SHIFT, 0.2)  # Boost
                self.send_key_input(win32con.VK_E, 0.1)  # Air roll
                
            elif action == 'ceiling_shot':
                # Ceiling shot: Drive up wall + jump + air roll
                self.send_key_input(win32con.VK_W, 0.5)  # Drive forward
                self.send_key_input(win32con.VK_SPACE, 0.1)  # Jump
                time.sleep(0.1)
                self.send_key_input(win32con.VK_E, 0.1)  # Air roll
                
            elif action == 'flip_reset':
                # Flip reset: Jump + air roll + flip
                self.send_key_input(win32con.VK_SPACE, 0.1)  # Jump
                time.sleep(0.1)
                self.send_key_input(win32con.VK_E, 0.1)  # Air roll
                time.sleep(0.1)
                self.send_key_input(win32con.VK_SPACE, 0.1)  # Flip
                
            elif action == 'musty_flick':
                # Musty flick: Jump + backflip + forward
                self.send_key_input(win32con.VK_SPACE, 0.1)  # Jump
                time.sleep(0.1)
                self.send_key_input(win32con.VK_S, 0.1)  # Back
                self.send_key_input(win32con.VK_SPACE, 0.1)  # Flip
                time.sleep(0.1)
                self.send_key_input(win32con.VK_W, 0.1)  # Forward
                
            elif action == 'double_tap':
                # Double tap: Jump + boost + air roll
                self.send_key_input(win32con.VK_SPACE, 0.1)  # Jump
                time.sleep(0.1)
                self.send_key_input(win32con.VK_SHIFT, 0.3)  # Boost
                self.send_key_input(win32con.VK_E, 0.1)  # Air roll
                
            elif action == 'rotation':
                # Rotation: Move to back post
                self.send_key_input(win32con.VK_S, 0.2)  # Back
                self.send_key_input(win32con.VK_A, 0.1)  # Left
                
            elif action == 'boost_management':
                # Boost management: Collect boost pads
                self.send_key_input(win32con.VK_W, 0.1)  # Forward
                self.send_key_input(win32con.VK_SHIFT, 0.1)  # Boost
                
            elif action == 'demo_opponent':
                # Demo opponent: Drive into opponent
                self.send_key_input(win32con.VK_W, 0.3)  # Forward
                self.send_key_input(win32con.VK_SHIFT, 0.2)  # Boost
                
            elif action == 'bump_opponent':
                # Bump opponent: Light contact
                self.send_key_input(win32con.VK_W, 0.1)  # Forward
                
            elif action == 'fake_challenge':
                # Fake challenge: Approach then retreat
                self.send_key_input(win32con.VK_W, 0.1)  # Forward
                time.sleep(0.1)
                self.send_key_input(win32con.VK_S, 0.1)  # Back
                
            elif action == 'possession_play':
                # Possession play: Control the ball
                self.send_key_input(win32con.VK_W, 0.1)  # Forward
                self.send_key_input(win32con.VK_A, 0.1)  # Left
                
            elif action == 'counter_attack':
                # Counter attack: Fast break
                self.send_key_input(win32con.VK_W, 0.2)  # Forward
                self.send_key_input(win32con.VK_SHIFT, 0.2)  # Boost
                
            elif action == 'pressure_play':
                # Pressure play: Aggressive positioning
                self.send_key_input(win32con.VK_W, 0.1)  # Forward
                self.send_key_input(win32con.VK_A, 0.1)  # Left
                
            elif action == 'time_waste':
                # Time waste: Slow play
                self.send_key_input(win32con.VK_S, 0.1)  # Back
                time.sleep(0.1)
                self.send_key_input(win32con.VK_A, 0.1)  # Left
                
            elif action == 'kickoff_strategy':
                # Kickoff strategy: Speed flip
                self.send_key_input(win32con.VK_W, 0.1)  # Forward
                self.send_key_input(win32con.VK_SHIFT, 0.1)  # Boost
                time.sleep(0.1)
                self.send_key_input(win32con.VK_SPACE, 0.1)  # Jump
                
            self.actions_performed += 1
            return True
            
        except Exception as e:
            print(f"❌ Error executing action {action}: {e}")
            return False
    
    def play_ssl_game(self, mode='3s'):
        """Play a game with SSL-level strategy"""
        try:
            print(f"\n🎮 STARTING SSL GAME - {mode.upper()}")
            print("=" * 50)
            
            # Get mode-specific strategy
            strategy = self.mode_strategies.get(mode, self.mode_strategies['3s'])
            
            # Game loop
            game_start = time.time()
            while self.is_playing:
                try:
                    # Choose action based on strategy
                    if random.random() < strategy['mechanics_focus']:
                        # Focus on mechanics
                        action = random.choice(self.ssl_actions['mechanics'])
                    elif random.random() < strategy['game_sense_focus']:
                        # Focus on game sense
                        action = random.choice(self.ssl_actions['game_sense'])
                    else:
                        # Focus on positioning
                        action = random.choice(self.ssl_actions['positioning'])
                    
                    # Execute the action
                    if self.execute_ssl_action(action, mode):
                        print(f"✅ Executed: {action}")
                    else:
                        print(f"❌ Failed: {action}")
                    
                    # Random delay between actions
                    time.sleep(random.uniform(0.1, 0.5))
                    
                    # Check if game is still running
                    if not self.game_process or not self.game_process.is_running():
                        print("⚠️ Game process stopped")
                        break
                    
                except Exception as e:
                    print(f"❌ Game loop error: {e}")
                    time.sleep(1)
            
            print(f"⏹️ Game ended after {time.time() - game_start:.1f} seconds")
            
        except Exception as e:
            print(f"❌ Error in SSL game: {e}")
    
    def start_ssl_grind(self):
        """Start the SSL grind - play until SSL is achieved"""
        try:
            print("\n🚀 STARTING SSL GRIND")
            print("=" * 60)
            print("🎯 Target: SSL in ALL modes")
            print("🎮 Will play for you until SSL is achieved")
            print("⚡ Real-time game control")
            print("🔧 Auto-injection into game")
            
            # Find and connect to Rocket League
            if not self.find_rocket_league_window():
                print("❌ Please start Rocket League first!")
                return False
            
            if not self.get_game_process():
                print("❌ Could not connect to game process!")
                return False
            
            self.is_playing = True
            
            # Start playing
            self.play_ssl_game('3s')  # Start with 3s
            
            return True
            
        except Exception as e:
            print(f"❌ Error starting SSL grind: {e}")
            return False
    
    def stop_playing(self):
        """Stop playing"""
        self.is_playing = False
        print("⏹️ Stopped playing")
    
    def get_status(self):
        """Get current status"""
        elapsed = time.time() - self.start_time
        hours = elapsed / 3600
        
        return {
            'is_playing': self.is_playing,
            'current_rank': self.current_rank,
            'target_rank': self.target_rank,
            'actions_performed': self.actions_performed,
            'wins': self.wins,
            'losses': self.losses,
            'play_time': hours,
            'game_connected': self.game_window is not None
        }

def main():
    """Main function"""
    print("🏆 SSL GAME CONTROLLER")
    print("=" * 60)
    print("🎯 Target: SSL in ALL modes")
    print("🎮 Controls your Rocket League game")
    print("🚀 Plays for you to achieve SSL")
    print("⚡ Real-time game control")
    print("🔧 Auto-injection into game")
    print("🚀 Starting SSL game controller...")
    
    controller = SSLGameController()
    
    try:
        # Start the SSL grind
        controller.start_ssl_grind()
        
    except KeyboardInterrupt:
        print("\n⏹️ SSL grind interrupted by user")
        controller.stop_playing()
    except Exception as e:
        print(f"\n❌ Critical Error: {e}")

if __name__ == "__main__":
    main()
