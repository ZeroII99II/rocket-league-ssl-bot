#!/usr/bin/env python3
"""
JSTN Complete Trainer - The Ultimate Rocket League AI
Uses ALL available workers and mechanics to create a bot that plays like jstn (Justin)
This is the main brain that coordinates all specialized workers into one unified system
"""

import os
import sys
import time
import torch
import numpy as np
import wandb
import redis
import threading
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional
import json
import queue
import multiprocessing as mp

# Add rocket-learn to path
sys.path.append(str(Path(__file__).parent / "rocket-learn-master"))

# Import all our modern components
from ModernObsBuilder import ModernObsBuilder
from ModernActionParser import ModernActionParser
from ModernRewardSystem import ModernRewardSystem
from ModernAgent import ModernAgent, ModernSelector
from SSLMechanics import SSLMechanics

# Import all specialized workers and learners
from worker_selector import worker_selector_main
from worker_dtap import worker_dtap_main
from worker_flip_reset import worker_flip_reset_main
from worker_aerial import worker_aerial_main
from worker_flick import worker_flick_main
from worker_ceil_pinch import worker_ceil_pinch_main
from worker_pinch import worker_pinch_main
from worker_wall import worker_wall_main
from worker_walldash import worker_walldash_main
from worker_recovery import worker_recovery_main
from worker_demo import worker_demo_main
from worker_gp import worker_gp_main
from worker_half_flip import worker_half_flip_main
from worker_lix import worker_lix_main
from worker_kickoff import worker_kickoff_main

# Import all learners
from learner_selector import learner_selector_main
from learner_dtap import learner_dtap_main
from learner_flip_reset import learner_flip_reset_main
from learner_aerial import learner_aerial_main
from learner_flick import learner_flick_main
from learner_ceil_pinch import learner_ceil_pinch_main
from learner_pinch import learner_pinch_main
from learner_wall import learner_wall_main
from learner_walldash import learner_walldash_main
from learner_recovery import learner_recovery_main
from learner_demo import learner_demo_main
from learner_gp import learner_gp_main
from learner_half_flip import learner_half_flip_main
from learner_lix import learner_lix_main
from learner_kickoff import learner_kickoff_main

# Import constants
from Constants_selector import FRAME_SKIP as SELECTOR_FRAME_SKIP, DB_NUM as SELECTOR_DB_NUM
from Constants_dtap import FRAME_SKIP as DTAP_FRAME_SKIP, DB_NUM as DTAP_DB_NUM
from Constants_flip_reset import FRAME_SKIP as FLIP_RESET_FRAME_SKIP, DB_NUM as FLIP_RESET_DB_NUM
from Constants_aerial import FRAME_SKIP as AERIAL_FRAME_SKIP, DB_NUM as AERIAL_DB_NUM
from Constants_flick import FRAME_SKIP as FLICK_FRAME_SKIP, DB_NUM as FLICK_DB_NUM
from Constants_ceil_pinch import FRAME_SKIP as CEIL_PINCH_FRAME_SKIP, DB_NUM as CEIL_PINCH_DB_NUM
from Constants_pinch import FRAME_SKIP as PINCH_FRAME_SKIP, DB_NUM as PINCH_DB_NUM
from Constants_wall import FRAME_SKIP as WALL_FRAME_SKIP, DB_NUM as WALL_DB_NUM
from Constants_walldash import FRAME_SKIP as WALLDASH_FRAME_SKIP, DB_NUM as WALLDASH_DB_NUM
from Constants_recovery import FRAME_SKIP as RECOVERY_FRAME_SKIP, DB_NUM as RECOVERY_DB_NUM
from Constants_demo import FRAME_SKIP as DEMO_FRAME_SKIP, DB_NUM as DEMO_DB_NUM
from Constants_gp import FRAME_SKIP as GP_FRAME_SKIP, DB_NUM as GP_DB_NUM
from Constants_half_flip import FRAME_SKIP as HALF_FLIP_FRAME_SKIP, DB_NUM as HALF_FLIP_DB_NUM
from Constants_lix import FRAME_SKIP as LIX_FRAME_SKIP, DB_NUM as LIX_DB_NUM
from Constants_kickoff import FRAME_SKIP as KICKOFF_FRAME_SKIP, DB_NUM as KICKOFF_DB_NUM

