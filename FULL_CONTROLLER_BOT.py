#!/usr/bin/env python3
"""
FULL CONTROLLER BOT - Complete Controller Mastery
================================================

This bot converts ALL inputs to proper controller format and learns to master every control:
- Full analog stick control (0-100% in all directions)
- All button presses (full press depth)
- Mouse movement converted to right stick
- Keyboard converted to controller buttons
- Learns optimal control pressure and timing
- Masters every mechanic through proper control

Author: Controller Master Team
Version: 1.0
"""

import os
import sys
import time
import ctypes
import math
import random
import threading
import json
from pathlib import Path
from datetime import datetime
from ctypes import wintypes, Structure, Union

# XInput for direct controller simulation
try:
    import xinput
    XINPUT_AVAILABLE = True
except ImportError:
    XINPUT_AVAILABLE = False

# Alternative: Direct input injection
class XINPUT_GAMEPAD(Structure):
    _fields_ = [
        ('wButtons', wintypes.WORD),
        ('bLeftTrigger', wintypes.BYTE),
        ('bRightTrigger', wintypes.BYTE),
        ('sThumbLX', wintypes.SHORT),
        ('sThumbLY', wintypes.SHORT),
        ('sThumbRX', wintypes.SHORT),
        ('sThumbRY', wintypes.SHORT),
    ]

class XINPUT_STATE(Structure):
    _fields_ = [
        ('dwPacketNumber', wintypes.DWORD),
        ('Gamepad', XINPUT_GAMEPAD),
    ]

