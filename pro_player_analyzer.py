#!/usr/bin/env python3
"""
Pro Player Video/Stream Analyzer
Analyzes YouTube videos and live streams to extract controller inputs and playstyle patterns
"""

import cv2
import numpy as np
import pytesseract
import re
import json
import time
import threading
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Dict, Tuple, Optional
import requests
from bs4 import BeautifulSoup
import yt_dlp
import subprocess
import os

@dataclass
class ControllerInput:
    """Represents a single controller input"""
    timestamp: float
    button: str  # A, B, X, Y, LB, RB, LT, RT, etc.
    action: str  # press, release, hold
    intensity: float  # 0.0 to 1.0 for analog inputs
    duration: float  # how long the input was held

@dataclass
class GameAction:
    """Represents a game action derived from controller inputs"""
    timestamp: float
    action_type: str  # jump, boost, steer_left, steer_right, etc.
    confidence: float
    context: str  # aerial, ground, kickoff, etc.

@dataclass
class ProPlayerData:
    """Complete data from analyzing a pro player"""
    player_name: str
    video_url: str
    timestamp: datetime
    controller_inputs: List[ControllerInput]
    game_actions: List[GameAction]
    playstyle_patterns: Dict[str, float]
    mechanics_used: List[str]

class ControllerOverlayDetector:
    """Detects and extracts controller overlay information from video frames"""
    
    def __init__(self):
        # Common controller overlay templates
        self.button_templates = {
            'A': cv2.imread('templates/button_a.png', cv2.IMREAD_GRAYSCALE) if os.path.exists('templates/button_a.png') else None,
            'B': cv2.imread('templates/button_b.png', cv2.IMREAD_GRAYSCALE) if os.path.exists('templates/button_b.png') else None,
            'X': cv2.imread('templates/button_x.png', cv2.IMREAD_GRAYSCALE) if os.path.exists('templates/button_x.png') else None,
            'Y': cv2.imread('templates/button_y.png', cv2.IMREAD_GRAYSCALE) if os.path.exists('templates/button_y.png') else None,
            'LB': cv2.imread('templates/button_lb.png', cv2.IMREAD_GRAYSCALE) if os.path.exists('templates/button_lb.png') else None,
            'RB': cv2.imread('templates/button_rb.png', cv2.IMREAD_GRAYSCALE) if os.path.exists('templates/button_rb.png') else None,
        }
        
        # Controller overlay regions (common positions)
        self.overlay_regions = [
            (50, 50, 300, 200),    # Top-left
            (50, 400, 300, 550),   # Bottom-left
            (1650, 50, 1900, 200), # Top-right
            (1650, 400, 1900, 550), # Bottom-right
        ]
        
        # Button color ranges for detection
        self.button_colors = {
            'pressed': [(0, 0, 200), (50, 50, 255)],      # Red when pressed
            'unpressed': [(100, 100, 100), (200, 200, 200)] # Gray when not pressed
        }
    
    def detect_controller_overlay(self, frame: np.ndarray) -> Dict[str, bool]:
        """Detect which buttons are pressed in the controller overlay"""
        button_states = {}
        
        # Convert to HSV for better color detection
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Check each overlay region
        for region in self.overlay_regions:
            x, y, w, h = region
            roi = frame[y:y+h, x:x+w]
            roi_hsv = hsv[y:y+h, x:x+w]
            
            # Look for button indicators
            for button, template in self.button_templates.items():
                if template is not None:
                    # Template matching
                    result = cv2.matchTemplate(roi, template, cv2.TM_CCOEFF_NORMED)
                    _, max_val, _, max_loc = cv2.minMaxLoc(result)
                    
                    if max_val > 0.7:  # Threshold for button detection
                        # Check if button appears pressed (red color)
                        button_roi = roi[max_loc[1]:max_loc[1]+template.shape[0], 
                                       max_loc[0]:max_loc[0]+template.shape[1]]
                        
                        # Check for red color (pressed state)
                        red_mask = cv2.inRange(button_roi, 
                                             np.array(self.button_colors['pressed'][0]), 
                                             np.array(self.button_colors['pressed'][1]))
                        
                        button_states[button] = cv2.countNonZero(red_mask) > 50
        
        return button_states
    
    def detect_analog_sticks(self, frame: np.ndarray) -> Dict[str, Tuple[float, float]]:
        """Detect analog stick positions"""
        stick_positions = {}
        
        # Look for analog stick indicators (usually circles or crosshairs)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect circles (analog stick indicators)
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20,
                                 param1=50, param2=30, minRadius=10, maxRadius=50)
        
        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            
            for i, (x, y, r) in enumerate(circles):
                # Determine if it's left or right stick based on position
                if x < frame.shape[1] // 2:
                    stick_name = 'left_stick'
                else:
                    stick_name = 'right_stick'
                
                # Calculate stick position relative to center
                center_x, center_y = frame.shape[1] // 2, frame.shape[0] // 2
                stick_x = (x - center_x) / 100.0  # Normalize
                stick_y = (y - center_y) / 100.0  # Normalize
                
                stick_positions[stick_name] = (stick_x, stick_y)
        
        return stick_positions

