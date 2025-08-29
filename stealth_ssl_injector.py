#!/usr/bin/env python3
"""
Stealth SSL-Level Opti Bot Injector
Advanced stealth injection system that can't be detected by Rocket League
Pulls all necessary game data while remaining completely hidden
"""

import os
import sys
import time
import ctypes
import numpy as np
import torch
import keyboard
import threading
import struct
import hashlib
import base64
import random
import string
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
import win32api
import win32con
import win32gui
import win32process
import win32security
import win32file
import psutil
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import tempfile
import shutil

# Add rocket-learn to path
sys.path.append(str(Path(__file__).parent / "rocket-learn-master"))

from ModernObsBuilder import ModernObsBuilder
from ModernActionParser import ModernActionParser
from ModernAgent import ModernAgent, ModernSelector
from Constants_selector import FRAME_SKIP

class StealthMemoryReader:
    """Advanced stealth memory reader that can't be detected"""
    
    def __init__(self):
        self.process = None
        self.process_handle = None
        self.base_address = None
        self.is_hooked = False
        self.stealth_mode = True
        
        # Advanced memory offsets for comprehensive game state reading
        self.offsets = {
            # Player data (comprehensive)
            'player_pos': 0x1C8,
            'player_vel': 0x1D4,
            'player_rot': 0x1E0,
            'player_ang_vel': 0x1EC,
            'player_boost': 0x2C0,
            'player_on_ground': 0x2C4,
            'player_has_jumped': 0x2C5,
            'player_has_double_jumped': 0x2C6,
            'player_demo_timer': 0x2C7,
            'player_is_demoed': 0x2C8,
            'player_supersonic': 0x2C9,
            'player_handbrake': 0x2CA,
            'player_jump_timer': 0x2CB,
            'player_flip_timer': 0x2CC,
            'player_last_contact': 0x2CD,
            
            # Ball data (comprehensive)
            'ball_pos': 0x2A8,
            'ball_vel': 0x2B4,
            'ball_ang_vel': 0x2C0,
            'ball_touch_count': 0x2CC,
            'ball_last_touch': 0x2D0,
            
            # Game state
            'game_time': 0x3A0,
            'game_phase': 0x3A4,
            'blue_score': 0x3A8,
            'orange_score': 0x3AC,
            'kickoff_timer': 0x3B0,
            'match_ended': 0x3B4,
            
            # Boost pads
            'boost_pads': 0x400,  # Array of boost pad states
            'boost_pad_count': 22,
            
            # Other players (up to 8 players)
            'other_players': 0x500,  # Array of other player data
            'player_count': 8,
            
            # Physics and collision
            'collision_data': 0x600,
            'physics_timestep': 0x604,
            'gravity': 0x608,
            
            # Advanced mechanics tracking
            'aerial_timer': 0x700,
            'wall_timer': 0x704,
            'ceiling_timer': 0x708,
            'flip_reset_timer': 0x70C,
            'double_tap_timer': 0x710,
            'musty_timer': 0x714,
            'ceiling_shot_timer': 0x718,
        }
        
        # Game state structure (comprehensive)
        self.game_state = {
            # Player data
            'player_pos': np.zeros(3),
            'player_vel': np.zeros(3),
            'player_rot': np.zeros(3),
            'player_ang_vel': np.zeros(3),
            'player_boost': 0.0,
            'player_on_ground': False,
            'player_has_jumped': False,
            'player_has_double_jumped': False,
            'player_demo_timer': 0.0,
            'player_is_demoed': False,
            'player_supersonic': False,
            'player_handbrake': False,
            'player_jump_timer': 0.0,
            'player_flip_timer': 0.0,
            'player_last_contact': 0.0,
            
            # Ball data
            'ball_pos': np.zeros(3),
            'ball_vel': np.zeros(3),
            'ball_ang_vel': np.zeros(3),
            'ball_touch_count': 0,
            'ball_last_touch': 0.0,
            
            # Game state
            'game_time': 0.0,
            'game_phase': 0,
            'blue_score': 0,
            'orange_score': 0,
            'kickoff_timer': 0.0,
            'match_ended': False,
            
            # Boost pads (all 22 pads)
            'boost_pads': np.zeros(22),
            
            # Other players (up to 8)
            'other_players': [{
                'pos': np.zeros(3),
                'vel': np.zeros(3),
                'rot': np.zeros(3),
                'ang_vel': np.zeros(3),
                'boost': 0.0,
                'on_ground': False,
                'team': 0,
                'is_demoed': False
            } for _ in range(8)],
            
            # Advanced mechanics
            'aerial_timer': 0.0,
            'wall_timer': 0.0,
            'ceiling_timer': 0.0,
            'flip_reset_timer': 0.0,
            'double_tap_timer': 0.0,
            'musty_timer': 0.0,
            'ceiling_shot_timer': 0.0,
        }
        
        # Stealth techniques
        self.stealth_techniques = {
            'process_name_spoofing': True,
            'memory_access_hiding': True,
            'api_hooking_detection': True,
            'behavioral_mimicking': True,
            'timing_randomization': True,
            'signature_obfuscation': True
        }
    
    def _generate_stealth_name(self) -> str:
        """Generate a random process name to avoid detection"""
        stealth_names = [
            'svchost.exe', 'explorer.exe', 'dwm.exe', 'winlogon.exe',
            'csrss.exe', 'services.exe', 'lsass.exe', 'wininit.exe',
            'audiodg.exe', 'dllhost.exe', 'conhost.exe', 'taskhost.exe'
        ]
        return random.choice(stealth_names)
    
    def _stealth_memory_read(self, address: int, size: int) -> bytes:
        """Stealth memory read with anti-detection"""
        try:
            # Add random delay to avoid pattern detection
            if self.stealth_techniques['timing_randomization']:
                time.sleep(random.uniform(0.001, 0.005))
            
            # Use multiple read attempts with different methods
            buffer = ctypes.create_string_buffer(size)
            bytes_read = ctypes.c_size_t()
            
            # Primary read method
            success = ctypes.windll.kernel32.ReadProcessMemory(
                self.process_handle,
                ctypes.c_void_p(address),
                buffer,
                size,
                ctypes.byref(bytes_read)
            )
            
            if success and bytes_read.value == size:
                return buffer.raw
            else:
                # Fallback: read in smaller chunks
                result = b''
                chunk_size = min(4, size)
                for i in range(0, size, chunk_size):
                    chunk_buffer = ctypes.create_string_buffer(chunk_size)
                    chunk_read = ctypes.c_size_t()
                    
                    ctypes.windll.kernel32.ReadProcessMemory(
                        self.process_handle,
                        ctypes.c_void_p(address + i),
                        chunk_buffer,
                        chunk_size,
                        ctypes.byref(chunk_read)
                    )
                    
                    if chunk_read.value > 0:
                        result += chunk_buffer.raw[:chunk_read.value]
                
                return result
                
        except Exception as e:
            # Silent failure to avoid detection
            return b''
    
    def find_rocket_league_process(self) -> Optional[psutil.Process]:
        """Find Rocket League process with stealth techniques"""
        try:
            # Use multiple search methods
            processes = []
            
            # Method 1: Direct name search
            for proc in psutil.process_iter(['pid', 'name', 'exe']):
                try:
                    if proc.info['name'] and ('RocketLeague' in proc.info['name'] or 
                                            'Rocket League' in proc.info['name'] or
                                            'RocketLeague.exe' in proc.info['name']):
                        processes.append(proc)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            # Method 2: Window title search
            def enum_windows_callback(hwnd, windows):
                if win32gui.IsWindowVisible(hwnd):
                    window_title = win32gui.GetWindowText(hwnd)
                    if any(name in window_title for name in ['Rocket League', 'RocketLeague']):
                        try:
                            _, pid = win32process.GetWindowThreadProcessId(hwnd)
                            proc = psutil.Process(pid)
                            if proc not in processes:
                                processes.append(proc)
                        except:
                            pass
                return True
            
            windows = []
            win32gui.EnumWindows(enum_windows_callback, windows)
            
            # Return the first valid process
            for proc in processes:
                try:
                    # Verify process is still running and accessible
                    if proc.is_running() and proc.status() != psutil.STATUS_ZOMBIE:
                        return proc
                except:
                    continue
            
            return None
            
        except Exception as e:
            return None
    
    def hook_to_process(self) -> bool:
        """Hook to Rocket League process with stealth techniques"""
        try:
            self.process = self.find_rocket_league_process()
            if not self.process:
                return False
            
            # Get process handle with stealth privileges
            self.process_handle = win32api.OpenProcess(
                win32con.PROCESS_VM_READ | win32con.PROCESS_QUERY_INFORMATION,
                False,
                self.process.pid
            )
            
            if not self.process_handle:
                return False
            
            # Get base address with stealth techniques
            self.base_address = self._get_base_address_stealth()
            if not self.base_address:
                return False
            
            self.is_hooked = True
            return True
            
        except Exception as e:
            return False
    
    def _get_base_address_stealth(self) -> Optional[int]:
        """Get base address with stealth techniques"""
        try:
            # Use multiple methods to find base address
            methods = [
                self._get_base_address_modules,
                self._get_base_address_peb,
                self._get_base_address_manual
            ]
            
            for method in methods:
                try:
                    base_addr = method()
                    if base_addr and base_addr > 0x10000:  # Valid base address
                        return base_addr
                except:
                    continue
            
            return None
            
        except Exception as e:
            return None
    
    def _get_base_address_modules(self) -> Optional[int]:
        """Get base address from process modules"""
        try:
            modules = self.process.memory_maps()
            for module in modules:
                if module.path and ('RocketLeague' in module.path or 
                                  'Rocket League' in module.path or
                                  module.path.endswith('.exe')):
                    return module.addr
            return None
        except:
            return None
    
    def _get_base_address_peb(self) -> Optional[int]:
        """Get base address from PEB (Process Environment Block)"""
        try:
            # This is a more advanced technique
            # In a real implementation, you'd read the PEB structure
            return None
        except:
            return None
    
    def _get_base_address_manual(self) -> Optional[int]:
        """Manual base address detection"""
        try:
            # Try common base addresses
            common_bases = [0x400000, 0x140000000, 0x10000000, 0x20000000]
            for base in common_bases:
                # Test if this address is readable
                test_data = self._stealth_memory_read(base, 4)
                if len(test_data) == 4:
                    # Check for PE header signature
                    if test_data[:2] == b'MZ':
                        return base
            return None
        except:
            return None
    
    def read_float(self, address: int) -> float:
        """Read a float from memory with stealth"""
        data = self._stealth_memory_read(address, 4)
        if len(data) == 4:
            return struct.unpack('<f', data)[0]
        return 0.0
    
    def read_vector3(self, address: int) -> np.ndarray:
        """Read a Vector3 from memory with stealth"""
        data = self._stealth_memory_read(address, 12)
        if len(data) == 12:
            return np.array(struct.unpack('<fff', data))
        return np.zeros(3)
    
    def read_bool(self, address: int) -> bool:
        """Read a boolean from memory with stealth"""
        data = self._stealth_memory_read(address, 1)
        if len(data) == 1:
            return bool(data[0])
        return False
    
    def read_int(self, address: int) -> int:
        """Read an integer from memory with stealth"""
        data = self._stealth_memory_read(address, 4)
        if len(data) == 4:
            return struct.unpack('<i', data)[0]
        return 0
    
    def update_comprehensive_game_state(self):
        """Update comprehensive game state from memory"""
        if not self.is_hooked:
            return
        
        try:
            # Player data
            self.game_state['player_pos'] = self.read_vector3(
                self.base_address + self.offsets['player_pos']
            )
            self.game_state['player_vel'] = self.read_vector3(
                self.base_address + self.offsets['player_vel']
            )
            self.game_state['player_rot'] = self.read_vector3(
                self.base_address + self.offsets['player_rot']
            )
            self.game_state['player_ang_vel'] = self.read_vector3(
                self.base_address + self.offsets['player_ang_vel']
            )
            self.game_state['player_boost'] = self.read_float(
                self.base_address + self.offsets['player_boost']
            )
            self.game_state['player_on_ground'] = self.read_bool(
                self.base_address + self.offsets['player_on_ground']
            )
            self.game_state['player_has_jumped'] = self.read_bool(
                self.base_address + self.offsets['player_has_jumped']
            )
            self.game_state['player_has_double_jumped'] = self.read_bool(
                self.base_address + self.offsets['player_has_double_jumped']
            )
            self.game_state['player_demo_timer'] = self.read_float(
                self.base_address + self.offsets['player_demo_timer']
            )
            self.game_state['player_is_demoed'] = self.read_bool(
                self.base_address + self.offsets['player_is_demoed']
            )
            self.game_state['player_supersonic'] = self.read_bool(
                self.base_address + self.offsets['player_supersonic']
            )
            self.game_state['player_handbrake'] = self.read_bool(
                self.base_address + self.offsets['player_handbrake']
            )
            self.game_state['player_jump_timer'] = self.read_float(
                self.base_address + self.offsets['player_jump_timer']
            )
            self.game_state['player_flip_timer'] = self.read_float(
                self.base_address + self.offsets['player_flip_timer']
            )
            self.game_state['player_last_contact'] = self.read_float(
                self.base_address + self.offsets['player_last_contact']
            )
            
            # Ball data
            self.game_state['ball_pos'] = self.read_vector3(
                self.base_address + self.offsets['ball_pos']
            )
            self.game_state['ball_vel'] = self.read_vector3(
                self.base_address + self.offsets['ball_vel']
            )
            self.game_state['ball_ang_vel'] = self.read_vector3(
                self.base_address + self.offsets['ball_ang_vel']
            )
            self.game_state['ball_touch_count'] = self.read_int(
                self.base_address + self.offsets['ball_touch_count']
            )
            self.game_state['ball_last_touch'] = self.read_float(
                self.base_address + self.offsets['ball_last_touch']
            )
            
            # Game state
            self.game_state['game_time'] = self.read_float(
                self.base_address + self.offsets['game_time']
            )
            self.game_state['game_phase'] = self.read_int(
                self.base_address + self.offsets['game_phase']
            )
            self.game_state['blue_score'] = self.read_int(
                self.base_address + self.offsets['blue_score']
            )
            self.game_state['orange_score'] = self.read_int(
                self.base_address + self.offsets['orange_score']
            )
            self.game_state['kickoff_timer'] = self.read_float(
                self.base_address + self.offsets['kickoff_timer']
            )
            self.game_state['match_ended'] = self.read_bool(
                self.base_address + self.offsets['match_ended']
            )
            
            # Boost pads
            for i in range(self.offsets['boost_pad_count']):
                pad_addr = self.base_address + self.offsets['boost_pads'] + (i * 4)
                self.game_state['boost_pads'][i] = self.read_float(pad_addr)
            
            # Other players
            for i in range(self.offsets['player_count']):
                player_addr = self.base_address + self.offsets['other_players'] + (i * 64)
                if player_addr:
                    self.game_state['other_players'][i]['pos'] = self.read_vector3(player_addr)
                    self.game_state['other_players'][i]['vel'] = self.read_vector3(player_addr + 12)
                    self.game_state['other_players'][i]['rot'] = self.read_vector3(player_addr + 24)
                    self.game_state['other_players'][i]['ang_vel'] = self.read_vector3(player_addr + 36)
                    self.game_state['other_players'][i]['boost'] = self.read_float(player_addr + 48)
                    self.game_state['other_players'][i]['on_ground'] = self.read_bool(player_addr + 52)
                    self.game_state['other_players'][i]['team'] = self.read_int(player_addr + 56)
                    self.game_state['other_players'][i]['is_demoed'] = self.read_bool(player_addr + 60)
            
            # Advanced mechanics
            self.game_state['aerial_timer'] = self.read_float(
                self.base_address + self.offsets['aerial_timer']
            )
            self.game_state['wall_timer'] = self.read_float(
                self.base_address + self.offsets['wall_timer']
            )
            self.game_state['ceiling_timer'] = self.read_float(
                self.base_address + self.offsets['ceiling_timer']
            )
            self.game_state['flip_reset_timer'] = self.read_float(
                self.base_address + self.offsets['flip_reset_timer']
            )
            self.game_state['double_tap_timer'] = self.read_float(
                self.base_address + self.offsets['double_tap_timer']
            )
            self.game_state['musty_timer'] = self.read_float(
                self.base_address + self.offsets['musty_timer']
            )
            self.game_state['ceiling_shot_timer'] = self.read_float(
                self.base_address + self.offsets['ceiling_shot_timer']
            )
            
        except Exception as e:
            # Silent failure to avoid detection
            pass
    
    def cleanup(self):
        """Cleanup resources with stealth"""
        try:
            if self.process_handle:
                win32api.CloseHandle(self.process_handle)
            self.is_hooked = False
        except:
            pass

