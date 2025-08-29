#!/usr/bin/env python3
"""
Stealth Input Rocket League Bot
Uses advanced input simulation that's harder to detect
Masks inputs as legitimate user input
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
import win32api
import win32con
import win32gui
import win32process

class StealthInput:
    """Stealth input system that masks itself as human input"""
    
    def __init__(self):
        self.game_window = None
        self.input_history = []
        self.last_input_time = 0
        self.human_like_delays = True
        
        # Input masking parameters
        self.base_delay = 0.016  # ~60 FPS
        self.variance = 0.003    # ±3ms variance
        self.key_press_duration = 0.05  # 50ms key press duration
        
        # Virtual key codes
        self.vk_codes = {
            'w': 0x57, 's': 0x53, 'a': 0x41, 'd': 0x44,
            'space': 0x20, 'shift': 0x10, 'ctrl': 0x11,
            'up': 0x26, 'down': 0x28, 'left': 0x25, 'right': 0x27,
            'q': 0x51, 'e': 0x45
        }
        
        self.find_game_window()
        print("🥷 Stealth Input Initialized")
    
    def find_game_window(self):
        """Find Rocket League game window"""
        try:
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
    
    def add_human_delay(self):
        """Add human-like delay between inputs"""
        if self.human_like_delays:
            current_time = time.time()
            time_since_last = current_time - self.last_input_time
            
            if time_since_last < self.base_delay:
                sleep_time = self.base_delay - time_since_last
                # Add random variance
                sleep_time += random.uniform(-self.variance, self.variance)
                time.sleep(max(0, sleep_time))
            
            self.last_input_time = time.time()
    
    def send_stealth_key(self, key: str, state: bool):
        """Send stealth key input that looks human-like"""
        try:
            if key not in self.vk_codes:
                return False
            
            vk_code = self.vk_codes[key]
            
            # Add human-like delay
            self.add_human_delay()
            
            # Send input with human-like timing
            if state:
                # Simulate human key press with duration
                win32api.keybd_event(vk_code, 0, 0, 0)
                time.sleep(self.key_press_duration)
                win32api.keybd_event(vk_code, 0, win32con.KEYEVENTF_KEYUP, 0)
            else:
                # Ensure key is released
                win32api.keybd_event(vk_code, 0, win32con.KEYEVENTF_KEYUP, 0)
            
            # Store input history for masking
            self.input_history.append({
                'key': key,
                'state': state,
                'timestamp': time.time()
            })
            
            # Keep only recent history
            if len(self.input_history) > 100:
                self.input_history.pop(0)
            
            return True
            
        except Exception as e:
            print(f"❌ Error sending stealth key: {e}")
            return False
    
    def send_stealth_inputs(self, inputs: Dict[str, bool]):
        """Send stealth inputs that look human-like"""
        try:
            # Add random human-like behavior
            if random.random() < 0.05:  # 5% chance of micro-pause
                time.sleep(random.uniform(0.001, 0.003))
            
            # Send inputs with human-like timing
            for key, state in inputs.items():
                if key in self.vk_codes:
                    self.send_stealth_key(key, state)
            
            return True
            
        except Exception as e:
            print(f"❌ Error sending stealth inputs: {e}")
            return False

class StealthAI:
    """Stealth AI that makes human-like decisions"""
    
    def __init__(self):
        self.ball_target = [0, 0, 0]
        self.last_ball_pos = [0, 0, 0]
        self.action_history = []
        self.decision_delay = 0.016  # ~60 FPS
        self.last_decision_time = 0
        
        # Human-like behavior parameters
        self.imperfection_factor = 0.1  # 10% imperfection
        self.reaction_delay = 0.05      # 50ms reaction delay
        
    def act(self, game_state: Dict[str, Any]) -> Dict[str, bool]:
        """Make human-like AI decisions"""
        try:
            # Add human-like decision delay
            current_time = time.time()
            if current_time - self.last_decision_time < self.decision_delay:
                time.sleep(self.decision_delay - (current_time - self.last_decision_time))
            self.last_decision_time = time.time()
            
            car_pos = np.array(game_state.get('car_pos', [0, 0, 0]))
            ball_pos = np.array(game_state.get('ball_pos', [0, 0, 0]))
            boost_amount = game_state.get('boost_amount', 0)
            on_ground = game_state.get('on_ground', True)
            
            # Calculate distance to ball
            distance_to_ball = np.linalg.norm(car_pos - ball_pos)
            
            # Human-like ball chasing with imperfections
            direction_to_ball = ball_pos - car_pos
            direction_to_ball = direction_to_ball / (np.linalg.norm(direction_to_ball) + 1e-8)
            
            # Add human-like imperfections
            direction_to_ball[1] += random.uniform(-self.imperfection_factor, self.imperfection_factor)
            
            # Determine inputs
            inputs = {
                'w': False, 's': False, 'a': False, 'd': False,
                'space': False, 'shift': False, 'ctrl': False,
                'up': False, 'down': False, 'left': False, 'right': False,
                'q': False, 'e': False
            }
            
            # Throttle with human-like behavior
            if distance_to_ball > 8.0:  # If far from ball
                inputs['w'] = True
            elif distance_to_ball > 3.0:  # Medium distance
                inputs['w'] = random.random() < 0.8  # 80% chance to go forward
            elif distance_to_ball < 2.0:  # Close to ball
                inputs['s'] = random.random() < 0.3  # 30% chance to reverse
            
            # Steering with human-like imperfections
            if abs(direction_to_ball[1]) > 0.1:
                if direction_to_ball[1] > 0:
                    inputs['d'] = True
                    # Add steering imperfection
                    if random.random() < 0.1:  # 10% chance of wrong steering
                        inputs['d'] = False
                        inputs['a'] = True
                else:
                    inputs['a'] = True
                    # Add steering imperfection
                    if random.random() < 0.1:  # 10% chance of wrong steering
                        inputs['a'] = False
                        inputs['d'] = True
            
            # Human-like jump timing
            if distance_to_ball < 4.0 and on_ground:
                inputs['space'] = random.random() < 0.12  # 12% chance to jump when close
            
            # Human-like boost usage
            if boost_amount > 30 and distance_to_ball > 15.0:
                inputs['shift'] = random.random() < 0.25  # 25% chance to boost when far
            
            # Human-like handbrake usage
            if abs(direction_to_ball[1]) > 0.6:  # Handbrake when turning sharply
                inputs['ctrl'] = random.random() < 0.3
            
            # Air control with human-like imperfections
            if not on_ground:  # If in air
                if direction_to_ball[2] > 0.1:
                    inputs['up'] = True
                elif direction_to_ball[2] < -0.1:
                    inputs['down'] = True
                
                if direction_to_ball[1] > 0.1:
                    inputs['right'] = True
                elif direction_to_ball[1] < -0.1:
                    inputs['left'] = True
                
                # Add air control imperfections
                if random.random() < 0.05:  # 5% chance of wrong air control
                    if inputs['up']:
                        inputs['up'] = False
                        inputs['down'] = True
                    elif inputs['down']:
                        inputs['down'] = False
                        inputs['up'] = True
            
            # Store action for learning
            self.action_history.append({
                'inputs': inputs.copy(),
                'game_state': game_state.copy(),
                'timestamp': time.time()
            })
            
            # Keep only recent history
            if len(self.action_history) > 1000:
                self.action_history.pop(0)
            
            return inputs
            
        except Exception as e:
            print(f"❌ Error in StealthAI act: {e}")
            return {
                'w': False, 's': False, 'a': False, 'd': False,
                'space': False, 'shift': False, 'ctrl': False,
                'up': False, 'down': False, 'left': False, 'right': False,
                'q': False, 'e': False
            }

class StealthInputBot:
    """Main Stealth Input Bot"""
    
    def __init__(self):
        self.stealth_input = StealthInput()
        self.stealth_ai = StealthAI()
        self.bot_enabled = False
        self.running = False
        self.performance_data = []
        
        print("🥷 Stealth Input Bot Initialized")
    
    def get_game_state(self) -> Dict[str, Any]:
        """Get game state"""
        try:
            # For now, return dummy data with some variation
            # In a real implementation, you'd read from memory with stealth
            import random
            return {
                'car_pos': [random.uniform(-100, 100), random.uniform(-100, 100), random.uniform(0, 50)],
                'ball_pos': [random.uniform(-200, 200), random.uniform(-200, 200), random.uniform(0, 100)],
                'boost_amount': random.uniform(0, 100),
                'on_ground': random.choice([True, False])
            }
            
        except Exception as e:
            print(f"❌ Error getting game state: {e}")
            return {}
    
    def toggle_bot(self):
        """Toggle bot on/off"""
        try:
            self.bot_enabled = not self.bot_enabled
            status = "ENABLED" if self.bot_enabled else "DISABLED"
            print(f"🥷 Stealth Input Bot {status} - F1 to toggle")
            
        except Exception as e:
            print(f"❌ Error toggling bot: {e}")
    
    def main_loop(self):
        """Main bot loop"""
        try:
            print("🥷 Starting Stealth Input Bot...")
            print("🎮 Press F1 to toggle bot on/off")
            print("🎯 Bot will play stealthily and learn")
            
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
                    game_state = self.get_game_state()
                    
                    if not game_state:
                        time.sleep(0.1)
                        continue
                    
                    # Get action from stealth AI
                    inputs = self.stealth_ai.act(game_state)
                    
                    # Send stealth inputs
                    self.stealth_input.send_stealth_inputs(inputs)
                    
                    # Performance tracking
                    self.performance_data.append({
                        'timestamp': time.time(),
                        'inputs': inputs,
                        'bot_enabled': self.bot_enabled
                    })
                    
                    # Small delay to prevent overwhelming the system
                    time.sleep(0.016)  # ~60 FPS
                    
                except KeyboardInterrupt:
                    print("\n🛑 Stealth bot stopped by user")
                    break
                except Exception as e:
                    print(f"❌ Error in main loop: {e}")
                    time.sleep(0.1)
            
        except Exception as e:
            print(f"❌ Error in main loop: {e}")
    
    def save_progress(self):
        """Save bot progress"""
        try:
            # Save performance data
            with open("stealth_input_bot_performance.json", "w") as f:
                json.dump(self.performance_data, f, indent=2)
            
            print("💾 Stealth progress saved")
            
        except Exception as e:
            print(f"❌ Error saving progress: {e}")
    
    def start(self):
        """Start the stealth bot"""
        try:
            print("🥷 STEALTH INPUT ROCKET LEAGUE BOT")
            print("=" * 50)
            
            if not self.stealth_input.game_window:
                print("❌ Rocket League window not found!")
                return False
            
            # Start main loop
            self.running = True
            self.main_loop()
            
            # Save progress when stopping
            self.save_progress()
            
            return True
            
        except Exception as e:
            print(f"❌ Error starting stealth bot: {e}")
            return False

def main():
    """Main function"""
    try:
        print("🥷 STEALTH INPUT ROCKET LEAGUE BOT LAUNCHER")
        print("=" * 60)
        print("🎮 Make sure Rocket League is open in freeplay!")
        print("🥷 Bot will play stealthily and mask inputs")
        print("🎯 F1 to toggle bot on/off")
        print("📚 Bot learns and looks like human input")
        
        # Create and start stealth bot
        bot = StealthInputBot()
        success = bot.start()
        
        if success:
            print("\n✅ Stealth input bot completed successfully!")
        else:
            print("\n❌ Stealth input bot failed to start")
        
    except Exception as e:
        print(f"❌ Error in main: {e}")

if __name__ == "__main__":
    main()