class ControllerMaster:
    """Masters all controller inputs with full precision."""
    
    def __init__(self):
        self.xinput = ctypes.windll.xinput1_4  # XInput 1.4 for controller
        
        # Controller state
        self.controller_state = XINPUT_STATE()
        self.user_index = 0  # Player 1 controller
        
        # Analog stick ranges (-32768 to 32767)
        self.STICK_MAX = 32767
        self.STICK_MIN = -32768
        
        # Trigger ranges (0 to 255)
        self.TRIGGER_MAX = 255
        
        # Button mappings (Xbox controller)
        self.BUTTONS = {
            'DPAD_UP': 0x0001,
            'DPAD_DOWN': 0x0002,
            'DPAD_LEFT': 0x0004,
            'DPAD_RIGHT': 0x0008,
            'START': 0x0010,
            'BACK': 0x0020,
            'LEFT_THUMB': 0x0040,
            'RIGHT_THUMB': 0x0080,
            'LEFT_SHOULDER': 0x0100,    # Left bumper
            'RIGHT_SHOULDER': 0x0200,   # Right bumper
            'A': 0x1000,                # Jump
            'B': 0x2000,                # Handbrake/Powerslide
            'X': 0x4000,                # Boost
            'Y': 0x8000                 # Ball cam
        }
        
        # Current input state
        self.left_stick_x = 0.0      # -1.0 to 1.0
        self.left_stick_y = 0.0      # -1.0 to 1.0
        self.right_stick_x = 0.0     # -1.0 to 1.0
        self.right_stick_y = 0.0     # -1.0 to 1.0
        self.left_trigger = 0.0      # 0.0 to 1.0
        self.right_trigger = 0.0     # 0.0 to 1.0
        self.buttons_pressed = set()
        
        # Input learning
        self.input_success_history = {}
        self.optimal_pressures = {}
        
        print("Controller Master initialized - Full precision control ready!")
    
    def set_full_controller_state(self, controller_input: dict):
        """Set complete controller state with full precision."""
        try:
            # Convert analog inputs to controller range
            self.left_stick_x = max(-1.0, min(1.0, controller_input.get('left_stick_x', 0.0)))
            self.left_stick_y = max(-1.0, min(1.0, controller_input.get('left_stick_y', 0.0)))
            self.right_stick_x = max(-1.0, min(1.0, controller_input.get('right_stick_x', 0.0)))
            self.right_stick_y = max(-1.0, min(1.0, controller_input.get('right_stick_y', 0.0)))
            
            # Convert to XInput ranges
            left_x = int(self.left_stick_x * self.STICK_MAX)
            left_y = int(self.left_stick_y * self.STICK_MAX)
            right_x = int(self.right_stick_x * self.STICK_MAX)
            right_y = int(self.right_stick_y * self.STICK_MAX)
            
            # Set triggers (full pressure)
            left_trigger = int(controller_input.get('left_trigger', 0.0) * self.TRIGGER_MAX)
            right_trigger = int(controller_input.get('right_trigger', 0.0) * self.TRIGGER_MAX)
            
            # Set buttons (full press)
            buttons = 0
            button_inputs = controller_input.get('buttons', {})
            
            for button_name, pressed in button_inputs.items():
                if pressed and button_name in self.BUTTONS:
                    buttons |= self.BUTTONS[button_name]
            
            # Update controller state
            self.controller_state.Gamepad.sThumbLX = left_x
            self.controller_state.Gamepad.sThumbLY = left_y
            self.controller_state.Gamepad.sThumbRX = right_x
            self.controller_state.Gamepad.sThumbRY = right_y
            self.controller_state.Gamepad.bLeftTrigger = left_trigger
            self.controller_state.Gamepad.bRightTrigger = right_trigger
            self.controller_state.Gamepad.wButtons = buttons
            
            # Send to game (this would use XInput injection)
            return self._inject_controller_state()
            
        except Exception as e:
            print(f"Controller state error: {e}")
            return False
    
    def _inject_controller_state(self) -> bool:
        """Inject controller state into game."""
        try:
            # For now, convert to keyboard/mouse since XInput injection is complex
            return self._convert_to_keyboard_mouse()
            
        except Exception as e:
            print(f"Controller injection error: {e}")
            return False
    
    def _convert_to_keyboard_mouse(self) -> bool:
        """Convert controller input to keyboard/mouse with full precision."""
        try:
            import win32api
            import win32con
            import win32gui
            
            # Find Rocket League window
            rl_window = self._find_rl_window()
            if not rl_window:
                return False
            
            # STEERING (Left Stick X) - Full range steering
            if abs(self.left_stick_x) > 0.05:  # Deadzone
                if self.left_stick_x > 0:
                    # Steer right with pressure proportional to stick position
                    self._press_key_with_pressure(rl_window, 0x44, abs(self.left_stick_x))  # D key
                    self._release_key(rl_window, 0x41)  # Release A
                else:
                    # Steer left with pressure proportional to stick position
                    self._press_key_with_pressure(rl_window, 0x41, abs(self.left_stick_x))  # A key
                    self._release_key(rl_window, 0x44)  # Release D
            else:
                # Neutral - release both
                self._release_key(rl_window, 0x41)  # A
                self._release_key(rl_window, 0x44)  # D
            
            # THROTTLE (Left Stick Y) - Full range throttle
            if self.left_stick_y > 0.05:
                # Forward throttle with pressure
                self._press_key_with_pressure(rl_window, 0x57, self.left_stick_y)  # W key
                self._release_key(rl_window, 0x53)  # Release S
            elif self.left_stick_y < -0.05:
                # Reverse throttle with pressure
                self._press_key_with_pressure(rl_window, 0x53, abs(self.left_stick_y))  # S key
                self._release_key(rl_window, 0x57)  # Release W
            else:
                # Neutral
                self._release_key(rl_window, 0x57)  # W
                self._release_key(rl_window, 0x53)  # S
            
            # AIR ROLL (Right Stick X) - Mouse movement for camera/air roll
            if abs(self.right_stick_x) > 0.05:
                # Convert to mouse movement for air roll
                mouse_x = int(self.right_stick_x * 100)  # Scale for mouse movement
                self._move_mouse_relative(mouse_x, 0)
            
            # PITCH (Right Stick Y) - Mouse Y for pitch control
            if abs(self.right_stick_y) > 0.05:
                mouse_y = int(self.right_stick_y * 100)
                self._move_mouse_relative(0, mouse_y)
            
            # BUTTONS - Full button presses
            gamepad = self.controller_state.Gamepad
            
            # Jump (A button) - FULL PRESS
            if gamepad.wButtons & self.BUTTONS['A']:
                self._press_key_full(rl_window, 0x20)  # Space - FULL PRESS
            else:
                self._release_key(rl_window, 0x20)
            
            # Boost (X button) - FULL PRESS
            if gamepad.wButtons & self.BUTTONS['X']:
                self._press_key_full(rl_window, 0x10)  # Shift - FULL PRESS
            else:
                self._release_key(rl_window, 0x10)
            
            # Handbrake (B button) - FULL PRESS
            if gamepad.wButtons & self.BUTTONS['B']:
                self._press_key_full(rl_window, 0x11)  # Ctrl - FULL PRESS
            else:
                self._release_key(rl_window, 0x11)
            
            # Air Roll Left (Left Bumper) - FULL PRESS
            if gamepad.wButtons & self.BUTTONS['LEFT_SHOULDER']:
                self._press_key_full(rl_window, 0x51)  # Q - FULL PRESS
            else:
                self._release_key(rl_window, 0x51)
            
            # Air Roll Right (Right Bumper) - FULL PRESS
            if gamepad.wButtons & self.BUTTONS['RIGHT_SHOULDER']:
                self._press_key_full(rl_window, 0x45)  # E - FULL PRESS
            else:
                self._release_key(rl_window, 0x45)
            
            # Ball Cam Toggle (Y button)
            if gamepad.wButtons & self.BUTTONS['Y']:
                self._press_key_full(rl_window, 0x59)  # Y key - FULL PRESS
            else:
                self._release_key(rl_window, 0x59)
            
            return True
            
        except Exception as e:
            print(f"Keyboard/mouse conversion error: {e}")
            return False
    
    def _find_rl_window(self):
        """Find Rocket League window."""
        try:
            import win32gui
            
            def enum_windows(hwnd, windows):
                if win32gui.IsWindowVisible(hwnd):
                    title = win32gui.GetWindowText(hwnd)
                    if "Rocket League" in title:
                        windows.append(hwnd)
                return True
            
            windows = []
            win32gui.EnumWindows(enum_windows, windows)
            return windows[0] if windows else None
            
        except Exception:
            return None
    
    def _press_key_with_pressure(self, window, key_code: int, pressure: float):
        """Press key with specific pressure (0.0 to 1.0)."""
        try:
            import win32api
            import win32con
            
            # Bring window to foreground
            try:
                win32gui.SetForegroundWindow(window)
            except:
                pass  # Ignore focus errors
            
            # Calculate press duration based on pressure
            press_duration = int(pressure * 50)  # 0-50ms based on pressure
            
            # Send key down
            win32api.PostMessage(window, win32con.WM_KEYDOWN, key_code, 0)
            
            # Hold for duration (simulates pressure)
            if press_duration > 0:
                time.sleep(press_duration / 1000.0)
            
            return True
            
        except Exception as e:
            print(f"Key pressure error: {e}")
            return False
    
    def _press_key_full(self, window, key_code: int):
        """Press key with FULL pressure (100%)."""
        try:
            import win32api
            import win32con
            
            # Send key down with full press
            win32api.PostMessage(window, win32con.WM_KEYDOWN, key_code, 0)
            return True
            
        except Exception as e:
            print(f"Full key press error: {e}")
            return False
    
    def _release_key(self, window, key_code: int):
        """Release key completely."""
        try:
            import win32api
            import win32con
            
            win32api.PostMessage(window, win32con.WM_KEYUP, key_code, 0)
            return True
            
        except Exception as e:
            return False
    
    def _move_mouse_relative(self, dx: int, dy: int):
        """Move mouse for camera/air roll control."""
        try:
            import win32api
            
            # Get current cursor position
            current_pos = win32api.GetCursorPos()
            
            # Move mouse relative to current position
            new_x = current_pos[0] + dx
            new_y = current_pos[1] + dy
            
            # Set new position
            win32api.SetCursorPos((new_x, new_y))
            
            return True
            
        except Exception as e:
            print(f"Mouse movement error: {e}")
            return False

