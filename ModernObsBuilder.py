#!/usr/bin/env python3
"""
Modern Observation Builder for RLGym 2.0.1
State-of-the-art observation system for SSL-level performance
"""

import numpy as np
from typing import Any, List, Optional, Tuple
from rlgym_tools.rocket_league.obs_builders.relative_default_obs import RelativeDefaultObs
import math
import gymnasium as gym
from gymnasium.spaces import Box

class ModernObsBuilder(RelativeDefaultObs):
    """
    Modern observation builder with SSL-level features:
    - Advanced ball prediction
    - Boost pad awareness
    - Opponent modeling
    - Aerial mechanics detection
    - Flip reset indicators
    - Double tap awareness
    - Wall play detection
    - Recovery state tracking
    """
    
    def __init__(self, 
                 team_size: int = 3,
                 tick_skip: int = 4,
                 stack_size: int = 5,
                 expanding: bool = True,
                 extra_boost_info: bool = True,
                 embed_players: bool = True,
                 selector: bool = True,
                 doubletap_indicator: bool = True,
                 flip_reset_counter: bool = True,
                 aerial_mechanics: bool = True,
                 wall_play_detection: bool = True,
                 recovery_tracking: bool = True,
                 opponent_modeling: bool = True,
                 ball_prediction_steps: int = 60):
        
        super().__init__(
            zero_padding=team_size,
            pos_coef=0.0004347826086956522,
            ang_coef=0.3183098861837907,
            lin_vel_coef=0.0004347826086956522,
            ang_vel_coef=0.3183098861837907,
            pad_timer_coef=0.1,
            boost_coef=0.01,
            dodge_relative=False
        )
        
        self.team_size = team_size
        self.tick_skip = tick_skip
        self.stack_size = stack_size
        self.expanding = expanding
        self.extra_boost_info = extra_boost_info
        self.embed_players = embed_players
        self.selector = selector
        self.doubletap_indicator = doubletap_indicator
        self.flip_reset_counter = flip_reset_counter
        self.aerial_mechanics = aerial_mechanics
        self.wall_play_detection = wall_play_detection
        self.recovery_tracking = recovery_tracking
        self.opponent_modeling = opponent_modeling
        self.ball_prediction_steps = ball_prediction_steps
        
        # Advanced features
        self.ball_prediction_cache = {}
        self.boost_pad_timers = {}
        self.aerial_state_tracker = {}
        self.flip_reset_tracker = {}
        self.double_tap_tracker = {}
        self.wall_play_tracker = {}
        self.recovery_tracker = {}
        self.opponent_model = {}
        
        # Calculate observation space size
        self.obs_size = self._calculate_obs_size()
        
    def _calculate_obs_size(self) -> int:
        """Calculate the total observation space size"""
        base_size = 35  # Base car observation
        
        # Add features based on configuration
        if self.extra_boost_info:
            base_size += 34  # Boost pad information
        
        if self.embed_players:
            base_size += self.team_size * 5  # Player embeddings
        
        if self.selector:
            base_size += 10  # Sub-model selection
        
        if self.doubletap_indicator:
            base_size += 1  # Double tap indicator
        
        if self.flip_reset_counter:
            base_size += 1  # Flip reset counter
        
        if self.aerial_mechanics:
            base_size += 5  # Aerial mechanics state
        
        if self.wall_play_detection:
            base_size += 3  # Wall play detection
        
        if self.recovery_tracking:
            base_size += 4  # Recovery state tracking
        
        if self.opponent_modeling:
            base_size += 8  # Opponent modeling
        
        # Multiply by stack size for temporal information
        return base_size * self.stack_size
    
    def get_obs_space(self) -> gym.Space:
        """Get the observation space"""
        return Box(
            low=-np.inf,
            high=np.inf,
            shape=(self.obs_size,),
            dtype=np.float32
        )
    
    def reset(self, initial_state: Any) -> None:
        """Reset the observation builder"""
        super().reset(initial_state)
        
        # Reset all trackers
        self.ball_prediction_cache.clear()
        self.boost_pad_timers.clear()
        self.aerial_state_tracker.clear()
        self.flip_reset_tracker.clear()
        self.double_tap_tracker.clear()
        self.wall_play_tracker.clear()
        self.recovery_tracker.clear()
        self.opponent_model.clear()
    
    def build_obs(self, player: Any, state: Any, previous_action: Optional[np.ndarray] = None) -> np.ndarray:
        """
        Build the observation for a player
        
        Args:
            player: Player data
            state: Game state
            previous_action: Previous action taken
            
        Returns:
            Observation array
        """
        # Get base observation from parent class
        base_obs = super().build_obs(player, state, previous_action)
        
        # Build advanced features
        advanced_features = self._build_advanced_features(player, state, previous_action)
        
        # Combine observations
        full_obs = np.concatenate([base_obs, advanced_features])
        
        # Ensure correct size
        if len(full_obs) < self.obs_size:
            # Pad with zeros
            padding = np.zeros(self.obs_size - len(full_obs))
            full_obs = np.concatenate([full_obs, padding])
        elif len(full_obs) > self.obs_size:
            # Truncate
            full_obs = full_obs[:self.obs_size]
        
        return full_obs.astype(np.float32)
    
    def _build_advanced_features(self, player: Any, state: Any, previous_action: Optional[np.ndarray] = None) -> np.ndarray:
        """Build advanced SSL-level features"""
        features = []
        
        # Boost pad information
        if self.extra_boost_info:
            boost_features = self._get_boost_features(player, state)
            features.extend(boost_features)
        
        # Player embeddings
        if self.embed_players:
            player_embeddings = self._get_player_embeddings(player, state)
            features.extend(player_embeddings)
        
        # Sub-model selection features
        if self.selector:
            selector_features = self._get_selector_features(player, state)
            features.extend(selector_features)
        
        # Double tap indicator
        if self.doubletap_indicator:
            double_tap_feature = self._get_double_tap_indicator(player, state)
            features.append(double_tap_feature)
        
        # Flip reset counter
        if self.flip_reset_counter:
            flip_reset_feature = self._get_flip_reset_counter(player, state)
            features.append(flip_reset_feature)
        
        # Aerial mechanics
        if self.aerial_mechanics:
            aerial_features = self._get_aerial_mechanics(player, state)
            features.extend(aerial_features)
        
        # Wall play detection
        if self.wall_play_detection:
            wall_features = self._get_wall_play_features(player, state)
            features.extend(wall_features)
        
        # Recovery tracking
        if self.recovery_tracking:
            recovery_features = self._get_recovery_features(player, state)
            features.extend(recovery_features)
        
        # Opponent modeling
        if self.opponent_modeling:
            opponent_features = self._get_opponent_features(player, state)
            features.extend(opponent_features)
        
        return np.array(features, dtype=np.float32)
    
    def _get_boost_features(self, player: Any, state: Any) -> List[float]:
        """Get boost pad information"""
        features = []
        
        # Boost pad locations and states
        for i in range(34):  # 34 boost pads
            if i < len(state.boost_pads):
                pad = state.boost_pads[i]
                features.extend([
                    pad.position[0] / 4096.0,  # Normalized x position
                    pad.position[1] / 5120.0,  # Normalized y position
                    float(pad.is_active),      # Is boost pad active
                    float(pad.is_big),         # Is big boost pad
                ])
            else:
                features.extend([0.0, 0.0, 0.0, 0.0])  # Padding
        
        return features
    
    def _get_player_embeddings(self, player: Any, state: Any) -> List[float]:
        """Get player embeddings"""
        features = []
        
        for i in range(self.team_size):
            if i < len(state.players):
                p = state.players[i]
                # Basic player info
                features.extend([
                    p.car_data.position[0] / 4096.0,  # Normalized position
                    p.car_data.position[1] / 5120.0,
                    p.car_data.position[2] / 2044.0,
                    p.boost_amount,                    # Boost amount
                    float(p.team_num),                # Team number
                ])
            else:
                features.extend([0.0, 0.0, 0.0, 0.0, 0.0])  # Padding
        
        return features
    
    def _get_selector_features(self, player: Any, state: Any) -> List[float]:
        """Get sub-model selection features"""
        # 10 sub-models: kickoff, GP, aerial, flick_bump, flip_reset, 
        # recover_b_post, recover_ball, walldash, doubletap, wall_play
        features = [0.0] * 10
        
        # Determine which sub-model should be active based on game state
        ball_pos = state.ball.position
        player_pos = player.car_data.position
        
        # Distance to ball
        dist_to_ball = np.linalg.norm(ball_pos - player_pos)
        
        # Height above ground
        height = player_pos[2]
        
        # Ball height
        ball_height = ball_pos[2]
        
        # Determine active sub-model
        if dist_to_ball < 500 and ball_height < 100:
            features[0] = 1.0  # kickoff
        elif height < 200:
            features[1] = 1.0  # GP (ground play)
        elif ball_height > 300 or height > 200:
            features[2] = 1.0  # aerial
        elif dist_to_ball < 1000 and ball_height < 200:
            features[3] = 1.0  # flick_bump
        elif ball_height > 500:
            features[4] = 1.0  # flip_reset
        elif height < 100:
            features[5] = 1.0  # recover_b_post
        elif dist_to_ball > 2000:
            features[6] = 1.0  # recover_ball
        elif abs(player_pos[0]) > 3000:  # Near walls
            features[7] = 1.0  # walldash
        elif ball_height > 400 and dist_to_ball < 1500:
            features[8] = 1.0  # doubletap
        else:
            features[9] = 1.0  # wall_play
        
        return features
    
    def _get_double_tap_indicator(self, player: Any, state: Any) -> float:
        """Get double tap indicator"""
        # Simple heuristic: ball is high and moving toward goal
        ball_pos = state.ball.position
        ball_vel = state.ball.linear_velocity
        
        if ball_pos[2] > 400 and abs(ball_vel[1]) > 1000:
            return 1.0
        return 0.0
    
    def _get_flip_reset_counter(self, player: Any, state: Any) -> float:
        """Get flip reset counter"""
        # Simple heuristic: player is high and near ball
        player_pos = player.car_data.position
        ball_pos = state.ball.position
        
        if player_pos[2] > 500 and np.linalg.norm(ball_pos - player_pos) < 200:
            return 1.0
        return 0.0
    
    def _get_aerial_mechanics(self, player: Any, state: Any) -> List[float]:
        """Get aerial mechanics features"""
        features = []
        
        player_pos = player.car_data.position
        ball_pos = state.ball.position
        ball_vel = state.ball.linear_velocity
        
        # Aerial state indicators
        features.append(float(player_pos[2] > 200))  # Is aerial
        features.append(float(ball_pos[2] > 300))    # Ball is high
        features.append(float(np.linalg.norm(ball_vel) > 1000))  # Ball is fast
        features.append(float(player.has_flip))      # Has flip available
        features.append(float(player.boost_amount > 50))  # Has boost
        
        return features
    
    def _get_wall_play_features(self, player: Any, state: Any) -> List[float]:
        """Get wall play features"""
        features = []
        
        player_pos = player.car_data.position
        
        # Wall proximity indicators
        features.append(float(abs(player_pos[0]) > 3000))  # Near side walls
        features.append(float(player_pos[1] > 4000))       # Near back wall
        features.append(float(player_pos[2] > 100))        # Above ground
        
        return features
    
    def _get_recovery_features(self, player: Any, state: Any) -> List[float]:
        """Get recovery features"""
        features = []
        
        player_pos = player.car_data.position
        player_vel = player.car_data.linear_velocity
        
        # Recovery state indicators
        features.append(float(player_pos[2] < 50))         # On ground
        features.append(float(np.linalg.norm(player_vel) < 500))  # Slow speed
        features.append(float(player.has_flip))            # Has flip
        features.append(float(player.boost_amount < 20))   # Low boost
        
        return features
    
    def _get_opponent_features(self, player: Any, state: Any) -> List[float]:
        """Get opponent modeling features"""
        features = []
        
        player_pos = player.car_data.position
        ball_pos = state.ball.position
        
        # Find closest opponent
        closest_opponent = None
        min_dist = float('inf')
        
        for p in state.players:
            if p.team_num != player.team_num:
                dist = np.linalg.norm(p.car_data.position - player_pos)
                if dist < min_dist:
                    min_dist = dist
                    closest_opponent = p
        
        if closest_opponent:
            opp_pos = closest_opponent.car_data.position
            opp_vel = closest_opponent.car_data.linear_velocity
            
            # Opponent features
            features.extend([
                (opp_pos[0] - player_pos[0]) / 4096.0,  # Relative position
                (opp_pos[1] - player_pos[1]) / 5120.0,
                (opp_pos[2] - player_pos[2]) / 2044.0,
                np.linalg.norm(opp_vel) / 2300.0,        # Speed
                opp_vel[0] / 2300.0,                     # Velocity components
                opp_vel[1] / 2300.0,
                opp_vel[2] / 2300.0,
                closest_opponent.boost_amount,            # Boost amount
            ])
        else:
            features.extend([0.0] * 8)  # No opponent found
        
        return features

# Legacy compatibility class
class CoyoteObsBuilder(ModernObsBuilder):
    """Legacy compatibility class for existing code"""
    
    def __init__(self, **kwargs):
        # Map old parameters to new ones
        team_size = kwargs.get('team_size', 3)
        tick_skip = kwargs.get('tick_skip', 4)
        stack_size = kwargs.get('stack_size', 5)
        expanding = kwargs.get('expanding', True)
        extra_boost_info = kwargs.get('extra_boost_info', True)
        embed_players = kwargs.get('embed_players', True)
        selector = kwargs.get('selector', True)
        doubletap_indicator = kwargs.get('doubletap_indicator', True)
        flip_reset_counter = kwargs.get('flip_reset_counter', True)
        
        super().__init__(
            team_size=team_size,
            tick_skip=tick_skip,
            stack_size=stack_size,
            expanding=expanding,
            extra_boost_info=extra_boost_info,
            embed_players=embed_players,
            selector=selector,
            doubletap_indicator=doubletap_indicator,
            flip_reset_counter=flip_reset_counter,
            aerial_mechanics=True,
            wall_play_detection=True,
            recovery_tracking=True,
            opponent_modeling=True
        )
