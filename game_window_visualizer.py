#!/usr/bin/env python3
"""
Game Window Visualizer - Creates a proper game-like window
This creates a window that looks more like a game interface
"""

import tkinter as tk
from tkinter import ttk
import threading
import time
import math
from typing import Dict, Any

class GameWindowVisualizer:
    def __init__(self):
        """Initialize the game window"""
        self.root = tk.Tk()
        self.root.title("🚀 JSTN Bot Training - Watch Your Bot Learn!")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1a1a1a')
        
        # Make window resizable and movable
        self.root.resizable(True, True)
        
        # Training data
        self.training_mode = "1s"
        self.episode = 0
        self.reward = 0.0
        self.skill_level = 0.0
        self.mechanics = {
            "aerial": 0.0,
            "flip_reset": 0.0,
            "double_tap": 0.0,
            "recovery": 0.0,
            "wall_play": 0.0
        }
        
        # Create the interface
        self.create_interface()
        
        # Animation variables
        self.ball_x = 600
        self.ball_y = 400
        self.ball_vx = 2
        self.ball_vy = 1
        
        print("🎮 Game Window Visualizer Created!")
        print("   📺 You can move this window around your desktop")
        print("   🎯 Watch your bot learn in real-time!")
    
    def create_interface(self):
        """Create the game interface"""
        # Main frame
        main_frame = tk.Frame(self.root, bg='#1a1a1a')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = tk.Label(main_frame, 
                              text="🚀 JSTN Bot Training Visualizer", 
                              font=('Arial', 24, 'bold'),
                              fg='#00ff00', bg='#1a1a1a')
        title_label.pack(pady=(0, 20))
        
        # Game field frame
        field_frame = tk.Frame(main_frame, bg='#2d5016', relief=tk.RAISED, bd=3)
        field_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Field canvas
        self.field_canvas = tk.Canvas(field_frame, bg='#2d5016', highlightthickness=0)
        self.field_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Training info frame
        info_frame = tk.Frame(main_frame, bg='#1a1a1a')
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Training mode
        self.mode_label = tk.Label(info_frame, 
                                  text=f"🎯 {self.training_mode.upper()} Training", 
                                  font=('Arial', 18, 'bold'),
                                  fg='#ffff00', bg='#1a1a1a')
        self.mode_label.pack(side=tk.LEFT, padx=(0, 20))
        
        # Episode and reward
        self.episode_label = tk.Label(info_frame, 
                                     text=f"Episode: {self.episode}", 
                                     font=('Arial', 14),
                                     fg='#ffffff', bg='#1a1a1a')
        self.episode_label.pack(side=tk.LEFT, padx=(0, 20))
        
        self.reward_label = tk.Label(info_frame, 
                                    text=f"Reward: {self.reward:.2f}", 
                                    font=('Arial', 14),
                                    fg='#00ff00', bg='#1a1a1a')
        self.reward_label.pack(side=tk.LEFT, padx=(0, 20))
        
        # Skill level
        self.skill_label = tk.Label(info_frame, 
                                   text=f"JSTN Level: {self.skill_level:.3f}", 
                                   font=('Arial', 14),
                                   fg='#ff00ff', bg='#1a1a1a')
        self.skill_label.pack(side=tk.LEFT)
        
        # Mechanics frame
        mechanics_frame = tk.Frame(main_frame, bg='#1a1a1a')
        mechanics_frame.pack(fill=tk.X)
        
        # Mechanics labels
        self.mechanics_labels = {}
        for i, (mechanic, level) in enumerate(self.mechanics.items()):
            label = tk.Label(mechanics_frame, 
                           text=f"{mechanic.replace('_', ' ').title()}: {level:.3f}", 
                           font=('Arial', 12),
                           fg='#ffffff', bg='#1a1a1a')
            label.grid(row=0, column=i, padx=10, sticky=tk.W)
            self.mechanics_labels[mechanic] = label
        
        # Instructions
        instructions = tk.Label(main_frame, 
                               text="🎮 This window shows your bot learning in real-time | 🖱️ You can move this window around | ⌨️ Close with X button", 
                               font=('Arial', 10),
                               fg='#cccccc', bg='#1a1a1a')
        instructions.pack(pady=(10, 0))
        
        # Start animation
        self.animate()
    
    def draw_field(self):
        """Draw the Rocket League field"""
        self.field_canvas.delete("all")
        
        width = self.field_canvas.winfo_width()
        height = self.field_canvas.winfo_height()
        
        if width <= 1 or height <= 1:
            return
        
        # Field background
        self.field_canvas.create_rectangle(0, 0, width, height, fill='#2d5016', outline='')
        
        # Center line
        self.field_canvas.create_line(width//2, 0, width//2, height, fill='white', width=3)
        
        # Center circle
        center_x, center_y = width//2, height//2
        self.field_canvas.create_oval(center_x-80, center_y-80, center_x+80, center_y+80, 
                                     outline='white', width=3, fill='')
        
        # Goals
        goal_width = 20
        goal_height = 120
        self.field_canvas.create_rectangle(50-goal_width//2, center_y-goal_height//2, 
                                          50+goal_width//2, center_y+goal_height//2, 
                                          outline='white', width=3, fill='')
        self.field_canvas.create_rectangle(width-50-goal_width//2, center_y-goal_height//2, 
                                          width-50+goal_width//2, center_y+goal_height//2, 
                                          outline='white', width=3, fill='')
        
        # Ball
        ball_size = 15
        self.field_canvas.create_oval(self.ball_x-ball_size, self.ball_y-ball_size, 
                                     self.ball_x+ball_size, self.ball_y+ball_size, 
                                     fill='orange', outline='white', width=2)
        
        # Cars (simulated)
        car_size = 20
        car1_x, car1_y = self.ball_x - 100, self.ball_y
        car2_x, car2_y = self.ball_x + 100, self.ball_y
        
        self.field_canvas.create_rectangle(car1_x-car_size, car1_y-car_size//2, 
                                          car1_x+car_size, car1_y+car_size//2, 
                                          fill='blue', outline='white', width=2)
        self.field_canvas.create_text(car1_x, car1_y-30, text="JSTN Bot", fill='white', font=('Arial', 10))
        
        self.field_canvas.create_rectangle(car2_x-car_size, car2_y-car_size//2, 
                                          car2_x+car_size, car2_y+car_size//2, 
                                          fill='red', outline='white', width=2)
        self.field_canvas.create_text(car2_x, car2_y-30, text="Opponent", fill='white', font=('Arial', 10))
    
    def animate(self):
        """Animate the ball movement"""
        try:
            # Update ball position
            self.ball_x += self.ball_vx
            self.ball_y += self.ball_vy
            
            # Get canvas dimensions safely
            canvas_width = self.field_canvas.winfo_width()
            canvas_height = self.field_canvas.winfo_height()
            
            # Only animate if canvas is ready
            if canvas_width > 1 and canvas_height > 1:
                # Bounce off walls
                if self.ball_x <= 20 or self.ball_x >= canvas_width - 20:
                    self.ball_vx = -self.ball_vx
                if self.ball_y <= 20 or self.ball_y >= canvas_height - 20:
                    self.ball_vy = -self.ball_vy
                
                # Keep ball in bounds
                self.ball_x = max(20, min(canvas_width - 20, self.ball_x))
                self.ball_y = max(20, min(canvas_height - 20, self.ball_y))
                
                # Redraw field
                self.draw_field()
            
            # Schedule next animation
            self.root.after(50, self.animate)  # ~20 FPS
            
        except Exception as e:
            print(f"Animation error: {e}")
            # Schedule next animation anyway
            self.root.after(50, self.animate)
    
    def update_training_data(self, mode: str, episode: int, reward: float, 
                           skill_level: float, mechanics: Dict[str, float]):
        """Update the training data display"""
        self.training_mode = mode
        self.episode = episode
        self.reward = reward
        self.skill_level = skill_level
        self.mechanics.update(mechanics)
        
        # Update labels
        self.mode_label.config(text=f"🎯 {mode.upper()} Training")
        self.episode_label.config(text=f"Episode: {episode}")
        self.reward_label.config(text=f"Reward: {reward:.2f}")
        self.skill_label.config(text=f"JSTN Level: {skill_level:.3f}")
        
        # Update mechanics
        for mechanic, level in mechanics.items():
            if mechanic in self.mechanics_labels:
                self.mechanics_labels[mechanic].config(
                    text=f"{mechanic.replace('_', ' ').title()}: {level:.3f}")
    
    def run(self):
        """Run the visualizer"""
        self.root.mainloop()

# Global visualizer instance
visualizer = None

def start_visualizer():
    """Start the visualizer in a separate thread"""
    global visualizer
    visualizer = GameWindowVisualizer()
    visualizer.run()

def update_visualizer(mode: str, episode: int, reward: float, 
                     skill_level: float, mechanics: Dict[str, float]):
    """Update the visualizer with new training data"""
    global visualizer
    if visualizer:
        visualizer.update_training_data(mode, episode, reward, skill_level, mechanics)

def stop_visualizer():
    """Stop the visualizer"""
    global visualizer
    if visualizer:
        visualizer.root.quit()

if __name__ == "__main__":
    # Test the visualizer
    print("🎮 Starting Game Window Visualizer Test...")
    start_visualizer()