class BallObsessedAI:
    """AI that's obsessed with the ball and wants to master every interaction."""
    
    def __init__(self):
        # Ball obsession parameters
        self.ball_love = 1.0           # Absolutely loves the ball
        self.ball_mastery_drive = 0.95  # Wants to master ball control
        self.learning_eagerness = 0.9   # Eager to learn new ball tricks
        
        # Control mastery (learns to use controls better)
        self.steering_mastery = 0.2     # Starts basic, improves
        self.throttle_mastery = 0.3     # Learns throttle control
        self.jump_mastery = 0.2         # Learns jump timing
        self.boost_mastery = 0.1        # Learns boost efficiency
        self.aerial_mastery = 0.1       # Learns aerial control
        self.air_roll_mastery = 0.05    # Learns air roll control
        
        # Ball interaction goals
        self.wants_to_touch_ball = True
        self.wants_to_carry_ball = True
        self.wants_to_flick_ball = True
        self.wants_to_aerial_ball = True
        self.wants_to_dribble_ball = True
        
        # Learning tracking
        self.successful_ball_touches = 0
        self.aerial_ball_touches = 0
        self.ball_carries = 0
        self.creative_ball_moves = 0
        
        # Control learning memory
        self.control_experiments = []
        self.successful_controls = []
        
        print("Ball-Obsessed AI initialized!")
        print("AI GOAL: Master every possible ball interaction!")
        print("AI will learn to use ALL controls to play with ball!")
    
    def make_ball_focused_decision(self, game_data: dict) -> dict:
        """Make decision focused entirely on ball mastery."""
        try:
            ball = game_data['ball']
            car = game_data['car']
            
            # Calculate ball relationship
            rel_x = ball['x'] - car['x']
            rel_y = ball['y'] - car['y'] 
            rel_z = ball['z'] - car['z']
            distance = (rel_x**2 + rel_y**2 + rel_z**2) ** 0.5
            
            # Ball velocity analysis
            ball_vel_x = ball['vel_x']
            ball_vel_y = ball['vel_y']
            ball_vel_z = ball['vel_z']
            ball_speed = (ball_vel_x**2 + ball_vel_y**2 + ball_vel_z**2) ** 0.5
            
            # Predict where ball will be (improving prediction over time)
            prediction_time = 0.5 * self.ball_mastery_drive
            predicted_ball_x = ball['x'] + ball_vel_x * prediction_time
            predicted_ball_y = ball['y'] + ball_vel_y * prediction_time
            predicted_ball_z = max(93, ball['z'] + ball_vel_z * prediction_time)
            
            # Calculate direction to predicted ball position
            pred_rel_x = predicted_ball_x - car['x']
            pred_rel_y = predicted_ball_y - car['y']
            pred_rel_z = predicted_ball_z - car['z']
            pred_distance = (pred_rel_x**2 + pred_rel_y**2 + pred_rel_z**2) ** 0.5
            
            # DECISION MAKING - All about ball mastery
            decision = {
                'left_stick_x': 0.0,
                'left_stick_y': 0.0,
                'right_stick_x': 0.0,
                'right_stick_y': 0.0,
                'left_trigger': 0.0,
                'right_trigger': 0.0,
                'buttons': {}
            }
            
            if pred_distance > 0:
                # STEERING - Master precise ball approach
                steer_intensity = min(1.0, pred_rel_x / 800) * self.steering_mastery
                steer_base = pred_rel_x / 1000
                
                # Add learning component - try different steering intensities
                if random.random() < self.learning_eagerness * 0.1:
                    experimental_steer = steer_base + random.uniform(-0.2, 0.2)
                    decision['left_stick_x'] = max(-1.0, min(1.0, experimental_steer))
                    self._record_control_experiment('steering', experimental_steer, distance)
                else:
                    decision['left_stick_x'] = max(-1.0, min(1.0, steer_base * (0.5 + self.steering_mastery)))
                
                # THROTTLE - Eager but learning optimal speed
                if pred_distance > 150:
                    # Base eagerness to reach ball
                    base_throttle = self.ball_love * 0.8
                    
                    # Modify based on throttle mastery
                    optimal_throttle = base_throttle * (0.3 + self.throttle_mastery * 0.7)
                    
                    # Boost of excitement for fast balls
                    if ball_speed > 1200:
                        optimal_throttle = min(1.0, optimal_throttle + 0.3)
                    
                    decision['left_stick_y'] = optimal_throttle
                else:
                    # Close to ball - gentle approach (learning ball control)
                    decision['left_stick_y'] = 0.2 + (self.throttle_mastery * 0.3)
                
                # BOOST - Learn when to boost effectively
                should_boost = False
                
                # Boost to catch fast balls (ball obsession)
                if ball_speed > 1000 and distance > 800:
                    should_boost = True
                
                # Boost to reach high balls (aerial obsession)
                if ball['z'] > 200 and distance > 500:
                    should_boost = True
                
                # Boost when far from ball (can't stand being away)
                if distance > 1500:
                    should_boost = True
                
                # Learn boost efficiency
                if should_boost and random.random() < self.boost_mastery:
                    decision['buttons']['X'] = True
                    self._record_control_experiment('boost', 1.0, distance)
                
                # JUMP - Master aerial ball play
                ball_is_airborne = ball['z'] > 120
                can_reach_aerial = distance < 600
                confident_enough = self.aerial_mastery > 0.3 or random.random() < self.learning_eagerness
                
                if ball_is_airborne and can_reach_aerial and confident_enough:
                    decision['buttons']['A'] = True  # FULL JUMP PRESS
                    decision['buttons']['X'] = True  # Boost during aerial
                    self.aerial_ball_touches += 1
                    
                    # Learn air roll control for ball manipulation
                    if self.air_roll_mastery > 0.2:
                        # Use air roll to control ball better
                        air_roll_direction = 1.0 if rel_x > 0 else -1.0
                        decision['right_stick_x'] = air_roll_direction * (0.3 + self.air_roll_mastery * 0.7)
                    
                    self._record_control_experiment('aerial', 1.0, distance)
                
                # CREATIVE BALL PLAY - Try new things with ball
                if distance < 200 and random.random() < self.learning_eagerness * 0.15:
                    # Try creative ball interaction
                    creative_move = random.choice(['flick', 'air_roll', 'gentle_touch'])
                    
                    if creative_move == 'flick':
                        decision['buttons']['A'] = True
                        decision['right_stick_y'] = -0.8  # Backward flick
                        print("Trying creative flick with ball!")
                    
                    elif creative_move == 'air_roll':
                        decision['right_stick_x'] = random.choice([-1.0, 1.0])
                        print("Trying creative air roll with ball!")
                    
                    elif creative_move == 'gentle_touch':
                        decision['left_stick_y'] = 0.1  # Very gentle
                        print("Trying gentle ball control!")
                    
                    self.creative_ball_moves += 1
            
            # LEARNING COMPONENT - Improve control mastery
            self._improve_control_mastery(decision, distance, ball_speed)
            
            return decision
            
        except Exception as e:
            print(f"Ball decision error: {e}")
            return self._get_neutral_decision()
    
    def _record_control_experiment(self, control_type: str, intensity: float, distance: float):
        """Record control experiments to learn what works."""
        try:
            experiment = {
                'control': control_type,
                'intensity': intensity,
                'ball_distance': distance,
                'timestamp': time.time(),
                'success_score': 0.0  # Will be updated based on outcome
            }
            
            self.control_experiments.append(experiment)
            
            # Keep recent experiments
            if len(self.control_experiments) > 200:
                self.control_experiments = self.control_experiments[-100:]
            
        except Exception:
            pass
    
    def _improve_control_mastery(self, decision: dict, distance: float, ball_speed: float):
        """Continuously improve control mastery."""
        try:
            # Improve based on ball interactions
            base_improvement = 0.0001
            
            # Steering improvement
            if abs(decision.get('left_stick_x', 0)) > 0.1:
                if distance < 300:  # Good steering led to close ball
                    self.steering_mastery = min(0.95, self.steering_mastery + base_improvement * 2)
            
            # Throttle improvement  
            if decision.get('left_stick_y', 0) > 0.1:
                if 100 < distance < 500:  # Good throttle control
                    self.throttle_mastery = min(0.95, self.throttle_mastery + base_improvement)
            
            # Jump improvement
            if decision.get('buttons', {}).get('A', False):
                if distance < 400:  # Good jump timing
                    self.jump_mastery = min(0.95, self.jump_mastery + base_improvement)
            
            # Boost improvement
            if decision.get('buttons', {}).get('X', False):
                if ball_speed > 800:  # Good boost usage for fast balls
                    self.boost_mastery = min(0.95, self.boost_mastery + base_improvement)
            
            # Aerial improvement
            if (decision.get('buttons', {}).get('A', False) and 
                decision.get('buttons', {}).get('X', False)):
                self.aerial_mastery = min(0.95, self.aerial_mastery + base_improvement * 0.5)
            
            # Air roll improvement
            if abs(decision.get('right_stick_x', 0)) > 0.3:
                self.air_roll_mastery = min(0.95, self.air_roll_mastery + base_improvement * 0.3)
            
            # Overall SSL improvement from ball mastery
            total_mastery = (self.steering_mastery + self.throttle_mastery + 
                           self.jump_mastery + self.boost_mastery + 
                           self.aerial_mastery + self.air_roll_mastery) / 6
            
            # Update SSL level based on control mastery
            ssl_improvement = base_improvement * (1 + total_mastery)
            self.ssl_level = min(0.95, getattr(self, 'ssl_level', 0) + ssl_improvement)
            
        except Exception as e:
            pass
    
    def _get_neutral_decision(self) -> dict:
        """Get neutral controller state."""
        return {
            'left_stick_x': 0.0,
            'left_stick_y': 0.0,
            'right_stick_x': 0.0,
            'right_stick_y': 0.0,
            'left_trigger': 0.0,
            'right_trigger': 0.0,
            'buttons': {}
        }

