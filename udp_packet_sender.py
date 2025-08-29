#!/usr/bin/env python3
"""
UDP Packet Sender - Sends game state data to Opti UDP Visualizer
Compatible with RocketSim format and RLGym GameState
"""

import socket
import struct
import time
import threading
import math
from typing import List, Optional, Dict, Any
from dataclasses import dataclass

# UDP Configuration
UDP_IP = "127.0.0.1"
UDP_PORT = 37020

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
class CarData:
    position: Vector3
    rotation: Rotator
    velocity: Vector3
    angular_velocity: Vector3
    boost: float
    on_ground: bool
    has_jumped: bool
    has_double_jumped: bool
    team: int

@dataclass
class BallData:
    position: Vector3
    velocity: Vector3
    angular_velocity: Vector3

@dataclass
class BoostPadData:
    position: Vector3
    is_active: bool
    is_large: bool

@dataclass
class GameStateData:
    ball: BallData
    cars: List[CarData]
    boost_pads: List[BoostPadData]
    time: float
    score_blue: int
    score_orange: int

class UDPPacketSender:
    def __init__(self, ip: str = UDP_IP, port: int = UDP_PORT):
        """Initialize UDP packet sender"""
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.running = True
        self.send_interval = 1.0 / 60.0  # 60 FPS
        self.last_send = 0
        
        print(f"📡 UDP Packet Sender initialized")
        print(f"   🎯 Target: {self.ip}:{self.port}")
        print(f"   ⚡ Send rate: {1.0/self.send_interval:.1f} FPS")
    
    def create_game_state_from_rlgym(self, rlgym_state) -> GameStateData:
        """Convert RLGym GameState to our format"""
        try:
            # Ball data
            ball = BallData(
                position=Vector3(
                    rlgym_state.ball.position.x,
                    rlgym_state.ball.position.y,
                    rlgym_state.ball.position.z
                ),
                velocity=Vector3(
                    rlgym_state.ball.linear_velocity.x,
                    rlgym_state.ball.linear_velocity.y,
                    rlgym_state.ball.linear_velocity.z
                ),
                angular_velocity=Vector3(
                    rlgym_state.ball.angular_velocity.x,
                    rlgym_state.ball.angular_velocity.y,
                    rlgym_state.ball.angular_velocity.z
                )
            )
            
            # Cars data
            cars = []
            for i, car in enumerate(rlgym_state.cars):
                car_data = CarData(
                    position=Vector3(
                        car.physics.location.x,
                        car.physics.location.y,
                        car.physics.location.z
                    ),
                    rotation=Rotator(
                        car.physics.rotation.pitch,
                        car.physics.rotation.yaw,
                        car.physics.rotation.roll
                    ),
                    velocity=Vector3(
                        car.physics.linear_velocity.x,
                        car.physics.linear_velocity.y,
                        car.physics.linear_velocity.z
                    ),
                    angular_velocity=Vector3(
                        car.physics.angular_velocity.x,
                        car.physics.angular_velocity.y,
                        car.physics.angular_velocity.z
                    ),
                    boost=car.boost_amount,
                    on_ground=car.on_ground,
                    has_jumped=car.has_jumped,
                    has_double_jumped=car.has_double_jumped,
                    team=car.team_num
                )
                cars.append(car_data)
            
            # Boost pads data
            boost_pads = []
            for pad in rlgym_state.boost_pads:
                boost_pad = BoostPadData(
                    position=Vector3(
                        pad.position.x,
                        pad.position.y,
                        pad.position.z
                    ),
                    is_active=pad.is_active,
                    is_large=pad.is_large
                )
                boost_pads.append(boost_pad)
            
            return GameStateData(
                ball=ball,
                cars=cars,
                boost_pads=boost_pads,
                time=time.time(),
                score_blue=rlgym_state.blue_score,
                score_orange=rlgym_state.orange_score
            )
            
        except Exception as e:
            print(f"Error converting RLGym state: {e}")
            return self.create_dummy_game_state()
    
    def create_dummy_game_state(self) -> GameStateData:
        """Create a dummy game state for testing"""
        # Dummy ball
        ball = BallData(
            position=Vector3(0, 0, 100),
            velocity=Vector3(50, 30, 20),
            angular_velocity=Vector3(0, 0, 0)
        )
        
        # Dummy cars
        cars = [
            CarData(
                position=Vector3(-500, 0, 0),
                rotation=Rotator(0, 0, 0),
                velocity=Vector3(0, 0, 0),
                angular_velocity=Vector3(0, 0, 0),
                boost=100.0,
                on_ground=True,
                has_jumped=False,
                has_double_jumped=False,
                team=0
            ),
            CarData(
                position=Vector3(500, 0, 0),
                rotation=Rotator(0, 0, 0),
                velocity=Vector3(0, 0, 0),
                angular_velocity=Vector3(0, 0, 0),
                boost=100.0,
                on_ground=True,
                has_jumped=False,
                has_double_jumped=False,
                team=1
            )
        ]
        
        # Dummy boost pads
        boost_pads = [
            BoostPadData(
                position=Vector3(0, 0, 0),
                is_active=True,
                is_large=True
            ),
            BoostPadData(
                position=Vector3(-2000, -1500, 0),
                is_active=True,
                is_large=True
            ),
            BoostPadData(
                position=Vector3(2000, -1500, 0),
                is_active=True,
                is_large=True
            ),
            BoostPadData(
                position=Vector3(-2000, 1500, 0),
                is_active=True,
                is_large=True
            ),
            BoostPadData(
                position=Vector3(2000, 1500, 0),
                is_active=True,
                is_large=True
            )
        ]
        
        return GameStateData(
            ball=ball,
            cars=cars,
            boost_pads=boost_pads,
            time=time.time(),
            score_blue=0,
            score_orange=0
        )
    
    def serialize_game_state(self, game_state: GameStateData) -> bytes:
        """Serialize game state to UDP packet format"""
        data = bytearray()
        
        # Ball position (3 floats)
        data.extend(struct.pack('<f', game_state.ball.position.x))
        data.extend(struct.pack('<f', game_state.ball.position.y))
        data.extend(struct.pack('<f', game_state.ball.position.z))
        
        # Ball velocity (3 floats)
        data.extend(struct.pack('<f', game_state.ball.velocity.x))
        data.extend(struct.pack('<f', game_state.ball.velocity.y))
        data.extend(struct.pack('<f', game_state.ball.velocity.z))
        
        # Ball angular velocity (3 floats)
        data.extend(struct.pack('<f', game_state.ball.angular_velocity.x))
        data.extend(struct.pack('<f', game_state.ball.angular_velocity.y))
        data.extend(struct.pack('<f', game_state.ball.angular_velocity.z))
        
        # Number of cars (1 uint32)
        data.extend(struct.pack('<I', len(game_state.cars)))
        
        # Cars data
        for car in game_state.cars:
            # Position (3 floats)
            data.extend(struct.pack('<f', car.position.x))
            data.extend(struct.pack('<f', car.position.y))
            data.extend(struct.pack('<f', car.position.z))
            
            # Rotation (3 floats)
            data.extend(struct.pack('<f', car.rotation.pitch))
            data.extend(struct.pack('<f', car.rotation.yaw))
            data.extend(struct.pack('<f', car.rotation.roll))
            
            # Velocity (3 floats)
            data.extend(struct.pack('<f', car.velocity.x))
            data.extend(struct.pack('<f', car.velocity.y))
            data.extend(struct.pack('<f', car.velocity.z))
            
            # Angular velocity (3 floats)
            data.extend(struct.pack('<f', car.angular_velocity.x))
            data.extend(struct.pack('<f', car.angular_velocity.y))
            data.extend(struct.pack('<f', car.angular_velocity.z))
            
            # Boost (1 float)
            data.extend(struct.pack('<f', car.boost))
            
            # Flags (1 uint32)
            flags = 0
            if car.on_ground:
                flags |= 1
            if car.has_jumped:
                flags |= 2
            if car.has_double_jumped:
                flags |= 4
            data.extend(struct.pack('<I', flags))
        
        # Number of boost pads (1 uint32)
        data.extend(struct.pack('<I', len(game_state.boost_pads)))
        
        # Boost pads data
        for pad in game_state.boost_pads:
            # Position (3 floats)
            data.extend(struct.pack('<f', pad.position.x))
            data.extend(struct.pack('<f', pad.position.y))
            data.extend(struct.pack('<f', pad.position.z))
            
            # Active flag (1 byte)
            data.extend(struct.pack('B', 1 if pad.is_active else 0))
            
            # Large flag (1 byte)
            data.extend(struct.pack('B', 1 if pad.is_large else 0))
        
        return bytes(data)
    
    def send_game_state(self, game_state: GameStateData):
        """Send game state via UDP"""
        try:
            packet = self.serialize_game_state(game_state)
            self.sock.sendto(packet, (self.ip, self.port))
        except Exception as e:
            print(f"Error sending UDP packet: {e}")
    
    def send_rlgym_state(self, rlgym_state):
        """Send RLGym GameState via UDP"""
        game_state = self.create_game_state_from_rlgym(rlgym_state)
        self.send_game_state(game_state)
    
    def send_dummy_data(self):
        """Send dummy data for testing"""
        game_state = self.create_dummy_game_state()
        self.send_game_state(game_state)
    
    def start_dummy_stream(self, duration: float = 60.0):
        """Start streaming dummy data for testing"""
        print(f"🎮 Starting dummy data stream for {duration} seconds...")
        
        start_time = time.time()
        while time.time() - start_time < duration and self.running:
            current_time = time.time()
            
            if current_time - self.last_send >= self.send_interval:
                # Animate dummy data
                game_state = self.create_dummy_game_state()
                
                # Animate ball
                t = current_time - start_time
                game_state.ball.position.x = 1000 * math.sin(t * 0.5)
                game_state.ball.position.y = 500 * math.cos(t * 0.3)
                game_state.ball.position.z = 200 + 100 * math.sin(t * 0.8)
                
                # Animate cars
                for i, car in enumerate(game_state.cars):
                    car.position.x += 10 * (1 if i == 0 else -1)
                    car.position.y += 5 * math.sin(t + i)
                    if car.position.x > 2000:
                        car.position.x = -2000
                    if car.position.x < -2000:
                        car.position.x = 2000
                
                self.send_game_state(game_state)
                self.last_send = current_time
            
            time.sleep(0.001)  # Small delay to prevent CPU overload
        
        print("✅ Dummy data stream completed")
    
    def close(self):
        """Close the UDP sender"""
        self.running = False
        self.sock.close()
        print("📡 UDP Packet Sender closed")

