#!/usr/bin/env python3
"""
Modern Reward System for RLGym 2.0.1
State-of-the-art reward system for SSL-level performance
"""

import numpy as np
from typing import Any, List, Optional, Tuple
from rlgym_tools.rocket_league.reward_functions.stack_reward import StackReward
from rlgym_tools.rocket_league.reward_functions.velocity_player_to_ball_reward import VelocityPlayerToBallReward
from rlgym_tools.rocket_league.reward_functions.ball_travel_reward import BallTravelReward
from rlgym_tools.rocket_league.reward_functions.boost_change_reward import BoostChangeReward
from rlgym_tools.rocket_league.reward_functions.boost_keep_reward import BoostKeepReward
from rlgym_tools.rocket_league.reward_functions.demo_reward import DemoReward
from rlgym_tools.rocket_league.reward_functions.episode_end_reward import EpisodeEndReward
from rlgym_tools.rocket_league.reward_functions.flip_reset_reward import FlipResetReward
from rlgym_tools.rocket_league.reward_functions.goal_prob_reward import GoalProbReward
from rlgym_tools.rocket_league.reward_functions.wavedash_reward import WavedashReward
from rlgym_tools.rocket_league.reward_functions.aerial_distance_reward import AerialDistanceReward
from rlgym_tools.rocket_league.reward_functions.advanced_touch_reward import AdvancedTouchReward

