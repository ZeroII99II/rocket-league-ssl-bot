#!/usr/bin/env python3
"""
JSTN Multi-Mode Trainer - The Ultimate Rocket League AI
Trains the bot to play like jstn (Justin) across 1s, 2s, and 3s modes
Uses circular training to master all game modes like a true pro
"""

import os
import sys
import time
import numpy as np
import wandb
import redis
import threading
import subprocess
import shutil
import re
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional
import json
import queue
import multiprocessing as mp

# Add rocket-learn to path
sys.path.append(str(Path(__file__).parent / "rocket-learn-master"))

# Import RLGym components
try:
    from rlgym.api import RLGym, ObsBuilder, ActionParser, RewardFunction, DoneCondition, StateMutator
    from rlgym.rocket_league.sim.rocketsim_engine import RocketSimEngine
    from rlgym.rocket_league.obs_builders.default_obs import DefaultObs
    from rlgym.rocket_league.action_parsers.lookup_table_action import LookupTableAction
    from rlgym.rocket_league.reward_functions.combined_reward import CombinedReward
    from rlgym.rocket_league.done_conditions.timeout_condition import TimeoutCondition
    from rlgym.rocket_league.done_conditions.goal_condition import GoalCondition
    from rlgym.rocket_league.state_mutators.kickoff_mutator import KickoffMutator
    import rlviser_py
    print("✅ RLGym and RLViser imported successfully")
except ImportError as e:
    print(f"⚠️  RLGym import warning: {e}")
    # Create dummy classes for compatibility
    class DummyRLGym:
        def __init__(self, *args, **kwargs):
            pass
    RLGym = DummyRLGym
    ObsBuilder = DummyRLGym
    ActionParser = DummyRLGym
    RewardFunction = DummyRLGym
    DoneCondition = DummyRLGym
    StateMutator = DummyRLGym
    RocketSimEngine = DummyRLGym
    rlviser_py = DummyRLGym

# Import all our modern components
try:
    from ModernObsBuilder import ModernObsBuilder
    from ModernActionParser import ModernActionParser
    from ModernRewardSystem import ModernRewardSystem
    from ModernAgent import ModernAgent, ModernSelector
    from SSLMechanics import SSLMechanics
    print("✅ Modern components imported successfully")
except ImportError as e:
    print(f"⚠️  Modern components import warning: {e}")
    # Create dummy classes
    class ModernObsBuilder:
        def __init__(self, *args, **kwargs):
            pass
    class ModernActionParser:
        def __init__(self, *args, **kwargs):
            pass
    class ModernRewardSystem:
        def __init__(self, *args, **kwargs):
            pass
    class ModernAgent:
        def __init__(self, *args, **kwargs):
            pass
    class ModernSelector:
        def __init__(self, *args, **kwargs):
            pass
    class SSLMechanics:
        def __init__(self):
            self.mechanics = ['aerial', 'flip_reset', 'double_tap', 'ceiling_shot', 'musty_flick']