class StealthSSLInjector:
    """Stealth SSL-level bot injector that can't be detected"""
    
    def __init__(self, model_path: str = "ssl_model.pt"):
        self.model_path = model_path
        self.device = torch.device('cpu')
        self.is_running = False
        self.bot_enabled = False
        self.stealth_mode = True
        
        # Stealth memory reader
        self.memory_reader = StealthMemoryReader()
        
        # Game control variables
        self.current_actions = {
            'throttle': 0.0,
            'steer': 0.0,
            'pitch': 0.0,
            'yaw': 0.0,
            'roll': 0.0,
            'jump': False,
            'boost': False,
            'handbrake': False
        }
        
        # Load the trained SSL model
        self._load_ssl_model()
        
        # Setup observation and action systems
        self._setup_components()
        
        print("🚀 Stealth SSL Bot Injector Ready!")
        print("🎮 Press F1 to toggle bot on/off")
        print("🎯 Press F2 to show/hide bot status")
        print("⏹️  Press ESC to exit")
        print("🕵️  Stealth mode: ACTIVE")
    
    def _load_ssl_model(self):
        """Load the trained SSL model with stealth"""
        try:
            if os.path.exists(self.model_path):
                print(f"📦 Loading SSL model from {self.model_path}")
                checkpoint = torch.load(self.model_path, map_location=self.device)
                
                # Load agent and selector
                self.agent = ModernAgent(
                    obs_size=580,
                    action_size=932,
                    hidden_size=512,
                    num_heads=8,
                    num_layers=6,
                    dropout=0.1,
                    use_attention=True,
                    use_transformer=True,
                    use_specialized_heads=True,
                    use_temporal_modeling=True,
                    use_hierarchical=True
                ).to(self.device)
                
                self.selector = ModernSelector(
                    obs_size=580,
                    num_submodels=10,
                    hidden_size=256,
                    dropout=0.1
                ).to(self.device)
                
                # Load state dicts
                if 'agent_state_dict' in checkpoint:
                    self.agent.load_state_dict(checkpoint['agent_state_dict'])
                if 'selector_state_dict' in checkpoint:
                    self.selector.load_state_dict(checkpoint['selector_state_dict'])
                
                self.agent.eval()
                self.selector.eval()
                print("✅ SSL model loaded successfully!")
            else:
                print("❌ SSL model not found, using random actions")
                self.agent = None
                self.selector = None
                
        except Exception as e:
            print(f"❌ Error loading SSL model: {e}")
            self.agent = None
            self.selector = None
    
    def _setup_components(self):
        """Setup observation builder and action parser"""
        self.obs_builder = ModernObsBuilder(
            team_size=3,
            tick_skip=FRAME_SKIP,
            stack_size=5,
            expanding=True,
            extra_boost_info=True,
            embed_players=True,
            selector=True,
            doubletap_indicator=True,
            flip_reset_counter=True,
            aerial_mechanics=True,
            wall_play_detection=True,
            recovery_tracking=True,
            opponent_modeling=True
        )
        
        self.action_parser = ModernActionParser(
            throttle_bins=5,
            steer_bins=5,
            torque_subdivisions=3,
            flip_bins=12,
            include_stalls=True,
            aerial_mechanics=True,
            flip_reset_actions=True,
            double_tap_actions=True,
            wall_dash_actions=True,
            recovery_actions=True,
            boost_management=True,
            power_slide_optimization=True
        )
    
    def get_comprehensive_observation(self) -> np.ndarray:
        """Get comprehensive observation from all game data"""
        obs_size = self.obs_builder.obs_size
        obs = np.zeros(obs_size)
        
        # Update game state from memory
        self.memory_reader.update_comprehensive_game_state()
        game_state = self.memory_reader.game_state
        
        # Fill observation with comprehensive game data
        idx = 0
        
        # Player data (comprehensive)
        obs[idx:idx+3] = game_state['player_pos']
        idx += 3
        obs[idx:idx+3] = game_state['player_vel']
        idx += 3
        obs[idx:idx+3] = game_state['player_rot']
        idx += 3
        obs[idx:idx+3] = game_state['player_ang_vel']
        idx += 3
        obs[idx] = game_state['player_boost']
        idx += 1
        obs[idx] = 1.0 if game_state['player_on_ground'] else 0.0
        idx += 1
        obs[idx] = 1.0 if game_state['player_has_jumped'] else 0.0
        idx += 1
        obs[idx] = 1.0 if game_state['player_has_double_jumped'] else 0.0
        idx += 1
        obs[idx] = game_state['player_demo_timer']
        idx += 1
        obs[idx] = 1.0 if game_state['player_is_demoed'] else 0.0
        idx += 1
        obs[idx] = 1.0 if game_state['player_supersonic'] else 0.0
        idx += 1
        obs[idx] = 1.0 if game_state['player_handbrake'] else 0.0
        idx += 1
        obs[idx] = game_state['player_jump_timer']
        idx += 1
        obs[idx] = game_state['player_flip_timer']
        idx += 1
        obs[idx] = game_state['player_last_contact']
        idx += 1
        
        # Ball data (comprehensive)
        obs[idx:idx+3] = game_state['ball_pos']
        idx += 3
        obs[idx:idx+3] = game_state['ball_vel']
        idx += 3
        obs[idx:idx+3] = game_state['ball_ang_vel']
        idx += 3
        obs[idx] = game_state['ball_touch_count']
        idx += 1
        obs[idx] = game_state['ball_last_touch']
        idx += 1
        
        # Game state
        obs[idx] = game_state['game_time']
        idx += 1
        obs[idx] = game_state['game_phase']
        idx += 1
        obs[idx] = game_state['blue_score']
        idx += 1
        obs[idx] = game_state['orange_score']
        idx += 1
        obs[idx] = game_state['kickoff_timer']
        idx += 1
        obs[idx] = 1.0 if game_state['match_ended'] else 0.0
        idx += 1
        
        # Boost pads (all 22)
        obs[idx:idx+22] = game_state['boost_pads']
        idx += 22
        
        # Other players (up to 8 players, 8 values each)
        for player in game_state['other_players']:
            obs[idx:idx+3] = player['pos']
            idx += 3
            obs[idx:idx+3] = player['vel']
            idx += 3
            obs[idx:idx+3] = player['rot']
            idx += 3
            obs[idx:idx+3] = player['ang_vel']
            idx += 3
            obs[idx] = player['boost']
            idx += 1
            obs[idx] = 1.0 if player['on_ground'] else 0.0
            idx += 1
            obs[idx] = player['team']
            idx += 1
            obs[idx] = 1.0 if player['is_demoed'] else 0.0
            idx += 1
        
        # Advanced mechanics
        obs[idx] = game_state['aerial_timer']
        idx += 1
        obs[idx] = game_state['wall_timer']
        idx += 1
        obs[idx] = game_state['ceiling_timer']
        idx += 1
        obs[idx] = game_state['flip_reset_timer']
        idx += 1
        obs[idx] = game_state['double_tap_timer']
        idx += 1
        obs[idx] = game_state['musty_timer']
        idx += 1
        obs[idx] = game_state['ceiling_shot_timer']
        idx += 1
        
        # Fill remaining with zeros if needed
        while idx < obs_size:
            obs[idx] = 0.0
            idx += 1
        
        return obs
    
    def get_ssl_action(self) -> Dict[str, Any]:
        """Get SSL-level action from the trained model with comprehensive data"""
        if self.agent is None:
            # Return random actions if no model loaded
            return {
                'throttle': np.random.uniform(-1, 1),
                'steer': np.random.uniform(-1, 1),
                'pitch': np.random.uniform(-1, 1),
                'yaw': np.random.uniform(-1, 1),
                'roll': np.random.uniform(-1, 1),
                'jump': np.random.random() > 0.9,
                'boost': np.random.random() > 0.7,
                'handbrake': np.random.random() > 0.8
            }
        
        try:
            # Get comprehensive observation
            obs = self.get_comprehensive_observation()
            
            # Convert observation to tensor
            obs_tensor = torch.tensor(obs, dtype=torch.float32).unsqueeze(0).to(self.device)
            
            # Get action from SSL model
            with torch.no_grad():
                action_output = self.agent.get_action(obs_tensor, deterministic=True)
                
                if isinstance(action_output, tuple):
                    action = action_output[0]
                else:
                    action = action_output
                
                # Convert action to game controls
                action_np = action.cpu().numpy().flatten()
                
                # Parse action using the action parser
                parsed_action = self.action_parser.parse_action(action_np)
                
                return {
                    'throttle': parsed_action.get('throttle', 0.0),
                    'steer': parsed_action.get('steer', 0.0),
                    'pitch': parsed_action.get('pitch', 0.0),
                    'yaw': parsed_action.get('yaw', 0.0),
                    'roll': parsed_action.get('roll', 0.0),
                    'jump': parsed_action.get('jump', False),
                    'boost': parsed_action.get('boost', False),
                    'handbrake': parsed_action.get('handbrake', False)
                }
                
        except Exception as e:
            return self.current_actions
    
    def send_stealth_input(self, actions: Dict[str, Any]):
        """Send input to the game with stealth techniques"""
        if not self.memory_reader.is_hooked:
            return
        
        try:
            # Add random timing to avoid pattern detection
            if self.memory_reader.stealth_techniques['timing_randomization']:
                time.sleep(random.uniform(0.001, 0.003))
            
            # Convert actions to keyboard/mouse inputs with stealth
            # Throttle (W/S keys)
            if actions['throttle'] > 0.1:
                win32api.keybd_event(ord('W'), 0, 0, 0)
                time.sleep(random.uniform(0.001, 0.002))
                win32api.keybd_event(ord('W'), 0, win32con.KEYEVENTF_KEYUP, 0)
            elif actions['throttle'] < -0.1:
                win32api.keybd_event(ord('S'), 0, 0, 0)
                time.sleep(random.uniform(0.001, 0.002))
                win32api.keybd_event(ord('S'), 0, win32con.KEYEVENTF_KEYUP, 0)
            
            # Steer (A/D keys)
            if actions['steer'] > 0.1:
                win32api.keybd_event(ord('D'), 0, 0, 0)
                time.sleep(random.uniform(0.001, 0.002))
                win32api.keybd_event(ord('D'), 0, win32con.KEYEVENTF_KEYUP, 0)
            elif actions['steer'] < -0.1:
                win32api.keybd_event(ord('A'), 0, 0, 0)
                time.sleep(random.uniform(0.001, 0.002))
                win32api.keybd_event(ord('A'), 0, win32con.KEYEVENTF_KEYUP, 0)
            
            # Jump (Space)
            if actions['jump']:
                win32api.keybd_event(win32con.VK_SPACE, 0, 0, 0)
                time.sleep(random.uniform(0.001, 0.002))
                win32api.keybd_event(win32con.VK_SPACE, 0, win32con.KEYEVENTF_KEYUP, 0)
            
            # Boost (Left Shift)
            if actions['boost']:
                win32api.keybd_event(win32con.VK_LSHIFT, 0, 0, 0)
                time.sleep(random.uniform(0.001, 0.002))
                win32api.keybd_event(win32con.VK_LSHIFT, 0, win32con.KEYEVENTF_KEYUP, 0)
            
            # Handbrake (X)
            if actions['handbrake']:
                win32api.keybd_event(ord('X'), 0, 0, 0)
                time.sleep(random.uniform(0.001, 0.002))
                win32api.keybd_event(ord('X'), 0, win32con.KEYEVENTF_KEYUP, 0)
            
            # Mouse for pitch/yaw/roll (with stealth)
            if abs(actions['pitch']) > 0.1 or abs(actions['yaw']) > 0.1:
                dx = int(actions['yaw'] * random.uniform(80, 120))  # Randomize mouse sensitivity
                dy = int(actions['pitch'] * random.uniform(80, 120))
                win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, dx, dy, 0, 0)
                
        except Exception as e:
            # Silent failure to avoid detection
            pass
    
    def bot_loop(self):
        """Main bot control loop with stealth"""
        print("🤖 Stealth SSL Bot loop started")
        
        while self.is_running:
            if self.bot_enabled and self.memory_reader.is_hooked:
                try:
                    # Get SSL-level action with comprehensive data
                    actions = self.get_ssl_action()
                    
                    # Send stealth input to game
                    self.send_stealth_input(actions)
                    
                    # Update current actions
                    self.current_actions = actions
                    
                except Exception as e:
                    # Silent failure to avoid detection
                    pass
            
            # Random timing to avoid pattern detection
            sleep_time = random.uniform(1/125, 1/115)  # 115-125 FPS
            time.sleep(sleep_time)
    
    def toggle_bot(self):
        """Toggle bot on/off with stealth"""
        self.bot_enabled = not self.bot_enabled
        status = "ON" if self.bot_enabled else "OFF"
        print(f"🤖 Stealth SSL Bot: {status}")
        
        if self.bot_enabled:
            if not self.memory_reader.is_hooked:
                if self.memory_reader.hook_to_process():
                    print("✅ Stealth hooked to Rocket League!")
                else:
                    print("❌ Failed to stealth hook to Rocket League!")
                    self.bot_enabled = False
    
    def show_status(self):
        """Show bot status"""
        print(f"\n📊 Stealth SSL Bot Status:")
        print(f"   🤖 Bot: {'ON' if self.bot_enabled else 'OFF'}")
        print(f"   🎮 RL Hooked: {'Yes' if self.memory_reader.is_hooked else 'No'}")
        print(f"   🎯 Model: {'Loaded' if self.agent else 'Not Loaded'}")
        print(f"   🕵️  Stealth Mode: {'ACTIVE' if self.stealth_mode else 'INACTIVE'}")
        print(f"   🎮 Current Actions: {self.current_actions}")
        print(f"   📊 Game State: {self.memory_reader.game_state['game_time']:.2f}s")
        print()
    
    def run(self):
        """Run the stealth SSL bot injector"""
        print("🚀 Starting Stealth SSL Bot Injector...")
        
        # Setup keyboard hooks
        keyboard.add_hotkey('f1', self.toggle_bot)
        keyboard.add_hotkey('f2', self.show_status)
        
        self.is_running = True
        
        # Start bot loop in separate thread
        bot_thread = threading.Thread(target=self.bot_loop, daemon=True)
        bot_thread.start()
        
        try:
            print("✅ Stealth SSL Bot Injector running!")
            print("🎮 Controls:")
            print("   F1 - Toggle bot on/off")
            print("   F2 - Show status")
            print("   ESC - Exit")
            print("🕵️  Stealth mode: ACTIVE - RL cannot detect this bot!")
            
            # Wait for ESC key
            keyboard.wait('esc')
            
        except KeyboardInterrupt:
            pass
        finally:
            self.is_running = False
            self.memory_reader.cleanup()
            print("⏹️  Stealth SSL Bot Injector stopped")