class VideoAnalyzer:
    """Analyzes YouTube videos for controller inputs and gameplay patterns"""
    
    def __init__(self):
        self.controller_detector = ControllerOverlayDetector()
        self.ydl_opts = {
            'format': 'best[height<=720]',  # Lower resolution for faster processing
            'quiet': True,
            'no_warnings': True,
        }
    
    def download_video(self, url: str) -> str:
        """Download video from YouTube URL"""
        print(f"📥 Downloading video: {url}")
        
        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_id = info['id']
            filename = f"temp_video_{video_id}.mp4"
            
            ydl.download([url])
            
            # Find the downloaded file
            for file in os.listdir('.'):
                if file.startswith(f"{info['title']}") and file.endswith('.mp4'):
                    os.rename(file, filename)
                    return filename
        
        return None
    
    def analyze_video(self, video_path: str, player_name: str) -> ProPlayerData:
        """Analyze video for controller inputs and gameplay patterns"""
        print(f"🎬 Analyzing video for {player_name}...")
        
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        controller_inputs = []
        game_actions = []
        frame_number = 0
        
        # Sample every 5th frame for performance
        sample_rate = 5
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            if frame_number % sample_rate == 0:
                timestamp = frame_number / fps
                
                # Detect controller overlay
                button_states = self.controller_detector.detect_controller_overlay(frame)
                stick_positions = self.controller_detector.detect_analog_sticks(frame)
                
                # Convert to controller inputs
                for button, pressed in button_states.items():
                    if pressed:
                        controller_inputs.append(ControllerInput(
                            timestamp=timestamp,
                            button=button,
                            action='press',
                            intensity=1.0,
                            duration=0.0
                        ))
                
                # Convert stick positions to inputs
                for stick, (x, y) in stick_positions.items():
                    if abs(x) > 0.1 or abs(y) > 0.1:  # Only record significant movements
                        controller_inputs.append(ControllerInput(
                            timestamp=timestamp,
                            button=stick,
                            action='move',
                            intensity=max(abs(x), abs(y)),
                            duration=0.0
                        ))
            
            frame_number += 1
        
        cap.release()
        
        # Analyze patterns
        playstyle_patterns = self.analyze_playstyle_patterns(controller_inputs)
        mechanics_used = self.detect_mechanics_used(controller_inputs)
        
        return ProPlayerData(
            player_name=player_name,
            video_url=video_path,
            timestamp=datetime.now(),
            controller_inputs=controller_inputs,
            game_actions=game_actions,
            playstyle_patterns=playstyle_patterns,
            mechanics_used=mechanics_used
        )
    
    def analyze_playstyle_patterns(self, inputs: List[ControllerInput]) -> Dict[str, float]:
        """Analyze playstyle patterns from controller inputs"""
        patterns = {}
        
        # Count button usage
        button_counts = {}
        for inp in inputs:
            button_counts[inp.button] = button_counts.get(inp.button, 0) + 1
        
        total_inputs = len(inputs)
        if total_inputs > 0:
            for button, count in button_counts.items():
                patterns[f"{button}_usage"] = count / total_inputs
        
        # Analyze timing patterns
        jump_inputs = [inp for inp in inputs if inp.button == 'A']
        boost_inputs = [inp for inp in inputs if inp.button == 'B']
        
        if len(jump_inputs) > 1:
            jump_intervals = [jump_inputs[i+1].timestamp - jump_inputs[i].timestamp 
                            for i in range(len(jump_inputs)-1)]
            patterns['jump_frequency'] = 1.0 / np.mean(jump_intervals) if jump_intervals else 0
        
        if len(boost_inputs) > 1:
            boost_intervals = [boost_inputs[i+1].timestamp - boost_inputs[i].timestamp 
                             for i in range(len(boost_inputs)-1)]
            patterns['boost_frequency'] = 1.0 / np.mean(boost_intervals) if boost_intervals else 0
        
        return patterns
    
    def detect_mechanics_used(self, inputs: List[ControllerInput]) -> List[str]:
        """Detect advanced mechanics from controller inputs"""
        mechanics = []
        
        # Detect fast aerial (jump + boost + tilt back quickly)
        jump_times = [inp.timestamp for inp in inputs if inp.button == 'A']
        boost_times = [inp.timestamp for inp in inputs if inp.button == 'B']
        
        for jump_time in jump_times:
            # Look for boost within 0.1 seconds of jump
            nearby_boosts = [bt for bt in boost_times if abs(bt - jump_time) < 0.1]
            if nearby_boosts:
                mechanics.append('fast_aerial')
                break
        
        # Detect wave dash (jump + dodge in quick succession)
        dodge_times = [inp.timestamp for inp in inputs if inp.button in ['X', 'Y']]
        for jump_time in jump_times:
            nearby_dodges = [dt for dt in dodge_times if 0.1 < abs(dt - jump_time) < 0.3]
            if nearby_dodges:
                mechanics.append('wave_dash')
                break
        
        # Detect flip reset (jump + dodge while in air)
        for i, inp in enumerate(inputs):
            if inp.button == 'A' and i < len(inputs) - 1:
                next_input = inputs[i + 1]
                if next_input.button in ['X', 'Y'] and next_input.timestamp - inp.timestamp < 0.5:
                    mechanics.append('flip_reset')
                    break
        
        return list(set(mechanics))  # Remove duplicates

