#!/usr/bin/env python3
"""
Game Visualizer - Creates a proper game window for watching training
This opens as a movable window on your desktop like a game
"""

import pygame
import sys
import threading
import time
import math
from typing import Dict, Any, Optional

class GameVisualizer:
    def __init__(self, width=1200, height=800):
        """Initialize the game visualizer window"""
        pygame.init()
        
        # Window settings
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        pygame.display.set_caption("🚀 JSTN Bot Training Visualizer - Watch Your Bot Learn!")
        
        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.BLUE = (0, 100, 255)
        self.ORANGE = (255, 100, 0)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.YELLOW = (255, 255, 0)
        self.PURPLE = (128, 0, 128)
        
        # Game state
        self.ball_pos = [width // 2, height // 2]
        self.ball_vel = [0, 0]
        self.cars = []
        self.goals = [(50, height // 2), (width - 50, height // 2)]
        
        # Training info
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
        
        print("🎮 Game Visualizer Window Created!")
        print("   📺 You can move this window around your desktop")
        print("   🎯 Watch your bot learn in real-time!")
    
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
    
    def draw_field(self):
        """Draw the Rocket League field"""
        # Field background
        pygame.draw.rect(self.screen, (50, 150, 50), (0, 0, self.width, self.height))
        
        # Center line
        pygame.draw.line(self.screen, self.WHITE, (self.width // 2, 0), 
                        (self.width // 2, self.height), 3)
        
        # Center circle
        pygame.draw.circle(self.screen, self.WHITE, (self.width // 2, self.height // 2), 80, 3)
        
        # Goals
        for goal_x, goal_y in self.goals:
            pygame.draw.rect(self.screen, self.WHITE, (goal_x - 10, goal_y - 60, 20, 120), 3)
    
    def draw_ball(self):
        """Draw the ball with physics"""
        # Animate ball movement
        self.ball_pos[0] += self.ball_vel[0] * 0.1
        self.ball_pos[1] += self.ball_vel[1] * 0.1
        
        # Keep ball in bounds
        self.ball_pos[0] = max(20, min(self.width - 20, self.ball_pos[0]))
        self.ball_pos[1] = max(20, min(self.height - 20, self.ball_pos[1]))
        
        # Draw ball
        pygame.draw.circle(self.screen, self.ORANGE, 
                          (int(self.ball_pos[0]), int(self.ball_pos[1])), 15)
        pygame.draw.circle(self.screen, self.WHITE, 
                          (int(self.ball_pos[0]), int(self.ball_pos[1])), 15, 2)
    
    def draw_cars(self):
        """Draw the cars"""
        for i, car in enumerate(self.cars):
            if len(car) >= 2:
                x, y = car[0], car[1]
                color = self.BLUE if i == 0 else self.RED
                
                # Draw car body
                pygame.draw.rect(self.screen, color, (x - 15, y - 10, 30, 20))
                pygame.draw.rect(self.screen, self.WHITE, (x - 15, y - 10, 30, 20), 2)
                
                # Draw car name
                text = self.font_small.render(f"Bot {i+1}", True, self.WHITE)
                self.screen.blit(text, (x - 15, y - 25))
    
    def draw_training_info(self):
        """Draw training information"""
        # Background for info panel
        info_rect = pygame.Rect(10, 10, 400, 200)
        pygame.draw.rect(self.screen, (0, 0, 0, 180), info_rect)
        pygame.draw.rect(self.screen, self.WHITE, info_rect, 2)
        
        # Training mode
        mode_text = self.font_large.render(f"🎯 {self.training_mode.upper()} Training", True, self.YELLOW)
        self.screen.blit(mode_text, (20, 20))
        
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
            "🎮 JSTN Bot Training Visualizer",
            "📺 This window shows your bot learning in real-time",
            "🖱️  You can move this window around your desktop",
            "⌨️  Press ESC to close",
            "🚀 Watch your bot become SSL level!"
        ]
        
        y_start = self.height - 120
        for i, instruction in enumerate(instructions):
            color = self.YELLOW if i == 0 else self.WHITE
            font = self.font_medium if i == 0 else self.font_small
            text = font.render(instruction, True, color)
            self.screen.blit(text, (10, y_start + i * 20))
    
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
            
            # Clear screen
            self.screen.fill(self.BLACK)
            
            # Draw everything
            self.draw_field()
            self.draw_ball()
            self.draw_cars()
            self.draw_training_info()
            self.draw_instructions()
            
            # Update display
            pygame.display.flip()
            clock.tick(60)  # 60 FPS
        
        pygame.quit()
        print("🎮 Visualizer window closed")

# Global visualizer instance
visualizer = None

def start_visualizer():
    """Start the visualizer in a separate thread"""
    global visualizer
    visualizer = GameVisualizer()
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
    print("🎮 Starting Game Visualizer Test...")
    start_visualizer()