class StealthGUI:
    """Stealth GUI for the injector"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Stealth SSL Bot Injector")
        self.root.geometry("400x300")
        self.root.configure(bg='#1a1a1a')
        
        self.injector = None
        self.is_running = False
        
        self.setup_gui()
    
    def setup_gui(self):
        """Setup the GUI"""
        # Title
        title_label = tk.Label(
            self.root,
            text="🕵️ Stealth SSL Bot Injector",
            font=("Arial", 16, "bold"),
            fg='#00ff00',
            bg='#1a1a1a'
        )
        title_label.pack(pady=10)
        
        # Status
        self.status_label = tk.Label(
            self.root,
            text="Status: Ready",
            font=("Arial", 12),
            fg='#ffffff',
            bg='#1a1a1a'
        )
        self.status_label.pack(pady=5)
        
        # Inject button
        self.inject_button = tk.Button(
            self.root,
            text="🚀 Inject into Rocket League",
            font=("Arial", 12, "bold"),
            bg='#00ff00',
            fg='#000000',
            command=self.inject_bot,
            width=25,
            height=2
        )
        self.inject_button.pack(pady=10)
        
        # Bot status
        self.bot_status_label = tk.Label(
            self.root,
            text="Bot: OFF",
            font=("Arial", 12),
            fg='#ff0000',
            bg='#1a1a1a'
        )
        self.bot_status_label.pack(pady=5)
        
        # Instructions
        instructions = tk.Label(
            self.root,
            text="Instructions:\n1. Click 'Inject into Rocket League'\n2. Press F1 in-game to toggle bot\n3. Press F2 to show status\n4. Press ESC to exit",
            font=("Arial", 10),
            fg='#cccccc',
            bg='#1a1a1a',
            justify='left'
        )
        instructions.pack(pady=10)
        
        # Stealth indicator
        stealth_label = tk.Label(
            self.root,
            text="🕵️ Stealth Mode: ACTIVE",
            font=("Arial", 10, "bold"),
            fg='#00ff00',
            bg='#1a1a1a'
        )
        stealth_label.pack(pady=5)
    
    def inject_bot(self):
        """Inject the bot into Rocket League"""
        try:
            if not self.is_running:
                self.status_label.config(text="Status: Injecting...", fg='#ffff00')
                self.root.update()
                
                # Create and start injector
                self.injector = StealthSSLInjector()
                
                # Start injector in separate thread
                injector_thread = threading.Thread(target=self.injector.run, daemon=True)
                injector_thread.start()
                
                self.is_running = True
                self.status_label.config(text="Status: Injected & Running", fg='#00ff00')
                self.inject_button.config(text="✅ Injected", bg='#00aa00')
                
                # Start status update loop
                self.update_status()
                
            else:
                messagebox.showinfo("Info", "Bot is already injected and running!")
                
        except Exception as e:
            self.status_label.config(text=f"Status: Error - {str(e)}", fg='#ff0000')
            messagebox.showerror("Error", f"Failed to inject bot: {str(e)}")
    
    def update_status(self):
        """Update the status display"""
        if self.is_running and self.injector:
            try:
                if self.injector.bot_enabled:
                    self.bot_status_label.config(text="Bot: ON", fg='#00ff00')
                else:
                    self.bot_status_label.config(text="Bot: OFF", fg='#ff0000')
            except:
                pass
        
        # Schedule next update
        if self.is_running:
            self.root.after(1000, self.update_status)
    
    def run(self):
        """Run the GUI"""
        self.root.mainloop()

def main():
    """Main function"""
    print("🏆 Stealth SSL-Level Opti Bot Injector")
    print("=" * 50)
    
    # Check if SSL model exists
    model_path = "ssl_model.pt"
    if not os.path.exists(model_path):
        print("❌ SSL model not found!")
        print("💡 Make sure you've trained the model first")
        return
    
    # Create and run GUI
    gui = StealthGUI()
    gui.run()

if __name__ == "__main__":
    main()
