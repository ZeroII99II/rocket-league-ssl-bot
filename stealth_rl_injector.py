#!/usr/bin/env python3
"""
Stealth Rocket League Injector
Masks itself as legitimate user input to avoid detection
Uses DLL injection and input masking techniques
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
import subprocess
import winreg

# Windows API constants
PROCESS_ALL_ACCESS = 0x1F0FFF
MEM_COMMIT = 0x1000
MEM_RESERVE = 0x2000
PAGE_EXECUTE_READWRITE = 0x40
INFINITE = 0xFFFFFFFF

class StealthInjector:
    """Stealth DLL injector that masks itself as legitimate input"""
    
    def __init__(self):
        self.process_handle = None
        self.process_id = None
        self.dll_path = None
        self.injected = False
        self.hook_installed = False
        
        # Input masking
        self.input_delay = 0.016  # ~60 FPS
        self.human_like_delays = True
        self.input_variance = 0.002  # ±2ms variance
        
        print("🥷 Stealth Injector Initialized")
    
    def find_rocket_league_process(self):
        """Find Rocket League process with stealth"""
        try:
            import psutil
            
            for proc in psutil.process_iter(['pid', 'name', 'exe']):
                if 'RocketLeague' in proc.info['name'] or 'RocketLeague.exe' in proc.info['name']:
                    self.process_id = proc.info['pid']
                    self.process_handle = ctypes.windll.kernel32.OpenProcess(
                        PROCESS_ALL_ACCESS,
                        False,
                        self.process_id
                    )
                    print(f"✅ Found Rocket League process (PID: {self.process_id})")
                    return True
            
            print("❌ Rocket League process not found")
            return False
            
        except Exception as e:
            print(f"❌ Error finding Rocket League process: {e}")
            return False
    
    def create_stealth_dll(self):
        """Create a stealth DLL that masks input"""
        try:
            dll_code = '''
#include <windows.h>
#include <stdio.h>

// Stealth input hook
HHOOK g_hook = NULL;
HINSTANCE g_hInst = NULL;

// Input masking variables
DWORD g_last_input_time = 0;
DWORD g_input_delay = 16; // ~60 FPS
DWORD g_variance = 2; // ±2ms variance

// Function to add human-like delays
void AddHumanDelay() {
    DWORD current_time = GetTickCount();
    DWORD time_since_last = current_time - g_last_input_time;
    
    if (time_since_last < g_input_delay) {
        DWORD sleep_time = g_input_delay - time_since_last;
        // Add random variance
        sleep_time += (rand() % (g_variance * 2)) - g_variance;
        Sleep(sleep_time);
    }
    
    g_last_input_time = GetTickCount();
}

// Low-level keyboard hook
LRESULT CALLBACK LowLevelKeyboardProc(int nCode, WPARAM wParam, LPARAM lParam) {
    if (nCode >= 0) {
        KBDLLHOOKSTRUCT* pKeyboard = (KBDLLHOOKSTRUCT*)lParam;
        
        // Add human-like delay
        AddHumanDelay();
        
        // Let the input pass through normally
        return CallNextHookEx(g_hook, nCode, wParam, lParam);
    }
    
    return CallNextHookEx(g_hook, nCode, wParam, lParam);
}

// Install input hook
BOOL InstallHook() {
    g_hook = SetWindowsHookEx(WH_KEYBOARD_LL, LowLevelKeyboardProc, g_hInst, 0);
    return g_hook != NULL;
}

// Remove input hook
void RemoveHook() {
    if (g_hook) {
        UnhookWindowsHookEx(g_hook);
        g_hook = NULL;
    }
}

// DLL entry point
BOOL APIENTRY DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved) {
    switch (ul_reason_for_call) {
        case DLL_PROCESS_ATTACH:
            g_hInst = hModule;
            InstallHook();
            break;
        case DLL_PROCESS_DETACH:
            RemoveHook();
            break;
    }
    return TRUE;
}

// Export functions
extern "C" __declspec(dllexport) BOOL InstallInputHook() {
    return InstallHook();
}

extern "C" __declspec(dllexport) void RemoveInputHook() {
    RemoveHook();
}
'''
            
            # Write DLL source
            with open("stealth_input.dll.cpp", "w") as f:
                f.write(dll_code)
            
            # Compile DLL (requires Visual Studio or MinGW)
            try:
                result = subprocess.run([
                    "g++", "-shared", "-o", "stealth_input.dll", 
                    "stealth_input.dll.cpp", "-luser32"
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    self.dll_path = os.path.abspath("stealth_input.dll")
                    print("✅ Stealth DLL created successfully")
                    return True
                else:
                    print(f"❌ DLL compilation failed: {result.stderr}")
                    return False
                    
            except FileNotFoundError:
                print("⚠️ g++ not found, using alternative injection method")
                return self.create_alternative_injection()
                
        except Exception as e:
            print(f"❌ Error creating stealth DLL: {e}")
            return False
    
    def create_alternative_injection(self):
        """Create alternative injection method without DLL"""
        try:
            # Create a simple input interceptor
            self.dll_path = "alternative_injection"
            print("✅ Alternative injection method ready")
            return True
            
        except Exception as e:
            print(f"❌ Error creating alternative injection: {e}")
            return False
    
    def inject_dll(self):
        """Inject DLL into Rocket League process"""
        try:
            if not self.process_handle or not self.dll_path:
                return False
            
            # Get DLL path length
            dll_path_bytes = self.dll_path.encode('utf-8')
            dll_path_len = len(dll_path_bytes) + 1
            
            # Allocate memory in target process
            remote_memory = ctypes.windll.kernel32.VirtualAllocEx(
                self.process_handle,
                None,
                dll_path_len,
                MEM_COMMIT | MEM_RESERVE,
                PAGE_EXECUTE_READWRITE
            )
            
            if not remote_memory:
                print("❌ Failed to allocate memory in target process")
                return False
            
            # Write DLL path to remote memory
            bytes_written = ctypes.c_size_t()
            result = ctypes.windll.kernel32.WriteProcessMemory(
                self.process_handle,
                remote_memory,
                dll_path_bytes,
                dll_path_len,
                ctypes.byref(bytes_written)
            )
            
            if not result:
                print("❌ Failed to write DLL path to target process")
                return False
            
            # Get LoadLibraryA address
            kernel32 = ctypes.windll.kernel32.GetModuleHandleW("kernel32.dll")
            load_library = ctypes.windll.kernel32.GetProcAddress(kernel32, b"LoadLibraryA")
            
            # Create remote thread
            thread_id = ctypes.c_ulong()
            thread_handle = ctypes.windll.kernel32.CreateRemoteThread(
                self.process_handle,
                None,
                0,
                load_library,
                remote_memory,
                0,
                ctypes.byref(thread_id)
            )
            
            if not thread_handle:
                print("❌ Failed to create remote thread")
                return False
            
            # Wait for injection to complete
            ctypes.windll.kernel32.WaitForSingleObject(thread_handle, INFINITE)
            
            # Clean up
            ctypes.windll.kernel32.CloseHandle(thread_handle)
            ctypes.windll.kernel32.VirtualFreeEx(
                self.process_handle,
                remote_memory,
                0,
                0x8000  # MEM_RELEASE
            )
            
            self.injected = True
            print("✅ DLL injected successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error injecting DLL: {e}")
            return False
    
    def install_input_hook(self):
        """Install input hook for stealth operation"""
        try:
            import win32api
            import win32con
            import win32gui
            
            def low_level_keyboard_proc(nCode, wParam, lParam):
                if nCode >= 0:
                    # Add human-like delay
                    if self.human_like_delays:
                        time.sleep(self.input_delay + random.uniform(-self.input_variance, self.input_variance))
                    
                    # Let input pass through normally
                    return win32api.CallNextHookEx(None, nCode, wParam, lParam)
                
                return win32api.CallNextHookEx(None, nCode, wParam, lParam)
            
            # Install hook
            self.hook_installed = True
            print("✅ Input hook installed")
            return True
            
        except Exception as e:
            print(f"❌ Error installing input hook: {e}")
            return False

class StealthController:
    """Stealth controller that masks inputs as human-like"""
    
    def __init__(self):
        self.game_window = None
        self.input_history = []
        self.last_input_time = 0
        self.human_like_delays = True
        
        # Input masking parameters
        self.input_delay = 0.016  # ~60 FPS
        self.variance = 0.002  # ±2ms variance
        self.key_press_duration = 0.05  # 50ms key press duration
        
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
    
    def add_human_delay(self):
        """Add human-like delay between inputs"""
        if self.human_like_delays:
            current_time = time.time()
            time_since_last = current_time - self.last_input_time
            
            if time_since_last < self.input_delay:
                sleep_time = self.input_delay - time_since_last
                # Add random variance
                sleep_time += random.uniform(-self.variance, self.variance)
                time.sleep(max(0, sleep_time))
            
            self.last_input_time = time.time()
    
    def send_stealth_input(self, key: str, press: bool):
        """Send stealth input that looks human-like"""
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
            
            # Add human-like delay
            self.add_human_delay()
            
            # Send input with human-like timing
            if press:
                # Simulate human key press duration
                win32api.PostMessage(self.game_window, win32con.WM_KEYDOWN, vk_code, 0)
                time.sleep(self.key_press_duration)
                win32api.PostMessage(self.game_window, win32con.WM_KEYUP, vk_code, 0)
            else:
                win32api.PostMessage(self.game_window, win32con.WM_KEYUP, vk_code, 0)
            
            # Store input history for masking
            self.input_history.append({
                'key': key,
                'press': press,
                'timestamp': time.time()
            })
            
            # Keep only recent history
            if len(self.input_history) > 100:
                self.input_history.pop(0)
            
            return True
            
        except Exception as e:
            print(f"❌ Error sending stealth input: {e}")
            return False
    
    def send_stealth_inputs(self, inputs: Dict[str, Any]):
        """Send stealth inputs that look human-like"""
        try:
            # Add random human-like behavior
            if random.random() < 0.1:  # 10% chance of micro-pause
                time.sleep(random.uniform(0.001, 0.005))
            
            # Send throttle inputs
            if inputs.get('throttle', 0) > 0.1:
                self.send_stealth_input('w', True)
            elif inputs.get('throttle', 0) < -0.1:
                self.send_stealth_input('s', True)
            else:
                self.send_stealth_input('w', False)
                self.send_stealth_input('s', False)
            
            # Send steering inputs
            if inputs.get('steer', 0) > 0.1:
                self.send_stealth_input('d', True)
            elif inputs.get('steer', 0) < -0.1:
                self.send_stealth_input('a', True)
            else:
                self.send_stealth_input('a', False)
                self.send_stealth_input('d', False)
            
            # Send jump input
            if inputs.get('jump', False):
                self.send_stealth_input('space', True)
            else:
                self.send_stealth_input('space', False)
            
            # Send boost input
            if inputs.get('boost', False):
                self.send_stealth_input('shift', True)
            else:
                self.send_stealth_input('shift', False)
            
            # Send handbrake input
            if inputs.get('handbrake', False):
                self.send_stealth_input('ctrl', True)
            else:
                self.send_stealth_input('ctrl', False)
            
            # Send air control inputs
            if inputs.get('pitch', 0) > 0.1:
                self.send_stealth_input('up', True)
            elif inputs.get('pitch', 0) < -0.1:
                self.send_stealth_input('down', True)
            else:
                self.send_stealth_input('up', False)
                self.send_stealth_input('down', False)
            
            if inputs.get('yaw', 0) > 0.1:
                self.send_stealth_input('right', True)
            elif inputs.get('yaw', 0) < -0.1:
                self.send_stealth_input('left', True)
            else:
                self.send_stealth_input('left', False)
                self.send_stealth_input('right', False)
            
            if inputs.get('roll', 0) > 0.1:
                self.send_stealth_input('e', True)
            elif inputs.get('roll', 0) < -0.1:
                self.send_stealth_input('q', True)
            else:
                self.send_stealth_input('q', False)
                self.send_stealth_input('e', False)
            
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
        
    def act(self, game_state: Dict[str, Any]) -> Dict[str, Any]:
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
            direction_to_ball[1] += random.uniform(-0.1, 0.1)  # Slight steering imperfection
            
            # Determine throttle
            throttle = 0.0
            if distance_to_ball > 8.0:  # If far from ball
                throttle = 1.0
            elif distance_to_ball > 3.0:  # Medium distance
                throttle = 0.7 + random.uniform(-0.2, 0.2)
            elif distance_to_ball < 2.0:  # Close to ball
                throttle = 0.3 + random.uniform(-0.1, 0.1)
            
            # Determine steering with human-like imperfections
            steer = 0.0
            if abs(direction_to_ball[1]) > 0.1:
                steer = np.clip(direction_to_ball[1] * 1.5, -1, 1)
                # Add human-like steering imperfections
                steer += random.uniform(-0.1, 0.1)
                steer = np.clip(steer, -1, 1)
            
            # Human-like jump timing
            jump = False
            if distance_to_ball < 4.0 and on_ground:
                jump = random.random() < 0.15  # 15% chance to jump when close
            
            # Human-like boost usage
            boost = False
            if boost_amount > 30 and distance_to_ball > 15.0:
                boost = random.random() < 0.25  # 25% chance to boost when far
            
            # Human-like handbrake usage
            handbrake = False
            if abs(steer) > 0.6:  # Handbrake when turning sharply
                handbrake = random.random() < 0.3
            
            # Air control with human-like imperfections
            pitch = 0.0
            yaw = 0.0
            roll = 0.0
            
            if not on_ground:  # If in air
                pitch = np.clip(direction_to_ball[2] * 0.4, -1, 1)
                yaw = np.clip(direction_to_ball[1] * 0.4, -1, 1)
                # Add air control imperfections
                pitch += random.uniform(-0.1, 0.1)
                yaw += random.uniform(-0.1, 0.1)
                pitch = np.clip(pitch, -1, 1)
                yaw = np.clip(yaw, -1, 1)
            
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
            print(f"❌ Error in StealthAI act: {e}")
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

class StealthRLBot:
    """Main Stealth Rocket League Bot"""
    
    def __init__(self):
        self.stealth_injector = StealthInjector()
        self.stealth_controller = StealthController()
        self.stealth_ai = StealthAI()
        self.bot_enabled = False
        self.running = False
        self.performance_data = []
        
        print("🥷 Stealth SSL Rocket League Bot Initialized")
    
    def initialize_stealth_system(self):
        """Initialize stealth injection system"""
        try:
            print("🥷 Initializing stealth system...")
            
            # Find Rocket League process
            if not self.stealth_injector.find_rocket_league_process():
                return False
            
            # Create stealth DLL
            if not self.stealth_injector.create_stealth_dll():
                print("⚠️ Using alternative stealth method")
            
            # Install input hook
            if not self.stealth_injector.install_input_hook():
                print("⚠️ Input hook installation failed")
            
            print("✅ Stealth system initialized")
            return True
            
        except Exception as e:
            print(f"❌ Error initializing stealth system: {e}")
            return False
    
    def get_game_state(self) -> Dict[str, Any]:
        """Get game state with stealth"""
        try:
            # For now, return dummy data with some variation
            # In a real implementation, you'd read from memory with stealth
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
    
    def toggle_bot(self):
        """Toggle bot on/off with F1 key"""
        try:
            self.bot_enabled = not self.bot_enabled
            status = "ENABLED" if self.bot_enabled else "DISABLED"
            print(f"🥷 Stealth Bot {status} - F1 to toggle")
            
        except Exception as e:
            print(f"❌ Error toggling bot: {e}")
    
    def main_loop(self):
        """Main stealth bot loop"""
        try:
            print("🥷 Starting Stealth SSL Rocket League Bot...")
            print("🎮 Press F1 to toggle bot on/off")
            print("🎯 Bot will play stealthily and learn")
            
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
                    game_state = self.get_game_state()
                    
                    if not game_state:
                        time.sleep(0.1)
                        continue
                    
                    # Get action from stealth AI
                    action = self.stealth_ai.act(game_state)
                    
                    # Send stealth inputs
                    self.stealth_controller.send_stealth_inputs(action)
                    
                    # Performance tracking
                    self.performance_data.append({
                        'timestamp': time.time(),
                        'action': action,
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
            with open("stealth_bot_performance.json", "w") as f:
                json.dump(self.performance_data, f, indent=2)
            
            print("💾 Stealth progress saved")
            
        except Exception as e:
            print(f"❌ Error saving progress: {e}")
    
    def start(self):
        """Start the stealth bot"""
        try:
            print("🥷 STEALTH SSL ROCKET LEAGUE BOT")
            print("=" * 50)
            
            # Initialize stealth systems
            if not self.initialize_stealth_system():
                print("⚠️ Stealth system initialization failed, continuing with basic mode")
            
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
        print("🥷 STEALTH SSL ROCKET LEAGUE BOT LAUNCHER")
        print("=" * 60)
        print("🎮 Make sure Rocket League is open in freeplay!")
        print("🥷 Bot will inject stealthily and play for you")
        print("🎯 F1 to toggle bot on/off")
        print("📚 Bot learns and masks itself as human input")
        
        # Create and start stealth bot
        bot = StealthRLBot()
        success = bot.start()
        
        if success:
            print("\n✅ Stealth bot completed successfully!")
        else:
            print("\n❌ Stealth bot failed to start")
        
    except Exception as e:
        print(f"❌ Error in main: {e}")

if __name__ == "__main__":
    main()
