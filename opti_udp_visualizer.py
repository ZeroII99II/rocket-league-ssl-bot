#!/usr/bin/env python3
"""
Opti UDP Visualizer - Full 3D Rocket League Visualizer
Authentic Rocket League experience with detailed 3D graphics and real-time bot training
"""

import pygame
import socket
import threading
import struct
import math
import time
import json
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

# UDP Configuration
UDP_IP = "127.0.0.1"
UDP_PORT = 37020
BUFFER_SIZE = 65536

# Rocket League Field Constants (exact measurements)
FIELD_LENGTH = 10240  # X-axis
FIELD_WIDTH = 8192    # Y-axis  
FIELD_HEIGHT = 2048   # Z-axis (ceiling)
GOAL_WIDTH = 1786
GOAL_HEIGHT = 642
GOAL_DEPTH = 880
BALL_RADIUS = 92.75
CAR_LENGTH = 118.01
CAR_WIDTH = 84.2
CAR_HEIGHT = 36.16

# Rocket League Colors (authentic)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE_TEAM = (0, 100, 255)
ORANGE_TEAM = (255, 100, 0)
FIELD_GREEN = (34, 139, 34)
FIELD_LINES = (255, 255, 255)
GOAL_BLUE = (0, 50, 200)
GOAL_ORANGE = (200, 50, 0)
BALL_WHITE = (255, 255, 255)
BALL_ORANGE = (255, 140, 0)
BOOST_YELLOW = (255, 215, 0)
BOOST_GRAY = (128, 128, 128)
WALL_COLOR = (50, 50, 50)
SKY_BLUE = (135, 206, 235)
SHADOW_GRAY = (64, 64, 64)

# Enhanced Colors for 3D Effect
DARK_GREEN = (0, 80, 0)
LIGHT_GREEN = (50, 200, 50)
DARK_BLUE = (0, 0, 100)
LIGHT_BLUE = (100, 150, 255)
DARK_ORANGE = (200, 50, 0)
LIGHT_ORANGE = (255, 150, 50)

class GameMode(Enum):
    SOCCER = 0
    HOOPS = 1

@dataclass
class Vector3:
    x: float
    y: float
    z: float

@dataclass
class Rotator:
    pitch: float
    yaw: float
    roll: float

@dataclass
class CarState:
    position: Vector3
    rotation: Rotator
    velocity: Vector3
    angular_velocity: Vector3
    boost: float
    on_ground: bool
    has_jumped: bool
    has_double_jumped: bool
    team: int  # 0 = blue, 1 = orange

@dataclass
class BallState:
    position: Vector3
    velocity: Vector3
    angular_velocity: Vector3

@dataclass
class BoostPad:
    position: Vector3
    is_active: bool
    is_large: bool

@dataclass
class GameState:
    ball: BallState
    cars: List[CarState]
    boost_pads: List[BoostPad]
    game_mode: GameMode
    time: float
    score_blue: int
    score_orange: int

