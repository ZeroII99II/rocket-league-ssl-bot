#!/usr/bin/env python3
"""
Modern Action Parser for RLGym 2.0.1
State-of-the-art action system for SSL-level performance
"""

import numpy as np
from typing import Any, List, Optional, Tuple
from rlgym_tools.rocket_league.action_parsers.advanced_lookup_table_action import AdvancedLookupTableAction
import gymnasium as gym
from gymnasium.spaces import Discrete, MultiDiscrete

class ModernActionParser(AdvancedLookupTableAction):
    """
    Modern action parser with SSL-level features:
    - Advanced aerial controls
    - Flip reset mechanics
    - Double tap actions
    - Wall dash mechanics
    - Recovery actions
    - Boost management
    - Power slide optimization
    """
    
    def __init__(self, 
                 throttle_bins: int = 5,
                 steer_bins: int = 5,
                 torque_subdivisions: int = 3,
                 flip_bins: int = 12,
                 include_stalls: bool = True,
                 aerial_mechanics: bool = True,
                 flip_reset_actions: bool = True,
                 double_tap_actions: bool = True,
                 wall_dash_actions: bool = True,
                 recovery_actions: bool = True,
                 boost_management: bool = True,
                 power_slide_optimization: bool = True):
        
        # Store parameters first
        self.throttle_bins = throttle_bins
        self.steer_bins = steer_bins
        self.torque_subdivisions = torque_subdivisions
        self.flip_bins = flip_bins
        
        super().__init__(
            throttle_bins=throttle_bins,
            steer_bins=steer_bins,
            torque_subdivisions=torque_subdivisions,
            flip_bins=flip_bins,
            include_stalls=include_stalls
        )
        
        self.aerial_mechanics = aerial_mechanics
        self.flip_reset_actions = flip_reset_actions
        self.double_tap_actions = double_tap_actions
        self.wall_dash_actions = wall_dash_actions
        self.recovery_actions = recovery_actions
        self.boost_management = boost_management
        self.power_slide_optimization = power_slide_optimization
        
        # Calculate action space size
        self.action_size = self._calculate_action_size()
        
        # Action mappings for SSL mechanics
        self._setup_ssl_actions()
        
    def _calculate_action_size(self) -> int:
        """Calculate the total action space size"""
        base_size = self.throttle_bins * self.steer_bins * self.torque_subdivisions * self.flip_bins
        
        # Add SSL-specific actions
        if self.aerial_mechanics:
            base_size += 8  # Aerial mechanics
        
        if self.flip_reset_actions:
            base_size += 4  # Flip reset actions
        
        if self.double_tap_actions:
            base_size += 6  # Double tap actions
        
        if self.wall_dash_actions:
            base_size += 4  # Wall dash actions
        
        if self.recovery_actions:
            base_size += 5  # Recovery actions
        
        if self.boost_management:
            base_size += 3  # Boost management
        
        if self.power_slide_optimization:
            base_size += 2  # Power slide optimization
        
        return base_size
    
    def _setup_ssl_actions(self):
        """Setup SSL-specific action mappings"""
        self.ssl_actions = {
            'aerial_mechanics': [
                'air_roll_left', 'air_roll_right', 'pitch_up', 'pitch_down',
                'yaw_left', 'yaw_right', 'boost', 'jump'
            ],
            'flip_reset_actions': [
                'flip_reset_attempt', 'flip_reset_recovery', 'flip_reset_follow', 'flip_reset_abort'
            ],
            'double_tap_actions': [
                'double_tap_setup', 'double_tap_first_touch', 'double_tap_second_touch',
                'double_tap_recovery', 'double_tap_abort', 'double_tap_follow'
            ],
            'wall_dash_actions': [
                'wall_dash_left', 'wall_dash_right', 'wall_dash_up', 'wall_dash_down'
            ],
            'recovery_actions': [
                'recovery_land', 'recovery_boost', 'recovery_flip', 'recovery_powerslide', 'recovery_wait'
            ],
            'boost_management': [
                'boost_conserve', 'boost_aggressive', 'boost_emergency'
            ],
            'power_slide_optimization': [
                'powerslide_on', 'powerslide_off'
            ]
        }
    
    def get_action_space(self) -> gym.Space:
        """Get the action space"""
        return Discrete(self.action_size)
    
    def parse_actions(self, actions: np.ndarray, state: Any) -> List[Any]:
        """
        Parse actions for all players
        
        Args:
            actions: Array of actions for all players
            state: Current game state
            
        Returns:
            List of parsed actions for each player
        """
        parsed_actions = []
        
        for i, action in enumerate(actions):
            if i < len(state.players):
                parsed_action = self._parse_single_action(action, state.players[i], state)
                parsed_actions.append(parsed_action)
            else:
                # Default action for missing players
                parsed_actions.append(self._get_default_action())
        
        return parsed_actions
    
    def _parse_single_action(self, action: int, player: Any, state: Any) -> Any:
        """Parse a single action for a player"""
        # Get base action from parent class
        base_action = super().parse_actions([action], state)[0]
        
        # Add SSL-specific modifications
        if self.aerial_mechanics:
            base_action = self._apply_aerial_mechanics(base_action, action, player, state)
        
        if self.flip_reset_actions:
            base_action = self._apply_flip_reset_actions(base_action, action, player, state)
        
        if self.double_tap_actions:
            base_action = self._apply_double_tap_actions(base_action, action, player, state)
        
        if self.wall_dash_actions:
            base_action = self._apply_wall_dash_actions(base_action, action, player, state)
        
        if self.recovery_actions:
            base_action = self._apply_recovery_actions(base_action, action, player, state)
        
        if self.boost_management:
            base_action = self._apply_boost_management(base_action, action, player, state)
        
        if self.power_slide_optimization:
            base_action = self._apply_power_slide_optimization(base_action, action, player, state)
        
        return base_action
    
    def _apply_aerial_mechanics(self, action: Any, action_id: int, player: Any, state: Any) -> Any:
        """Apply aerial mechanics to the action"""
        player_pos = player.car_data.position
        ball_pos = state.ball.position
        
        # Check if player is in aerial position
        if player_pos[2] > 200:  # Above ground
            # Enhanced aerial controls
            if action_id % 8 == 0:  # Air roll left
                action.air_roll = -1.0
            elif action_id % 8 == 1:  # Air roll right
                action.air_roll = 1.0
            elif action_id % 8 == 2:  # Pitch up
                action.pitch = 1.0
            elif action_id % 8 == 3:  # Pitch down
                action.pitch = -1.0
            elif action_id % 8 == 4:  # Yaw left
                action.yaw = -1.0
            elif action_id % 8 == 5:  # Yaw right
                action.yaw = 1.0
            elif action_id % 8 == 6:  # Boost
                action.boost = True
            elif action_id % 8 == 7:  # Jump
                action.jump = True
        
        return action
    
    def _apply_flip_reset_actions(self, action: Any, action_id: int, player: Any, state: Any) -> Any:
        """Apply flip reset actions"""
        player_pos = player.car_data.position
        ball_pos = state.ball.position
        
        # Check if conditions are right for flip reset
        if (player_pos[2] > 500 and 
            np.linalg.norm(ball_pos - player_pos) < 200 and
            not player.has_flip):
            
            if action_id % 4 == 0:  # Flip reset attempt
                action.pitch = 0.5
                action.jump = True
            elif action_id % 4 == 1:  # Flip reset recovery
                action.pitch = -0.5
                action.boost = True
            elif action_id % 4 == 2:  # Flip reset follow
                action.throttle = 1.0
                action.boost = True
            elif action_id % 4 == 3:  # Flip reset abort
                action.pitch = -1.0
                action.boost = True
        
        return action
    
    def _apply_double_tap_actions(self, action: Any, action_id: int, player: Any, state: Any) -> Any:
        """Apply double tap actions"""
        ball_pos = state.ball.position
        ball_vel = state.ball.linear_velocity
        
        # Check if conditions are right for double tap
        if ball_pos[2] > 400 and abs(ball_vel[1]) > 1000:
            if action_id % 6 == 0:  # Double tap setup
                action.throttle = 1.0
                action.boost = True
            elif action_id % 6 == 1:  # First touch
                action.jump = True
                action.boost = True
            elif action_id % 6 == 2:  # Second touch
                action.pitch = 1.0
                action.boost = True
            elif action_id % 6 == 3:  # Recovery
                action.pitch = -0.5
                action.boost = True
            elif action_id % 6 == 4:  # Abort
                action.pitch = -1.0
                action.boost = True
            elif action_id % 6 == 5:  # Follow
                action.throttle = 1.0
                action.boost = True
        
        return action
    
    def _apply_wall_dash_actions(self, action: Any, action_id: int, player: Any, state: Any) -> Any:
        """Apply wall dash actions"""
        player_pos = player.car_data.position
        
        # Check if near walls
        if abs(player_pos[0]) > 3000:  # Near side walls
            if action_id % 4 == 0:  # Wall dash left
                action.steer = -1.0
                action.jump = True
            elif action_id % 4 == 1:  # Wall dash right
                action.steer = 1.0
                action.jump = True
            elif action_id % 4 == 2:  # Wall dash up
                action.pitch = 1.0
                action.jump = True
            elif action_id % 4 == 3:  # Wall dash down
                action.pitch = -1.0
                action.jump = True
        
        return action
    
    def _apply_recovery_actions(self, action: Any, action_id: int, player: Any, state: Any) -> Any:
        """Apply recovery actions"""
        player_pos = player.car_data.position
        player_vel = player.car_data.linear_velocity
        
        # Check if in recovery state
        if (player_pos[2] < 50 or 
            np.linalg.norm(player_vel) < 500 or
            not player.has_flip):
            
            if action_id % 5 == 0:  # Recovery land
                action.pitch = -1.0
                action.throttle = 0.0
            elif action_id % 5 == 1:  # Recovery boost
                action.boost = True
                action.throttle = 1.0
            elif action_id % 5 == 2:  # Recovery flip
                action.jump = True
                action.pitch = 0.5
            elif action_id % 5 == 3:  # Recovery powerslide
                action.handbrake = True
                action.steer = 0.5
            elif action_id % 5 == 4:  # Recovery wait
                action.throttle = 0.0
                action.steer = 0.0
        
        return action
    
    def _apply_boost_management(self, action: Any, action_id: int, player: Any, state: Any) -> Any:
        """Apply boost management"""
        boost_amount = player.boost_amount
        
        if action_id % 3 == 0:  # Boost conserve
            if boost_amount < 30:
                action.boost = False
        elif action_id % 3 == 1:  # Boost aggressive
            if boost_amount > 20:
                action.boost = True
        elif action_id % 3 == 2:  # Boost emergency
            if boost_amount > 0:
                action.boost = True
        
        return action
    
    def _apply_power_slide_optimization(self, action: Any, action_id: int, player: Any, state: Any) -> Any:
        """Apply power slide optimization"""
        player_vel = player.car_data.linear_velocity
        speed = np.linalg.norm(player_vel)
        
        if action_id % 2 == 0:  # Powerslide on
            if speed > 1000:  # High speed
                action.handbrake = True
        elif action_id % 2 == 1:  # Powerslide off
            action.handbrake = False
        
        return action
    
    def _get_default_action(self) -> Any:
        """Get default action for missing players"""
        # Create a default action object
        class DefaultAction:
            def __init__(self):
                self.throttle = 0.0
                self.steer = 0.0
                self.pitch = 0.0
                self.yaw = 0.0
                self.roll = 0.0
                self.jump = False
                self.boost = False
                self.handbrake = False
        
        return DefaultAction()

# Legacy compatibility class
class CoyoteAction(ModernActionParser):
    """Legacy compatibility class for existing code"""
    
    def __init__(self, **kwargs):
        # Map old parameters to new ones
        throttle_bins = kwargs.get('throttle_bins', 5)
        steer_bins = kwargs.get('steer_bins', 5)
        torque_subdivisions = kwargs.get('torque_subdivisions', 3)
        flip_bins = kwargs.get('flip_bins', 12)
        include_stalls = kwargs.get('include_stalls', True)
        
        super().__init__(
            throttle_bins=throttle_bins,
            steer_bins=steer_bins,
            torque_subdivisions=torque_subdivisions,
            flip_bins=flip_bins,
            include_stalls=include_stalls,
            aerial_mechanics=True,
            flip_reset_actions=True,
            double_tap_actions=True,
            wall_dash_actions=True,
            recovery_actions=True,
            boost_management=True,
            power_slide_optimization=True
        )