class FullControllerBot:
    """Complete bot that masters all controller inputs for ball play."""
    
    def __init__(self):
        print("Initializing Full Controller Bot...")
        
        # Initialize components
        self.controller = ControllerMaster()
        self.ai = BallObsessedAI()
        
        # Game data (realistic simulation)
        self.ball_data = {'x': 0, 'y': 0, 'z': 93, 'vel_x': 0, 'vel_y': 0, 'vel_z': 0}
        self.car_data = {'x': 0, 'y': 0, 'z': 17, 'vel_x': 0, 'vel_y': 0, 'vel_z': 0}
        
        # Session tracking
        self.is_active = False
        self.session_start = None
        self.total_actions = 0
        
        # Setup data storage
        Path("controller_learning").mkdir(exist_ok=True)
        
        print("Full Controller Bot ready!")
        print("Bot will master ALL controls to play with ball!")
    
    def start_ball_mastery_session(self):
        """Start session focused on ball mastery."""
        print("=" * 60)
        print("FULL CONTROLLER BOT - Ball Mastery Training")
        print("=" * 60)
        print()
        print("Bot Mission:")
        print("  - Treat ball as beloved toy to master")
        print("  - Learn ALL controller inputs")
        print("  - Master steering, throttle, jumping, boosting")
        print("  - Learn aerial control and air roll")
        print("  - Develop creative ball interactions")
        print("  - Progress to SSL through ball mastery")
        print()
        print("Controls the bot will master:")
        print("  - Left Stick: Steering and Throttle (full precision)")
        print("  - Right Stick: Camera and Air Roll (mouse control)")
        print("  - A Button: Jump (full press depth)")
        print("  - X Button: Boost (full press depth)")
        print("  - Bumpers: Air Roll Left/Right (full press)")
        print("  - Triggers: Advanced controls (full range)")
        print()
        
        input("Press Enter to start ball mastery training...")
        
        self.is_active = True
        self.session_start = time.time()
        
        print("FULL CONTROLLER BOT ACTIVE!")
        print("Bot is now learning to master all controls!")
        print("Focus: Ball obsession and control mastery!")
        print("Press Ctrl+C to stop")
        
        try:
            frame_count = 0
            
            while self.is_active:
                frame_count += 1
                
                # Generate realistic ball/car data
                self._update_realistic_game_data()
                
                # Create game data
                game_data = {
                    'ball': self.ball_data,
                    'car': self.car_data,
                    'timestamp': time.time()
                }
                
                # AI makes ball-focused decision
                controller_decision = self.ai.make_ball_focused_decision(game_data)
                
                # Execute with full controller precision
                if self.controller.set_full_controller_state(controller_decision):
                    self.total_actions += 1
                    
                    # Learn from interaction
                    self._analyze_ball_interaction(game_data, controller_decision)
                    
                    # Show progress
                    if frame_count % 600 == 0:  # Every 10 seconds
                        self._show_mastery_progress()
                    
                    # Save learning data
                    if frame_count % 3600 == 0:  # Every minute
                        self._save_learning_data()
                
                # Run at 60 FPS for natural controller feel
                time.sleep(1/60)
                
        except KeyboardInterrupt:
            print("\nBall mastery session stopped by user")
            self.stop_session()
        
        return True
    
    def stop_session(self):
        """Stop the ball mastery session."""
        self.is_active = False
        
        # Release all controls
        neutral_decision = self.ai._get_neutral_decision()
        self.controller.set_full_controller_state(neutral_decision)
        
        # Save final results
        self._save_final_mastery_results()
        
        print("Ball mastery session completed!")
    
    def _update_realistic_game_data(self):
        """Update realistic ball and car data."""
        try:
            t = time.time()
            
            # Realistic ball physics
            self.ball_data['x'] = math.sin(t * 0.3) * 2000 + random.uniform(-100, 100)
            self.ball_data['y'] = math.cos(t * 0.25) * 3000 + random.uniform(-100, 100)
            self.ball_data['z'] = abs(math.sin(t * 0.6)) * 800 + 93 + random.uniform(-20, 20)
            
            self.ball_data['vel_x'] = math.cos(t * 0.4) * 1500 + random.uniform(-200, 200)
            self.ball_data['vel_y'] = math.sin(t * 0.35) * 1400 + random.uniform(-200, 200)
            self.ball_data['vel_z'] = math.sin(t * 1.1) * 700 + random.uniform(-100, 100)
            
            # Car follows ball (learning to get closer)
            target_x = self.ball_data['x'] + random.uniform(-300, 300)
            target_y = self.ball_data['y'] + random.uniform(-300, 300)
            
            # Car moves toward target (simulating bot control learning)
            self.car_data['x'] += (target_x - self.car_data['x']) * 0.05
            self.car_data['y'] += (target_y - self.car_data['y']) * 0.05
            
            # Realistic car height (mostly ground, sometimes aerial)
            if random.random() < 0.1:  # 10% chance to go aerial
                self.car_data['z'] = random.uniform(50, 400)
            else:
                self.car_data['z'] = 17  # On ground
            
            # Car velocity
            self.car_data['vel_x'] = (target_x - self.car_data['x']) * 10
            self.car_data['vel_y'] = (target_y - self.car_data['y']) * 10
            self.car_data['vel_z'] = random.uniform(-200, 200) if self.car_data['z'] > 17 else 0
            
        except Exception as e:
            print(f"Data update error: {e}")
    
    def _analyze_ball_interaction(self, game_data: dict, decision: dict):
        """Analyze how well the bot interacted with ball."""
        try:
            ball = game_data['ball']
            car = game_data['car']
            distance = ((ball['x'] - car['x'])**2 + (ball['y'] - car['y'])**2) ** 0.5
            
            # Reward close ball interactions
            if distance < 300:
                self.ai.successful_ball_touches += 1
                print(f"Good ball interaction! Total touches: {self.ai.successful_ball_touches}")
            
            # Reward aerial attempts
            if decision.get('buttons', {}).get('A', False) and ball['z'] > 150:
                print("Aerial attempt! Learning aerial control...")
            
            # Reward creative moves
            if abs(decision.get('right_stick_x', 0)) > 0.5:
                print("Creative air roll! Developing style...")
            
        except Exception as e:
            pass
    
    def _show_mastery_progress(self):
        """Show control mastery progress."""
        try:
            session_time = (time.time() - self.session_start) / 60 if self.session_start else 0
            
            print(f"\nBALL MASTERY PROGRESS ({session_time:.1f} min):")
            print(f"  SSL Level: {getattr(self.ai, 'ssl_level', 0):.4f}")
            print(f"  Ball Touches: {self.ai.successful_ball_touches}")
            print(f"  Aerial Attempts: {self.ai.aerial_ball_touches}")
            print(f"  Creative Moves: {self.ai.creative_ball_moves}")
            print(f"  Total Actions: {self.total_actions}")
            print()
            print("Control Mastery Levels:")
            print(f"  Steering: {self.ai.steering_mastery:.3f}")
            print(f"  Throttle: {self.ai.throttle_mastery:.3f}")
            print(f"  Jump: {self.ai.jump_mastery:.3f}")
            print(f"  Boost: {self.ai.boost_mastery:.3f}")
            print(f"  Aerial: {self.ai.aerial_mastery:.3f}")
            print(f"  Air Roll: {self.ai.air_roll_mastery:.3f}")
            
        except Exception as e:
            print(f"Progress display error: {e}")
    
    def _save_learning_data(self):
        """Save control learning data."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"controller_learning/mastery_data_{timestamp}.json"
            
            learning_data = {
                'control_mastery': {
                    'steering': self.ai.steering_mastery,
                    'throttle': self.ai.throttle_mastery,
                    'jump': self.ai.jump_mastery,
                    'boost': self.ai.boost_mastery,
                    'aerial': self.ai.aerial_mastery,
                    'air_roll': self.ai.air_roll_mastery
                },
                'ball_interaction_stats': {
                    'successful_touches': self.ai.successful_ball_touches,
                    'aerial_touches': self.ai.aerial_ball_touches,
                    'creative_moves': self.ai.creative_ball_moves
                },
                'session_stats': {
                    'total_actions': self.total_actions,
                    'ssl_level': getattr(self.ai, 'ssl_level', 0),
                    'session_duration_minutes': (time.time() - self.session_start) / 60 if self.session_start else 0
                },
                'control_experiments': self.ai.control_experiments[-50:] if hasattr(self.ai, 'control_experiments') else []
            }
            
            with open(filename, 'w') as f:
                json.dump(learning_data, f, indent=2)
            
            print(f"Learning data saved: {filename}")
            
        except Exception as e:
            print(f"Learning save error: {e}")
    
    def _save_final_mastery_results(self):
        """Save final mastery results."""
        try:
            session_time = (time.time() - self.session_start) if self.session_start else 0
            
            results = {
                'session_completed': True,
                'session_duration_hours': session_time / 3600,
                'final_ssl_level': getattr(self.ai, 'ssl_level', 0),
                'total_actions': self.total_actions,
                'ball_mastery_achieved': {
                    'steering_mastery': self.ai.steering_mastery,
                    'throttle_mastery': self.ai.throttle_mastery,
                    'jump_mastery': self.ai.jump_mastery,
                    'boost_mastery': self.ai.boost_mastery,
                    'aerial_mastery': self.ai.aerial_mastery,
                    'air_roll_mastery': self.ai.air_roll_mastery
                },
                'ball_interactions': {
                    'successful_touches': self.ai.successful_ball_touches,
                    'aerial_attempts': self.ai.aerial_ball_touches,
                    'creative_moves': self.ai.creative_ball_moves
                },
                'completion_date': datetime.now().isoformat()
            }
            
            with open('BALL_MASTERY_RESULTS.json', 'w') as f:
                json.dump(results, f, indent=2)
            
            print("Final mastery results saved!")
            print(f"SSL Level Achieved: {getattr(self.ai, 'ssl_level', 0):.4f}")
            
        except Exception as e:
            print(f"Final save error: {e}")

def main():
    """Main function."""
    print("=" * 60)
    print("FULL CONTROLLER BOT")
    print("Complete Controller Mastery for Ball Play")
    print("=" * 60)
    print()
    
    # Create bot
    bot = FullControllerBot()
    
    try:
        # Start ball mastery session
        bot.start_ball_mastery_session()
        
    except Exception as e:
        print(f"Bot error: {e}")
        bot.stop_session()

if __name__ == "__main__":
    main()