class StreamAnalyzer:
    """Real-time analysis of live streams"""
    
    def __init__(self):
        self.controller_detector = ControllerOverlayDetector()
        self.is_analyzing = False
        self.current_data = None
    
    def start_stream_analysis(self, stream_url: str, player_name: str):
        """Start analyzing a live stream"""
        print(f"🔴 Starting live stream analysis for {player_name}")
        print(f"📺 Stream URL: {stream_url}")
        
        self.is_analyzing = True
        
        # Use yt-dlp to get stream URL
        ydl_opts = {
            'format': 'best[height<=720]',
            'quiet': True,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(stream_url, download=False)
                stream_url = info['url']
            
            # Start video capture from stream
            cap = cv2.VideoCapture(stream_url)
            
            if not cap.isOpened():
                print("❌ Could not open stream")
                return
            
            print("✅ Stream opened successfully")
            
            # Analyze stream in real-time
            self.analyze_stream_realtime(cap, player_name)
            
        except Exception as e:
            print(f"❌ Stream analysis error: {e}")
    
    def analyze_stream_realtime(self, cap: cv2.VideoCapture, player_name: str):
        """Analyze stream in real-time"""
        frame_count = 0
        controller_inputs = []
        
        while self.is_analyzing and cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            # Analyze every 10th frame for performance
            if frame_count % 10 == 0:
                timestamp = time.time()
                
                # Detect controller overlay
                button_states = self.controller_detector.detect_controller_overlay(frame)
                stick_positions = self.controller_detector.detect_analog_sticks(frame)
                
                # Convert to controller inputs
                for button, pressed in button_states.items():
                    if pressed:
                        controller_inputs.append(ControllerInput(
                            timestamp=timestamp,
                            button=button,
                            action='press',
                            intensity=1.0,
                            duration=0.0
                        ))
                
                # Update current data
                self.current_data = {
                    'player_name': player_name,
                    'timestamp': timestamp,
                    'button_states': button_states,
                    'stick_positions': stick_positions,
                    'total_inputs': len(controller_inputs)
                }
                
                # Print current state
                if button_states:
                    print(f"🎮 {player_name} inputs: {button_states}")
            
            frame_count += 1
            time.sleep(0.1)  # Small delay to prevent overwhelming
        
        cap.release()
    
    def stop_analysis(self):
        """Stop stream analysis"""
        self.is_analyzing = False
        print("⏹️ Stream analysis stopped")

class ProPlayerLearningSystem:
    """Main system for learning from pro players"""
    
    def __init__(self):
        self.video_analyzer = VideoAnalyzer()
        self.stream_analyzer = StreamAnalyzer()
        self.learned_patterns = {}
        self.training_data = []
    
    def learn_from_youtube_video(self, url: str, player_name: str) -> ProPlayerData:
        """Learn from a YouTube video"""
        print(f"🎥 Learning from {player_name}'s YouTube video...")
        
        # Download video
        video_path = self.video_analyzer.download_video(url)
        if not video_path:
            print("❌ Failed to download video")
            return None
        
        # Analyze video
        player_data = self.video_analyzer.analyze_video(video_path, player_name)
        
        # Save data
        self.save_player_data(player_data)
        
        # Clean up
        if os.path.exists(video_path):
            os.remove(video_path)
        
        return player_data
    
    def learn_from_live_stream(self, stream_url: str, player_name: str):
        """Learn from a live stream"""
        print(f"🔴 Learning from {player_name}'s live stream...")
        
        # Start stream analysis in separate thread
        stream_thread = threading.Thread(
            target=self.stream_analyzer.start_stream_analysis,
            args=(stream_url, player_name)
        )
        stream_thread.daemon = True
        stream_thread.start()
        
        return stream_thread
    
    def save_player_data(self, player_data: ProPlayerData):
        """Save player data to file"""
        filename = f"pro_data_{player_data.player_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        # Convert to JSON-serializable format
        data_dict = asdict(player_data)
        data_dict['timestamp'] = player_data.timestamp.isoformat()
        
        with open(filename, 'w') as f:
            json.dump(data_dict, f, indent=2)
        
        print(f"💾 Saved player data to {filename}")
    
    def load_player_data(self, filename: str) -> ProPlayerData:
        """Load player data from file"""
        with open(filename, 'r') as f:
            data_dict = json.load(f)
        
        # Convert back to ProPlayerData
        data_dict['timestamp'] = datetime.fromisoformat(data_dict['timestamp'])
        data_dict['controller_inputs'] = [ControllerInput(**inp) for inp in data_dict['controller_inputs']]
        data_dict['game_actions'] = [GameAction(**action) for action in data_dict['game_actions']]
        
        return ProPlayerData(**data_dict)
    
    def generate_training_data(self, player_data: ProPlayerData) -> List[Dict]:
        """Generate training data for our bot from pro player data"""
        training_data = []
        
        for inp in player_data.controller_inputs:
            # Convert controller input to bot action
            bot_action = self.convert_to_bot_action(inp)
            if bot_action:
                training_data.append({
                    'timestamp': inp.timestamp,
                    'action': bot_action,
                    'confidence': 0.9,  # High confidence from pro player
                    'source': f"pro_{player_data.player_name}"
                })
        
        return training_data
    
    def convert_to_bot_action(self, controller_input: ControllerInput) -> Optional[Dict]:
        """Convert controller input to bot action format"""
        action_mapping = {
            'A': 'jump',
            'B': 'boost',
            'X': 'dodge_left',
            'Y': 'dodge_right',
            'LB': 'powerslide',
            'RB': 'air_roll',
            'left_stick': 'steer',
            'right_stick': 'camera'
        }
        
        if controller_input.button in action_mapping:
            return {
                'type': action_mapping[controller_input.button],
                'intensity': controller_input.intensity,
                'duration': controller_input.duration
            }
        
        return None

def main():
    """Main function for testing the pro player learning system"""
    print("🚀 Pro Player Learning System")
    print("=" * 50)
    
    learning_system = ProPlayerLearningSystem()
    
    # Example YouTube URLs (you can replace with actual jstn/GarettG videos)
    jstn_videos = [
        "https://www.youtube.com/watch?v=example1",  # Replace with real URLs
        "https://www.youtube.com/watch?v=example2",
    ]
    
    garettg_videos = [
        "https://www.youtube.com/watch?v=example3",  # Replace with real URLs
        "https://www.youtube.com/watch?v=example4",
    ]
    
    # Learn from jstn videos
    print("\n🎯 Learning from jstn videos...")
    for video_url in jstn_videos:
        try:
            player_data = learning_system.learn_from_youtube_video(video_url, "jstn")
            if player_data:
                print(f"✅ Learned from jstn video: {len(player_data.controller_inputs)} inputs")
                print(f"🎮 Mechanics detected: {player_data.mechanics_used}")
                print(f"📊 Playstyle patterns: {player_data.playstyle_patterns}")
        except Exception as e:
            print(f"❌ Error learning from jstn video: {e}")
    
    # Learn from GarettG videos
    print("\n🎯 Learning from GarettG videos...")
    for video_url in garettg_videos:
        try:
            player_data = learning_system.learn_from_youtube_video(video_url, "GarettG")
            if player_data:
                print(f"✅ Learned from GarettG video: {len(player_data.controller_inputs)} inputs")
                print(f"🎮 Mechanics detected: {player_data.mechanics_used}")
                print(f"📊 Playstyle patterns: {player_data.playstyle_patterns}")
        except Exception as e:
            print(f"❌ Error learning from GarettG video: {e}")
    
    print("\n🎉 Pro player learning complete!")
    print("💡 Use this data to train your bot to play like the pros!")

if __name__ == "__main__":
    main()

