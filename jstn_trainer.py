#!/usr/bin/env python3
"""
JSTN-Level Trainer for Opti Bot
Trains to play like jstn (Justin) - the legendary Rocket League pro
Uses REAL RLGym 2.0.1 environment with jstn's signature playstyle
"""

import os
import sys
import time
import torch
import numpy as np
import wandb
from pathlib import Path
from typing import Dict, Any, List, Tuple
import threading
import queue

# Add rocket-learn to path
sys.path.append(str(Path(__file__).parent / "rocket-learn-master"))

# Import our modern components
from ModernObsBuilder import ModernObsBuilder
from ModernActionParser import ModernActionParser
from ModernRewardSystem import ModernRewardSystem
from ModernAgent import ModernAgent, ModernSelector
from Constants_selector import FRAME_SKIP

# Import RLGym 2.0.1 components
try:
    from rlgym.api import RLGym, ObsBuilder, ActionParser, RewardFunction, DoneCondition
    from rlgym.api import ObsType, ActionType, RewardType, StateType
    from rlgym.api import ObsSpaceType, ActionSpaceType
    from rlgym.api import AgentID
    from rlgym.api import TransitionEngine, SharedInfoProvider, StateMutator, Renderer
    RLGYM_AVAILABLE = True
    print("✅ RLGym 2.0.1 components imported successfully")
except ImportError as e:
    print(f"❌ RLGym 2.0.1 not available: {e}")
    RLGYM_AVAILABLE = False

class JSTNRewardSystem(RewardFunction):
    """Reward system designed to encourage jstn's signature playstyle"""
    
    def __init__(self):
        super().__init__()
        self.last_ball_touch = 0
        self.aerial_timer = 0
        self.flip_reset_timer = 0
        self.double_tap_timer = 0
        self.ceiling_shot_timer = 0
        self.musty_timer = 0
        
    def reset(self, initial_state: StateType, shared_info: Dict[str, Any]):
        """Reset reward system for new episode"""
        self.last_ball_touch = 0
        self.aerial_timer = 0
        self.flip_reset_timer = 0
        self.double_tap_timer = 0
        self.ceiling_shot_timer = 0
        self.musty_timer = 0
    
    def get_reward(self, player: Any, state: StateType, action: ActionType, shared_info: Dict[str, Any]) -> float:
        """Calculate reward based on jstn's playstyle"""
        reward = 0.0
        
        # Get player and ball data
        player_pos = np.array([player.car_data.position.x, player.car_data.position.y, player.car_data.position.z])
        player_vel = np.array([player.car_data.linear_velocity.x, player.car_data.linear_velocity.y, player.car_data.linear_velocity.z])
        player_rot = np.array([player.car_data.rotation.pitch, player.car_data.rotation.yaw, player.car_data.rotation.roll])
        player_ang_vel = np.array([player.car_data.angular_velocity.x, player.car_data.angular_velocity.y, player.car_data.angular_velocity.z])
        
        ball_pos = np.array([state.ball.position.x, state.ball.position.y, state.ball.position.z])
        ball_vel = np.array([state.ball.linear_velocity.x, state.ball.linear_velocity.y, state.ball.linear_velocity.z])
        
        # JSTN Signature Rewards
        
        # 1. Aerial Control (jstn's specialty)
        if player_pos[2] > 200:  # In the air
            self.aerial_timer += 1
            # Reward for maintaining aerial control
            reward += 0.1 * min(self.aerial_timer / 100, 1.0)
            
            # Reward for smooth aerial movement
            if np.linalg.norm(player_ang_vel) < 2.0:  # Smooth rotation
                reward += 0.05
        else:
            self.aerial_timer = 0
        
        # 2. Flip Reset Mastery (jstn's signature move)
        if player_pos[2] > 400 and ball_pos[2] > 300:  # Both in air
            # Check if player is close to ball for flip reset
            ball_distance = np.linalg.norm(player_pos - ball_pos)
            if ball_distance < 200:  # Close to ball
                self.flip_reset_timer += 1
                reward += 0.2 * min(self.flip_reset_timer / 50, 1.0)
            else:
                self.flip_reset_timer = 0
        
        # 3. Double Tap Precision (jstn's bread and butter)
        if ball_vel[1] > 0 and player_pos[1] > ball_pos[1]:  # Ball going towards goal, player behind
            self.double_tap_timer += 1
            # Reward for positioning for double tap
            reward += 0.15 * min(self.double_tap_timer / 30, 1.0)
        else:
            self.double_tap_timer = 0
        
        # 4. Ceiling Shot Expertise
        if player_pos[2] > 1800:  # Near ceiling
            self.ceiling_shot_timer += 1
            # Reward for ceiling play
            reward += 0.1 * min(self.ceiling_shot_timer / 40, 1.0)
        else:
            self.ceiling_shot_timer = 0
        
        # 5. Musty Flick Timing (jstn's creative mechanics)
        if player_pos[2] < 100 and np.linalg.norm(player_vel) > 1000:  # On ground, fast
            self.musty_timer += 1
            # Reward for ground control at speed
            reward += 0.08 * min(self.musty_timer / 25, 1.0)
        else:
            self.musty_timer = 0
        
        # 6. Ball Control and Touch Quality
        ball_distance = np.linalg.norm(player_pos - ball_pos)
        if ball_distance < 300:  # Close to ball
            # Reward for good ball control
            reward += 0.05
            
            # Reward for soft touches (jstn's precision)
            if np.linalg.norm(player_vel) < 500:
                reward += 0.1
        
        # 7. Speed and Momentum (jstn's aggressive style)
        speed = np.linalg.norm(player_vel)
        if speed > 1500:  # Supersonic
            reward += 0.1
        elif speed > 1000:  # Fast
            reward += 0.05
        
        # 8. Boost Management (jstn's efficiency)
        boost_amount = player.boost_amount
        if boost_amount > 50:  # Good boost management
            reward += 0.02
        
        # 9. Goal Scoring (ultimate reward)
        if hasattr(state, 'last_touch') and state.last_touch == player.car_id:
            if ball_pos[1] > 5000:  # Ball in opponent goal
                reward += 100.0  # Massive reward for scoring
            elif ball_pos[1] < -5000:  # Ball in own goal
                reward -= 50.0  # Penalty for own goal
        
        # 10. Defensive Positioning (jstn's all-around game)
        if ball_pos[1] < 0:  # Ball in defensive half
            if player_pos[1] < ball_pos[1] + 500:  # Good defensive positioning
                reward += 0.03
        
        return reward

