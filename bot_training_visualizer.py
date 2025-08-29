#!/usr/bin/env python3
"""
Bot Training Visualizer - Shows what the bot is seeing, thinking, and doing
Multi-panel view like the user's setup with real-time bot training data
"""

import pygame
import math
import sys
import threading
import time
import json
from typing import Dict, Any, List
from datetime import datetime

class BotTrainingVisualizer:
    def __init__(self, width=1600, height=1000):
        """Initialize the bot training visualizer"""
        pygame.init()
        
        # Window settings
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        pygame.display.set_caption("🤖 JSTN Bot Training - Watch Your Bot Learn!")
        
        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.BLUE = (0, 100, 255)
        self.ORANGE = (255, 100, 0)
        self.GREEN = (0, 200, 0)
        self.RED = (255, 50, 50)
        self.YELLOW = (255, 255, 0)
        self.PURPLE = (150, 0, 150)
        self.GRAY = (100, 100, 100)
        self.DARK_GREEN = (0, 100, 0)
        self.CYAN = (0, 255, 255)
        self.PINK = (255, 100, 150)
        
        # Panel dimensions
        self.left_panel_width = int(width * 0.4)   # 3D game view
        self.middle_panel_width = int(width * 0.35) # Bot thoughts/console
        self.right_panel_width = int(width * 0.25)  # 2D tactical map
        
        # Fonts
        self.font_large = pygame.font.Font(None, 24)
        self.font_medium = pygame.font.Font(None, 18)
        self.font_small = pygame.font.Font(None, 14)
        self.font_tiny = pygame.font.Font(None, 12)
        
        # Bot training data
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
        
        # Bot state data
        self.bot_thoughts = []
        self.bot_actions = []
        self.bot_observations = []
        self.bot_predictions = []
        self.console_output = []
        
        # Game state
        self.ball_pos = [0, 0, 100]
        self.ball_vel = [50, 30, 20]
        self.cars = [[-500, 0, 0], [500, 0, 0]]
        self.boost_pads = []
        
        # Animation
        self.animation_time = 0
        self.running = True
        self.last_update = time.time()
        
        # Initialize boost pads
        self.init_boost_pads()
        
        print("🤖 Bot Training Visualizer Created!")
        print("   📺 Multi-panel view showing bot's thoughts and actions!")
        print("   🧠 Watch your bot learn in real-time!")
    
    def init_boost_pads(self):
        """Initialize boost pad positions"""
        self.boost_pads = [
            {"pos": [0, 0, 0], "size": "large", "active": True},
            {"pos": [-2000, -1500, 0], "size": "large", "active": True},
            {"pos": [2000, -1500, 0], "size": "large", "active": True},
            {"pos": [-2000, 1500, 0], "size": "large", "active": True},
            {"pos": [2000, 1500, 0], "size": "large", "active": True},
        ]
        
        for x in range(-1800, 2000, 400):
            self.boost_pads.append({"pos": [x, -1500, 0], "size": "small", "active": True})
            self.boost_pads.append({"pos": [x, 1500, 0], "size": "small", "active": True})
    
    def project_3d_to_2d(self, x, y, z):
        """Project 3D coordinates to 2D screen coordinates"""
        scale = 0.08
        screen_x = self.left_panel_width // 2 + (x - y) * scale
        screen_y = self.height // 2 + (x + y) * scale * 0.5 - z * scale * 0.3
        return int(screen_x), int(screen_y)
    
    def draw_left_panel_3d(self):
        """Draw the 3D game view (left panel)"""
        # Panel background
        pygame.draw.rect(self.screen, (20, 20, 40), (0, 0, self.left_panel_width, self.height))
        
        # Draw 3D field
        self.draw_3d_field()
        self.draw_ball()
        self.draw_cars()
        self.draw_boost_pads()
        
        # Panel title
        title = self.font_large.render("🎮 3D Game View", True, self.YELLOW)
        self.screen.blit(title, (10, 10))
    
    def draw_3d_field(self):
        """Draw the 3D Rocket League field"""
        # Field background
        corners = [
            [-2000, -1500, 0], [2000, -1500, 0], [2000, 1500, 0], [-2000, 1500, 0]
        ]
        
        screen_corners = []
        for corner in corners:
            x, y = self.project_3d_to_2d(corner[0], corner[1], corner[2])
            screen_corners.append((x, y))
        
        pygame.draw.polygon(self.screen, self.DARK_GREEN, screen_corners)
        
        # Field lines
        # Center line
        start = self.project_3d_to_2d(0, -1500, 0)
        end = self.project_3d_to_2d(0, 1500, 0)
        pygame.draw.line(self.screen, self.WHITE, start, end, 2)
        
        # Goals
        # Blue goal
        goal_corners = [
            [-2000, -500, 0], [-2000, 500, 0], [-2000, 500, 500], [-2000, -500, 500]
        ]
        screen_goal = []
        for corner in goal_corners:
            x, y = self.project_3d_to_2d(corner[0], corner[1], corner[2])
            screen_goal.append((x, y))
        pygame.draw.polygon(self.screen, self.BLUE, screen_goal)
        
        # Orange goal
        goal_corners = [
            [2000, -500, 0], [2000, 500, 0], [2000, 500, 500], [2000, -500, 500]
        ]
        screen_goal = []
        for corner in goal_corners:
            x, y = self.project_3d_to_2d(corner[0], corner[1], corner[2])
            screen_goal.append((x, y))
        pygame.draw.polygon(self.screen, self.ORANGE, screen_goal)
    
    def draw_ball(self):
        """Draw the ball in 3D"""
        x, y = self.project_3d_to_2d(self.ball_pos[0], self.ball_pos[1], self.ball_pos[2])
        if 0 <= x < self.left_panel_width and 0 <= y < self.height:
            # Ball shadow
            shadow_x, shadow_y = self.project_3d_to_2d(self.ball_pos[0], self.ball_pos[1], 0)
            pygame.draw.circle(self.screen, (50, 50, 50), (shadow_x, shadow_y), 8)
            
            # Ball
            pygame.draw.circle(self.screen, self.ORANGE, (x, y), 10)
            pygame.draw.circle(self.screen, self.WHITE, (x, y), 10, 2)
    
    def draw_cars(self):
        """Draw cars in 3D"""
        for i, car in enumerate(self.cars):
            if len(car) >= 3:
                x, y = self.project_3d_to_2d(car[0], car[1], car[2])
                if 0 <= x < self.left_panel_width and 0 <= y < self.height:
                    color = self.BLUE if i == 0 else self.RED
                    pygame.draw.rect(self.screen, color, (x - 12, y - 8, 24, 16))
                    pygame.draw.rect(self.screen, self.WHITE, (x - 12, y - 8, 24, 16), 2)
    
    def draw_boost_pads(self):
        """Draw boost pads in 3D"""
        for pad in self.boost_pads:
            if pad["active"]:
                x, y = self.project_3d_to_2d(pad["pos"][0], pad["pos"][1], pad["pos"][2])
                if 0 <= x < self.left_panel_width and 0 <= y < self.height:
                    size = 8 if pad["size"] == "large" else 4
                    color = self.YELLOW if pad["size"] == "large" else self.GRAY
                    pygame.draw.circle(self.screen, color, (x, y), size)
    
    def draw_middle_panel_thoughts(self):
        """Draw the bot's thoughts and console (middle panel)"""
        x_start = self.left_panel_width
        
        # Panel background
        pygame.draw.rect(self.screen, (30, 30, 30), (x_start, 0, self.middle_panel_width, self.height))
        
        # Panel title
        title = self.font_large.render("🧠 Bot's Thoughts & Actions", True, self.CYAN)
        self.screen.blit(title, (x_start + 10, 10))
        
        # Training info
        y_pos = 40
        info_texts = [
            f"Mode: {self.training_mode.upper()}",
            f"Episode: {self.episode}",
            f"Reward: {self.reward:.2f}",
            f"JSTN Level: {self.skill_level:.3f}"
        ]
        
        for text in info_texts:
            rendered = self.font_medium.render(text, True, self.WHITE)
            self.screen.blit(rendered, (x_start + 10, y_pos))
            y_pos += 25
        
        # Bot's current thoughts
        y_pos += 20
        thoughts_title = self.font_medium.render("🤔 What I'm Thinking:", True, self.YELLOW)
        self.screen.blit(thoughts_title, (x_start + 10, y_pos))
        y_pos += 25
        
        thoughts = [
            f"Ball position: ({self.ball_pos[0]:.0f}, {self.ball_pos[1]:.0f}, {self.ball_pos[2]:.0f})",
            f"Ball velocity: ({self.ball_vel[0]:.0f}, {self.ball_vel[1]:.0f}, {self.ball_vel[2]:.0f})",
            f"Distance to ball: {math.sqrt(sum((self.ball_pos[i] - self.cars[0][i])**2 for i in range(3))):.0f}",
            f"Learning aerial: {self.mechanics['aerial']:.3f}",
            f"Learning flip reset: {self.mechanics['flip_reset']:.3f}",
            f"Learning double tap: {self.mechanics['double_tap']:.3f}"
        ]
        
        for thought in thoughts:
            rendered = self.font_small.render(thought, True, self.WHITE)
            self.screen.blit(rendered, (x_start + 10, y_pos))
            y_pos += 18
        
        # Bot's actions
        y_pos += 20
        actions_title = self.font_medium.render("⚡ What I'm Doing:", True, self.GREEN)
        self.screen.blit(actions_title, (x_start + 10, y_pos))
        y_pos += 25
        
        actions = [
            "🎯 Targeting ball position",
            "🚀 Calculating boost needed",
            "🔄 Planning flip reset attempt",
            "📐 Adjusting car angle",
            "⚡ Executing aerial maneuver",
            "🎮 Learning from this action"
        ]
        
        for action in actions:
            rendered = self.font_small.render(action, True, self.WHITE)
            self.screen.blit(rendered, (x_start + 10, y_pos))
            y_pos += 18
        
        # Console output
        y_pos += 20
        console_title = self.font_medium.render("📟 Training Console:", True, self.PURPLE)
        self.screen.blit(console_title, (x_start + 10, y_pos))
        y_pos += 25
        
        console_messages = [
            f"[{datetime.now().strftime('%H:%M:%S')}] Episode {self.episode} started",
            f"[{datetime.now().strftime('%H:%M:%S')}] Bot analyzing game state...",
            f"[{datetime.now().strftime('%H:%M:%S')}] Calculating optimal action...",
            f"[{datetime.now().strftime('%H:%M:%S')}] Executing aerial maneuver",
            f"[{datetime.now().strftime('%H:%M:%S')}] Learning from result...",
            f"[{datetime.now().strftime('%H:%M:%S')}] Skill level: {self.skill_level:.3f}"
        ]
        
        for msg in console_messages:
            rendered = self.font_tiny.render(msg, True, self.CYAN)
            self.screen.blit(rendered, (x_start + 10, y_pos))
            y_pos += 15
    
    def draw_right_panel_tactical(self):
        """Draw the 2D tactical map (right panel)"""
        x_start = self.left_panel_width + self.middle_panel_width
        
        # Panel background
        pygame.draw.rect(self.screen, (20, 40, 20), (x_start, 0, self.right_panel_width, self.height))
        
        # Panel title
        title = self.font_large.render("🗺️ Tactical Map", True, self.GREEN)
        self.screen.blit(title, (x_start + 10, 10))
        
        # Field dimensions
        field_x = x_start + 20
        field_y = 50
        field_width = self.right_panel_width - 40
        field_height = int(field_width * 0.6)
        
        # Draw field
        pygame.draw.rect(self.screen, self.DARK_GREEN, (field_x, field_y, field_width, field_height))
        pygame.draw.rect(self.screen, self.WHITE, (field_x, field_y, field_width, field_height), 2)
        
        # Center line
        pygame.draw.line(self.screen, self.WHITE, 
                        (field_x + field_width//2, field_y), 
                        (field_x + field_width//2, field_y + field_height), 2)
        
        # Goals
        goal_width = 20
        goal_height = 60
        # Blue goal (left)
        pygame.draw.rect(self.screen, self.BLUE, 
                        (field_x - goal_width//2, field_y + field_height//2 - goal_height//2, 
                         goal_width, goal_height))
        # Orange goal (right)
        pygame.draw.rect(self.screen, self.ORANGE, 
                        (field_x + field_width - goal_width//2, field_y + field_height//2 - goal_height//2, 
                         goal_width, goal_height))
        
        # Convert 3D positions to 2D tactical map
        def to_tactical_pos(x, y):
            tactical_x = field_x + field_width//2 + (x / 4000) * (field_width//2)
            tactical_y = field_y + field_height//2 + (y / 3000) * (field_height//2)
            return int(tactical_x), int(tactical_y)
        
        # Draw ball
        ball_x, ball_y = to_tactical_pos(self.ball_pos[0], self.ball_pos[1])
        pygame.draw.circle(self.screen, self.ORANGE, (ball_x, ball_y), 8)
        pygame.draw.circle(self.screen, self.WHITE, (ball_x, ball_y), 8, 2)
        
        # Draw cars
        for i, car in enumerate(self.cars):
            car_x, car_y = to_tactical_pos(car[0], car[1])
            color = self.BLUE if i == 0 else self.RED
            pygame.draw.rect(self.screen, color, (car_x - 8, car_y - 6, 16, 12))
            pygame.draw.rect(self.screen, self.WHITE, (car_x - 8, car_y - 6, 16, 12), 2)
            
            # Car labels
            label = "JSTN" if i == 0 else f"Bot{i+1}"
            text = self.font_tiny.render(label, True, self.WHITE)
            self.screen.blit(text, (car_x - 10, car_y - 20))
        
        # Draw boost pads
        for pad in self.boost_pads:
            if pad["active"]:
                pad_x, pad_y = to_tactical_pos(pad["pos"][0], pad["pos"][1])
                size = 4 if pad["size"] == "large" else 2
                color = self.YELLOW if pad["size"] == "large" else self.GRAY
                pygame.draw.circle(self.screen, color, (pad_x, pad_y), size)
        
        # Training progress
        y_pos = field_y + field_height + 20
        progress_title = self.font_medium.render("📊 Learning Progress:", True, self.YELLOW)
        self.screen.blit(progress_title, (x_start + 10, y_pos))
        y_pos += 25
        
        for mechanic, level in self.mechanics.items():
            # Progress bar
            bar_width = 100
            bar_height = 15
            bar_x = x_start + 10
            bar_y = y_pos
            
            # Background
            pygame.draw.rect(self.screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
            # Progress
            progress_width = int(bar_width * level)
            pygame.draw.rect(self.screen, self.GREEN, (bar_x, bar_y, progress_width, bar_height))
            pygame.draw.rect(self.screen, self.WHITE, (bar_x, bar_y, bar_width, bar_height), 1)
            
            # Label
            label = self.font_tiny.render(mechanic.replace('_', ' ').title(), True, self.WHITE)
            self.screen.blit(label, (bar_x + bar_width + 10, bar_y + 2))
            
            y_pos += 20
    
    def update_training_data(self, mode: str, episode: int, reward: float, 
                           skill_level: float, mechanics: Dict[str, float]):
        """Update the training data to display"""
        self.training_mode = mode
        self.episode = episode
        self.reward = reward
        self.skill_level = skill_level
        self.mechanics.update(mechanics)
    
    def update_game_state(self, ball_pos: list, ball_vel: list, cars: list):
        """Update the game state for visualization"""
        self.ball_pos = ball_pos
        self.ball_vel = ball_vel
        self.cars = cars
    
    def run(self):
        """Main game loop"""
        clock = pygame.time.Clock()
        
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                elif event.type == pygame.VIDEORESIZE:
                    self.width, self.height = event.w, event.h
                    self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
                    # Recalculate panel widths
                    self.left_panel_width = int(self.width * 0.4)
                    self.middle_panel_width = int(self.width * 0.35)
                    self.right_panel_width = int(self.width * 0.25)
            
            # Update animation
            self.animation_time += 0.1
            
            # Animate ball
            self.ball_pos[0] += self.ball_vel[0] * 0.1
            self.ball_pos[1] += self.ball_vel[1] * 0.1
            self.ball_pos[2] += self.ball_vel[2] * 0.1
            
            # Bounce ball off walls
            if abs(self.ball_pos[0]) > 2000:
                self.ball_vel[0] = -self.ball_vel[0]
            if abs(self.ball_pos[1]) > 1500:
                self.ball_vel[1] = -self.ball_vel[1]
            if self.ball_pos[2] < 0:
                self.ball_vel[2] = -self.ball_vel[2]
                self.ball_pos[2] = 0
            
            # Keep ball in bounds
            self.ball_pos[0] = max(-2000, min(2000, self.ball_pos[0]))
            self.ball_pos[1] = max(-1500, min(1500, self.ball_pos[1]))
            self.ball_pos[2] = max(0, min(1000, self.ball_pos[2]))
            
            # Clear screen
            self.screen.fill(self.BLACK)
            
            # Draw all panels
            self.draw_left_panel_3d()
            self.draw_middle_panel_thoughts()
            self.draw_right_panel_tactical()
            
            # Update display
            pygame.display.flip()
            clock.tick(60)  # 60 FPS
        
        pygame.quit()
        print("🤖 Bot Training Visualizer closed")

# Global visualizer instance
visualizer = None

def start_visualizer():
    """Start the visualizer in a separate thread"""
    global visualizer
    visualizer = BotTrainingVisualizer()
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
        visualizer.running = False

if __name__ == "__main__":
    # Test the visualizer
    print("🤖 Starting Bot Training Visualizer Test...")
    start_visualizer()