class ModernRewardSystem:
    """
    Modern reward system with SSL-level features:
    - Advanced ball control rewards
    - Aerial mechanics rewards
    - Flip reset rewards
    - Double tap rewards
    - Wall play rewards
    - Recovery rewards
    - Boost management rewards
    - Team play rewards
    - Opponent pressure rewards
    - Mechanical skill rewards
    """
    
    def __init__(self, 
                 team_size: int = 3,
                 reward_weights: Optional[dict] = None,
                 ssl_mode: bool = True,
                 advanced_mechanics: bool = True,
                 team_play: bool = True,
                 opponent_pressure: bool = True):
        
        self.team_size = team_size
        self.ssl_mode = ssl_mode
        self.advanced_mechanics = advanced_mechanics
        self.team_play = team_play
        self.opponent_pressure = opponent_pressure
        
        # Default reward weights for SSL-level performance
        self.reward_weights = reward_weights or self._get_default_weights()
        
        # Initialize reward functions
        self.reward_functions = self._initialize_reward_functions()
        
        # Create stacked reward function
        self.stacked_reward = StackReward(self.reward_functions)
        
        # SSL-specific tracking
        self.ssl_tracking = {
            'flip_resets': 0,
            'double_taps': 0,
            'aerial_goals': 0,
            'wall_plays': 0,
            'recoveries': 0,
            'boost_efficiency': 0.0,
            'mechanical_skill': 0.0
        }
        
    def _get_default_weights(self) -> dict:
        """Get default reward weights for SSL-level performance"""
        return {
            # Basic rewards
            'goal': 100.0,
            'save': 50.0,
            'touch': 10.0,
            'ball_velocity': 5.0,
            'player_velocity': 2.0,
            'boost_usage': 1.0,
            'demo': 20.0,
            'episode_end': 10.0,
            
            # SSL-specific rewards
            'flip_reset': 50.0,
            'double_tap': 75.0,
            'aerial_goal': 60.0,
            'wall_play': 15.0,
            'recovery': 25.0,
            'boost_efficiency': 5.0,
            'mechanical_skill': 10.0,
            'team_play': 20.0,
            'opponent_pressure': 15.0,
            
            # Advanced mechanics
            'air_roll': 5.0,
            'power_slide': 3.0,
            'wavedash': 8.0,
            'ceiling_shot': 40.0,
            'musty_flick': 30.0,
            'speed_flip': 15.0,
            'chain_dash': 20.0,
            'stall': 25.0,
            
            # Positioning and strategy
            'positioning': 8.0,
            'rotation': 12.0,
            'challenge': 10.0,
            'fake_challenge': 15.0,
            'boost_steal': 25.0,
            'boost_deny': 20.0,
            
            # Penalties
            'own_goal': -100.0,
            'bad_touch': -5.0,
            'waste_boost': -2.0,
            'bad_positioning': -3.0,
            'ball_chase': -5.0,
            'overcommit': -8.0
        }
    
    def _initialize_reward_functions(self) -> List[Any]:
        """Initialize all reward functions"""
        reward_functions = []
        
        # Basic reward functions
        reward_functions.append(VelocityPlayerToBallReward(
            include_negative_values=True,
            use_trajectory_comparison=True,
            use_dot_quotient=True
        ))
        
        reward_functions.append(BallTravelReward())
        reward_functions.append(BoostChangeReward())
        reward_functions.append(BoostKeepReward())
        reward_functions.append(DemoReward())
        reward_functions.append(EpisodeEndReward())
        
        # SSL-specific reward functions
        if self.ssl_mode:
            reward_functions.append(FlipResetReward())
            reward_functions.append(GoalProbReward())
            reward_functions.append(WavedashReward())
            reward_functions.append(AerialDistanceReward())
            reward_functions.append(AdvancedTouchReward())
        
        # Add custom SSL reward functions
        if self.advanced_mechanics:
            reward_functions.append(self._create_double_tap_reward())
            reward_functions.append(self._create_aerial_mechanics_reward())
            reward_functions.append(self._create_wall_play_reward())
            reward_functions.append(self._create_recovery_reward())
            reward_functions.append(self._create_boost_efficiency_reward())
            reward_functions.append(self._create_mechanical_skill_reward())
        
        if self.team_play:
            reward_functions.append(self._create_team_play_reward())
            reward_functions.append(self._create_rotation_reward())
            reward_functions.append(self._create_positioning_reward())
        
        if self.opponent_pressure:
            reward_functions.append(self._create_opponent_pressure_reward())
            reward_functions.append(self._create_challenge_reward())
            reward_functions.append(self._create_boost_steal_reward())
        
        return reward_functions
    
    def _create_double_tap_reward(self):
        """Create double tap reward function"""
        class DoubleTapReward:
            def __init__(self, weight: float = 75.0):
                self.weight = weight
                self.last_ball_height = 0.0
                self.double_tap_sequence = False
                self.first_touch_height = 0.0
            
            def __call__(self, player: Any, state: Any, previous_action: Any) -> float:
                reward = 0.0
                ball_pos = state.ball.position
                ball_vel = state.ball.linear_velocity
                
                # Detect double tap setup
                if ball_pos[2] > 400 and abs(ball_vel[1]) > 1000:
                    if not self.double_tap_sequence:
                        self.double_tap_sequence = True
                        self.first_touch_height = ball_pos[2]
                        reward += self.weight * 0.1  # Setup reward
                
                # Detect first touch
                if (self.double_tap_sequence and 
                    ball_pos[2] > self.first_touch_height * 0.8 and
                    np.linalg.norm(ball_vel) > 1500):
                    reward += self.weight * 0.3  # First touch reward
                
                # Detect second touch (goal)
                if (self.double_tap_sequence and 
                    ball_pos[2] > 200 and
                    abs(ball_vel[1]) > 2000):
                    reward += self.weight * 0.6  # Second touch reward
                    self.double_tap_sequence = False
                
                # Reset sequence if ball hits ground
                if ball_pos[2] < 100:
                    self.double_tap_sequence = False
                
                return reward
        
        return DoubleTapReward(self.reward_weights['double_tap'])
    
    def _create_aerial_mechanics_reward(self):
        """Create aerial mechanics reward function"""
        class AerialMechanicsReward:
            def __init__(self, weight: float = 10.0):
                self.weight = weight
                self.aerial_time = 0
                self.last_height = 0.0
            
            def __call__(self, player: Any, state: Any, previous_action: Any) -> float:
                reward = 0.0
                player_pos = player.car_data.position
                ball_pos = state.ball.position
                
                # Aerial time reward
                if player_pos[2] > 200:
                    self.aerial_time += 1
                    reward += self.weight * 0.1 * (self.aerial_time / 100.0)
                else:
                    self.aerial_time = 0
                
                # Height gain reward
                if player_pos[2] > self.last_height:
                    reward += self.weight * 0.2 * (player_pos[2] - self.last_height) / 1000.0
                
                self.last_height = player_pos[2]
                
                # Ball height correlation reward
                if ball_pos[2] > 300 and player_pos[2] > 200:
                    reward += self.weight * 0.3
                
                return reward
        
        return AerialMechanicsReward(self.reward_weights['aerial_goal'])
    
    def _create_wall_play_reward(self):
        """Create wall play reward function"""
        class WallPlayReward:
            def __init__(self, weight: float = 15.0):
                self.weight = weight
                self.wall_time = 0
                self.last_wall_contact = False
            
            def __call__(self, player: Any, state: Any, previous_action: Any) -> float:
                reward = 0.0
                player_pos = player.car_data.position
                ball_pos = state.ball.position
                
                # Wall proximity reward
                if abs(player_pos[0]) > 3000:  # Near side walls
                    self.wall_time += 1
                    reward += self.weight * 0.1 * (self.wall_time / 50.0)
                else:
                    self.wall_time = 0
                
                # Wall-ball interaction reward
                if (abs(player_pos[0]) > 3000 and 
                    np.linalg.norm(ball_pos - player_pos) < 500):
                    reward += self.weight * 0.5
                
                # Wall shot reward
                if (abs(player_pos[0]) > 3000 and 
                    ball_pos[2] > 200 and
                    abs(ball_pos[1]) > 3000):
                    reward += self.weight * 0.8
                
                return reward
        
        return WallPlayReward(self.reward_weights['wall_play'])
    
    def _create_recovery_reward(self):
        """Create recovery reward function"""
        class RecoveryReward:
            def __init__(self, weight: float = 25.0):
                self.weight = weight
                self.recovery_time = 0
                self.last_ground_contact = True
            
            def __call__(self, player: Any, state: Any, previous_action: Any) -> float:
                reward = 0.0
                player_pos = player.car_data.position
                player_vel = player.car_data.linear_velocity
                
                # Ground contact reward
                if player_pos[2] < 50 and not self.last_ground_contact:
                    reward += self.weight * 0.5  # Landing reward
                    self.recovery_time = 0
                
                # Recovery time penalty
                if player_pos[2] > 50:
                    self.recovery_time += 1
                    if self.recovery_time > 100:  # Too long in air
                        reward -= self.weight * 0.1
                
                # Speed recovery reward
                if (player_pos[2] < 50 and 
                    np.linalg.norm(player_vel) > 1000):
                    reward += self.weight * 0.3
                
                self.last_ground_contact = player_pos[2] < 50
                
                return reward
        
        return RecoveryReward(self.reward_weights['recovery'])
    
    def _create_boost_efficiency_reward(self):
        """Create boost efficiency reward function"""
        class BoostEfficiencyReward:
            def __init__(self, weight: float = 5.0):
                self.weight = weight
                self.last_boost = 100.0
                self.boost_usage = 0.0
            
            def __call__(self, player: Any, state: Any, previous_action: Any) -> float:
                reward = 0.0
                current_boost = player.boost_amount
                
                # Boost usage tracking
                boost_used = self.last_boost - current_boost
                if boost_used > 0:
                    self.boost_usage += boost_used
                
                # Efficiency reward (more boost used = more reward if used effectively)
                if self.boost_usage > 0:
                    reward += self.weight * 0.1 * self.boost_usage
                
                # Boost conservation reward
                if current_boost > 80:
                    reward += self.weight * 0.05
                
                self.last_boost = current_boost
                
                return reward
        
        return BoostEfficiencyReward(self.reward_weights['boost_efficiency'])
    
    def _create_mechanical_skill_reward(self):
        """Create mechanical skill reward function"""
        class MechanicalSkillReward:
            def __init__(self, weight: float = 10.0):
                self.weight = weight
                self.skill_actions = 0
                self.last_action = None
            
            def __call__(self, player: Any, state: Any, previous_action: Any) -> float:
                reward = 0.0
                
                # Air roll reward
                if hasattr(previous_action, 'air_roll') and abs(previous_action.air_roll) > 0.5:
                    reward += self.weight * 0.2
                    self.skill_actions += 1
                
                # Power slide reward
                if hasattr(previous_action, 'handbrake') and previous_action.handbrake:
                    reward += self.weight * 0.1
                    self.skill_actions += 1
                
                # Jump timing reward
                if hasattr(previous_action, 'jump') and previous_action.jump:
                    reward += self.weight * 0.1
                    self.skill_actions += 1
                
                # Boost timing reward
                if hasattr(previous_action, 'boost') and previous_action.boost:
                    reward += self.weight * 0.1
                    self.skill_actions += 1
                
                # Skill combination reward
                if self.skill_actions > 3:
                    reward += self.weight * 0.5
                    self.skill_actions = 0
                
                return reward
        
        return MechanicalSkillReward(self.reward_weights['mechanical_skill'])
    
    def _create_team_play_reward(self):
        """Create team play reward function"""
        class TeamPlayReward:
            def __init__(self, weight: float = 20.0):
                self.weight = weight
                self.team_positions = []
            
            def __call__(self, player: Any, state: Any, previous_action: Any) -> float:
                reward = 0.0
                
                # Team positioning reward
                team_players = [p for p in state.players if p.team_num == player.team_num]
                if len(team_players) > 1:
                    positions = [p.car_data.position for p in team_players]
                    distances = [np.linalg.norm(pos - player.car_data.position) for pos in positions]
                    
                    # Optimal spacing reward
                    avg_distance = np.mean(distances)
                    if 500 < avg_distance < 1500:
                        reward += self.weight * 0.3
                
                # Pass reward
                ball_pos = state.ball.position
                for teammate in team_players:
                    if teammate != player:
                        teammate_pos = teammate.car_data.position
                        if np.linalg.norm(ball_pos - teammate_pos) < 300:
                            reward += self.weight * 0.5
                
                return reward
        
        return TeamPlayReward(self.reward_weights['team_play'])
    
    def _create_rotation_reward(self):
        """Create rotation reward function"""
        class RotationReward:
            def __init__(self, weight: float = 12.0):
                self.weight = weight
                self.last_position = None
            
            def __call__(self, player: Any, state: Any, previous_action: Any) -> float:
                reward = 0.0
                player_pos = player.car_data.position
                ball_pos = state.ball.position
                
                # Rotation away from ball reward
                if self.last_position is not None:
                    ball_distance = np.linalg.norm(ball_pos - player_pos)
                    last_ball_distance = np.linalg.norm(ball_pos - self.last_position)
                    
                    if ball_distance > last_ball_distance:  # Moving away from ball
                        reward += self.weight * 0.2
                
                self.last_position = player_pos.copy()
                
                return reward
        
        return RotationReward(self.reward_weights['rotation'])
    
    def _create_positioning_reward(self):
        """Create positioning reward function"""
        class PositioningReward:
            def __init__(self, weight: float = 8.0):
                self.weight = weight
            
            def __call__(self, player: Any, state: Any, previous_action: Any) -> float:
                reward = 0.0
                player_pos = player.car_data.position
                ball_pos = state.ball.position
                
                # Defensive positioning
                if player.team_num == 0:  # Blue team
                    goal_pos = np.array([0, -5120, 0])
                else:  # Orange team
                    goal_pos = np.array([0, 5120, 0])
                
                # Distance to goal reward
                goal_distance = np.linalg.norm(player_pos - goal_pos)
                if goal_distance < 2000:  # Good defensive position
                    reward += self.weight * 0.3
                
                # Ball-goal line positioning
                ball_goal_vector = goal_pos - ball_pos
                player_ball_vector = player_pos - ball_pos
                
                if np.dot(ball_goal_vector, player_ball_vector) > 0:  # Between ball and goal
                    reward += self.weight * 0.5
                
                return reward
        
        return PositioningReward(self.reward_weights['positioning'])
    
    def _create_opponent_pressure_reward(self):
        """Create opponent pressure reward function"""
        class OpponentPressureReward:
            def __init__(self, weight: float = 15.0):
                self.weight = weight
            
            def __call__(self, player: Any, state: Any, previous_action: Any) -> float:
                reward = 0.0
                player_pos = player.car_data.position
                ball_pos = state.ball.position
                
                # Find closest opponent
                opponents = [p for p in state.players if p.team_num != player.team_num]
                if opponents:
                    closest_opponent = min(opponents, 
                                         key=lambda p: np.linalg.norm(p.car_data.position - player_pos))
                    
                    # Pressure reward
                    opponent_distance = np.linalg.norm(closest_opponent.car_data.position - player_pos)
                    if opponent_distance < 1000:
                        reward += self.weight * 0.3
                    
                    # Challenge reward
                    if opponent_distance < 500:
                        reward += self.weight * 0.5
                
                return reward
        
        return OpponentPressureReward(self.reward_weights['opponent_pressure'])
    
    def _create_challenge_reward(self):
        """Create challenge reward function"""
        class ChallengeReward:
            def __init__(self, weight: float = 10.0):
                self.weight = weight
            
            def __call__(self, player: Any, state: Any, previous_action: Any) -> float:
                reward = 0.0
                player_pos = player.car_data.position
                ball_pos = state.ball.position
                
                # Challenge timing reward
                ball_distance = np.linalg.norm(ball_pos - player_pos)
                if 200 < ball_distance < 800:  # Good challenge range
                    reward += self.weight * 0.4
                
                # Speed challenge reward
                player_vel = player.car_data.linear_velocity
                if np.linalg.norm(player_vel) > 1500:  # Fast challenge
                    reward += self.weight * 0.3
                
                return reward
        
        return ChallengeReward(self.reward_weights['challenge'])
    
    def _create_boost_steal_reward(self):
        """Create boost steal reward function"""
        class BoostStealReward:
            def __init__(self, weight: float = 25.0):
                self.weight = weight
                self.last_boost = 100.0
            
            def __call__(self, player: Any, state: Any, previous_action: Any) -> float:
                reward = 0.0
                current_boost = player.boost_amount
                
                # Boost gain reward
                boost_gained = current_boost - self.last_boost
                if boost_gained > 0:
                    reward += self.weight * 0.1 * boost_gained
                
                # Big boost steal reward
                if boost_gained > 80:  # Big boost pad
                    reward += self.weight * 0.5
                
                self.last_boost = current_boost
                
                return reward
        
        return BoostStealReward(self.reward_weights['boost_steal'])
    
    def get_reward(self, player: Any, state: Any, previous_action: Any) -> float:
        """Get the total reward for a player"""
        # Get reward from stacked reward function
        reward = self.stacked_reward.get_reward(player, state, previous_action)
        
        # Add SSL-specific tracking
        self._update_ssl_tracking(player, state, previous_action, reward)
        
        return reward
    
    def _update_ssl_tracking(self, player: Any, state: Any, previous_action: Any, reward: float):
        """Update SSL-specific tracking metrics"""
        # Track flip resets
        if reward > 50 and hasattr(previous_action, 'jump') and previous_action.jump:
            self.ssl_tracking['flip_resets'] += 1
        
        # Track double taps
        if reward > 75:
            self.ssl_tracking['double_taps'] += 1
        
        # Track aerial goals
        if reward > 60 and player.car_data.position[2] > 200:
            self.ssl_tracking['aerial_goals'] += 1
        
        # Track wall plays
        if reward > 15 and abs(player.car_data.position[0]) > 3000:
            self.ssl_tracking['wall_plays'] += 1
        
        # Track recoveries
        if reward > 25 and player.car_data.position[2] < 50:
            self.ssl_tracking['recoveries'] += 1
        
        # Track boost efficiency
        if reward > 0:
            self.ssl_tracking['boost_efficiency'] += reward * 0.01
        
        # Track mechanical skill
        if reward > 10:
            self.ssl_tracking['mechanical_skill'] += reward * 0.02
    
    def get_ssl_stats(self) -> dict:
        """Get SSL tracking statistics"""
        return self.ssl_tracking.copy()
    
    def reset_ssl_stats(self):
        """Reset SSL tracking statistics"""
        for key in self.ssl_tracking:
            self.ssl_tracking[key] = 0 if isinstance(self.ssl_tracking[key], int) else 0.0

# Legacy compatibility class
class ZeroSumReward(ModernRewardSystem):
    """Legacy compatibility class for existing code"""
    
    def __init__(self, **kwargs):
        # Map old parameters to new ones
        team_size = kwargs.get('team_size', 3)
        reward_weights = kwargs.get('reward_weights', None)
        
        super().__init__(
            team_size=team_size,
            reward_weights=reward_weights,
            ssl_mode=True,
            advanced_mechanics=True,
            team_play=True,
            opponent_pressure=True
        )