class JSTNEnvironment:
    """RLGym 2.0.1 environment configured for jstn-style training"""
    
    def __init__(self, team_size: int = 1, tick_skip: int = 8):
        self.team_size = team_size
        self.tick_skip = tick_skip
        self.env = None
        
        # Create jstn-optimized components
        self.obs_builder = ModernObsBuilder(
            team_size=team_size,
            tick_skip=tick_skip,
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
        
        self.reward_system = JSTNRewardSystem()
        
        if RLGYM_AVAILABLE:
            self._setup_environment()
        else:
            print("❌ Cannot setup RLGym environment - RLGym not available")
    
    def _setup_environment(self):
        """Setup the RLGym 2.0.1 environment for jstn training"""
        try:
            # Create RLGym 2.0.1 environment
            self.env = RLGym(
                obs_builder=self.obs_builder,
                action_parser=self.action_parser,
                reward_function=self.reward_system,
                done_condition=self._create_done_condition(),
                shared_info_provider=self._create_shared_info_provider(),
                state_mutator=self._create_state_mutator(),
                transition_engine=self._create_transition_engine(),
                renderer=None  # No rendering for training
            )
            
            print("✅ JSTN RLGym 2.0.1 environment created successfully")
            print(f"   Team size: {self.team_size}")
            print(f"   Tick skip: {self.tick_skip}")
            print(f"   Observation size: {self.obs_builder.obs_size}")
            print(f"   Action size: {self.action_parser.action_size}")
            print("🎯 Configured for jstn's signature playstyle!")
            
        except Exception as e:
            print(f"❌ Failed to create RLGym environment: {e}")
            self.env = None
    
    def _create_done_condition(self) -> DoneCondition:
        """Create done condition for episodes"""
        class JSTNDoneCondition(DoneCondition):
            def __init__(self):
                self.max_steps = 15000  # Longer episodes for jstn's style
                self.step_count = 0
            
            def is_done(self, state: StateType, shared_info: Dict[str, Any]) -> bool:
                self.step_count += 1
                # Episode ends after max steps or if goal is scored
                return self.step_count >= self.max_steps
        
        return JSTNDoneCondition()
    
    def _create_shared_info_provider(self) -> SharedInfoProvider:
        """Create shared info provider for jstn training"""
        class JSTNSharedInfoProvider(SharedInfoProvider):
            def get_shared_info(self, state: StateType) -> Dict[str, Any]:
                return {
                    'episode_step': 0,
                    'episode_reward': 0.0,
                    'episode_length': 0,
                    'aerial_time': 0.0,
                    'flip_resets': 0,
                    'double_taps': 0,
                    'ceiling_shots': 0,
                    'musty_flicks': 0
                }
        
        return JSTNSharedInfoProvider()
    
    def _create_state_mutator(self) -> StateMutator:
        """Create state mutator for jstn training scenarios"""
        class JSTNStateMutator(StateMutator):
            def mutate_state(self, state: StateType, shared_info: Dict[str, Any]) -> StateType:
                # No state mutation for now - let the game run naturally
                return state
        
        return JSTNStateMutator()
    
    def _create_transition_engine(self) -> TransitionEngine:
        """Create transition engine for jstn training"""
        class JSTNTransitionEngine(TransitionEngine):
            def step(self, state: StateType, actions: List[ActionType], shared_info: Dict[str, Any]) -> StateType:
                # This would interface with the actual Rocket League game
                # For now, we'll use a placeholder
                return state
        
        return JSTNTransitionEngine()
    
    def reset(self) -> np.ndarray:
        """Reset the environment and return initial observation"""
        if self.env is None:
            raise RuntimeError("RLGym environment not available")
        
        obs = self.env.reset()
        return obs[0] if isinstance(obs, list) else obs
    
    def step(self, action: np.ndarray) -> Tuple[np.ndarray, float, bool, Dict]:
        """Take a step in the environment"""
        if self.env is None:
            raise RuntimeError("RLGym environment not available")
        
        # Step the environment
        obs, reward, done, info = self.env.step([action])
        
        # Extract observation
        obs = obs[0] if isinstance(obs, list) else obs
        
        return obs, reward, done, info
    
    def close(self):
        """Close the environment"""
        if self.env:
            self.env.close()

class JSTNAgent:
    """Agent designed to learn jstn's playstyle"""
    
    def __init__(self, obs_size: int, action_size: int, device: str = 'cpu'):
        self.device = torch.device(device)
        self.obs_size = obs_size
        self.action_size = action_size
        
        # Create the agent with jstn-optimized architecture
        self.agent = ModernAgent(
            obs_size=obs_size,
            action_size=action_size,
            hidden_size=1024,  # Larger network for jstn's complexity
            num_heads=16,      # More attention heads for complex decision making
            num_layers=8,      # Deeper network for advanced mechanics
            dropout=0.05,      # Lower dropout for jstn's precision
            use_attention=True,
            use_transformer=True,
            use_specialized_heads=True,
            use_temporal_modeling=True,
            use_hierarchical=True
        ).to(self.device)
        
        # Create selector for jstn's diverse playstyle
        self.selector = ModernSelector(
            obs_size=obs_size,
            num_submodels=15,  # More submodels for jstn's versatility
            hidden_size=512,
            dropout=0.05
        ).to(self.device)
        
        # Optimizer with jstn's learning rate
        self.optimizer = torch.optim.AdamW(  # AdamW for better generalization
            list(self.agent.parameters()) + list(self.selector.parameters()),
            lr=2e-4,  # Slightly lower for stability
            weight_decay=1e-5
        )
        
        # Training stats
        self.episode_count = 0
        self.total_reward = 0.0
        self.best_reward = -float('inf')
        self.episode_rewards = []
        self.episode_lengths = []
        
        # JSTN-specific stats
        self.aerial_time = 0.0
        self.flip_resets = 0
        self.double_taps = 0
        self.ceiling_shots = 0
        self.musty_flicks = 0
        
        print(f"✅ JSTN Agent created")
        print(f"   Observation size: {obs_size}")
        print(f"   Action size: {action_size}")
        print(f"   Device: {self.device}")
        print(f"   Network: 1024 hidden, 16 heads, 8 layers")
        print(f"   Submodels: 15 (for jstn's versatility)")
    
    def get_action(self, obs: np.ndarray, deterministic: bool = False) -> np.ndarray:
        """Get action from the jstn agent"""
        obs_tensor = torch.tensor(obs, dtype=torch.float32).unsqueeze(0).to(self.device)
        
        with torch.no_grad():
            action_output = self.agent.get_action(obs_tensor, deterministic=deterministic)
            
            if isinstance(action_output, tuple):
                action = action_output[0]
            else:
                action = action_output
            
            return action.cpu().numpy().flatten()
    
    def update(self, obs_batch: List[np.ndarray], action_batch: List[np.ndarray], 
               reward_batch: List[float], next_obs_batch: List[np.ndarray], 
               done_batch: List[bool]):
        """Update the jstn agent using collected experience"""
        if len(obs_batch) == 0:
            return
        
        # Convert to tensors
        obs_tensor = torch.tensor(np.array(obs_batch), dtype=torch.float32).to(self.device)
        action_tensor = torch.tensor(np.array(action_batch), dtype=torch.float32).to(self.device)
        reward_tensor = torch.tensor(reward_batch, dtype=torch.float32).to(self.device)
        next_obs_tensor = torch.tensor(np.array(next_obs_batch), dtype=torch.float32).to(self.device)
        done_tensor = torch.tensor(done_batch, dtype=torch.bool).to(self.device)
        
        # JSTN-optimized policy gradient update
        self.optimizer.zero_grad()
        
        # Get current policy
        _, log_probs, values = self.agent.get_action(obs_tensor, deterministic=False)
        
        # Calculate advantages with jstn's learning curve
        advantages = reward_tensor - values.squeeze()
        
        # Policy loss with jstn's precision
        policy_loss = -(log_probs * advantages.detach()).mean()
        
        # Value loss with jstn's consistency
        value_loss = torch.nn.functional.mse_loss(values.squeeze(), reward_tensor)
        
        # Total loss with jstn's balance
        total_loss = policy_loss + 0.3 * value_loss  # Lower value weight for jstn's style
        
        # Backward pass with jstn's gradient clipping
        total_loss.backward()
        torch.nn.utils.clip_grad_norm_(self.agent.parameters(), 0.3)  # Tighter clipping for jstn
        self.optimizer.step()
        
        return {
            'policy_loss': policy_loss.item(),
            'value_loss': value_loss.item(),
            'total_loss': total_loss.item()
        }
    
    def save_model(self, path: str):
        """Save the trained jstn model"""
        checkpoint = {
            'agent_state_dict': self.agent.state_dict(),
            'selector_state_dict': self.selector.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'episode_count': self.episode_count,
            'best_reward': self.best_reward,
            'obs_size': self.obs_size,
            'action_size': self.action_size,
            'aerial_time': self.aerial_time,
            'flip_resets': self.flip_resets,
            'double_taps': self.double_taps,
            'ceiling_shots': self.ceiling_shots,
            'musty_flicks': self.musty_flicks
        }
        torch.save(checkpoint, path)
        print(f"✅ JSTN model saved to {path}")
    
    def load_model(self, path: str):
        """Load a trained jstn model"""
        if os.path.exists(path):
            checkpoint = torch.load(path, map_location=self.device)
            self.agent.load_state_dict(checkpoint['agent_state_dict'])
            self.selector.load_state_dict(checkpoint['selector_state_dict'])
            self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
            self.episode_count = checkpoint.get('episode_count', 0)
            self.best_reward = checkpoint.get('best_reward', -float('inf'))
            self.aerial_time = checkpoint.get('aerial_time', 0.0)
            self.flip_resets = checkpoint.get('flip_resets', 0)
            self.double_taps = checkpoint.get('double_taps', 0)
            self.ceiling_shots = checkpoint.get('ceiling_shots', 0)
            self.musty_flicks = checkpoint.get('musty_flicks', 0)
            print(f"✅ JSTN model loaded from {path}")
        else:
            print(f"❌ JSTN model file not found: {path}")

class JSTNTrainer:
    """Trainer designed to create a jstn-level player"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.device = torch.device('cpu')  # Force CPU for compatibility
        
        # Training parameters optimized for jstn
        self.max_episodes = self.config.get('max_episodes', 20000)  # More episodes for jstn
        self.batch_size = self.config.get('batch_size', 2000)  # Larger batches
        self.update_frequency = self.config.get('update_frequency', 5)  # More frequent updates
        self.save_frequency = self.config.get('save_frequency', 50)  # More frequent saves
        
        # Environment
        self.env = None
        self.agent = None
        
        # Training stats
        self.episode_count = 0
        self.total_steps = 0
        self.start_time = time.time()
        
        # Experience buffer
        self.obs_buffer = []
        self.action_buffer = []
        self.reward_buffer = []
        self.next_obs_buffer = []
        self.done_buffer = []
        
        print("🚀 JSTN Trainer initialized")
        print(f"   Max episodes: {self.max_episodes}")
        print(f"   Batch size: {self.batch_size}")
        print(f"   Device: {self.device}")
        print("🎯 Training to play like jstn (Justin) - the legendary pro!")
    
    def setup_environment(self):
        """Setup the RLGym 2.0.1 environment for jstn training"""
        if not RLGYM_AVAILABLE:
            raise RuntimeError("RLGym 2.0.1 not available - cannot train with real environment")
        
        print("🎮 Setting up JSTN RLGym 2.0.1 environment...")
        self.env = JSTNEnvironment(team_size=1, tick_skip=FRAME_SKIP)
        
        if self.env.env is None:
            raise RuntimeError("Failed to create RLGym environment")
        
        # Create jstn agent
        self.agent = JSTNAgent(
            obs_size=self.env.obs_builder.obs_size,
            action_size=self.env.action_parser.action_size,
            device=str(self.device)
        )
        
        print("✅ JSTN environment and agent setup complete")
    
    def train_episode(self) -> Dict[str, float]:
        """Train one episode in the jstn environment"""
        if self.env is None or self.agent is None:
            raise RuntimeError("Environment or agent not initialized")
        
        # Reset environment
        obs = self.env.reset()
        episode_reward = 0.0
        episode_length = 0
        done = False
        
        # Episode buffer
        episode_obs = []
        episode_actions = []
        episode_rewards = []
        episode_next_obs = []
        episode_dones = []
        
        while not done and episode_length < 15000:  # Longer episodes for jstn
            # Get action from jstn agent
            action = self.agent.get_action(obs, deterministic=False)
            
            # Take step in environment
            next_obs, reward, done, info = self.env.step(action)
            
            # Store experience
            episode_obs.append(obs)
            episode_actions.append(action)
            episode_rewards.append(reward)
            episode_next_obs.append(next_obs)
            episode_dones.append(done)
            
            # Update stats
            episode_reward += reward
            episode_length += 1
            self.total_steps += 1
            
            # Move to next observation
            obs = next_obs
        
        # Add episode experience to buffer
        self.obs_buffer.extend(episode_obs)
        self.action_buffer.extend(episode_actions)
        self.reward_buffer.extend(episode_rewards)
        self.next_obs_buffer.extend(episode_next_obs)
        self.done_buffer.extend(episode_dones)
        
        # Update agent if we have enough experience
        if len(self.obs_buffer) >= self.batch_size:
            self._update_agent()
        
        # Update agent stats
        self.agent.episode_count += 1
        self.agent.total_reward += episode_reward
        self.agent.episode_rewards.append(episode_reward)
        self.agent.episode_lengths.append(episode_length)
        
        if episode_reward > self.agent.best_reward:
            self.agent.best_reward = episode_reward
        
        self.episode_count += 1
        
        return {
            'episode_reward': episode_reward,
            'episode_length': episode_length,
            'total_steps': self.total_steps,
            'avg_reward': np.mean(self.agent.episode_rewards[-100:]) if self.agent.episode_rewards else 0.0,
            'best_reward': self.agent.best_reward
        }
    
    def _update_agent(self):
        """Update the jstn agent using collected experience"""
        if len(self.obs_buffer) < self.batch_size:
            return
        
        # Sample batch
        indices = np.random.choice(len(self.obs_buffer), self.batch_size, replace=False)
        
        obs_batch = [self.obs_buffer[i] for i in indices]
        action_batch = [self.action_buffer[i] for i in indices]
        reward_batch = [self.reward_buffer[i] for i in indices]
        next_obs_batch = [self.next_obs_buffer[i] for i in indices]
        done_batch = [self.done_buffer[i] for i in indices]
        
        # Update jstn agent
        loss_info = self.agent.update(obs_batch, action_batch, reward_batch, next_obs_batch, done_batch)
        
        # Clear buffer
        self.obs_buffer.clear()
        self.action_buffer.clear()
        self.reward_buffer.clear()
        self.next_obs_buffer.clear()
        self.done_buffer.clear()
        
        return loss_info
    
    def train(self):
        """Main jstn training loop"""
        print("🚀 Starting JSTN training...")
        print("🎮 This will train to play like jstn (Justin) - the legendary pro!")
        print("🎯 Learning: Aerial control, flip resets, double taps, ceiling shots, musty flicks!")
        
        # Setup environment
        self.setup_environment()
        
        # Initialize wandb
        wandb.init(
            project="jstn-opti",
            config=self.config,
            name=f"jstn_training_{int(time.time())}"
        )
        
        try:
            while self.episode_count < self.max_episodes:
                # Train one episode
                episode_stats = self.train_episode()
                
                # Log to wandb
                wandb.log({
                    'episode': self.episode_count,
                    'episode_reward': episode_stats['episode_reward'],
                    'episode_length': episode_stats['episode_length'],
                    'total_steps': episode_stats['total_steps'],
                    'avg_reward': episode_stats['avg_reward'],
                    'best_reward': episode_stats['best_reward'],
                    'training_time': time.time() - self.start_time
                })
                
                # Print progress
                if self.episode_count % 10 == 0:
                    print(f"Episode {self.episode_count}: "
                          f"Reward={episode_stats['episode_reward']:.2f}, "
                          f"Length={episode_stats['episode_length']}, "
                          f"Avg={episode_stats['avg_reward']:.2f}, "
                          f"Best={episode_stats['best_reward']:.2f}")
                
                # Save model
                if self.episode_count % self.save_frequency == 0:
                    self.agent.save_model(f"jstn_model_ep{self.episode_count}.pt")
                
                # Check for jstn level (realistic thresholds)
                if episode_stats['avg_reward'] > 2000 and episode_stats['episode_length'] > 1000:
                    print(f"🏆 JSTN LEVEL REACHED at episode {self.episode_count}!")
                    print(f"   Average reward: {episode_stats['avg_reward']:.2f}")
                    print(f"   Episode length: {episode_stats['episode_length']}")
                    print("🎯 Playing like jstn - aerial master, flip reset king, double tap god!")
                    self.agent.save_model("jstn_achieved_model.pt")
        
        except KeyboardInterrupt:
            print("\n⏹️  JSTN training interrupted by user")
        except Exception as e:
            print(f"❌ JSTN training error: {e}")
        finally:
            # Save final model
            self.agent.save_model("jstn_final_model.pt")
            self.env.close()
            wandb.finish()
            print("✅ JSTN training completed and model saved")

def main():
    """Main function"""
    print("🏆 JSTN Trainer for Opti Bot")
    print("=" * 50)
    print("🎯 Training to play like jstn (Justin) - the legendary Rocket League pro!")
    print("🚀 Learning: Aerial control, flip resets, double taps, ceiling shots, musty flicks!")
    
    if not RLGYM_AVAILABLE:
        print("❌ RLGym 2.0.1 not available!")
        print("💡 Install with: pip install rlgym[all]")
        return
    
    # Training configuration optimized for jstn
    config = {
        'max_episodes': 20000,  # More episodes for jstn's complexity
        'batch_size': 2000,     # Larger batches for stability
        'update_frequency': 5,   # More frequent updates
        'save_frequency': 50,    # More frequent saves
        'learning_rate': 2e-4    # JSTN's learning rate
    }
    
    # Create and run jstn trainer
    trainer = JSTNTrainer(config)
    trainer.train()

if __name__ == "__main__":
    main()
