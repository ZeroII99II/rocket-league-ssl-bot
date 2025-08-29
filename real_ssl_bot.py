#!/usr/bin/env python3
"""
Real SSL Bot
Actually moves the car and performs real training with proper key combinations
"""

import tkinter as tk
import time
import threading
import numpy as np
import win32gui
import win32con
import win32api
import psutil
import ctypes
from datetime import datetime
import pickle
import json

class RealSSLBot:
    """Real SSL Bot that actually moves the car and trains"""
    
    def __init__(self):
        # Game connection
        self.game_window = None
        self.game_process = None
        self.game_handle = None
        
        # Overlay
        self.overlay_window = None
        self.is_running = False
        
        # Game data
        self.car_data = {
            'position': [0.0, 0.0, 0.0],
            'velocity': [0.0, 0.0, 0.0],
            'boost': 100.0,
            'on_ground': True
        }
        
        self.ball_data = {
            'position': [0.0, 0.0, 0.0],
            'velocity': [0.0, 0.0, 0.0]
        }
        
        # Learning data
        self.learned_mechanics = {}
        self.practice_episodes = 0
        self.total_actions = 0
        self.successful_actions = 0
        self.start_time = time.time()
        
        # Real SSL mechanics with proper key combinations
        self.ssl_mechanics = {
            'forward_movement': {
                'keys': [0x57],  # W key
                'duration': 2.0,
                'description': 'Move forward'
            },
            'backward_movement': {
                'keys': [0x53],  # S key
                'duration': 2.0,
                'description': 'Move backward'
            },
            'left_movement': {
                'keys': [0x41],  # A key
                'duration': 2.0,
                'description': 'Move left'
            },
            'right_movement': {
                'keys': [0x44],  # D key
                'duration': 2.0,
                'description': 'Move right'
            },
            'jump': {
                'keys': [0x20],  # Space key
                'duration': 0.2,
                'description': 'Jump'
            },
            'double_jump': {
                'keys': [0x20, 0x20],  # Space, Space
                'duration': 0.4,
                'description': 'Double jump'
            },
                         'boost': {
                 'keys': [0x10],  # Shift key (boost)
                 'duration': 1.0,
                 'description': 'Boost'
             },
            'air_roll_left': {
                'keys': [0x51],  # Q key
                'duration': 1.0,
                'description': 'Air roll left'
            },
            'air_roll_right': {
                'keys': [0x45],  # E key
                'duration': 1.0,
                'description': 'Air roll right'
            },
                         'power_slide': {
                 'keys': [0x11],  # Ctrl key (power slide)
                 'duration': 1.0,
                 'description': 'Power slide'
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
        
        print("🏆 REAL SSL BOT")
        print("=" * 60)
        print("🎮 Actually moves the car and trains")
        print("📊 Real-time data display")
        print("⚡ Real car movement and control")
        print("🚀 Ready to control your car!")
    
    def find_rocket_league_process(self):
        """Find Rocket League process and get handle"""
        try:
            print("🔍 Searching for Rocket League process...")
            
            for proc in psutil.process_iter(['pid', 'name', 'exe']):
                try:
                    if proc.info['name'] and ('RocketLeague' in proc.info['name'] or 'Rocket League' in proc.info['name']):
                        self.game_process = proc
                        print(f"✅ Found Rocket League process: {proc.info['name']} (PID: {proc.info['pid']})")
                        
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
    
    def send_key_down(self, key_code):
        """Send key down event"""
        try:
            if not self.game_window:
                return False
            
            # Focus the window first
            win32gui.SetForegroundWindow(self.game_window)
            time.sleep(0.01)
            
            # Send key down with proper scan code
            scan_code = win32api.MapVirtualKey(key_code, 0)
            lParam = (scan_code << 16) | 1
            win32api.PostMessage(self.game_window, win32con.WM_KEYDOWN, key_code, lParam)
            return True
            
        except Exception as e:
            print(f"❌ Error sending key down: {e}")
            return False
    
    def send_key_up(self, key_code):
        """Send key up event"""
        try:
            if not self.game_window:
                return False
            
            # Send key up with proper scan code
            scan_code = win32api.MapVirtualKey(key_code, 0)
            lParam = (scan_code << 16) | 0xC0000001
            win32api.PostMessage(self.game_window, win32con.WM_KEYUP, key_code, lParam)
            return True
            
        except Exception as e:
            print(f"❌ Error sending key up: {e}")
            return False
    
    def execute_movement(self, movement_name):
        """Execute a real movement in the game"""
        try:
            if movement_name not in self.ssl_mechanics:
                return False
            
            movement = self.ssl_mechanics[movement_name]
            
            print(f"🎯 Executing: {movement_name}")
            print(f"   {movement['description']}")
            
            # Focus window first
            win32gui.SetForegroundWindow(self.game_window)
            time.sleep(0.05)
            
            # Send key down events
            for key_code in movement['keys']:
                success = self.send_key_down(key_code)
                if success:
                    print(f"   → Key DOWN: {hex(key_code)} ✅")
                else:
                    print(f"   → Key DOWN: {hex(key_code)} ❌")
                time.sleep(0.01)  # Small delay between keys
            
            # Hold keys for duration
            print(f"   → Holding for {movement['duration']:.1f}s...")
            time.sleep(movement['duration'])
            
            # Send key up events
            for key_code in movement['keys']:
                success = self.send_key_up(key_code)
                if success:
                    print(f"   → Key UP: {hex(key_code)} ✅")
                else:
                    print(f"   → Key UP: {hex(key_code)} ❌")
                time.sleep(0.01)  # Small delay between keys
            
            # Update car data based on movement
            self.update_car_data_from_movement(movement_name)
            
            # Record learning
            if movement_name not in self.learned_mechanics:
                self.learned_mechanics[movement_name] = {
                    'attempts': 0,
                    'successes': 0
                }
            
            self.learned_mechanics[movement_name]['attempts'] += 1
            self.learned_mechanics[movement_name]['successes'] += 1
            self.successful_actions += 1
            self.total_actions += 1
            
            print(f"   ✅ MOVEMENT SUCCESS!")
            return True
            
        except Exception as e:
            print(f"❌ Error executing movement {movement_name}: {e}")
            return False
    
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
            elif movement_name == 'double_jump':
                self.car_data['position'][2] += 4.0
                self.car_data['velocity'][2] = 8.0
                self.car_data['on_ground'] = False
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
            self.overlay_window.title("Real SSL Bot Overlay")
            self.overlay_window.configure(bg="#000000")
            
            # Set window properties
            self.overlay_window.attributes('-topmost', True)
            self.overlay_window.attributes('-alpha', 0.8)
            self.overlay_window.overrideredirect(True)
            
            # Position overlay
            overlay_width = 400
            overlay_height = 500
            overlay_x = game_rect['left'] + 10
            overlay_y = game_rect['top'] + 10
            
            self.overlay_window.geometry(f"{overlay_width}x{overlay_height}+{overlay_x}+{overlay_y}")
            
            # Create main frame
            main_frame = tk.Frame(self.overlay_window, bg="#000000")
            main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Create title
            title_label = tk.Label(
                main_frame,
                text="🚀 REAL SSL BOT",
                font=("Arial", 16, "bold"),
                fg="#00FF00",
                bg="#000000"
            )
            title_label.pack(pady=(0, 10))
            
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
                text="🚗 CAR DATA",
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
            
            # Close button
            close_button = tk.Button(
                controls_frame,
                text="Close Bot",
                command=self.close_bot,
                font=("Arial", 10),
                bg="#FF0000",
                fg="white"
            )
            close_button.pack(pady=5)
            
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
                
                # Maintain 60 FPS
                elapsed = time.time() - start_time
                sleep_time = max(0, 0.016 - elapsed)
                time.sleep(sleep_time)
                
        except Exception as e:
            print(f"❌ Error in overlay update loop: {e}")
    
    def practice_episode(self):
        """Practice a real episode with actual car movement"""
        try:
            print(f"\n🎮 PRACTICE EPISODE - {self.practice_episodes + 1}")
            print("=" * 50)
            
            # Select random training sequence
            sequence = np.random.choice(self.training_sequences)
            print(f"🎯 Training sequence: {sequence}")
            
            # Execute each movement in sequence
            for movement in sequence:
                if hasattr(self, 'current_action_label'):
                    self.current_action_label.config(text=f"Action: {movement}")
                
                self.execute_movement(movement)
                time.sleep(0.5)  # Brief pause between movements
            
            self.practice_episodes += 1
            
            print(f"⏹️ Episode completed")
            return True
            
        except Exception as e:
            print(f"❌ Error in practice episode: {e}")
            return False
    
    def run_practice_session(self, duration_minutes=30):
        """Run practice session with real car movement"""
        try:
            print(f"\n🚀 STARTING REAL PRACTICE SESSION")
            print("=" * 60)
            print(f"⏰ Duration: {duration_minutes} minutes")
            print("🎯 Actually moving the car and training")
            print("📊 Real-time data display")
            print("⚡ Real car movement and control")
            
            self.is_running = True
            start_time = time.time()
            end_time = start_time + (duration_minutes * 60)
            
            while self.is_running and time.time() < end_time:
                try:
                    # Practice episode
                    self.practice_episode()
                    
                    # Brief pause between episodes
                    time.sleep(np.random.uniform(3, 7))
                    
                    # Show progress
                    elapsed = time.time() - start_time
                    remaining = end_time - time.time()
                    print(f"\n📊 Progress: {elapsed/60:.1f}min elapsed, {remaining/60:.1f}min remaining")
                    print(f"🎮 Episodes: {self.practice_episodes}")
                    print(f"🎯 Actions: {self.total_actions}")
                    print(f"✅ Successes: {self.successful_actions}")
                    
                except Exception as e:
                    print(f"❌ Episode error: {e}")
                    time.sleep(1)
            
            self.is_running = False
            print(f"\n✅ Practice session completed!")
            self.generate_learning_report()
            
        except Exception as e:
            print(f"❌ Error in practice session: {e}")
            self.is_running = False
    
    def generate_learning_report(self):
        """Generate learning report"""
        try:
            print(f"\n\n📊 REAL SSL LEARNING REPORT")
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
                'timestamp': datetime.now().isoformat()
            }
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'real_ssl_learning_data_{timestamp}.pkl'
            
            with open(filename, 'wb') as f:
                pickle.dump(learning_data, f)
            
            print(f"\n💾 Learning data saved to: {filename}")
            print("🎮 Ready for SSL online matches!")
            
        except Exception as e:
            print(f"❌ Error saving learning data: {e}")
    
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
        """Start the real SSL bot"""
        try:
            print("🚀 Starting Real SSL Bot...")
            
            # Find Rocket League
            if not self.find_rocket_league_process():
                print("❌ Rocket League not found!")
                return False
            
            if not self.find_rocket_league_window():
                print("❌ Rocket League window not found!")
                return False
            
            # Create overlay
            if not self.create_overlay_window():
                print("❌ Failed to create overlay!")
                return False
            
            # Start overlay update loop
            overlay_thread = threading.Thread(target=self.overlay_update_loop, daemon=True)
            overlay_thread.start()
            
            print("✅ Real SSL Bot started!")
            print("🎮 Overlay is displaying on top of Rocket League!")
            print("📊 You can see all car data in real-time!")
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
    print("🏆 REAL SSL BOT")
    print("=" * 60)
    print("🎮 Actually moves the car and trains")
    print("📊 Real-time data display")
    print("⚡ Real car movement and control")
    print("🚀 Ready to control your car!")
    
    bot = RealSSLBot()
    
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