class JSTNCompleteTrainer:
    """
    The Ultimate JSTN Trainer - Coordinates ALL workers and mechanics
    This is the main brain that makes the bot play like jstn (Justin)
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.device = torch.device('cpu')  # Force CPU for compatibility
        
        # JSTN-specific configuration
        self.jstn_playstyle = {
            'aerial_aggression': 0.9,      # jstn's signature aerial play
            'flip_reset_mastery': 0.95,    # jstn's flip reset expertise
            'double_tap_precision': 0.9,   # jstn's double tap accuracy
            'ceiling_shot_skill': 0.85,    # jstn's ceiling play
            'musty_flick_timing': 0.8,     # jstn's creative mechanics
            'speed_control': 0.9,          # jstn's speed management
            'boost_efficiency': 0.85,      # jstn's boost usage
            'recovery_speed': 0.9,         # jstn's quick recoveries
            'wall_play': 0.8,              # jstn's wall mechanics
            'team_play': 0.7,              # jstn's team coordination
            'mechanical_creativity': 0.95  # jstn's innovative plays
        }
        
        # Training configuration
        self.max_episodes = self.config.get('max_episodes', 50000)
        self.batch_size = self.config.get('batch_size', 1000)
        self.learning_rate = self.config.get('learning_rate', 3e-4)
        self.gamma = self.config.get('gamma', 0.99)
        
        # Worker configuration
        self.workers = {
            'selector': {'db': SELECTOR_DB_NUM, 'frame_skip': SELECTOR_FRAME_SKIP, 'priority': 1.0},
            'dtap': {'db': DTAP_DB_NUM, 'frame_skip': DTAP_FRAME_SKIP, 'priority': 0.9},
            'flip_reset': {'db': FLIP_RESET_DB_NUM, 'frame_skip': FLIP_RESET_FRAME_SKIP, 'priority': 0.95},
            'aerial': {'db': AERIAL_DB_NUM, 'frame_skip': AERIAL_FRAME_SKIP, 'priority': 0.9},
            'flick': {'db': FLICK_DB_NUM, 'frame_skip': FLICK_FRAME_SKIP, 'priority': 0.8},
            'ceil_pinch': {'db': CEIL_PINCH_DB_NUM, 'frame_skip': CEIL_PINCH_FRAME_SKIP, 'priority': 0.85},
            'pinch': {'db': PINCH_DB_NUM, 'frame_skip': PINCH_FRAME_SKIP, 'priority': 0.8},
            'wall': {'db': WALL_DB_NUM, 'frame_skip': WALL_FRAME_SKIP, 'priority': 0.8},
            'walldash': {'db': WALLDASH_DB_NUM, 'frame_skip': WALLDASH_FRAME_SKIP, 'priority': 0.75},
            'recovery': {'db': RECOVERY_DB_NUM, 'frame_skip': RECOVERY_FRAME_SKIP, 'priority': 0.9},
            'demo': {'db': DEMO_DB_NUM, 'frame_skip': DEMO_FRAME_SKIP, 'priority': 0.6},
            'gp': {'db': GP_DB_NUM, 'frame_skip': GP_FRAME_SKIP, 'priority': 0.7},
            'half_flip': {'db': HALF_FLIP_DB_NUM, 'frame_skip': HALF_FLIP_FRAME_SKIP, 'priority': 0.7},
            'lix': {'db': LIX_DB_NUM, 'frame_skip': LIX_FRAME_SKIP, 'priority': 0.8},
            'kickoff': {'db': KICKOFF_DB_NUM, 'frame_skip': KICKOFF_FRAME_SKIP, 'priority': 0.8}
        }
        
        # SSL Mechanics system
        self.ssl_mechanics = SSLMechanics()
        
        # Training state
        self.episode_count = 0
        self.total_steps = 0
        self.start_time = time.time()
        self.best_reward = -float('inf')
        
        # Performance tracking
        self.performance_metrics = {
            'episode_rewards': [],
            'episode_lengths': [],
            'jstn_mechanics': {},
            'worker_performance': {},
            'ssl_level': 0.0,
            'mechanical_skill': 0.0,
            'aerial_mastery': 0.0,
            'flip_reset_skill': 0.0,
            'double_tap_accuracy': 0.0,
            'ceiling_shot_skill': 0.0,
            'musty_flick_timing': 0.0,
            'recovery_speed': 0.0,
            'wall_play_skill': 0.0,
            'team_coordination': 0.0
        }
        
        # Worker processes
        self.worker_processes = {}
        self.learner_processes = {}
        
        # Redis connections
        self.redis_connections = {}
        
        print("🏆 JSTN Complete Trainer initialized")
        print("🎯 Training to play like jstn (Justin) - the legendary pro!")
        print("🚀 Using ALL available workers and mechanics")
        print(f"📊 Workers: {len(self.workers)}")
        print(f"🧠 SSL Mechanics: {len(self.ssl_mechanics.mechanics)}")
    
    def setup_redis_connections(self):
        """Setup Redis connections for all workers"""
        print("🔗 Setting up Redis connections...")
        
        for worker_name, config in self.workers.items():
            try:
                redis_conn = redis.Redis(
                    host='localhost',
                    port=6379,
                    db=config['db'],
                    decode_responses=True
                )
                # Test connection
                redis_conn.ping()
                self.redis_connections[worker_name] = redis_conn
                print(f"✅ Redis connection for {worker_name} (DB {config['db']})")
            except Exception as e:
                print(f"❌ Failed to connect to Redis for {worker_name}: {e}")
    
    def start_workers(self):
        """Start all worker processes"""
        print("🚀 Starting all worker processes...")
        
        worker_functions = {
            'selector': worker_selector_main,
            'dtap': worker_dtap_main,
            'flip_reset': worker_flip_reset_main,
            'aerial': worker_aerial_main,
            'flick': worker_flick_main,
            'ceil_pinch': worker_ceil_pinch_main,
            'pinch': worker_pinch_main,
            'wall': worker_wall_main,
            'walldash': worker_walldash_main,
            'recovery': worker_recovery_main,
            'demo': worker_demo_main,
            'gp': worker_gp_main,
            'half_flip': worker_half_flip_main,
            'lix': worker_lix_main,
            'kickoff': worker_kickoff_main
        }
        
        for worker_name, worker_func in worker_functions.items():
            try:
                # Start worker process
                process = mp.Process(target=worker_func, name=f"worker_{worker_name}")
                process.start()
                self.worker_processes[worker_name] = process
                print(f"✅ Started {worker_name} worker (PID: {process.pid})")
                
                # Small delay between starting workers
                time.sleep(0.5)
                
            except Exception as e:
                print(f"❌ Failed to start {worker_name} worker: {e}")
    
    def start_learners(self):
        """Start all learner processes"""
        print("🧠 Starting all learner processes...")
        
        learner_functions = {
            'selector': learner_selector_main,
            'dtap': learner_dtap_main,
            'flip_reset': learner_flip_reset_main,
            'aerial': learner_aerial_main,
            'flick': learner_flick_main,
            'ceil_pinch': learner_ceil_pinch_main,
            'pinch': learner_pinch_main,
            'wall': learner_wall_main,
            'walldash': learner_walldash_main,
            'recovery': learner_recovery_main,
            'demo': learner_demo_main,
            'gp': learner_gp_main,
            'half_flip': learner_half_flip_main,
            'lix': learner_lix_main,
            'kickoff': learner_kickoff_main
        }
        
        for learner_name, learner_func in learner_functions.items():
            try:
                # Start learner process
                process = mp.Process(target=learner_func, name=f"learner_{learner_name}")
                process.start()
                self.learner_processes[learner_name] = process
                print(f"✅ Started {learner_name} learner (PID: {process.pid})")
                
                # Small delay between starting learners
                time.sleep(0.5)
                
            except Exception as e:
                print(f"❌ Failed to start {learner_name} learner: {e}")
    
    def monitor_workers(self):
        """Monitor worker and learner processes"""
        print("👀 Monitoring worker and learner processes...")
        
        while True:
            # Check worker processes
            for worker_name, process in self.worker_processes.items():
                if not process.is_alive():
                    print(f"⚠️  Worker {worker_name} died, restarting...")
                    try:
                        # Restart worker
                        worker_func = globals()[f"worker_{worker_name}_main"]
                        new_process = mp.Process(target=worker_func, name=f"worker_{worker_name}")
                        new_process.start()
                        self.worker_processes[worker_name] = new_process
                        print(f"✅ Restarted {worker_name} worker (PID: {new_process.pid})")
                    except Exception as e:
                        print(f"❌ Failed to restart {worker_name} worker: {e}")
            
            # Check learner processes
            for learner_name, process in self.learner_processes.items():
                if not process.is_alive():
                    print(f"⚠️  Learner {learner_name} died, restarting...")
                    try:
                        # Restart learner
                        learner_func = globals()[f"learner_{learner_name}_main"]
                        new_process = mp.Process(target=learner_func, name=f"learner_{learner_name}")
                        new_process.start()
                        self.learner_processes[learner_name] = new_process
                        print(f"✅ Restarted {learner_name} learner (PID: {new_process.pid})")
                    except Exception as e:
                        print(f"❌ Failed to restart {learner_name} learner: {e}")
            
            # Sleep before next check
            time.sleep(10)
    
    def collect_performance_data(self):
        """Collect performance data from all workers"""
        print("📊 Collecting performance data from all workers...")
        
        for worker_name, redis_conn in self.redis_connections.items():
            try:
                # Get worker stats
                stats = redis_conn.hgetall(f"worker_stats_{worker_name}")
                if stats:
                    self.performance_metrics['worker_performance'][worker_name] = stats
                
                # Get JSTN-specific metrics
                jstn_metrics = redis_conn.hgetall(f"jstn_metrics_{worker_name}")
                if jstn_metrics:
                    self.performance_metrics['jstn_mechanics'][worker_name] = jstn_metrics
                
            except Exception as e:
                print(f"❌ Failed to collect data from {worker_name}: {e}")
    
    def calculate_jstn_level(self):
        """Calculate overall JSTN skill level"""
        print("🎯 Calculating JSTN skill level...")
        
        # JSTN-specific skill calculations
        aerial_skill = self.performance_metrics.get('aerial_mastery', 0.0)
        flip_reset_skill = self.performance_metrics.get('flip_reset_skill', 0.0)
        double_tap_skill = self.performance_metrics.get('double_tap_accuracy', 0.0)
        ceiling_skill = self.performance_metrics.get('ceiling_shot_skill', 0.0)
        musty_skill = self.performance_metrics.get('musty_flick_timing', 0.0)
        recovery_skill = self.performance_metrics.get('recovery_speed', 0.0)
        wall_skill = self.performance_metrics.get('wall_play_skill', 0.0)
        team_skill = self.performance_metrics.get('team_coordination', 0.0)
        
        # Weighted average based on jstn's playstyle
        jstn_weights = {
            'aerial': 0.25,      # jstn's signature
            'flip_reset': 0.20,  # jstn's mastery
            'double_tap': 0.15,  # jstn's precision
            'ceiling': 0.10,     # jstn's creativity
            'musty': 0.10,       # jstn's innovation
            'recovery': 0.10,    # jstn's speed
            'wall': 0.05,        # jstn's versatility
            'team': 0.05         # jstn's coordination
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
        
        self.performance_metrics['ssl_level'] = jstn_level
        self.performance_metrics['mechanical_skill'] = jstn_level
        
        return jstn_level
    
    def log_to_wandb(self):
        """Log metrics to wandb"""
        if self.episode_count % 100 == 0:  # Log every 100 episodes
            wandb.log({
                'episode': self.episode_count,
                'jstn_level': self.performance_metrics['ssl_level'],
                'mechanical_skill': self.performance_metrics['mechanical_skill'],
                'aerial_mastery': self.performance_metrics['aerial_mastery'],
                'flip_reset_skill': self.performance_metrics['flip_reset_skill'],
                'double_tap_accuracy': self.performance_metrics['double_tap_accuracy'],
                'ceiling_shot_skill': self.performance_metrics['ceiling_shot_skill'],
                'musty_flick_timing': self.performance_metrics['musty_flick_timing'],
                'recovery_speed': self.performance_metrics['recovery_speed'],
                'wall_play_skill': self.performance_metrics['wall_play_skill'],
                'team_coordination': self.performance_metrics['team_coordination'],
                'training_time': time.time() - self.start_time,
                'total_steps': self.total_steps
            })
    
    def print_progress(self):
        """Print training progress"""
        if self.episode_count % 1000 == 0:
            elapsed_time = time.time() - self.start_time
            episodes_per_second = self.episode_count / elapsed_time if elapsed_time > 0 else 0
            
            print(f"📈 Episode {self.episode_count} | "
                  f"JSTN Level: {self.performance_metrics['ssl_level']:.3f} | "
                  f"Mechanical Skill: {self.performance_metrics['mechanical_skill']:.3f} | "
                  f"Aerial: {self.performance_metrics['aerial_mastery']:.3f} | "
                  f"Flip Reset: {self.performance_metrics['flip_reset_skill']:.3f} | "
                  f"Double Tap: {self.performance_metrics['double_tap_accuracy']:.3f} | "
                  f"Episodes/sec: {episodes_per_second:.2f}")
            
            # Check if we've reached JSTN level
            if self.performance_metrics['ssl_level'] > 0.9:
                print(f"🏆 JSTN LEVEL ACHIEVED! Episode {self.episode_count}")
                print("🎯 Playing like jstn - aerial master, flip reset king, double tap god!")
                self.save_jstn_model()
    
    def save_jstn_model(self):
        """Save the JSTN model"""
        model_path = Path("models")
        model_path.mkdir(exist_ok=True)
        
        # Save JSTN-specific model
        jstn_model = {
            'jstn_level': self.performance_metrics['ssl_level'],
            'mechanical_skill': self.performance_metrics['mechanical_skill'],
            'aerial_mastery': self.performance_metrics['aerial_mastery'],
            'flip_reset_skill': self.performance_metrics['flip_reset_skill'],
            'double_tap_accuracy': self.performance_metrics['double_tap_accuracy'],
            'ceiling_shot_skill': self.performance_metrics['ceiling_shot_skill'],
            'musty_flick_timing': self.performance_metrics['musty_flick_timing'],
            'recovery_speed': self.performance_metrics['recovery_speed'],
            'wall_play_skill': self.performance_metrics['wall_play_skill'],
            'team_coordination': self.performance_metrics['team_coordination'],
            'episode_count': self.episode_count,
            'training_time': time.time() - self.start_time,
            'jstn_playstyle': self.jstn_playstyle,
            'performance_metrics': self.performance_metrics
        }
        
        torch.save(jstn_model, model_path / f"jstn_complete_model_ep{self.episode_count}.pt")
        print(f"💾 Saved JSTN model at episode {self.episode_count}")
    
    def train(self):
        """Main training loop - coordinates all workers and learners"""
        print("🚀 Starting JSTN Complete Training...")
        print("🎮 This will train the ENTIRE bot to play like jstn (Justin)!")
        print("🎯 Using ALL available workers and mechanics!")
        
        # Initialize wandb
        wandb.init(
            project="jstn-complete-opti",
            config=self.config,
            name=f"jstn_complete_training_{int(time.time())}"
        )
        
        try:
            # Setup Redis connections
            self.setup_redis_connections()
            
            # Start all workers
            self.start_workers()
            
            # Start all learners
            self.start_learners()
            
            # Start monitoring thread
            monitor_thread = threading.Thread(target=self.monitor_workers, daemon=True)
            monitor_thread.start()
            
            print("✅ All workers and learners started!")
            print("🎯 Training to play like jstn - the legendary pro!")
            
            # Main training loop
            while self.episode_count < self.max_episodes:
                # Collect performance data
                self.collect_performance_data()
                
                # Calculate JSTN level
                jstn_level = self.calculate_jstn_level()
                
                # Log to wandb
                self.log_to_wandb()
                
                # Print progress
                self.print_progress()
                
                # Update episode count
                self.episode_count += 1
                self.total_steps += 1000  # Approximate steps per episode
                
                # Save model periodically
                if self.episode_count % 5000 == 0:
                    self.save_jstn_model()
                
                # Sleep to prevent overwhelming the system
                time.sleep(1)
        
        except KeyboardInterrupt:
            print("\n⏹️  JSTN training interrupted by user")
        except Exception as e:
            print(f"❌ JSTN training error: {e}")
        finally:
            # Cleanup
            self.cleanup()
            wandb.finish()
            print("✅ JSTN training completed!")
    
    def cleanup(self):
        """Cleanup all processes and connections"""
        print("🧹 Cleaning up...")
        
        # Terminate worker processes
        for worker_name, process in self.worker_processes.items():
            try:
                process.terminate()
                process.join(timeout=5)
                if process.is_alive():
                    process.kill()
                print(f"✅ Terminated {worker_name} worker")
            except Exception as e:
                print(f"❌ Failed to terminate {worker_name} worker: {e}")
        
        # Terminate learner processes
        for learner_name, process in self.learner_processes.items():
            try:
                process.terminate()
                process.join(timeout=5)
                if process.is_alive():
                    process.kill()
                print(f"✅ Terminated {learner_name} learner")
            except Exception as e:
                print(f"❌ Failed to terminate {learner_name} learner: {e}")
        
        # Close Redis connections
        for worker_name, redis_conn in self.redis_connections.items():
            try:
                redis_conn.close()
                print(f"✅ Closed Redis connection for {worker_name}")
            except Exception as e:
                print(f"❌ Failed to close Redis connection for {worker_name}: {e}")
        
        # Save final model
        self.save_jstn_model()
        print("💾 Saved final JSTN model")

def main():
    """Main function"""
    print("🏆 JSTN Complete Trainer for Opti Bot")
    print("=" * 60)
    print("🎯 Training the ENTIRE bot to play like jstn (Justin)!")
    print("🚀 Using ALL available workers and mechanics!")
    print("🧠 This is the main brain that coordinates everything!")
    
    # Training configuration optimized for JSTN
    config = {
        'max_episodes': 50000,  # More episodes for JSTN's complexity
        'batch_size': 1000,     # Larger batches for stability
        'learning_rate': 3e-4,  # JSTN's learning rate
        'gamma': 0.99,          # JSTN's discount factor
        'jstn_mode': True,      # Enable JSTN-specific training
        'use_all_workers': True, # Use all available workers
        'ssl_mechanics': True,   # Enable SSL mechanics
        'multi_mode_training': True, # Enable multi-mode training
        'real_rlgym': True      # Use real RLGym environment
    }
    
    # Create and run JSTN trainer
    trainer = JSTNCompleteTrainer(config)
    trainer.train()

if __name__ == "__main__":
    main()
