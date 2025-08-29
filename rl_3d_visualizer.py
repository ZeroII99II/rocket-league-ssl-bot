#!/usr/bin/env python3
"""
Rocket League 3D-Style Visualizer
Creates a 3D-looking Rocket League field with proper perspective
"""

import pygame
import math
import sys
import threading
import time
from typing import Dict, Any

class RL3DVisualizer:
    def __init__(self, width=1400, height=900):
        """Initialize the 3D-style visualizer"""
        pygame.init()
        
        # Window settings
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        pygame.display.set_caption("🚀 JSTN Bot Training - 3D Rocket League Visualizer")
        
        # Colors (Rocket League style)
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
        
        # 3D perspective settings
        self.camera_angle = 0
        self.field_length = 4000
        self.field_width = 3000
        self.field_height = 1000
        
        # Game objects
        self.ball_pos = [0, 0, 100]
        self.ball_vel = [50, 30, 20]
        self.cars = [[-500, 0, 0], [500, 0, 0]]  # Add some cars
        self.boost_pads = []
        
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
        
        # Fonts
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
        
        # Animation
        self.animation_time = 0
        self.running = True
        
        # Initialize boost pads
        self.init_boost_pads()
        
        print("🎮 3D Rocket League Visualizer Created!")
        print("   📺 Full 3D perspective like the real game!")
        print("   🎯 Watch your bot learn in 3D!")
    
    def init_boost_pads(self):
        """Initialize boost pad positions"""
        # Large boost pads
        self.boost_pads = [
            # Center
            {"pos": [0, 0, 0], "size": "large", "active": True},
            # Corners
            {"pos": [-2000, -1500, 0], "size": "large", "active": True},
            {"pos": [2000, -1500, 0], "size": "large", "active": True},
            {"pos": [-2000, 1500, 0], "size": "large", "active": True},
            {"pos": [2000, 1500, 0], "size": "large", "active": True},
        ]
        
        # Small boost pads along the sides
        for x in range(-1800, 2000, 400):
            self.boost_pads.append({"pos": [x, -1500, 0], "size": "small", "active": True})
            self.boost_pads.append({"pos": [x, 1500, 0], "size": "small", "active": True})
    
    def project_3d_to_2d(self, x, y, z):
        """Project 3D coordinates to 2D screen coordinates with perspective"""
        # Simple isometric projection that actually works
        # Scale down the field to fit on screen
        scale = 0.15
        
        # Isometric projection
        screen_x = self.width // 2 + (x - y) * scale
        screen_y = self.height // 2 + (x + y) * scale * 0.5 - z * scale * 0.3
        
        return int(screen_x), int(screen_y)
    
    def draw_3d_field(self):
        """Draw the 3D Rocket League field"""
        # Field background (ground)
        corners = [
            [-self.field_length//2, -self.field_width//2, 0],
            [self.field_length//2, -self.field_width//2, 0],
            [self.field_length//2, self.field_width//2, 0],
            [-self.field_length//2, self.field_width//2, 0]
        ]
        
        # Project corners to 2D
        screen_corners = []
        for corner in corners:
            x, y = self.project_3d_to_2d(corner[0], corner[1], corner[2])
            if x is not None:
                screen_corners.append((x, y))
        
        if len(screen_corners) == 4:
            pygame.draw.polygon(self.screen, self.DARK_GREEN, screen_corners)
        
        # Field lines
        self.draw_field_lines()
        
        # Goals
        self.draw_goals()
        
        # Boost pads
        self.draw_boost_pads()
    
    def draw_field_lines(self):
        """Draw field lines in 3D"""
        # Center line
        start = self.project_3d_to_2d(0, -self.field_width//2, 0)
        end = self.project_3d_to_2d(0, self.field_width//2, 0)
        if start[0] is not None and end[0] is not None:
            pygame.draw.line(self.screen, self.WHITE, start, end, 3)
        
        # Center circle
        for angle in range(0, 360, 10):
            x = math.cos(math.radians(angle)) * 1000
            y = math.sin(math.radians(angle)) * 1000
            pos = self.project_3d_to_2d(x, y, 0)
            if pos[0] is not None:
                pygame.draw.circle(self.screen, self.WHITE, pos, 2)
    
    def draw_goals(self):
        """Draw the goals in 3D"""
        # Blue goal (left)
        goal_corners = [
            [-self.field_length//2, -500, 0],
            [-self.field_length//2, 500, 0],
            [-self.field_length//2, 500, 500],
            [-self.field_length//2, -500, 500]
        ]
        
        screen_corners = []
        for corner in goal_corners:
            x, y = self.project_3d_to_2d(corner[0], corner[1], corner[2])
            if x is not None:
                screen_corners.append((x, y))
        
        if len(screen_corners) == 4:
            pygame.draw.polygon(self.screen, self.BLUE, screen_corners)
            pygame.draw.polygon(self.screen, self.WHITE, screen_corners, 3)
        
        # Orange goal (right)
        goal_corners = [
            [self.field_length//2, -500, 0],
            [self.field_length//2, 500, 0],
            [self.field_length//2, 500, 500],
            [self.field_length//2, -500, 500]
        ]
        
        screen_corners = []
        for corner in goal_corners:
            x, y = self.project_3d_to_2d(corner[0], corner[1], corner[2])
            if x is not None:
                screen_corners.append((x, y))
        
        if len(screen_corners) == 4:
            pygame.draw.polygon(self.screen, self.ORANGE, screen_corners)
            pygame.draw.polygon(self.screen, self.WHITE, screen_corners, 3)
    
    def draw_boost_pads(self):
        """Draw boost pads in 3D"""
        for pad in self.boost_pads:
            if pad["active"]:
                x, y = self.project_3d_to_2d(pad["pos"][0], pad["pos"][1], pad["pos"][2])
                if x is not None:
                    size = 20 if pad["size"] == "large" else 10
                    color = self.YELLOW if pad["size"] == "large" else self.GRAY
                    pygame.draw.circle(self.screen, color, (x, y), size)
                    pygame.draw.circle(self.screen, self.WHITE, (x, y), size, 2)
    
    def draw_ball(self):
        """Draw the ball in 3D"""
        x, y = self.project_3d_to_2d(self.ball_pos[0], self.ball_pos[1], self.ball_pos[2])
        if x is not None and 0 <= x < self.width and 0 <= y < self.height:
            # Ball shadow
            shadow_x, shadow_y = self.project_3d_to_2d(self.ball_pos[0], self.ball_pos[1], 0)
            if shadow_x is not None and 0 <= shadow_x < self.width and 0 <= shadow_y < self.height:
                pygame.draw.circle(self.screen, (50, 50, 50), (shadow_x, shadow_y), 12)
            
            # Ball
            pygame.draw.circle(self.screen, self.ORANGE, (x, y), 15)
            pygame.draw.circle(self.screen, self.WHITE, (x, y), 15, 2)
            
            # Ball trail (simplified)
            for i in range(1, 4):
                trail_x = x - self.ball_vel[0] * i * 0.5
                trail_y = y + self.ball_vel[1] * i * 0.5
                if 0 <= trail_x < self.width and 0 <= trail_y < self.height:
                    pygame.draw.circle(self.screen, (255, 150, 0), (int(trail_x), int(trail_y)), 15 - i * 3)
    
    def draw_cars(self):
        """Draw cars in 3D"""
        for i, car in enumerate(self.cars):
            if len(car) >= 3:
                x, y = self.project_3d_to_2d(car[0], car[1], car[2])
                if x is not None:
                    color = self.BLUE if i == 0 else self.RED
                    
                    # Car body
                    pygame.draw.rect(self.screen, color, (x - 20, y - 15, 40, 30))
                    pygame.draw.rect(self.screen, self.WHITE, (x - 20, y - 15, 40, 30), 2)
                    
                    # Car name
                    text = self.font_small.render(f"JSTN Bot" if i == 0 else f"Bot {i+1}", True, self.WHITE)
                    self.screen.blit(text, (x - 30, y - 35))
    
    def draw_training_info(self):
        """Draw training information overlay"""
        # Background panel
        panel_rect = pygame.Rect(10, 10, 450, 250)
        pygame.draw.rect(self.screen, (0, 0, 0, 200), panel_rect)
        pygame.draw.rect(self.screen, self.WHITE, panel_rect, 2)
        
        # Title
        title_text = self.font_large.render(f"🎯 {self.training_mode.upper()} Training", True, self.YELLOW)
        self.screen.blit(title_text, (20, 20))
        
        # Episode and reward
        episode_text = self.font_medium.render(f"Episode: {self.episode}", True, self.WHITE)
        self.screen.blit(episode_text, (20, 70))
        
        reward_text = self.font_medium.render(f"Reward: {self.reward:.2f}", True, self.GREEN)
        self.screen.blit(reward_text, (20, 100))
        
        # Skill level
        skill_text = self.font_medium.render(f"JSTN Level: {self.skill_level:.3f}", True, self.PURPLE)
        self.screen.blit(skill_text, (20, 130))
        
        # Mechanics
        y_offset = 160
        for mechanic, level in self.mechanics.items():
            mechanic_text = self.font_small.render(f"{mechanic.replace('_', ' ').title()}: {level:.3f}", True, self.WHITE)
            self.screen.blit(mechanic_text, (20, y_offset))
            y_offset += 20
    
    def draw_instructions(self):
        """Draw instructions"""
        instructions = [
            "🎮 3D Rocket League Training Visualizer",
            "📺 Full 3D perspective like the real game!",
            "🖱️  Move this window around your desktop",
            "⌨️  Press ESC to close",
            "🚀 Watch your bot become SSL level!"
        ]
        
        y_start = self.height - 120
        for i, instruction in enumerate(instructions):
            color = self.YELLOW if i == 0 else self.WHITE
            font = self.font_medium if i == 0 else self.font_small
            text = font.render(instruction, True, color)
            self.screen.blit(text, (10, y_start + i * 20))
    
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
            
            # Update animation
            self.animation_time += 0.1
            
            # Animate ball
            self.ball_pos[0] += self.ball_vel[0] * 0.1
            self.ball_pos[1] += self.ball_vel[1] * 0.1
            self.ball_pos[2] += self.ball_vel[2] * 0.1
            
            # Bounce ball off walls
            if abs(self.ball_pos[0]) > self.field_length//2:
                self.ball_vel[0] = -self.ball_vel[0]
            if abs(self.ball_pos[1]) > self.field_width//2:
                self.ball_vel[1] = -self.ball_vel[1]
            if self.ball_pos[2] < 0:
                self.ball_vel[2] = -self.ball_vel[2]
                self.ball_pos[2] = 0
            
            # Keep ball in bounds
            self.ball_pos[0] = max(-self.field_length//2, min(self.field_length//2, self.ball_pos[0]))
            self.ball_pos[1] = max(-self.field_width//2, min(self.field_width//2, self.ball_pos[1]))
            self.ball_pos[2] = max(0, min(1000, self.ball_pos[2]))
            
            # Clear screen
            self.screen.fill(self.BLACK)
            
            # Draw everything
            self.draw_3d_field()
            self.draw_ball()
            self.draw_cars()
            self.draw_training_info()
            self.draw_instructions()
            
            # Update display
            pygame.display.flip()
            clock.tick(60)  # 60 FPS
        
        pygame.quit()
        print("🎮 3D Visualizer window closed")

# Global visualizer instance
visualizer = None

def start_visualizer():
    """Start the visualizer in a separate thread"""
    global visualizer
    visualizer = RL3DVisualizer()
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
    print("🎮 Starting 3D Rocket League Visualizer Test...")
    start_visualizer()