# Global sender instance
_sender_instance: Optional[UDPPacketSender] = None

def get_sender() -> UDPPacketSender:
    """Get or create global sender instance"""
    global _sender_instance
    if _sender_instance is None:
        _sender_instance = UDPPacketSender()
    return _sender_instance

def send_rlgym_state(rlgym_state):
    """Convenience function to send RLGym state"""
    sender = get_sender()
    sender.send_rlgym_state(rlgym_state)

def send_dummy_data():
    """Convenience function to send dummy data"""
    sender = get_sender()
    sender.send_dummy_data()

def start_dummy_stream(duration: float = 60.0):
    """Convenience function to start dummy stream"""
    sender = get_sender()
    sender.start_dummy_stream(duration)

def close_sender():
    """Convenience function to close sender"""
    global _sender_instance
    if _sender_instance:
        _sender_instance.close()
        _sender_instance = None

if __name__ == "__main__":
    # Test the UDP sender
    print("🧪 Testing UDP Packet Sender...")
    
    sender = UDPPacketSender()
    
    # Send some dummy data
    for i in range(10):
        sender.send_dummy_data()
        time.sleep(0.1)
        print(f"Sent packet {i+1}/10")
    
    # Start dummy stream
    sender.start_dummy_stream(10.0)
    
    sender.close()
    print("✅ UDP Packet Sender test completed")