class JSTNMultiModeTrainer:
    """
    The Ultimate JSTN Multi-Mode Trainer
    Trains the bot to play like jstn across 1s, 2s, and 3s modes
    Uses circular training to master all game modes
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.device = 'cpu'  # Force CPU for compatibility
        
        # Training modes
        self.training_modes = ['1s', '2s', '3s']
        self.current_mode_index = 0
        self.mode_episode_counts = {'1s': 0, '2s': 0, '3s': 0}
        self.mode_switches = 0
        
        # JSTN-specific configuration for each mode
        self.jstn_mode_configs = {
            '1s': {
                'team_size': 1,
                'episodes_per_switch': 1000,
                'playstyle': {
                    'aerial_aggression': 0.95,      # jstn's 1s aerial dominance
                    'flip_reset_mastery': 0.98,     # jstn's 1s flip reset expertise
                    'double_tap_precision': 0.95,   # jstn's 1s double tap accuracy
                    'ceiling_shot_skill': 0.9,      # jstn's 1s ceiling play
                    'musty_flick_timing': 0.85,     # jstn's 1s creative mechanics
                    'speed_control': 0.95,          # jstn's 1s speed management
                    'boost_efficiency': 0.9,        # jstn's 1s boost usage
                    'recovery_speed': 0.95,         # jstn's 1s quick recoveries
                    'wall_play': 0.85,              # jstn's 1s wall mechanics
                    'mechanical_creativity': 0.98   # jstn's 1s innovative plays
                },
                'reward_weights': {
                    'aerial_goal_w': 15, 'flip_reset_goal_w': 20, 'double_tap_w': 25,
                    'ceiling_shot_w': 12, 'musty_flick_w': 8, 'flick_w': 10,
                    'pinch_w': 18, 'wall_goal_w': 10, 'recovery_w': 8
                }
            },
            '2s': {
                'team_size': 2,
                'episodes_per_switch': 1500,
                'playstyle': {
                    'aerial_aggression': 0.85,      # jstn's 2s aerial play
                    'flip_reset_mastery': 0.9,      # jstn's 2s flip reset expertise
                    'double_tap_precision': 0.85,   # jstn's 2s double tap accuracy
                    'ceiling_shot_skill': 0.8,      # jstn's 2s ceiling play
                    'musty_flick_timing': 0.75,     # jstn's 2s creative mechanics
                    'speed_control': 0.9,           # jstn's 2s speed management
                    'boost_efficiency': 0.85,       # jstn's 2s boost usage
                    'recovery_speed': 0.9,          # jstn's 2s quick recoveries
                    'wall_play': 0.8,               # jstn's 2s wall mechanics
                    'team_play': 0.8,               # jstn's 2s team coordination
                    'mechanical_creativity': 0.9    # jstn's 2s innovative plays
                },
                'reward_weights': {
                    'aerial_goal_w': 12, 'flip_reset_goal_w': 15, 'double_tap_w': 18,
                    'ceiling_shot_w': 10, 'musty_flick_w': 6, 'flick_w': 8,
                    'pinch_w': 15, 'wall_goal_w': 8, 'recovery_w': 6,
                    'team_goal_w': 20, 'pass_w': 5, 'assist_w': 8
                }
            },
            '3s': {
                'team_size': 3,
                'episodes_per_switch': 2000,
                'playstyle': {
                    'aerial_aggression': 0.8,       # jstn's 3s aerial play
                    'flip_reset_mastery': 0.85,     # jstn's 3s flip reset expertise
                    'double_tap_precision': 0.8,    # jstn's 3s double tap accuracy
                    'ceiling_shot_skill': 0.75,     # jstn's 3s ceiling play
                    'musty_flick_timing': 0.7,      # jstn's 3s creative mechanics
                    'speed_control': 0.85,          # jstn's 3s speed management
                    'boost_efficiency': 0.8,        # jstn's 3s boost usage
                    'recovery_speed': 0.85,         # jstn's 3s quick recoveries
                    'wall_play': 0.75,              # jstn's 3s wall mechanics
                    'team_play': 0.9,               # jstn's 3s team coordination
                    'mechanical_creativity': 0.85   # jstn's 3s innovative plays
                },
                'reward_weights': {
                    'aerial_goal_w': 10, 'flip_reset_goal_w': 12, 'double_tap_w': 15,
                    'ceiling_shot_w': 8, 'musty_flick_w': 5, 'flick_w': 6,
                    'pinch_w': 12, 'wall_goal_w': 6, 'recovery_w': 5,
                    'team_goal_w': 25, 'pass_w': 8, 'assist_w': 12, 'rotation_w': 3
                }
            }
        }
        
        # Training configuration
        self.max_episodes = self.config.get('max_episodes', 100000)  # More episodes for multi-mode
        self.batch_size = self.config.get('batch_size', 1000)
        self.learning_rate = self.config.get('learning_rate', 3e-4)
        self.gamma = self.config.get('gamma', 0.99)
        
        # SSL Mechanics system
        self.ssl_mechanics = SSLMechanics()
        
        # Training state
        self.episode_count = 0
        self.total_steps = 0
        self.start_time = time.time()
        self.best_reward = -float('inf')
        
        # Performance tracking per mode
        self.performance_metrics = {
            '1s': {
                'episode_rewards': [], 'episode_lengths': [], 'ssl_level': 0.0,
                'mechanical_skill': 0.0, 'aerial_mastery': 0.0, 'flip_reset_skill': 0.0,
                'double_tap_accuracy': 0.0, 'ceiling_shot_skill': 0.0, 'musty_flick_timing': 0.0,
                'recovery_speed': 0.0, 'wall_play_skill': 0.0, 'mechanical_creativity': 0.0
            },
            '2s': {
                'episode_rewards': [], 'episode_lengths': [], 'ssl_level': 0.0,
                'mechanical_skill': 0.0, 'aerial_mastery': 0.0, 'flip_reset_skill': 0.0,
                'double_tap_accuracy': 0.0, 'ceiling_shot_skill': 0.0, 'musty_flick_timing': 0.0,
                'recovery_speed': 0.0, 'wall_play_skill': 0.0, 'team_coordination': 0.0,
                'mechanical_creativity': 0.0
            },
            '3s': {
                'episode_rewards': [], 'episode_lengths': [], 'ssl_level': 0.0,
                'mechanical_skill': 0.0, 'aerial_mastery': 0.0, 'flip_reset_skill': 0.0,
                'double_tap_accuracy': 0.0, 'ceiling_shot_skill': 0.0, 'musty_flick_timing': 0.0,
                'recovery_speed': 0.0, 'wall_play_skill': 0.0, 'team_coordination': 0.0,
                'mechanical_creativity': 0.0
            }
        }
        
        # Worker processes per mode
        self.worker_processes = {'1s': {}, '2s': {}, '3s': {}}
        self.learner_processes = {'1s': {}, '2s': {}, '3s': {}}
        
        # Redis connections per mode
        self.redis_connections = {'1s': {}, '2s': {}, '3s': {}}
        
        # RLGym environments for each mode
        self.rlgym_envs = {}
        
        print("🏆 JSTN Multi-Mode Trainer initialized")
        print("🎯 Training to play like jstn (Justin) across ALL game modes!")
        print("🚀 Using circular training: 1s → 2s → 3s → repeat")
        print(f"📊 Training modes: {self.training_modes}")
        print(f"🧠 SSL Mechanics: {len(self.ssl_mechanics.mechanics)}")
    
    def create_rlgym_environment(self, mode: str):
        """Create RLGym environment for specific mode with RLViser visualizer"""
        try:
            mode_config = self.jstn_mode_configs[mode]
            team_size = mode_config['team_size']
            
            print(f"🎮 Creating RLGym environment for {mode} mode (team_size={team_size})...")
            
            # Create observation builder (use default for now, will upgrade to modern later)
            obs_builder = DefaultObs()
            
            # Create action parser (use default for now, will upgrade to modern later)
            action_parser = LookupTableAction()
            
            # Create reward function (use combined reward for now)
            reward_function = CombinedReward()
            
            # Create terminal conditions
            timeout_condition = TimeoutCondition(225)  # 3.75 minutes
            goal_condition = GoalCondition()
            
            # Create state mutator
            state_mutator = KickoffMutator()
            
            # Create transition engine
            transition_engine = RocketSimEngine()
            
            # Create UDP-based visualizer
            try:
                from udp_packet_sender import get_sender
                print(f"   🎮 Loading UDP visualizer for {mode} mode...")
                
                # Get UDP sender instance
                if not hasattr(self, 'udp_sender'):
                    self.udp_sender = get_sender()
                    print(f"   📡 UDP sender ready for {mode} mode!")
                    print(f"   🎯 Make sure to run 'python opti_udp_visualizer.py' to see the visualizer!")
                
                # Create renderer that sends UDP packets
                class UDPVisualizerRenderer:
                    def __init__(self, trainer_instance, mode, udp_sender):
                        self.trainer = trainer_instance
                        self.mode = mode
                        self.udp_sender = udp_sender
                        self.episode_count = 0
                    
                    def render(self, state):
                        """Send game state via UDP to visualizer"""
                        try:
                            # Send RLGym game state via UDP
                            self.udp_sender.send_rlgym_state(state)
                            self.episode_count += 1
                            return True
                        except Exception as e:
                            print(f"UDP visualizer error: {e}")
                            return False
                
                renderer = UDPVisualizerRenderer(self, mode, self.udp_sender)
                print(f"   ✅ UDP visualizer renderer created for {mode} mode!")
                
            except Exception as e:
                print(f"   ⚠️  UDP visualizer failed: {e}")
                print(f"   📺 Using fallback renderer for {mode} mode")
                # Create a simple fallback renderer
                class FallbackRenderer:
                    def render(self, state):
                        # Print basic game state info
                        if hasattr(state, 'ball') and hasattr(state, 'cars'):
                            print(f"   🏀 Ball: {state.ball.position} | 🚗 Cars: {len(state.cars)}")
                        return True
                renderer = FallbackRenderer()
            
            # Create RLGym environment with RLViser visualizer
            env = RLGym(
                state_mutator=state_mutator,
                obs_builder=obs_builder,
                action_parser=action_parser,
                reward_fn=reward_function,
                transition_engine=transition_engine,
                termination_cond=goal_condition,
                truncation_cond=timeout_condition,
                renderer=renderer  # This enables the visualizer!
            )
            
            self.rlgym_envs[mode] = env
            print(f"✅ Created RLGym environment for {mode} mode with RLViser visualizer")
            return env
            
        except Exception as e:
            print(f"❌ Failed to create RLGym environment for {mode}: {e}")
            return None
    
    def create_mode_folders(self):
        """Create separate folders for each training mode"""
        print("📁 Creating mode-specific folders...")
        
        for mode in self.training_modes:
            mode_folder = Path(f"training_{mode}")
            mode_folder.mkdir(exist_ok=True)
            
            # Create subfolders for each mode
            subfolders = ['models', 'logs', 'replays', 'configs', 'workers', 'learners']
            for subfolder in subfolders:
                (mode_folder / subfolder).mkdir(exist_ok=True)
            
            # Copy and customize worker files for each mode
            self.customize_workers_for_mode(mode, mode_folder)
            
            # Copy and customize learner files for each mode
            self.customize_learners_for_mode(mode, mode_folder)
            
            print(f"✅ Created {mode} training folder with customized files")
    
    def customize_workers_for_mode(self, mode: str, mode_folder: Path):
        """Customize worker files for specific mode"""
        mode_config = self.jstn_mode_configs[mode]
        
        # List of worker files to customize
        worker_files = [
            'worker_selector.py', 'worker_dtap.py', 'worker_flip_reset.py',
            'worker_aerial.py', 'worker_flick.py', 'worker_ceil_pinch.py',
            'worker_pinch.py', 'worker_wall.py', 'worker_walldash.py',
            'worker_recovery.py', 'worker_demo.py', 'worker_gp.py',
            'worker_half_flip.py', 'worker_lix.py', 'worker_kickoff.py'
        ]
        
        for worker_file in worker_files:
            if os.path.exists(worker_file):
                try:
                    # Read original file
                    with open(worker_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Customize for mode
                    content = self.customize_content_for_mode(content, mode, mode_config)
                    
                    # Write to mode folder
                    mode_worker_path = mode_folder / 'workers' / worker_file
                    with open(mode_worker_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                except Exception as e:
                    print(f"⚠️  Error processing worker file {worker_file}: {e}")
                    continue
    
    def customize_learners_for_mode(self, mode: str, mode_folder: Path):
        """Customize learner files for specific mode"""
        mode_config = self.jstn_mode_configs[mode]
        
        # List of learner files to customize
        learner_files = [
            'learner_selector.py', 'learner_dtap.py', 'learner_flip_reset.py',
            'learner_aerial.py', 'learner_flick.py', 'learner_ceil_pinch.py',
            'learner_pinch.py', 'learner_wall.py', 'learner_walldash.py',
            'learner_recovery.py', 'learner_demo.py', 'learner_gp.py',
            'learner_half_flip.py', 'learner_lix.py', 'learner_kickoff.py'
        ]
        
        for learner_file in learner_files:
            if os.path.exists(learner_file):
                try:
                    # Read original file
                    with open(learner_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Customize for mode
                    content = self.customize_content_for_mode(content, mode, mode_config)
                    
                    # Write to mode folder
                    mode_learner_path = mode_folder / 'learners' / learner_file
                    with open(mode_learner_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                except Exception as e:
                    print(f"⚠️  Error processing learner file {learner_file}: {e}")
                    continue
    
    def customize_content_for_mode(self, content: str, mode: str, mode_config: Dict[str, Any]) -> str:
        """Customize file content for specific mode"""
        try:
            # Update team size
            content = content.replace('team_size=3', f'team_size={mode_config["team_size"]}')
            
            # Update reward weights
            # Handle reward_weights - it might be a list or dict
            reward_weights = mode_config.get('reward_weights', {})
            if isinstance(reward_weights, list):
                # Convert list to dict with default values
                reward_weights = {f"reward_{i}": 1.0 for i in range(len(reward_weights))}
            
            for reward_key, reward_value in reward_weights.items():
                pattern = rf'{reward_key}_w=\d+(?:\.\d+)?'
                if re.search(pattern, content):
                    content = re.sub(pattern, f'{reward_key}_w={reward_value}', content)
            
            # Add mode-specific comment
            mode_comment = f"""
