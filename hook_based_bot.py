#!/usr/bin/env python3
"""
Hook-Based Rocket League Bot
Uses Windows hooks to intercept and modify input before it reaches the game
Most practical and stealthy approach
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

# Windows API constants
WH_KEYBOARD_LL = 13
WH_MOUSE_LL = 14
WM_KEYDOWN = 0x0100
WM_KEYUP = 0x0101
WM_SYSKEYDOWN = 0x0104
WM_SYSKEYUP = 0x0105
HC_ACTION = 0

class InputHook:
    """Windows input hook for intercepting keyboard/mouse input"""
    
    def __init__(self):
        self.hook_keyboard = None
        self.hook_mouse = None
        self.bot_enabled = False
        self.input_state = {
            'w': False, 's': False, 'a': False, 'd': False,
            'space': False, 'shift': False, 'ctrl': False,
            'up': False, 'down': False, 'left': False, 'right': False,
            'q': False, 'e': False
        }
        self.ai_inputs = {}
        self.last_ai_update = 0
        
        # Virtual key codes
        self.vk_codes = {
            'w': 0x57, 's': 0x53, 'a': 0x41, 'd': 0x44,
            'space': 0x20, 'shift': 0x10, 'ctrl': 0x11,
            'up': 0x26, 'down': 0x28, 'left': 0x25, 'right': 0x27,
            'q': 0x51, 'e': 0x45
        }
        
        print("🪝 Input Hook Initialized")
    
    def keyboard_hook_proc(self, nCode, wParam, lParam):
        """Keyboard hook procedure"""
        try:
            if nCode >= HC_ACTION:
                # Get keyboard data
                kb_data = ctypes.cast(lParam, ctypes.POINTER(ctypes.c_ulong)).contents
                vk_code = kb_data.value & 0xFFFF
                
                # Check if this is a key we're controlling
                key_name = None
                for name, code in self.vk_codes.items():
                    if code == vk_code:
                        key_name = name
                        break
                
                if key_name and self.bot_enabled:
                    # Check if AI wants to override this key
                    if key_name in self.ai_inputs:
                        ai_state = self.ai_inputs[key_name]
                        current_state = wParam == WM_KEYDOWN or wParam == WM_SYSKEYDOWN
                        
                        # If AI state differs from current state, override
                        if ai_state != current_state:
                            # Don't pass the original input to the game
                            return 1  # Block the input
                    
                    # Update our input state
                    self.input_state[key_name] = wParam == WM_KEYDOWN or wParam == WM_SYSKEYDOWN
            
            # Pass the input to the next hook
            return ctypes.windll.user32.CallNextHookExW(self.hook_keyboard, nCode, wParam, lParam)
            
        except Exception as e:
            print(f"❌ Error in keyboard hook: {e}")
            return ctypes.windll.user32.CallNextHookExW(self.hook_keyboard, nCode, wParam, lParam)
    
    def mouse_hook_proc(self, nCode, wParam, lParam):
        """Mouse hook procedure"""
        try:
            if nCode >= HC_ACTION:
                # For now, just pass mouse input through
                pass
            
            return ctypes.windll.user32.CallNextHookExW(self.hook_mouse, nCode, wParam, lParam)
            
        except Exception as e:
            print(f"❌ Error in mouse hook: {e}")
            return ctypes.windll.user32.CallNextHookExW(self.hook_mouse, nCode, wParam, lParam)
    
    def install_hooks(self):
        """Install input hooks"""
        try:
            # Define hook procedure types
            HOOKPROC = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_int, ctypes.wintypes.WPARAM, ctypes.wintypes.LPARAM)
            
            # Create hook procedures
            self.keyboard_proc = HOOKPROC(self.keyboard_hook_proc)
            self.mouse_proc = HOOKPROC(self.mouse_hook_proc)
            
            # Install keyboard hook
            self.hook_keyboard = ctypes.windll.user32.SetWindowsHookExW(
                WH_KEYBOARD_LL,
                self.keyboard_proc,
                ctypes.windll.kernel32.GetModuleHandleW(None),
                0
            )
            
            if not self.hook_keyboard:
                print("❌ Failed to install keyboard hook")
                return False
            
            # Install mouse hook
            self.hook_mouse = ctypes.windll.user32.SetWindowsHookExW(
                WH_MOUSE_LL,
                self.mouse_proc,
                ctypes.windll.kernel32.GetModuleHandleW(None),
                0
            )
            
            if not self.hook_mouse:
                print("❌ Failed to install mouse hook")
                return False
            
            print("✅ Input hooks installed successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error installing hooks: {e}")
            return False
    
    def uninstall_hooks(self):
        """Uninstall input hooks"""
        try:
            if self.hook_keyboard:
                ctypes.windll.user32.UnhookWindowsHookEx(self.hook_keyboard)
                self.hook_keyboard = None
            
            if self.hook_mouse:
                ctypes.windll.user32.UnhookWindowsHookEx(self.hook_mouse)
                self.hook_mouse = None
            
            print("✅ Input hooks uninstalled")
            
        except Exception as e:
            print(f"❌ Error uninstalling hooks: {e}")
    
    def set_ai_inputs(self, inputs: Dict[str, bool]):
        """Set AI inputs"""
        self.ai_inputs = inputs.copy()
        self.last_ai_update = time.time()
    
    def send_input(self, key: str, state: bool):
        """Send input to the game"""
        try:
            if key not in self.vk_codes:
                return False
            
            vk_code = self.vk_codes[key]
            
            # Create input structure
            if state:
                # Key down
                ctypes.windll.user32.keybd_event(vk_code, 0, 0, 0)
            else:
                # Key up
                ctypes.windll.user32.keybd_event(vk_code, 0, 2, 0)  # KEYEVENTF_KEYUP = 2
            
            return True
            
        except Exception as e:
            print(f"❌ Error sending input: {e}")
            return False

class HookBasedAI:
    """AI for hook-based bot"""
    
    def __init__(self):
        self.ball_target = [0, 0, 0]
        self.last_ball_pos = [0, 0, 0]
        self.action_history = []
        
    def act(self, game_state: Dict[str, Any]) -> Dict[str, bool]:
        """Make AI decision"""
        try:
            car_pos = np.array(game_state.get('car_pos', [0, 0, 0]))
            ball_pos = np.array(game_state.get('ball_pos', [0, 0, 0]))
            boost_amount = game_state.get('boost_amount', 0)
            on_ground = game_state.get('on_ground', True)
            
            # Calculate distance to ball
            distance_to_ball = np.linalg.norm(car_pos - ball_pos)
            
            # Simple ball chasing
            direction_to_ball = ball_pos - car_pos
            direction_to_ball = direction_to_ball / (np.linalg.norm(direction_to_ball) + 1e-8)
            
            # Determine inputs
            inputs = {
                'w': False, 's': False, 'a': False, 'd': False,
                'space': False, 'shift': False, 'ctrl': False,
                'up': False, 'down': False, 'left': False, 'right': False,
                'q': False, 'e': False
            }
            
            # Throttle
            if distance_to_ball > 5.0:
                inputs['w'] = True
            elif distance_to_ball < 2.0:
                inputs['s'] = True
            
            # Steering
            if direction_to_ball[1] > 0.1:
                inputs['d'] = True
            elif direction_to_ball[1] < -0.1:
                inputs['a'] = True
            
            # Jump
            if distance_to_ball < 3.0 and on_ground:
                inputs['space'] = random.random() < 0.1
            
            # Boost
            if boost_amount > 20 and distance_to_ball > 10.0:
                inputs['shift'] = random.random() < 0.3
            
            # Handbrake
            if abs(direction_to_ball[1]) > 0.5:
                inputs['ctrl'] = random.random() < 0.2
            
            # Air control
            if not on_ground:
                if direction_to_ball[2] > 0.1:
                    inputs['up'] = True
                elif direction_to_ball[2] < -0.1:
                    inputs['down'] = True
                
                if direction_to_ball[1] > 0.1:
                    inputs['right'] = True
                elif direction_to_ball[1] < -0.1:
                    inputs['left'] = True
            
            return inputs
            
        except Exception as e:
            print(f"❌ Error in AI act: {e}")
            return {}

class HookBasedBot:
    """Main Hook-Based Bot"""
    
    def __init__(self):
        self.input_hook = InputHook()
        self.ai = HookBasedAI()
        self.bot_enabled = False
        self.running = False
        self.performance_data = []
        
        print("🪝 Hook-Based Bot Initialized")
    
    def initialize_hooks(self):
        """Initialize input hooks"""
        try:
            print("🪝 Initializing input hooks...")
            
            if not self.input_hook.install_hooks():
                return False
            
            print("✅ Input hooks initialized")
            return True
            
        except Exception as e:
            print(f"❌ Error initializing hooks: {e}")
            return False
    
    def get_game_state(self) -> Dict[str, Any]:
        """Get game state"""
        try:
            # For now, return dummy data
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
            self.input_hook.bot_enabled = self.bot_enabled
            status = "ENABLED" if self.bot_enabled else "DISABLED"
            print(f"🪝 Hook-Based Bot {status} - F1 to toggle")
            
        except Exception as e:
            print(f"❌ Error toggling bot: {e}")
    
    def main_loop(self):
        """Main bot loop"""
        try:
            print("🪝 Starting Hook-Based Bot...")
            print("🎮 Press F1 to toggle bot on/off")
            print("🎯 Bot will intercept and modify inputs")
            
            while self.running:
                try:
                    # Check for F1 key press
                    if keyboard.is_pressed('f1'):
                        self.toggle_bot()
                        time.sleep(0.5)
                    
                    if not self.bot_enabled:
                        time.sleep(0.1)
                        continue
                    
                    # Get game state
                    game_state = self.get_game_state()
                    
                    if not game_state:
                        time.sleep(0.1)
                        continue
                    
                    # Make AI decision
                    ai_inputs = self.ai.act(game_state)
                    
                    # Set AI inputs in hook
                    self.input_hook.set_ai_inputs(ai_inputs)
                    
                    # Performance tracking
                    self.performance_data.append({
                        'timestamp': time.time(),
                        'ai_inputs': ai_inputs,
                        'bot_enabled': self.bot_enabled
                    })
                    
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
            with open("hook_bot_performance.json", "w") as f:
                json.dump(self.performance_data, f, indent=2)
            
            print("💾 Progress saved")
            
        except Exception as e:
            print(f"❌ Error saving progress: {e}")
    
    def start(self):
        """Start the bot"""
        try:
            print("🪝 HOOK-BASED ROCKET LEAGUE BOT")
            print("=" * 50)
            
            # Initialize hooks
            if not self.initialize_hooks():
                print("❌ Failed to initialize hooks")
                return False
            
            # Start main loop
            self.running = True
            self.main_loop()
            
            # Uninstall hooks
            self.input_hook.uninstall_hooks()
            
            # Save progress
            self.save_progress()
            
            return True
            
        except Exception as e:
            print(f"❌ Error starting bot: {e}")
            return False

def main():
    """Main function"""
    try:
        print("🪝 HOOK-BASED ROCKET LEAGUE BOT LAUNCHER")
        print("=" * 60)
        print("🎮 Make sure Rocket League is open in freeplay!")
        print("🪝 Bot will intercept inputs and modify them")
        print("🎯 F1 to toggle bot on/off")
        print("📚 Most stealthy approach - intercepts at OS level")
        
        # Create and start bot
        bot = HookBasedBot()
        success = bot.start()
        
        if success:
            print("\n✅ Hook-based bot completed successfully!")
        else:
            print("\n❌ Hook-based bot failed to start")
        
    except Exception as e:
        print(f"❌ Error in main: {e}")

if __name__ == "__main__":
    main()