class OptiUDPVisualizer:
    def __init__(self, width=1920, height=1080):
        """Initialize the Full 3D Rocket League Visualizer"""
        pygame.init()
        
        # Window settings - Full HD for maximum detail
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        pygame.display.set_caption("🤖 Opti JSTN Bot Training - Full 3D Rocket League Visualizer")
        
        # Panel dimensions - Main 3D view takes most space
        self.game_view_width = int(width * 0.7)   # Main 3D Rocket League view
        self.info_panel_width = int(width * 0.3)  # Bot info panel
        
        # Fonts - Larger for better readability
        self.font_large = pygame.font.Font(None, 32)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 18)
        self.font_tiny = pygame.font.Font(None, 14)
        
        # Advanced 3D Camera System
        self.camera_pos = Vector3(0, -8000, 3000)  # Higher and further for overview
        self.camera_target = Vector3(0, 0, 0)
        self.camera_up = Vector3(0, 0, 1)
        self.camera_distance = 8000
        self.camera_height = 3000
        self.camera_pitch = math.radians(25)  # Better angle for overview
        self.camera_yaw = math.radians(0)
        self.camera_roll = math.radians(0)
        
        # 3D Rendering Settings
        self.fov = math.radians(60)  # Field of view
        self.near_plane = 100
        self.far_plane = 20000
        self.perspective_scale = 0.8
        
        # Game state
        self.game_state: Optional[GameState] = None
        self.last_update = time.time()
        self.fps = 0
        self.frame_count = 0
        
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
            "wall_play": 0.0,
            "dribbling": 0.0,
            "shooting": 0.0,
            "defending": 0.0
        }
        
        # Bot thoughts and actions
        self.bot_thoughts = []
        self.bot_actions = []
        self.console_messages = []
        
        # Controls
        self.menu_open = True
        self.paused = False
        self.game_speed = 1.0
        self.camera_focus = 0  # 0-7 for cars, 8 for director, 9 for free
        
        # 3D Rendering Cache
        self.field_vertices = []
        self.goal_vertices = []
        self.boost_pad_vertices = []
        self.wall_vertices = []
        self.ceiling_vertices = []
        
        # Initialize 3D geometry
        self.init_3d_geometry()
        
        # UDP Socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((UDP_IP, UDP_PORT))
        self.sock.settimeout(0.1)  # Non-blocking
        
        # Threading
        self.running = True
        self.udp_thread = threading.Thread(target=self.udp_listener, daemon=True)
        self.udp_thread.start()
        
        print("🤖 Full 3D Rocket League Visualizer Created!")
        print(f"   📡 Listening on UDP {UDP_IP}:{UDP_PORT}")
        print("   🎮 Controls: ESC=Menu, 1-8=Cars, 9=Director, 0=Free, WASD=Move, Space/Ctrl=Up/Down")
        print("   ⚡ P=Pause, +/-=Speed, R=Reset ball, Click=Drag objects")
        print("   🎯 Full 3D Rocket League experience with authentic graphics!")
    
    def init_3d_geometry(self):
        """Initialize all 3D geometry for the Rocket League field"""
        # Field vertices (ground)
        self.field_vertices = [
            # Main field
            Vector3(-FIELD_LENGTH/2, -FIELD_WIDTH/2, 0),
            Vector3(FIELD_LENGTH/2, -FIELD_WIDTH/2, 0),
            Vector3(FIELD_LENGTH/2, FIELD_WIDTH/2, 0),
            Vector3(-FIELD_LENGTH/2, FIELD_WIDTH/2, 0),
        ]
        
        # Goal vertices (Blue goal - left)
        self.goal_vertices = [
            # Blue goal
            Vector3(-FIELD_LENGTH/2, -GOAL_WIDTH/2, 0),
            Vector3(-FIELD_LENGTH/2 - GOAL_DEPTH, -GOAL_WIDTH/2, 0),
            Vector3(-FIELD_LENGTH/2 - GOAL_DEPTH, GOAL_WIDTH/2, 0),
            Vector3(-FIELD_LENGTH/2, GOAL_WIDTH/2, 0),
            Vector3(-FIELD_LENGTH/2, -GOAL_WIDTH/2, GOAL_HEIGHT),
            Vector3(-FIELD_LENGTH/2 - GOAL_DEPTH, -GOAL_WIDTH/2, GOAL_HEIGHT),
            Vector3(-FIELD_LENGTH/2 - GOAL_DEPTH, GOAL_WIDTH/2, GOAL_HEIGHT),
            Vector3(-FIELD_LENGTH/2, GOAL_WIDTH/2, GOAL_HEIGHT),
            
            # Orange goal (right)
            Vector3(FIELD_LENGTH/2, -GOAL_WIDTH/2, 0),
            Vector3(FIELD_LENGTH/2 + GOAL_DEPTH, -GOAL_WIDTH/2, 0),
            Vector3(FIELD_LENGTH/2 + GOAL_DEPTH, GOAL_WIDTH/2, 0),
            Vector3(FIELD_LENGTH/2, GOAL_WIDTH/2, 0),
            Vector3(FIELD_LENGTH/2, -GOAL_WIDTH/2, GOAL_HEIGHT),
            Vector3(FIELD_LENGTH/2 + GOAL_DEPTH, -GOAL_WIDTH/2, GOAL_HEIGHT),
            Vector3(FIELD_LENGTH/2 + GOAL_DEPTH, GOAL_WIDTH/2, GOAL_HEIGHT),
            Vector3(FIELD_LENGTH/2, GOAL_WIDTH/2, GOAL_HEIGHT),
        ]
        
        # Wall vertices
        self.wall_vertices = [
            # Side walls
            Vector3(-FIELD_LENGTH/2, -FIELD_WIDTH/2, 0),
            Vector3(-FIELD_LENGTH/2, -FIELD_WIDTH/2, FIELD_HEIGHT),
            Vector3(FIELD_LENGTH/2, -FIELD_WIDTH/2, FIELD_HEIGHT),
            Vector3(FIELD_LENGTH/2, -FIELD_WIDTH/2, 0),
            
            Vector3(-FIELD_LENGTH/2, FIELD_WIDTH/2, 0),
            Vector3(-FIELD_LENGTH/2, FIELD_WIDTH/2, FIELD_HEIGHT),
            Vector3(FIELD_LENGTH/2, FIELD_WIDTH/2, FIELD_HEIGHT),
            Vector3(FIELD_LENGTH/2, FIELD_WIDTH/2, 0),
            
            # End walls
            Vector3(-FIELD_LENGTH/2, -FIELD_WIDTH/2, 0),
            Vector3(-FIELD_LENGTH/2, -FIELD_WIDTH/2, FIELD_HEIGHT),
            Vector3(-FIELD_LENGTH/2, FIELD_WIDTH/2, FIELD_HEIGHT),
            Vector3(-FIELD_LENGTH/2, FIELD_WIDTH/2, 0),
            
            Vector3(FIELD_LENGTH/2, -FIELD_WIDTH/2, 0),
            Vector3(FIELD_LENGTH/2, -FIELD_WIDTH/2, FIELD_HEIGHT),
            Vector3(FIELD_LENGTH/2, FIELD_WIDTH/2, FIELD_HEIGHT),
            Vector3(FIELD_LENGTH/2, FIELD_WIDTH/2, 0),
        ]
        
        # Ceiling vertices
        self.ceiling_vertices = [
            Vector3(-FIELD_LENGTH/2, -FIELD_WIDTH/2, FIELD_HEIGHT),
            Vector3(FIELD_LENGTH/2, -FIELD_WIDTH/2, FIELD_HEIGHT),
            Vector3(FIELD_LENGTH/2, FIELD_WIDTH/2, FIELD_HEIGHT),
            Vector3(-FIELD_LENGTH/2, FIELD_WIDTH/2, FIELD_HEIGHT),
        ]
        
        # Boost pad positions (large and small)
        self.boost_pad_vertices = []
        
        # Large boost pads
        large_boost_positions = [
            Vector3(0, 0, 0),  # Center
            Vector3(-FIELD_LENGTH/2 + 1000, -FIELD_WIDTH/2 + 1000, 0),  # Blue corner
            Vector3(FIELD_LENGTH/2 - 1000, -FIELD_WIDTH/2 + 1000, 0),   # Blue corner
            Vector3(-FIELD_LENGTH/2 + 1000, FIELD_WIDTH/2 - 1000, 0),   # Orange corner
            Vector3(FIELD_LENGTH/2 - 1000, FIELD_WIDTH/2 - 1000, 0),    # Orange corner
        ]
        
        for pos in large_boost_positions:
            self.boost_pad_vertices.append({
                'pos': pos,
                'size': 'large',
                'radius': 165
            })
        
        # Small boost pads (along the sides)
        small_boost_positions = []
        for x in range(-int(FIELD_LENGTH/2) + 500, int(FIELD_LENGTH/2), 1000):
            small_boost_positions.extend([
                Vector3(x, -FIELD_WIDTH/2 + 500, 0),
                Vector3(x, FIELD_WIDTH/2 - 500, 0)
            ])
        
        for pos in small_boost_positions:
            self.boost_pad_vertices.append({
                'pos': pos,
                'size': 'small',
                'radius': 55
            })
    
    def advanced_3d_projection(self, pos: Vector3) -> Tuple[int, int, float]:
        """Advanced 3D to 2D projection with depth information"""
        # Translate relative to camera
        x_cam = pos.x - self.camera_pos.x
        y_cam = pos.y - self.camera_pos.y
        z_cam = pos.z - self.camera_pos.z
        
        # Apply camera rotations
        # Yaw rotation (around Z-axis)
        cos_yaw = math.cos(self.camera_yaw)
        sin_yaw = math.sin(self.camera_yaw)
        x_rot = x_cam * cos_yaw - y_cam * sin_yaw
        y_rot = x_cam * sin_yaw + y_cam * cos_yaw
        z_rot = z_cam
        
        # Pitch rotation (around X-axis)
        cos_pitch = math.cos(self.camera_pitch)
        sin_pitch = math.sin(self.camera_pitch)
        x_final = x_rot
        y_final = y_rot * cos_pitch - z_rot * sin_pitch
        z_final = y_rot * sin_pitch + z_rot * cos_pitch
        
        # Perspective projection
        if z_final < self.near_plane:
            z_final = self.near_plane
        
        # Calculate screen coordinates
        screen_x = int(self.game_view_width // 2 + (x_final / z_final) * self.perspective_scale * self.game_view_width)
        screen_y = int(self.height // 2 - (y_final / z_final) * self.perspective_scale * self.height)
        
        # Depth for z-buffering
        depth = z_final
        
        return screen_x, screen_y, depth
    
    def project_3d_to_2d(self, pos: Vector3) -> Tuple[int, int]:
        """Simple 3D to 2D projection (backward compatibility)"""
        x, y, _ = self.advanced_3d_projection(pos)
        return x, y
    
    def udp_listener(self):
        """Listen for UDP packets from RocketSim"""
        while self.running:
            try:
                data, addr = self.sock.recvfrom(BUFFER_SIZE)
                self.parse_udp_packet(data)
            except socket.timeout:
                continue
            except Exception as e:
                print(f"UDP Error: {e}")
                time.sleep(0.1)
    
    def parse_udp_packet(self, data: bytes):
        """Parse UDP packet data from RocketSim"""
        try:
            # Simple packet format: [ball_pos(12)][ball_vel(12)][ball_ang_vel(12)][num_cars(4)][cars...][num_boost(4)][boost_pads...]
            offset = 0
            
            # Ball position (3 floats)
            ball_x = struct.unpack('<f', data[offset:offset+4])[0]
            ball_y = struct.unpack('<f', data[offset+4:offset+8])[0]
            ball_z = struct.unpack('<f', data[offset+8:offset+12])[0]
            offset += 12
            
            # Ball velocity (3 floats)
            ball_vx = struct.unpack('<f', data[offset:offset+4])[0]
            ball_vy = struct.unpack('<f', data[offset+4:offset+8])[0]
            ball_vz = struct.unpack('<f', data[offset+8:offset+12])[0]
            offset += 12
            
            # Ball angular velocity (3 floats)
            ball_avx = struct.unpack('<f', data[offset:offset+4])[0]
            ball_avy = struct.unpack('<f', data[offset+4:offset+8])[0]
            ball_avz = struct.unpack('<f', data[offset+8:offset+12])[0]
            offset += 12
            
            # Number of cars
            num_cars = struct.unpack('<I', data[offset:offset+4])[0]
            offset += 4
            
            cars = []
            for i in range(num_cars):
                # Car data: [pos(12)][rot(12)][vel(12)][ang_vel(12)][boost(4)][flags(4)]
                car_x = struct.unpack('<f', data[offset:offset+4])[0]
                car_y = struct.unpack('<f', data[offset+4:offset+8])[0]
                car_z = struct.unpack('<f', data[offset+8:offset+12])[0]
                offset += 12
                
                car_pitch = struct.unpack('<f', data[offset:offset+4])[0]
                car_yaw = struct.unpack('<f', data[offset+4:offset+8])[0]
                car_roll = struct.unpack('<f', data[offset+8:offset+12])[0]
                offset += 12
                
                car_vx = struct.unpack('<f', data[offset:offset+4])[0]
                car_vy = struct.unpack('<f', data[offset+4:offset+8])[0]
                car_vz = struct.unpack('<f', data[offset+8:offset+12])[0]
                offset += 12
                
                car_avx = struct.unpack('<f', data[offset:offset+4])[0]
                car_avy = struct.unpack('<f', data[offset+4:offset+8])[0]
                car_avz = struct.unpack('<f', data[offset+8:offset+12])[0]
                offset += 12
                
                car_boost = struct.unpack('<f', data[offset:offset+4])[0]
                offset += 4
                
                car_flags = struct.unpack('<I', data[offset:offset+4])[0]
                offset += 4
                
                car = CarState(
                    position=Vector3(car_x, car_y, car_z),
                    rotation=Rotator(car_pitch, car_yaw, car_roll),
                    velocity=Vector3(car_vx, car_vy, car_vz),
                    angular_velocity=Vector3(car_avx, car_avy, car_avz),
                    boost=car_boost,
                    on_ground=bool(car_flags & 1),
                    has_jumped=bool(car_flags & 2),
                    has_double_jumped=bool(car_flags & 4),
                    team=i % 2  # Simple team assignment
                )
                cars.append(car)
            
            # Number of boost pads
            num_boost = struct.unpack('<I', data[offset:offset+4])[0]
            offset += 4
            
            boost_pads = []
            for i in range(num_boost):
                # Boost pad: [pos(12)][active(1)][large(1)]
                pad_x = struct.unpack('<f', data[offset:offset+4])[0]
                pad_y = struct.unpack('<f', data[offset+4:offset+8])[0]
                pad_z = struct.unpack('<f', data[offset+8:offset+12])[0]
                offset += 12
                
                pad_active = bool(data[offset])
                offset += 1
                
                pad_large = bool(data[offset])
                offset += 1
                
                boost_pad = BoostPad(
                    position=Vector3(pad_x, pad_y, pad_z),
                    is_active=pad_active,
                    is_large=pad_large
                )
                boost_pads.append(boost_pad)
            
            # Create game state
            self.game_state = GameState(
                ball=BallState(
                    position=Vector3(ball_x, ball_y, ball_z),
                    velocity=Vector3(ball_vx, ball_vy, ball_vz),
                    angular_velocity=Vector3(ball_avx, ball_avy, ball_avz)
                ),
                cars=cars,
                boost_pads=boost_pads,
                game_mode=GameMode.SOCCER,
                time=time.time(),
                score_blue=0,
                score_orange=0
            )
            
            # Update training data based on game state
            self.update_training_data()
            
        except Exception as e:
            print(f"Packet parsing error: {e}")
    
    def update_training_data(self):
        """Update training data based on current game state"""
        if not self.game_state:
            return
        
        # Simulate training progress
        self.episode += 1
        self.reward = len(self.game_state.cars) * 10 + self.game_state.ball.position.z * 0.01
        self.skill_level = min(1.0, self.episode * 0.001)
        
        # Update mechanics based on ball height and car actions
        ball_height = self.game_state.ball.position.z
        if ball_height > 500:
            self.mechanics["aerial"] = min(1.0, self.mechanics["aerial"] + 0.01)
        
        # Update bot thoughts
        self.bot_thoughts = [
            f"Ball at ({self.game_state.ball.position.x:.0f}, {self.game_state.ball.position.y:.0f}, {self.game_state.ball.position.z:.0f})",
            f"Ball speed: {math.sqrt(self.game_state.ball.velocity.x**2 + self.game_state.ball.velocity.y**2 + self.game_state.ball.velocity.z**2):.0f}",
            f"Cars on field: {len(self.game_state.cars)}",
            f"Active boost pads: {sum(1 for pad in self.game_state.boost_pads if pad.is_active)}"
        ]
        
        # Update bot actions
        self.bot_actions = [
            "🎯 Analyzing ball trajectory",
            "🚀 Calculating optimal approach",
            "🔄 Planning aerial maneuver",
            "📐 Adjusting car orientation",
            "⚡ Executing action",
            "🎮 Learning from result"
        ]
        
        # Update console messages
        self.console_messages = [
            f"[{time.strftime('%H:%M:%S')}] Episode {self.episode} - Ball height: {ball_height:.0f}",
            f"[{time.strftime('%H:%M:%S')}] Bot analyzing {len(self.game_state.cars)} cars",
            f"[{time.strftime('%H:%M:%S')}] Calculating optimal strategy...",
            f"[{time.strftime('%H:%M:%S')}] Executing JSTN-level maneuver",
            f"[{time.strftime('%H:%M:%S')}] Learning rate: {self.skill_level:.3f}"
        ]
    
    def project_3d_to_2d(self, pos: Vector3) -> Tuple[int, int]:
        """Project 3D coordinates to 2D screen coordinates"""
        # Translate relative to camera
        x_cam = pos.x - self.camera_pos.x
        y_cam = pos.y - self.camera_pos.y
        z_cam = pos.z - self.camera_pos.z
        
        # Rotate around X-axis (pitch)
        y_rot_x = y_cam * math.cos(self.camera_pitch) - z_cam * math.sin(self.camera_pitch)
        z_rot_x = y_cam * math.sin(self.camera_pitch) + z_cam * math.cos(self.camera_pitch)
        
        # Rotate around Z-axis (yaw)
        x_rot_z = x_cam * math.cos(self.camera_yaw) - y_rot_x * math.sin(self.camera_yaw)
        y_rot_z = x_cam * math.sin(self.camera_yaw) + y_rot_x * math.cos(self.camera_yaw)
        
        # Perspective projection
        if y_rot_z < 100:
            y_rot_z = 100
        
        scale = 0.15
        screen_x = int(self.left_panel_width // 2 + x_rot_z / y_rot_z * scale * self.left_panel_width)
        screen_y = int(self.height // 2 - z_rot_x / y_rot_z * scale * self.height)
        
        return screen_x, screen_y
    
    def draw_main_3d_view(self):
        """Draw the main 3D Rocket League view"""
        # Sky background
        pygame.draw.rect(self.screen, SKY_BLUE, (0, 0, self.game_view_width, self.height))
        
        if not self.game_state:
            # Draw waiting message
            text = self.font_large.render("Waiting for UDP data...", True, WHITE)
            text_rect = text.get_rect(center=(self.game_view_width//2, self.height//2))
            self.screen.blit(text, text_rect)
            return
        
        # Draw 3D environment in proper order (back to front)
        self.draw_ceiling()
        self.draw_walls()
        self.draw_goals()
        self.draw_field()
        self.draw_field_lines()
        self.draw_boost_pads()
        self.draw_cars()
        self.draw_ball()
        
        # UI overlay
        self.draw_3d_ui()
    
    def draw_ceiling(self):
        """Draw the ceiling of the arena"""
        ceiling_points = []
        for vertex in self.ceiling_vertices:
            x, y, depth = self.advanced_3d_projection(vertex)
            if 0 <= x < self.game_view_width and 0 <= y < self.height:
                ceiling_points.append((x, y))
        
        if len(ceiling_points) >= 3:
            pygame.draw.polygon(self.screen, (200, 200, 200), ceiling_points)
    
    def draw_walls(self):
        """Draw the walls of the arena"""
        # Draw side walls
        wall_sections = [
            # Left wall
            [self.wall_vertices[0], self.wall_vertices[1], self.wall_vertices[2], self.wall_vertices[3]],
            # Right wall  
            [self.wall_vertices[4], self.wall_vertices[5], self.wall_vertices[6], self.wall_vertices[7]],
            # Back wall
            [self.wall_vertices[8], self.wall_vertices[9], self.wall_vertices[10], self.wall_vertices[11]],
            # Front wall
            [self.wall_vertices[12], self.wall_vertices[13], self.wall_vertices[14], self.wall_vertices[15]]
        ]
        
        for wall in wall_sections:
            wall_points = []
            for vertex in wall:
                x, y, depth = self.advanced_3d_projection(vertex)
                if 0 <= x < self.game_view_width and 0 <= y < self.height:
                    wall_points.append((x, y))
            
            if len(wall_points) >= 3:
                pygame.draw.polygon(self.screen, WALL_COLOR, wall_points)
                pygame.draw.polygon(self.screen, WHITE, wall_points, 2)
    
    def draw_goals(self):
        """Draw the goals with 3D depth"""
        # Blue goal (left)
        blue_goal_faces = [
            # Front face
            [self.goal_vertices[0], self.goal_vertices[1], self.goal_vertices[2], self.goal_vertices[3]],
            # Back face
            [self.goal_vertices[4], self.goal_vertices[5], self.goal_vertices[6], self.goal_vertices[7]],
            # Top face
            [self.goal_vertices[0], self.goal_vertices[4], self.goal_vertices[7], self.goal_vertices[3]],
            # Bottom face
            [self.goal_vertices[1], self.goal_vertices[5], self.goal_vertices[6], self.goal_vertices[2]],
            # Left side
            [self.goal_vertices[0], self.goal_vertices[1], self.goal_vertices[5], self.goal_vertices[4]],
            # Right side
            [self.goal_vertices[2], self.goal_vertices[3], self.goal_vertices[7], self.goal_vertices[6]]
        ]
        
        for face in blue_goal_faces:
            face_points = []
            for vertex in face:
                x, y, depth = self.advanced_3d_projection(vertex)
                if 0 <= x < self.game_view_width and 0 <= y < self.height:
                    face_points.append((x, y))
            
            if len(face_points) >= 3:
                pygame.draw.polygon(self.screen, GOAL_BLUE, face_points)
                pygame.draw.polygon(self.screen, WHITE, face_points, 2)
        
        # Orange goal (right)
        orange_goal_faces = [
            # Front face
            [self.goal_vertices[8], self.goal_vertices[9], self.goal_vertices[10], self.goal_vertices[11]],
            # Back face
            [self.goal_vertices[12], self.goal_vertices[13], self.goal_vertices[14], self.goal_vertices[15]],
            # Top face
            [self.goal_vertices[8], self.goal_vertices[12], self.goal_vertices[15], self.goal_vertices[11]],
            # Bottom face
            [self.goal_vertices[9], self.goal_vertices[13], self.goal_vertices[14], self.goal_vertices[10]],
            # Left side
            [self.goal_vertices[8], self.goal_vertices[9], self.goal_vertices[13], self.goal_vertices[12]],
            # Right side
            [self.goal_vertices[10], self.goal_vertices[11], self.goal_vertices[15], self.goal_vertices[14]]
        ]
        
        for face in orange_goal_faces:
            face_points = []
            for vertex in face:
                x, y, depth = self.advanced_3d_projection(vertex)
                if 0 <= x < self.game_view_width and 0 <= y < self.height:
                    face_points.append((x, y))
            
            if len(face_points) >= 3:
                pygame.draw.polygon(self.screen, GOAL_ORANGE, face_points)
                pygame.draw.polygon(self.screen, WHITE, face_points, 2)
    
    def draw_field(self):
        """Draw the main field surface"""
        field_points = []
        for vertex in self.field_vertices:
            x, y, depth = self.advanced_3d_projection(vertex)
            if 0 <= x < self.game_view_width and 0 <= y < self.height:
                field_points.append((x, y))
        
        if len(field_points) >= 3:
            pygame.draw.polygon(self.screen, FIELD_GREEN, field_points)
    
    def draw_field_lines(self):
        """Draw the field lines and markings"""
        # Center line
        center_start = Vector3(0, -FIELD_WIDTH/2, 0)
        center_end = Vector3(0, FIELD_WIDTH/2, 0)
        start_x, start_y, _ = self.advanced_3d_projection(center_start)
        end_x, end_y, _ = self.advanced_3d_projection(center_end)
        
        if (0 <= start_x < self.game_view_width and 0 <= start_y < self.height) or \
           (0 <= end_x < self.game_view_width and 0 <= end_y < self.height):
            pygame.draw.line(self.screen, FIELD_LINES, (start_x, start_y), (end_x, end_y), 3)
        
        # Center circle
        circle_center = Vector3(0, 0, 0)
        center_x, center_y, _ = self.advanced_3d_projection(circle_center)
        if 0 <= center_x < self.game_view_width and 0 <= center_y < self.height:
            # Draw center circle (simplified as a small circle)
            pygame.draw.circle(self.screen, FIELD_LINES, (center_x, center_y), 20, 2)
    
    def draw_boost_pads(self):
        """Draw boost pads with 3D effect"""
        for pad_data in self.boost_pad_vertices:
            pos = pad_data['pos']
            size = pad_data['size']
            radius = pad_data['radius']
            
            x, y, depth = self.advanced_3d_projection(pos)
            if 0 <= x < self.game_view_width and 0 <= y < self.height:
                # Scale radius based on depth
                scaled_radius = max(5, int(radius / (depth / 1000)))
                
                if size == 'large':
                    # Large boost pad with 3D effect
                    pygame.draw.circle(self.screen, BOOST_YELLOW, (x, y), scaled_radius)
                    pygame.draw.circle(self.screen, WHITE, (x, y), scaled_radius, 2)
                    # Inner circle
                    pygame.draw.circle(self.screen, (255, 255, 0), (x, y), scaled_radius//2)
                else:
                    # Small boost pad
                    pygame.draw.circle(self.screen, BOOST_GRAY, (x, y), scaled_radius)
                    pygame.draw.circle(self.screen, WHITE, (x, y), scaled_radius, 1)
    
    def draw_cars(self):
        """Draw cars with detailed 3D representation"""
        if not self.game_state:
            return
        
        for i, car in enumerate(self.game_state.cars):
            x, y, depth = self.advanced_3d_projection(car.position)
            if 0 <= x < self.game_view_width and 0 <= y < self.height:
                # Scale car size based on depth
                car_length = max(10, int(CAR_LENGTH / (depth / 1000)))
                car_width = max(6, int(CAR_WIDTH / (depth / 1000)))
                
                # Car color based on team
                car_color = BLUE_TEAM if car.team == 0 else ORANGE_TEAM
                
                # Draw car body
                pygame.draw.rect(self.screen, car_color, 
                               (x - car_length//2, y - car_width//2, car_length, car_width))
                pygame.draw.rect(self.screen, WHITE, 
                               (x - car_length//2, y - car_width//2, car_length, car_width), 2)
                
                # Draw car wheels (simplified)
                wheel_size = max(2, car_width//3)
                pygame.draw.circle(self.screen, (50, 50, 50), 
                                 (x - car_length//3, y - car_width//2), wheel_size)
                pygame.draw.circle(self.screen, (50, 50, 50), 
                                 (x + car_length//3, y - car_width//2), wheel_size)
                pygame.draw.circle(self.screen, (50, 50, 50), 
                                 (x - car_length//3, y + car_width//2), wheel_size)
                pygame.draw.circle(self.screen, (50, 50, 50), 
                                 (x + car_length//3, y + car_width//2), wheel_size)
                
                # Car label
                label = "JSTN" if i == 0 else f"Bot{i+1}"
                text = self.font_tiny.render(label, True, WHITE)
                self.screen.blit(text, (x - 15, y - 25))
    
    def draw_ball(self):
        """Draw the ball with 3D effect and shadow"""
        if not self.game_state:
            return
        
        ball_pos = self.game_state.ball.position
        x, y, depth = self.advanced_3d_projection(ball_pos)
        
        if 0 <= x < self.game_view_width and 0 <= y < self.height:
            # Scale ball size based on depth
            ball_radius = max(8, int(BALL_RADIUS / (depth / 1000)))
            
            # Draw ball shadow on ground
            shadow_pos = Vector3(ball_pos.x, ball_pos.y, 0)
            shadow_x, shadow_y, _ = self.advanced_3d_projection(shadow_pos)
            if 0 <= shadow_x < self.game_view_width and 0 <= shadow_y < self.height:
                pygame.draw.circle(self.screen, SHADOW_GRAY, (shadow_x, shadow_y), ball_radius//2)
            
            # Draw ball with gradient effect
            pygame.draw.circle(self.screen, BALL_WHITE, (x, y), ball_radius)
            pygame.draw.circle(self.screen, BALL_ORANGE, (x, y), ball_radius, 2)
            
            # Ball pattern (simplified)
            pygame.draw.circle(self.screen, (200, 200, 200), (x, y), ball_radius//2, 1)
    
    def draw_3d_ui(self):
        """Draw UI overlay for the 3D view"""
        # Title
        title = self.font_large.render("🎮 Full 3D Rocket League View", True, WHITE)
        self.screen.blit(title, (10, 10))
        
        # FPS counter
        fps_text = self.font_small.render(f"FPS: {self.fps}", True, WHITE)
        self.screen.blit(fps_text, (10, 50))
        
        # Camera info
        camera_text = self.font_tiny.render(f"Camera: {self.camera_focus} | Speed: {self.game_speed:.1f}x", True, WHITE)
        self.screen.blit(camera_text, (10, 80))
    
    def draw_3d_field(self):
        """Draw the 3D Rocket League field"""
        # Field corners
        corners = [
            Vector3(-FIELD_LENGTH/2, -FIELD_WIDTH/2, 0),
            Vector3(FIELD_LENGTH/2, -FIELD_WIDTH/2, 0),
            Vector3(FIELD_LENGTH/2, FIELD_WIDTH/2, 0),
            Vector3(-FIELD_LENGTH/2, FIELD_WIDTH/2, 0)
        ]
        
        screen_corners = []
        for corner in corners:
            x, y = self.project_3d_to_2d(corner)
            screen_corners.append((x, y))
        
        pygame.draw.polygon(self.screen, DARK_GREEN, screen_corners)
        
        # Field lines
        # Center line
        start = self.project_3d_to_2d(Vector3(0, -FIELD_WIDTH/2, 0))
        end = self.project_3d_to_2d(Vector3(0, FIELD_WIDTH/2, 0))
        pygame.draw.line(self.screen, WHITE, start, end, 2)
        
        # Goals
        # Blue goal
        goal_corners = [
            Vector3(-FIELD_LENGTH/2, -GOAL_WIDTH/2, 0),
            Vector3(-FIELD_LENGTH/2, GOAL_WIDTH/2, 0),
            Vector3(-FIELD_LENGTH/2, GOAL_WIDTH/2, GOAL_HEIGHT),
            Vector3(-FIELD_LENGTH/2, -GOAL_WIDTH/2, GOAL_HEIGHT)
        ]
        screen_goal = []
        for corner in goal_corners:
            x, y = self.project_3d_to_2d(corner)
            screen_goal.append((x, y))
        pygame.draw.polygon(self.screen, BLUE, screen_goal)
        
        # Orange goal
        goal_corners = [
            Vector3(FIELD_LENGTH/2, -GOAL_WIDTH/2, 0),
            Vector3(FIELD_LENGTH/2, GOAL_WIDTH/2, 0),
            Vector3(FIELD_LENGTH/2, GOAL_WIDTH/2, GOAL_HEIGHT),
            Vector3(FIELD_LENGTH/2, -GOAL_WIDTH/2, GOAL_HEIGHT)
        ]
        screen_goal = []
        for corner in goal_corners:
            x, y = self.project_3d_to_2d(corner)
            screen_goal.append((x, y))
        pygame.draw.polygon(self.screen, ORANGE, screen_goal)
    
    def draw_ball(self):
        """Draw the ball in 3D"""
        if not self.game_state:
            return
        
        x, y = self.project_3d_to_2d(self.game_state.ball.position)
        if 0 <= x < self.left_panel_width and 0 <= y < self.height:
            # Ball shadow
            shadow_pos = Vector3(self.game_state.ball.position.x, self.game_state.ball.position.y, 0)
            shadow_x, shadow_y = self.project_3d_to_2d(shadow_pos)
            pygame.draw.circle(self.screen, (50, 50, 50), (shadow_x, shadow_y), 8)
            
            # Ball
            pygame.draw.circle(self.screen, ORANGE, (x, y), 10)
            pygame.draw.circle(self.screen, WHITE, (x, y), 10, 2)
    
    def draw_car(self, car: CarState, index: int):
        """Draw a car in 3D"""
        x, y = self.project_3d_to_2d(car.position)
        if 0 <= x < self.left_panel_width and 0 <= y < self.height:
            color = BLUE if car.team == 0 else ORANGE
            pygame.draw.rect(self.screen, color, (x - 12, y - 8, 24, 16))
            pygame.draw.rect(self.screen, WHITE, (x - 12, y - 8, 24, 16), 2)
            
            # Car label
            label = f"JSTN" if index == 0 else f"Bot{index+1}"
            text = self.font_tiny.render(label, True, WHITE)
            self.screen.blit(text, (x - 10, y - 20))
    
    def draw_boost_pad(self, pad: BoostPad):
        """Draw a boost pad in 3D"""
        if not pad.is_active:
            return
        
        x, y = self.project_3d_to_2d(pad.position)
        if 0 <= x < self.left_panel_width and 0 <= y < self.height:
            size = 8 if pad.is_large else 4
            color = YELLOW if pad.is_large else GRAY
            pygame.draw.circle(self.screen, color, (x, y), size)
            pygame.draw.circle(self.screen, WHITE, (x, y), size, 1)
    
    def draw_middle_panel_thoughts(self):
        """Draw the bot's thoughts and console (middle panel)"""
        x_start = self.left_panel_width
        
        # Panel background
        pygame.draw.rect(self.screen, (30, 30, 30), (x_start, 0, self.middle_panel_width, self.height))
        
        # Panel title
        title = self.font_large.render("🧠 Bot's Thoughts & Actions", True, CYAN)
        self.screen.blit(title, (x_start + 10, 10))
        
        # Training info
        y_pos = 40
        info_texts = [
            f"Mode: {self.training_mode.upper()}",
            f"Episode: {self.episode}",
            f"Reward: {self.reward:.2f}",
            f"JSTN Level: {self.skill_level:.3f}",
            f"UDP: {UDP_IP}:{UDP_PORT}"
        ]
        
        for text in info_texts:
            rendered = self.font_medium.render(text, True, WHITE)
            self.screen.blit(rendered, (x_start + 10, y_pos))
            y_pos += 25
        
        # Bot's current thoughts
        y_pos += 20
        thoughts_title = self.font_medium.render("🤔 What I'm Thinking:", True, YELLOW)
        self.screen.blit(thoughts_title, (x_start + 10, y_pos))
        y_pos += 25
        
        for thought in self.bot_thoughts:
            rendered = self.font_small.render(thought, True, WHITE)
            self.screen.blit(rendered, (x_start + 10, y_pos))
            y_pos += 18
        
        # Bot's actions
        y_pos += 20
        actions_title = self.font_medium.render("⚡ What I'm Doing:", True, GREEN)
        self.screen.blit(actions_title, (x_start + 10, y_pos))
        y_pos += 25
        
        for action in self.bot_actions:
            rendered = self.font_small.render(action, True, WHITE)
            self.screen.blit(rendered, (x_start + 10, y_pos))
            y_pos += 18
        
        # Console output
        y_pos += 20
        console_title = self.font_medium.render("📟 Training Console:", True, PURPLE)
        self.screen.blit(console_title, (x_start + 10, y_pos))
        y_pos += 25
        
        for msg in self.console_messages:
            rendered = self.font_tiny.render(msg, True, CYAN)
            self.screen.blit(rendered, (x_start + 10, y_pos))
            y_pos += 15
    
    def draw_right_panel_tactical(self):
        """Draw the 2D tactical map (right panel)"""
        x_start = self.left_panel_width + self.middle_panel_width
        
        # Panel background
        pygame.draw.rect(self.screen, (20, 40, 20), (x_start, 0, self.right_panel_width, self.height))
        
        # Panel title
        title = self.font_large.render("🗺️ Tactical Map", True, GREEN)
        self.screen.blit(title, (x_start + 10, 10))
        
        # Field dimensions
        field_x = x_start + 20
        field_y = 50
        field_width = self.right_panel_width - 40
        field_height = int(field_width * 0.6)
        
        # Draw field
        pygame.draw.rect(self.screen, DARK_GREEN, (field_x, field_y, field_width, field_height))
        pygame.draw.rect(self.screen, WHITE, (field_x, field_y, field_width, field_height), 2)
        
        # Center line
        pygame.draw.line(self.screen, WHITE, 
                        (field_x + field_width//2, field_y), 
                        (field_x + field_width//2, field_y + field_height), 2)
        
        # Goals
        goal_width = 20
        goal_height = 60
        # Blue goal (left)
        pygame.draw.rect(self.screen, BLUE, 
                        (field_x - goal_width//2, field_y + field_height//2 - goal_height//2, 
                         goal_width, goal_height))
        # Orange goal (right)
        pygame.draw.rect(self.screen, ORANGE, 
                        (field_x + field_width - goal_width//2, field_y + field_height//2 - goal_height//2, 
                         goal_width, goal_height))
        
        if self.game_state:
            # Convert 3D positions to 2D tactical map
            def to_tactical_pos(pos: Vector3):
                tactical_x = field_x + field_width//2 + (pos.x / FIELD_LENGTH) * (field_width//2)
                tactical_y = field_y + field_height//2 + (pos.y / FIELD_WIDTH) * (field_height//2)
                return int(tactical_x), int(tactical_y)
            
            # Draw ball
            ball_x, ball_y = to_tactical_pos(self.game_state.ball.position)
            pygame.draw.circle(self.screen, ORANGE, (ball_x, ball_y), 8)
            pygame.draw.circle(self.screen, WHITE, (ball_x, ball_y), 8, 2)
            
            # Draw cars
            for i, car in enumerate(self.game_state.cars):
                car_x, car_y = to_tactical_pos(car.position)
                color = BLUE if car.team == 0 else ORANGE
                pygame.draw.rect(self.screen, color, (car_x - 8, car_y - 6, 16, 12))
                pygame.draw.rect(self.screen, WHITE, (car_x - 8, car_y - 6, 16, 12), 2)
                
                # Car labels
                label = "JSTN" if i == 0 else f"Bot{i+1}"
                text = self.font_tiny.render(label, True, WHITE)
                self.screen.blit(text, (car_x - 10, car_y - 20))
            
            # Draw boost pads
            for pad in self.game_state.boost_pads:
                if pad.is_active:
                    pad_x, pad_y = to_tactical_pos(pad.position)
                    size = 4 if pad.is_large else 2
                    color = YELLOW if pad.is_large else GRAY
                    pygame.draw.circle(self.screen, color, (pad_x, pad_y), size)
        
        # Training progress
        y_pos = field_y + field_height + 20
        progress_title = self.font_medium.render("📊 Learning Progress:", True, YELLOW)
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
            pygame.draw.rect(self.screen, GREEN, (bar_x, bar_y, progress_width, bar_height))
            pygame.draw.rect(self.screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 1)
            
            # Label
            label = self.font_tiny.render(mechanic.replace('_', ' ').title(), True, WHITE)
            self.screen.blit(label, (bar_x + bar_width + 10, bar_y + 2))
            
            y_pos += 20
    
    def draw_menu(self):
        """Draw the control menu"""
        if not self.menu_open:
            return
        
        # Menu background
        menu_width = 400
        menu_height = 300
        menu_x = (self.width - menu_width) // 2
        menu_y = (self.height - menu_height) // 2
        
        pygame.draw.rect(self.screen, (40, 40, 40), (menu_x, menu_y, menu_width, menu_height))
        pygame.draw.rect(self.screen, WHITE, (menu_x, menu_y, menu_width, menu_height), 2)
        
        # Menu title
        title = self.font_large.render("🎮 Opti UDP Visualizer Controls", True, YELLOW)
        title_rect = title.get_rect(center=(menu_x + menu_width//2, menu_y + 30))
        self.screen.blit(title, title_rect)
        
        # Controls
        controls = [
            "ESC - Toggle menu",
            "1-8 - Car camera focus",
            "9 - Director camera",
            "0 - Free camera",
            "WASD - Move camera",
            "Space/Ctrl - Up/Down",
            "P - Pause/Play",
            "+/- - Speed up/down",
            "= - Reset speed",
            "R - Reset ball to goal"
        ]
        
        y_pos = menu_y + 60
        for control in controls:
            text = self.font_small.render(control, True, WHITE)
            self.screen.blit(text, (menu_x + 20, y_pos))
            y_pos += 20
    
    def handle_input(self, event):
        """Handle keyboard and mouse input"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.menu_open = not self.menu_open
            
            elif not self.menu_open:  # Only process other keys when menu is closed
                if event.key == pygame.K_p:
                    self.paused = not self.paused
                elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    self.game_speed = min(3.0, self.game_speed + 0.5)
                elif event.key == pygame.K_MINUS:
                    self.game_speed = max(0.5, self.game_speed - 0.5)
                elif event.key == pygame.K_0:
                    self.game_speed = 1.0
                elif event.key == pygame.K_r:
                    # Reset ball to goal (would need to send UDP command)
                    pass
                elif pygame.K_1 <= event.key <= pygame.K_8:
                    self.camera_focus = event.key - pygame.K_1
                elif event.key == pygame.K_9:
                    self.camera_focus = 8  # Director camera
                elif event.key == pygame.K_0:
                    self.camera_focus = 9  # Free camera
    
    def run(self):
        """Main game loop"""
        clock = pygame.time.Clock()
        
        while self.running:
            current_time = time.time()
            
            # Calculate FPS
            self.frame_count += 1
            if current_time - self.last_update >= 1.0:
                self.fps = self.frame_count
                self.frame_count = 0
                self.last_update = current_time
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.handle_input(event)
            
            # Clear screen
            self.screen.fill(BLACK)
            
            # Draw all panels
            self.draw_left_panel_3d()
            self.draw_middle_panel_thoughts()
            self.draw_right_panel_tactical()
            
            # Draw menu if open
            self.draw_menu()
            
            # Update display
            pygame.display.flip()
            clock.tick(60)  # 60 FPS
        
        # Cleanup
        self.sock.close()
        pygame.quit()
        print("🤖 Opti UDP Visualizer closed")

def main():
    """Main function to run the visualizer"""
    print("🚀 Starting Opti UDP Visualizer...")
    print("   📡 This visualizer listens for UDP packets from RocketSim")
    print("   🎮 Press ESC to toggle controls menu")
    print("   ⚡ Make sure your training system is sending UDP data!")
    
    visualizer = OptiUDPVisualizer()
    visualizer.run()

if __name__ == "__main__":
    main()