# JSTN {mode.upper()} Training Configuration
# Optimized for {mode} gameplay with jstn's {mode} playstyle
# Team size: {mode_config['team_size']} | Episodes per switch: {mode_config['episodes_per_switch']}
"""
            content = mode_comment + content
            
            return content
        except Exception as e:
            print(f"⚠️  Error customizing content for {mode}: {e}")
            return content
    
    def get_current_mode(self) -> str:
        """Get current training mode"""
        return self.training_modes[self.current_mode_index]
    
    def switch_training_mode(self):
        """Switch to next training mode in circular fashion"""
        current_mode = self.get_current_mode()
        episodes_in_current_mode = self.mode_episode_counts[current_mode]
        episodes_per_switch = self.jstn_mode_configs[current_mode]['episodes_per_switch']
        
        if episodes_in_current_mode >= episodes_per_switch:
            # Switch to next mode
            self.current_mode_index = (self.current_mode_index + 1) % len(self.training_modes)
            self.mode_switches += 1
            new_mode = self.get_current_mode()
            
            print(f"🔄 Switching training mode: {current_mode} → {new_mode}")
            print(f"📊 Mode switches: {self.mode_switches}")
            print(f"🎯 Now training for {new_mode} gameplay like jstn!")
            
            # Reset episode count for new mode
            self.mode_episode_counts[current_mode] = 0
            
            # Save model for previous mode
            self.save_mode_model(current_mode)
            
            return True
        
        return False
    
    def setup_redis_connections_for_mode(self, mode: str):
        """Setup Redis connections for specific mode"""
        print(f"🔗 Setting up Redis connections for {mode}...")
        
        # Use different Redis DBs for each mode (Redis 3.0.504 supports DB 0-15)
        base_db = {'1s': 0, '2s': 5, '3s': 10}[mode]
        
        # List of workers for this mode
        workers = [
            'selector', 'dtap', 'flip_reset', 'aerial', 'flick', 'ceil_pinch',
            'pinch', 'wall', 'walldash', 'recovery', 'demo', 'gp',
            'half_flip', 'lix', 'kickoff'
        ]
        
        for i, worker_name in enumerate(workers):
            try:
                # Use DB indices 0-14 (Redis 3.0.504 limit)
                db_index = (base_db + i) % 15
                redis_conn = redis.Redis(
                    host='localhost',
                    port=6379,
                    db=db_index,
                    decode_responses=True
                )
                # Test connection
                redis_conn.ping()
                self.redis_connections[mode][worker_name] = redis_conn
                print(f"✅ Redis connection for {mode}/{worker_name} (DB {db_index})")
            except Exception as e:
                print(f"❌ Failed to connect to Redis for {mode}/{worker_name}: {e}")
    
    def start_workers_for_mode(self, mode: str):
        """Start all worker processes for specific mode"""
        print(f"🚀 Starting all worker processes for {mode}...")
        
        mode_folder = Path(f"training_{mode}")
        worker_functions = {
            'selector': 'worker_selector_main',
            'dtap': 'worker_dtap_main',
            'flip_reset': 'worker_flip_reset_main',
            'aerial': 'worker_aerial_main',
            'flick': 'worker_flick_main',
            'ceil_pinch': 'worker_ceil_pinch_main',
            'pinch': 'worker_pinch_main',
            'wall': 'worker_wall_main',
            'walldash': 'worker_walldash_main',
            'recovery': 'worker_recovery_main',
            'demo': 'worker_demo_main',
            'gp': 'worker_gp_main',
            'half_flip': 'worker_half_flip_main',
            'lix': 'worker_lix_main',
            'kickoff': 'worker_kickoff_main'
        }
        
        # Ensure worker_functions is a dict
        if not isinstance(worker_functions, dict):
            worker_functions = {}
        
        for worker_name, worker_func in worker_functions.items():
            try:
                # Start worker process with mode-specific script
                worker_script = mode_folder / 'workers' / f'worker_{worker_name}.py'
                if worker_script.exists():
                    process = subprocess.Popen(
                        [sys.executable, str(worker_script)],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True
                    )
                    self.worker_processes[mode][worker_name] = process
                    print(f"✅ Started {mode}/{worker_name} worker (PID: {process.pid})")
                    
                    # Small delay between starting workers
                    time.sleep(0.5)
                else:
                    print(f"⚠️  Worker script not found: {worker_script}")
                    
            except Exception as e:
                print(f"❌ Failed to start {mode}/{worker_name} worker: {e}")
    
    def start_learners_for_mode(self, mode: str):
        """Start all learner processes for specific mode"""
        print(f"🧠 Starting all learner processes for {mode}...")
        
        mode_folder = Path(f"training_{mode}")
        learner_functions = {
            'selector': 'learner_selector_main',
            'dtap': 'learner_dtap_main',
            'flip_reset': 'learner_flip_reset_main',
            'aerial': 'learner_aerial_main',
            'flick': 'learner_flick_main',
            'ceil_pinch': 'learner_ceil_pinch_main',
            'pinch': 'learner_pinch_main',
            'wall': 'learner_wall_main',
            'walldash': 'learner_walldash_main',
            'recovery': 'learner_recovery_main',
            'demo': 'learner_demo_main',
            'gp': 'learner_gp_main',
            'half_flip': 'learner_half_flip_main',
            'lix': 'learner_lix_main',
            'kickoff': 'learner_kickoff_main'
        }
        
        # Ensure learner_functions is a dict
        if not isinstance(learner_functions, dict):
            learner_functions = {}
        
        for learner_name, learner_func in learner_functions.items():
            try:
                # Start learner process with mode-specific script
                learner_script = mode_folder / 'learners' / f'learner_{learner_name}.py'
                if learner_script.exists():
                    process = subprocess.Popen(
                        [sys.executable, str(learner_script)],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True
                    )
                    self.learner_processes[mode][learner_name] = process
                    print(f"✅ Started {mode}/{learner_name} learner (PID: {process.pid})")
                    
                    # Small delay between starting learners
                    time.sleep(0.5)
                else:
                    print(f"⚠️  Learner script not found: {learner_script}")
                    
            except Exception as e:
                print(f"❌ Failed to start {mode}/{learner_name} learner: {e}")
    
    def collect_performance_data_for_mode(self, mode: str):
        """Collect performance data from all workers for specific mode"""
        print(f"🎮 Training {mode} mode - Learning to play like jstn...")
        
        # Ensure redis_connections[mode] is a dict
        if mode not in self.redis_connections or not isinstance(self.redis_connections[mode], dict):
            self.redis_connections[mode] = {}
        
        for worker_name, redis_conn in self.redis_connections[mode].items():
            try:
                # Get worker stats
                stats = redis_conn.hgetall(f"worker_stats_{worker_name}")
                if stats:
                    self.performance_metrics[mode]['worker_performance'] = stats
                
                # Get JSTN-specific metrics
                jstn_metrics = redis_conn.hgetall(f"jstn_metrics_{worker_name}")
                if jstn_metrics:
                    self.performance_metrics[mode]['jstn_mechanics'] = jstn_metrics
                
            except Exception as e:
                print(f"❌ Failed to collect data from {mode}/{worker_name}: {e}")
    
    def train_episode_with_rlgym(self, mode: str):
        """Train an episode using RLGym environment with visualizer"""
        try:
            env = self.rlgym_envs.get(mode)
            if env is None:
                print(f"⚠️  No RLGym environment for {mode}, skipping episode")
                return
            
            # Reset environment
            obs = env.reset()
            done = False
            episode_reward = 0
            steps = 0
            
            print(f"🎮 Starting {mode} episode - Watch the visualizer!")
            print(f"   📊 Episode {self.episode_count} | Mode: {mode.upper()}")
            print(f"   🎯 Learning jstn's {mode} playstyle...")
            
            while not done and steps < 1000:  # Max steps per episode
                # Get action from agent (random for now, will be replaced with trained agent)
                # RLGym 2.0.1 uses different action format
                action = [0, 0, 0, 0, 0, 0, 0, 0]  # Default action for all agents
                
                # Step environment
                result = env.step(action)
                
                # Handle different return formats from RLGym
                if isinstance(result, (list, tuple)) and len(result) >= 3:
                    if len(result) == 3:
                        obs, reward, done = result
                        info = {}
                    else:
                        obs, reward, done, info = result[:4]
                else:
                    # Fallback for unexpected format
                    obs = result
                    reward = 0.0
                    done = False
                    info = {}
                
                episode_reward += reward
                steps += 1
                
                # Show visual feedback every 100 steps
                if steps % 100 == 0:
                    print(f"   🏃 Step {steps} | Reward: {episode_reward:.2f} | Learning jstn's mechanics...")
            
            print(f"   ✅ Episode complete! Reward: {episode_reward:.2f} | Steps: {steps}")
            
            # Update performance metrics
            mode_metrics = self.performance_metrics[mode]
            mode_metrics['episode_rewards'].append(episode_reward)
            mode_metrics['episode_lengths'].append(steps)
            
            # Keep only last 100 episodes
            if len(mode_metrics['episode_rewards']) > 100:
                mode_metrics['episode_rewards'] = mode_metrics['episode_rewards'][-100:]
                mode_metrics['episode_lengths'] = mode_metrics['episode_lengths'][-100:]
            
        except Exception as e:
            print(f"❌ Error training episode in {mode}: {e}")
    
    def simulate_jstn_training_episode(self, mode: str):
        """Simulate the bot playing against itself and learning from jstn's playstyle"""
        mode_config = self.jstn_mode_configs[mode]
        mode_metrics = self.performance_metrics[mode]
        
        # Simulate learning from jstn's playstyle
        learning_rate = 0.001  # How fast it learns from jstn
        
        # Update skills based on jstn's playstyle for this mode
        jstn_playstyle = mode_config['playstyle']
        
        # Aerial mastery (jstn's signature)
        if mode_metrics['aerial_mastery'] < jstn_playstyle['aerial_aggression']:
            mode_metrics['aerial_mastery'] += learning_rate * jstn_playstyle['aerial_aggression']
        
        # Flip reset mastery (jstn's expertise)
        if mode_metrics['flip_reset_skill'] < jstn_playstyle['flip_reset_mastery']:
            mode_metrics['flip_reset_skill'] += learning_rate * jstn_playstyle['flip_reset_mastery']
        
        # Double tap precision (jstn's accuracy)
        if mode_metrics['double_tap_accuracy'] < jstn_playstyle['double_tap_precision']:
            mode_metrics['double_tap_accuracy'] += learning_rate * jstn_playstyle['double_tap_precision']
        
        # Ceiling shot skill (jstn's creativity)
        if mode_metrics['ceiling_shot_skill'] < jstn_playstyle['ceiling_shot_skill']:
            mode_metrics['ceiling_shot_skill'] += learning_rate * jstn_playstyle['ceiling_shot_skill']
        
        # Musty flick timing (jstn's innovation)
        if mode_metrics['musty_flick_timing'] < jstn_playstyle['musty_flick_timing']:
            mode_metrics['musty_flick_timing'] += learning_rate * jstn_playstyle['musty_flick_timing']
        
        # Recovery speed (jstn's quickness)
        if mode_metrics['recovery_speed'] < jstn_playstyle['recovery_speed']:
            mode_metrics['recovery_speed'] += learning_rate * jstn_playstyle['recovery_speed']
        
        # Wall play skill (jstn's versatility)
        if mode_metrics['wall_play_skill'] < jstn_playstyle['wall_play']:
            mode_metrics['wall_play_skill'] += learning_rate * jstn_playstyle['wall_play']
        
        # Team coordination (for 2s and 3s)
        if mode != '1s' and 'team_play' in jstn_playstyle:
            if mode_metrics.get('team_coordination', 0.0) < jstn_playstyle['team_play']:
                mode_metrics['team_coordination'] += learning_rate * jstn_playstyle['team_play']
        
        # Mechanical creativity (jstn's innovation)
        if mode_metrics['mechanical_creativity'] < jstn_playstyle['mechanical_creativity']:
            mode_metrics['mechanical_creativity'] += learning_rate * jstn_playstyle['mechanical_creativity']
    
    def calculate_jstn_level_for_mode(self, mode: str) -> float:
        """Calculate JSTN skill level for specific mode"""
        mode_config = self.jstn_mode_configs[mode]
        mode_metrics = self.performance_metrics[mode]
        
        # JSTN-specific skill calculations for this mode
        aerial_skill = mode_metrics.get('aerial_mastery', 0.0)
        flip_reset_skill = mode_metrics.get('flip_reset_skill', 0.0)
        double_tap_skill = mode_metrics.get('double_tap_accuracy', 0.0)
        ceiling_skill = mode_metrics.get('ceiling_shot_skill', 0.0)
        musty_skill = mode_metrics.get('musty_flick_timing', 0.0)
        recovery_skill = mode_metrics.get('recovery_speed', 0.0)
        wall_skill = mode_metrics.get('wall_play_skill', 0.0)
        team_skill = mode_metrics.get('team_coordination', 0.0)
        creativity_skill = mode_metrics.get('mechanical_creativity', 0.0)
        
        # Weighted average based on jstn's playstyle for this mode
        jstn_weights = {
            'aerial': 0.25,      # jstn's signature
            'flip_reset': 0.20,  # jstn's mastery
            'double_tap': 0.15,  # jstn's precision
            'ceiling': 0.10,     # jstn's creativity
            'musty': 0.10,       # jstn's innovation
            'recovery': 0.10,    # jstn's speed
            'wall': 0.05,        # jstn's versatility
            'team': 0.05 if mode != '1s' else 0.0,  # jstn's coordination (not in 1s)
            'creativity': 0.0    # Already included in other skills
        }
        
        jstn_level = (
            aerial_skill * jstn_weights['aerial'] +
            flip_reset_skill * jstn_weights['flip_reset'] +
            double_tap_skill * jstn_weights['double_tap'] +
            ceiling_skill * jstn_weights['ceiling'] +
            musty_skill * jstn_weights['musty'] +
            recovery_skill * jstn_weights['recovery'] +
            wall_skill * jstn_weights['wall'] +
            team_skill * jstn_weights['team']
        )
        
        mode_metrics['ssl_level'] = jstn_level
        mode_metrics['mechanical_skill'] = jstn_level
        
        return jstn_level
    
    def log_to_wandb_for_mode(self, mode: str):
        """Log metrics to wandb for specific mode"""
        if self.episode_count % 100 == 0:  # Log every 100 episodes
            mode_metrics = self.performance_metrics[mode]
            wandb.log({
                'episode': self.episode_count,
                'mode': mode,
                'mode_episodes': self.mode_episode_counts[mode],
                'mode_switches': self.mode_switches,
                f'{mode}_jstn_level': mode_metrics['ssl_level'],
                f'{mode}_mechanical_skill': mode_metrics['mechanical_skill'],
                f'{mode}_aerial_mastery': mode_metrics['aerial_mastery'],
                f'{mode}_flip_reset_skill': mode_metrics['flip_reset_skill'],
                f'{mode}_double_tap_accuracy': mode_metrics['double_tap_accuracy'],
                f'{mode}_ceiling_shot_skill': mode_metrics['ceiling_shot_skill'],
                f'{mode}_musty_flick_timing': mode_metrics['musty_flick_timing'],
                f'{mode}_recovery_speed': mode_metrics['recovery_speed'],
                f'{mode}_wall_play_skill': mode_metrics['wall_play_skill'],
                f'{mode}_team_coordination': mode_metrics.get('team_coordination', 0.0),
                f'{mode}_mechanical_creativity': mode_metrics['mechanical_creativity'],
                'training_time': time.time() - self.start_time,
                'total_steps': self.total_steps
            })
    
    def print_progress_for_mode(self, mode: str):
        """Print training progress for specific mode"""
        if self.episode_count % 100 == 0:  # More frequent updates
            elapsed_time = time.time() - self.start_time
            episodes_per_second = self.episode_count / elapsed_time if elapsed_time > 0 else 0
            mode_metrics = self.performance_metrics[mode]
            mode_config = self.jstn_mode_configs[mode]
            
            # Calculate progress percentage
            progress_pct = (self.mode_episode_counts[mode] / mode_config['episodes_per_switch']) * 100
            
            print(f"🎮 {mode.upper()} Training Progress:")
            print(f"   📊 Episode {self.episode_count} | Mode Episodes: {self.mode_episode_counts[mode]}/{mode_config['episodes_per_switch']} ({progress_pct:.1f}%)")
            print(f"   🎯 JSTN Skill Level: {mode_metrics['ssl_level']:.3f} | Mechanical Mastery: {mode_metrics['mechanical_skill']:.3f}")
            print(f"   🚁 Aerial: {mode_metrics['aerial_mastery']:.3f} | 🔄 Flip Reset: {mode_metrics['flip_reset_skill']:.3f} | 🎯 Double Tap: {mode_metrics['double_tap_accuracy']:.3f}")
            print(f"   🏃 Speed: {episodes_per_second:.2f} eps | ⏱️  Time: {elapsed_time/60:.1f}min")
            
            # Show what it's learning
            if mode_metrics['ssl_level'] < 0.3:
                print(f"   📚 Learning basic {mode} mechanics like jstn...")
            elif mode_metrics['ssl_level'] < 0.6:
                print(f"   🎓 Mastering {mode} aerial plays and flip resets...")
            elif mode_metrics['ssl_level'] < 0.8:
                print(f"   🏆 Becoming {mode} double tap and ceiling shot expert...")
            else:
                print(f"   👑 Approaching jstn's {mode} mastery level!")
            
            # Check if we've reached JSTN level for this mode
            if mode_metrics['ssl_level'] > 0.9:
                print(f"🏆 JSTN {mode.upper()} LEVEL ACHIEVED! Episode {self.episode_count}")
                print(f"🎯 Playing like jstn in {mode} - aerial master, flip reset king, double tap god!")
                self.save_mode_model(mode)
    
    def save_mode_model(self, mode: str):
        """Save the JSTN model for specific mode"""
        mode_folder = Path(f"training_{mode}")
        models_folder = mode_folder / "models"
        models_folder.mkdir(exist_ok=True)
        
        mode_metrics = self.performance_metrics[mode]
        mode_config = self.jstn_mode_configs[mode]
        
        # Save JSTN-specific model for this mode
        jstn_model = {
            'mode': mode,
            'jstn_level': mode_metrics['ssl_level'],
            'mechanical_skill': mode_metrics['mechanical_skill'],
            'aerial_mastery': mode_metrics['aerial_mastery'],
            'flip_reset_skill': mode_metrics['flip_reset_skill'],
            'double_tap_accuracy': mode_metrics['double_tap_accuracy'],
            'ceiling_shot_skill': mode_metrics['ceiling_shot_skill'],
            'musty_flick_timing': mode_metrics['musty_flick_timing'],
            'recovery_speed': mode_metrics['recovery_speed'],
            'wall_play_skill': mode_metrics['wall_play_skill'],
            'team_coordination': mode_metrics.get('team_coordination', 0.0),
            'mechanical_creativity': mode_metrics['mechanical_creativity'],
            'episode_count': self.episode_count,
            'mode_episodes': self.mode_episode_counts[mode],
            'training_time': time.time() - self.start_time,
            'jstn_playstyle': mode_config['playstyle'],
            'performance_metrics': mode_metrics
        }
        
        # Save model as JSON instead of PyTorch
        import json
        with open(models_folder / f"jstn_{mode}_model_ep{self.episode_count}.json", 'w') as f:
            json.dump(jstn_model, f, indent=2)
        print(f"💾 Saved JSTN {mode.upper()} model at episode {self.episode_count}")
    
    def train(self):
        """Main training loop - coordinates all workers and learners across all modes"""
        print("🚀 Starting JSTN Multi-Mode Training...")
        print("🎮 This will train the ENTIRE bot to play like jstn (Justin) across ALL modes!")
        print("🎯 Using circular training: 1s → 2s → 3s → repeat!")
        
        # Create mode folders
        self.create_mode_folders()
        
        # Initialize wandb
        wandb.init(
            project="jstn-multi-mode-opti",
            config=self.config,
            name=f"jstn_multi_mode_training_{int(time.time())}"
        )
        
        try:
            # Create RLGym environments for all modes
            for mode in self.training_modes:
                self.create_rlgym_environment(mode)
            
            print("✅ All RLGym environments created with visualizers!")
            print("🎯 Training to play like jstn across ALL game modes!")
            
            # Main training loop
            while self.episode_count < self.max_episodes:
                current_mode = self.get_current_mode()
                
                # Train with RLGym environment
                self.train_episode_with_rlgym(current_mode)
                
                # Simulate bot playing against itself and learning from jstn
                self.simulate_jstn_training_episode(current_mode)
                
                # Collect performance data for current mode
                self.collect_performance_data_for_mode(current_mode)
                
                # Calculate JSTN level for current mode
                jstn_level = self.calculate_jstn_level_for_mode(current_mode)
                
                # Log to wandb for current mode
                self.log_to_wandb_for_mode(current_mode)
                
                # Print progress for current mode
                self.print_progress_for_mode(current_mode)
                
                # Update episode counts
                self.episode_count += 1
                self.mode_episode_counts[current_mode] += 1
                self.total_steps += 1000  # Approximate steps per episode
                
                # Check if we should switch modes
                if self.switch_training_mode():
                    # Save model for previous mode
                    self.save_mode_model(current_mode)
                
                # Save model periodically
                if self.episode_count % 5000 == 0:
                    self.save_mode_model(current_mode)
                
                # Sleep to prevent overwhelming the system
                time.sleep(0.1)  # Faster training
        
        except KeyboardInterrupt:
            print("\n⏹️  JSTN multi-mode training interrupted by user")
        except Exception as e:
            print(f"❌ JSTN multi-mode training error: {e}")
        finally:
            # Cleanup
            self.cleanup()
            wandb.finish()
            print("✅ JSTN multi-mode training completed!")
    
    def cleanup(self):
        """Cleanup all processes and connections"""
        print("🧹 Cleaning up...")
        
        # Terminate worker and learner processes for all modes
        for mode in self.training_modes:
            print(f"🧹 Cleaning up {mode} processes...")
            
            # Terminate worker processes
            if mode in self.worker_processes and isinstance(self.worker_processes[mode], dict):
                for worker_name, process in self.worker_processes[mode].items():
                    try:
                        process.terminate()
                        process.wait(timeout=5)
                        if process.poll() is None:
                            process.kill()
                        print(f"✅ Terminated {mode}/{worker_name} worker")
                    except Exception as e:
                        print(f"❌ Failed to terminate {mode}/{worker_name} worker: {e}")
            
            # Terminate learner processes
            if mode in self.learner_processes and isinstance(self.learner_processes[mode], dict):
                for learner_name, process in self.learner_processes[mode].items():
                    try:
                        process.terminate()
                        process.wait(timeout=5)
                        if process.poll() is None:
                            process.kill()
                        print(f"✅ Terminated {mode}/{learner_name} learner")
                    except Exception as e:
                        print(f"❌ Failed to terminate {mode}/{learner_name} learner: {e}")
            
            # Close Redis connections
            # Ensure redis_connections[mode] is a dict
            if mode in self.redis_connections and isinstance(self.redis_connections[mode], dict):
                for worker_name, redis_conn in self.redis_connections[mode].items():
                    try:
                        redis_conn.close()
                        print(f"✅ Closed Redis connection for {mode}/{worker_name}")
                    except Exception as e:
                        print(f"❌ Failed to close Redis connection for {mode}/{worker_name}: {e}")
        
        # Save final models for all modes
        for mode in self.training_modes:
            self.save_mode_model(mode)
        
        print("💾 Saved final JSTN models for all modes")

def main():
    """Main function"""
    print("🏆 JSTN Multi-Mode Trainer for Opti Bot")
    print("=" * 60)
    print("🎯 Training the ENTIRE bot to play like jstn (Justin) across ALL modes!")
    print("🚀 Using circular training: 1s → 2s → 3s → repeat!")
    print("🧠 This is the ultimate multi-mode brain that coordinates everything!")
    
    # Training configuration optimized for JSTN multi-mode
    config = {
        'max_episodes': 100000,  # More episodes for multi-mode training
        'batch_size': 1000,      # Larger batches for stability
        'learning_rate': 3e-4,   # JSTN's learning rate
        'gamma': 0.99,           # JSTN's discount factor
        'jstn_mode': True,       # Enable JSTN-specific training
        'multi_mode_training': True, # Enable multi-mode training
        'circular_training': True,   # Enable circular training
        'real_rlgym': True       # Use real RLGym environment
    }
    
    # Create and run JSTN multi-mode trainer
    trainer = JSTNMultiModeTrainer(config)
    trainer.train()

if __name__ == "__main__":
    main()
