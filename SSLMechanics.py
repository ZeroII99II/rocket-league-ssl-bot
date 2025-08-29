#!/usr/bin/env python3
"""
SSL Mechanics System for RLGym 2.0.1
Complete implementation of all modern SSL-level mechanics and techniques
"""

import numpy as np
import torch
import torch.nn as nn
from typing import Any, Dict, List, Optional, Tuple
import math

class SSLMechanics:
    """
    Complete SSL mechanics system including:
    - Flip resets
    - Double taps
    - Air dribbles
    - Ceiling shots
    - Musty flicks
    - Speed flips
    - Chain dashes
    - Stalls
    - Wave dashes
    - Wall dashes
    - Power shots
    - Fakes
    - Demos
    - Boost management
    - Recovery techniques
    """
    
    def __init__(self):
        self.mechanics = {
            'flip_reset': FlipResetMechanic(),
            'double_tap': DoubleTapMechanic(),
            'air_dribble': AirDribbleMechanic(),
            'ceiling_shot': CeilingShotMechanic(),
            'musty_flick': MustyFlickMechanic(),
            'speed_flip': SpeedFlipMechanic(),
            'chain_dash': ChainDashMechanic(),
            'stall': StallMechanic(),
            'wave_dash': WaveDashMechanic(),
            'wall_dash': WallDashMechanic(),
            'power_shot': PowerShotMechanic(),
            'fake': FakeMechanic(),
            'demo': DemoMechanic(),
            'boost_management': BoostManagementMechanic(),
            'recovery': RecoveryMechanic()
        }
        
        # SSL skill levels
        self.skill_levels = {
            'bronze': 0.1,
            'silver': 0.2,
            'gold': 0.3,
            'platinum': 0.4,
            'diamond': 0.5,
            'champion': 0.6,
            'grand_champion': 0.7,
            'supersonic_legend': 0.8,
            'ssl_plus': 0.9,
            'pro': 1.0
        }
        
        # Current skill level
        self.current_skill_level = 'supersonic_legend'
        
    def execute_mechanic(self, mechanic_name: str, player: Any, state: Any, action: Any) -> Tuple[bool, float]:
        """
        Execute a specific mechanic
        
        Args:
            mechanic_name: Name of the mechanic to execute
            player: Player data
            state: Game state
            action: Current action
            
        Returns:
            success: Whether the mechanic was executed successfully
            reward: Reward for the mechanic execution
        """
        if mechanic_name in self.mechanics:
            mechanic = self.mechanics[mechanic_name]
            success, reward = mechanic.execute(player, state, action)
            
            # Scale reward based on skill level
            skill_multiplier = self.skill_levels[self.current_skill_level]
            reward *= skill_multiplier
            
            return success, reward
        
        return False, 0.0
    
    def get_available_mechanics(self, player: Any, state: Any) -> List[str]:
        """Get list of available mechanics for current situation"""
        available = []
        
        for name, mechanic in self.mechanics.items():
            if mechanic.is_available(player, state):
                available.append(name)
        
        return available
    
    def update_skill_level(self, performance_metrics: Dict[str, float]):
        """Update skill level based on performance"""
        # Calculate overall performance
        overall_performance = np.mean(list(performance_metrics.values()))
        
        # Update skill level based on performance
        if overall_performance > 0.9:
            self.current_skill_level = 'pro'
        elif overall_performance > 0.8:
            self.current_skill_level = 'ssl_plus'
        elif overall_performance > 0.7:
            self.current_skill_level = 'supersonic_legend'
        elif overall_performance > 0.6:
            self.current_skill_level = 'grand_champion'
        elif overall_performance > 0.5:
            self.current_skill_level = 'champion'
        else:
            self.current_skill_level = 'diamond'

class BaseMechanic:
    """Base class for all SSL mechanics"""
    
    def __init__(self, name: str, difficulty: float = 0.5):
        self.name = name
        self.difficulty = difficulty
        self.success_count = 0
        self.attempt_count = 0
        
    def execute(self, player: Any, state: Any, action: Any) -> Tuple[bool, float]:
        """Execute the mechanic"""
        self.attempt_count += 1
        
        if self.is_available(player, state):
            success = self._execute_mechanic(player, state, action)
            if success:
                self.success_count += 1
                reward = self._calculate_reward(player, state, action)
                return True, reward
        
        return False, 0.0
    
    def is_available(self, player: Any, state: Any) -> bool:
        """Check if mechanic is available in current situation"""
        raise NotImplementedError
    
    def _execute_mechanic(self, player: Any, state: Any, action: Any) -> bool:
        """Execute the specific mechanic"""
        raise NotImplementedError
    
    def _calculate_reward(self, player: Any, state: Any, action: Any) -> float:
        """Calculate reward for successful mechanic execution"""
        return 10.0 * self.difficulty
    
    def get_success_rate(self) -> float:
        """Get success rate of the mechanic"""
        if self.attempt_count == 0:
            return 0.0
        return self.success_count / self.attempt_count

class FlipResetMechanic(BaseMechanic):
    """Flip reset mechanic implementation"""
    
    def __init__(self):
        super().__init__("flip_reset", difficulty=0.9)
        self.flip_reset_sequence = False
        self.ball_contact_time = 0
        
    def is_available(self, player: Any, state: Any) -> bool:
        """Check if flip reset is available"""
        player_pos = player.car_data.position
        ball_pos = state.ball.position
        
        # Must be high in the air
        if player_pos[2] < 500:
            return False
        
        # Must be close to ball
        if np.linalg.norm(ball_pos - player_pos) > 200:
            return False
        
        # Must not have flip available
        if player.has_flip:
            return False
        
        return True
    
    def _execute_mechanic(self, player: Any, state: Any, action: Any) -> bool:
        """Execute flip reset"""
        player_pos = player.car_data.position
        ball_pos = state.ball.position
        
        # Check for ball contact
        if np.linalg.norm(ball_pos - player_pos) < 100:
            self.ball_contact_time += 1
            
            # Successful flip reset if in contact for multiple frames
            if self.ball_contact_time > 3:
                self.flip_reset_sequence = True
                return True
        else:
            self.ball_contact_time = 0
        
        return False
    
    def _calculate_reward(self, player: Any, state: Any, action: Any) -> float:
        """Calculate flip reset reward"""
        base_reward = 50.0
        
        # Bonus for maintaining control after reset
        if self.flip_reset_sequence:
            base_reward += 25.0
        
        return base_reward

class DoubleTapMechanic(BaseMechanic):
    """Double tap mechanic implementation"""
    
    def __init__(self):
        super().__init__("double_tap", difficulty=0.8)
        self.setup_phase = False
        self.first_touch = False
        self.second_touch = False
        
    def is_available(self, player: Any, state: Any) -> bool:
        """Check if double tap is available"""
        ball_pos = state.ball.position
        ball_vel = state.ball.linear_velocity
        
        # Ball must be high and moving toward goal
        if ball_pos[2] < 400:
            return False
        
        if abs(ball_vel[1]) < 1000:
            return False
        
        return True
    
    def _execute_mechanic(self, player: Any, state: Any, action: Any) -> bool:
        """Execute double tap"""
        ball_pos = state.ball.position
        ball_vel = state.ball.linear_velocity
        player_pos = player.car_data.position
        
        # Setup phase
        if not self.setup_phase and ball_pos[2] > 400:
            self.setup_phase = True
            return True
        
        # First touch
        if self.setup_phase and not self.first_touch:
            if np.linalg.norm(ball_pos - player_pos) < 200:
                self.first_touch = True
                return True
        
        # Second touch
        if self.first_touch and not self.second_touch:
            if ball_pos[2] > 200 and abs(ball_vel[1]) > 2000:
                self.second_touch = True
                return True
        
        return False
    
    def _calculate_reward(self, player: Any, state: Any, action: Any) -> float:
        """Calculate double tap reward"""
        base_reward = 75.0
        
        if self.setup_phase:
            base_reward += 10.0
        if self.first_touch:
            base_reward += 20.0
        if self.second_touch:
            base_reward += 30.0
        
        return base_reward

class AirDribbleMechanic(BaseMechanic):
    """Air dribble mechanic implementation"""
    
    def __init__(self):
        super().__init__("air_dribble", difficulty=0.7)
        self.dribble_touches = 0
        self.max_touches = 0
        
    def is_available(self, player: Any, state: Any) -> bool:
        """Check if air dribble is available"""
        player_pos = player.car_data.position
        ball_pos = state.ball.position
        
        # Must be in the air
        if player_pos[2] < 200:
            return False
        
        # Must be close to ball
        if np.linalg.norm(ball_pos - player_pos) > 300:
            return False
        
        return True
    
    def _execute_mechanic(self, player: Any, state: Any, action: Any) -> bool:
        """Execute air dribble"""
        player_pos = player.car_data.position
        ball_pos = state.ball.position
        
        # Check for ball contact
        if np.linalg.norm(ball_pos - player_pos) < 150:
            self.dribble_touches += 1
            self.max_touches = max(self.max_touches, self.dribble_touches)
            return True
        
        return False
    
    def _calculate_reward(self, player: Any, state: Any, action: Any) -> float:
        """Calculate air dribble reward"""
        base_reward = 5.0 * self.dribble_touches
        
        # Bonus for maintaining dribble
        if self.dribble_touches > 3:
            base_reward += 20.0
        
        return base_reward

class CeilingShotMechanic(BaseMechanic):
    """Ceiling shot mechanic implementation"""
    
    def __init__(self):
        super().__init__("ceiling_shot", difficulty=0.8)
        self.ceiling_contact = False
        self.shot_attempted = False
        
    def is_available(self, player: Any, state: Any) -> bool:
        """Check if ceiling shot is available"""
        player_pos = player.car_data.position
        ball_pos = state.ball.position
        
        # Must be near ceiling
        if player_pos[2] < 1800:
            return False
        
        # Ball must be in good position
        if ball_pos[2] < 300:
            return False
        
        return True
    
    def _execute_mechanic(self, player: Any, state: Any, action: Any) -> bool:
        """Execute ceiling shot"""
        player_pos = player.car_data.position
        ball_pos = state.ball.position
        
        # Check for ceiling contact
        if player_pos[2] > 1900:
            self.ceiling_contact = True
        
        # Check for shot attempt
        if self.ceiling_contact and not self.shot_attempted:
            if np.linalg.norm(ball_pos - player_pos) < 400:
                self.shot_attempted = True
                return True
        
        return False
    
    def _calculate_reward(self, player: Any, state: Any, action: Any) -> float:
        """Calculate ceiling shot reward"""
        base_reward = 40.0
        
        if self.ceiling_contact:
            base_reward += 15.0
        if self.shot_attempted:
            base_reward += 25.0
        
        return base_reward

class MustyFlickMechanic(BaseMechanic):
    """Musty flick mechanic implementation"""
    
    def __init__(self):
        super().__init__("musty_flick", difficulty=0.8)
        self.flick_sequence = False
        self.flick_power = 0.0
        
    def is_available(self, player: Any, state: Any) -> bool:
        """Check if musty flick is available"""
        player_pos = player.car_data.position
        ball_pos = state.ball.position
        
        # Must be on ground or low in air
        if player_pos[2] > 200:
            return False
        
        # Must be close to ball
        if np.linalg.norm(ball_pos - player_pos) > 300:
            return False
        
        # Must have flip available
        if not player.has_flip:
            return False
        
        return True
    
    def _execute_mechanic(self, player: Any, state: Any, action: Any) -> bool:
        """Execute musty flick"""
        # Check for flick sequence
        if hasattr(action, 'jump') and action.jump:
            if hasattr(action, 'pitch') and action.pitch > 0.5:
                self.flick_sequence = True
                self.flick_power = abs(action.pitch)
                return True
        
        return False
    
    def _calculate_reward(self, player: Any, state: Any, action: Any) -> float:
        """Calculate musty flick reward"""
        base_reward = 30.0
        
        if self.flick_sequence:
            base_reward += 20.0 * self.flick_power
        
        return base_reward

class SpeedFlipMechanic(BaseMechanic):
    """Speed flip mechanic implementation"""
    
    def __init__(self):
        super().__init__("speed_flip", difficulty=0.7)
        self.flip_sequence = False
        self.speed_gained = 0.0
        
    def is_available(self, player: Any, state: Any) -> bool:
        """Check if speed flip is available"""
        player_pos = player.car_data.position
        ball_pos = state.ball.position
        
        # Must be on ground
        if player_pos[2] > 50:
            return False
        
        # Must have flip available
        if not player.has_flip:
            return False
        
        # Must be moving
        player_vel = player.car_data.linear_velocity
        if np.linalg.norm(player_vel) < 500:
            return False
        
        return True
    
    def _execute_mechanic(self, player: Any, state: Any, action: Any) -> bool:
        """Execute speed flip"""
        # Check for speed flip sequence
        if hasattr(action, 'jump') and action.jump:
            if hasattr(action, 'pitch') and action.pitch > 0.5:
                if hasattr(action, 'roll') and abs(action.roll) > 0.5:
                    self.flip_sequence = True
                    return True
        
        return False
    
    def _calculate_reward(self, player: Any, state: Any, action: Any) -> float:
        """Calculate speed flip reward"""
        base_reward = 15.0
        
        if self.flip_sequence:
            base_reward += 10.0
        
        return base_reward

class ChainDashMechanic(BaseMechanic):
    """Chain dash mechanic implementation"""
    
    def __init__(self):
        super().__init__("chain_dash", difficulty=0.9)
        self.dash_count = 0
        self.max_dashes = 0
        
    def is_available(self, player: Any, state: Any) -> bool:
        """Check if chain dash is available"""
        player_pos = player.car_data.position
        
        # Must be on ground
        if player_pos[2] > 50:
            return False
        
        # Must have flip available
        if not player.has_flip:
            return False
        
        return True
    
    def _execute_mechanic(self, player: Any, state: Any, action: Any) -> bool:
        """Execute chain dash"""
        # Check for dash sequence
        if hasattr(action, 'jump') and action.jump:
            if hasattr(action, 'pitch') and action.pitch > 0.5:
                self.dash_count += 1
                self.max_dashes = max(self.max_dashes, self.dash_count)
                return True
        
        return False
    
    def _calculate_reward(self, player: Any, state: Any, action: Any) -> float:
        """Calculate chain dash reward"""
        base_reward = 5.0 * self.dash_count
        
        # Bonus for multiple dashes
        if self.dash_count > 2:
            base_reward += 20.0
        
        return base_reward

class StallMechanic(BaseMechanic):
    """Stall mechanic implementation"""
    
    def __init__(self):
        super().__init__("stall", difficulty=0.8)
        self.stall_sequence = False
        self.stall_duration = 0
        
    def is_available(self, player: Any, state: Any) -> bool:
        """Check if stall is available"""
        player_pos = player.car_data.position
        
        # Must be in the air
        if player_pos[2] < 300:
            return False
        
        # Must not have flip available
        if player.has_flip:
            return False
        
        return True
    
    def _execute_mechanic(self, player: Any, state: Any, action: Any) -> bool:
        """Execute stall"""
        # Check for stall sequence
        if hasattr(action, 'pitch') and action.pitch < -0.5:
            if hasattr(action, 'yaw') and abs(action.yaw) > 0.5:
                self.stall_sequence = True
                self.stall_duration += 1
                return True
        
        return False
    
    def _calculate_reward(self, player: Any, state: Any, action: Any) -> float:
        """Calculate stall reward"""
        base_reward = 25.0
        
        if self.stall_sequence:
            base_reward += 5.0 * self.stall_duration
        
        return base_reward

class WaveDashMechanic(BaseMechanic):
    """Wave dash mechanic implementation"""
    
    def __init__(self):
        super().__init__("wave_dash", difficulty=0.6)
        self.dash_sequence = False
        self.landing_angle = 0.0
        
    def is_available(self, player: Any, state: Any) -> bool:
        """Check if wave dash is available"""
        player_pos = player.car_data.position
        
        # Must be in the air
        if player_pos[2] < 100:
            return False
        
        # Must have flip available
        if not player.has_flip:
            return False
        
        return True
    
    def _execute_mechanic(self, player: Any, state: Any, action: Any) -> bool:
        """Execute wave dash"""
        # Check for wave dash sequence
        if hasattr(action, 'jump') and action.jump:
            if hasattr(action, 'pitch') and action.pitch < -0.5:
                self.dash_sequence = True
                return True
        
        return False
    
    def _calculate_reward(self, player: Any, state: Any, action: Any) -> float:
        """Calculate wave dash reward"""
        base_reward = 8.0
        
        if self.dash_sequence:
            base_reward += 5.0
        
        return base_reward

class WallDashMechanic(BaseMechanic):
    """Wall dash mechanic implementation"""
    
    def __init__(self):
        super().__init__("wall_dash", difficulty=0.7)
        self.wall_contact = False
        self.dash_sequence = False
        
    def is_available(self, player: Any, state: Any) -> bool:
        """Check if wall dash is available"""
        player_pos = player.car_data.position
        
        # Must be near walls
        if abs(player_pos[0]) < 3000:
            return False
        
        # Must have flip available
        if not player.has_flip:
            return False
        
        return True
    
    def _execute_mechanic(self, player: Any, state: Any, action: Any) -> bool:
        """Execute wall dash"""
        player_pos = player.car_data.position
        
        # Check for wall contact
        if abs(player_pos[0]) > 3500:
            self.wall_contact = True
        
        # Check for dash sequence
        if self.wall_contact and hasattr(action, 'jump') and action.jump:
            if hasattr(action, 'steer') and abs(action.steer) > 0.5:
                self.dash_sequence = True
                return True
        
        return False
    
    def _calculate_reward(self, player: Any, state: Any, action: Any) -> float:
        """Calculate wall dash reward"""
        base_reward = 12.0
        
        if self.wall_contact:
            base_reward += 8.0
        if self.dash_sequence:
            base_reward += 10.0
        
        return base_reward

class PowerShotMechanic(BaseMechanic):
    """Power shot mechanic implementation"""
    
    def __init__(self):
        super().__init__("power_shot", difficulty=0.6)
        self.shot_power = 0.0
        self.shot_accuracy = 0.0
        
    def is_available(self, player: Any, state: Any) -> bool:
        """Check if power shot is available"""
        player_pos = player.car_data.position
        ball_pos = state.ball.position
        
        # Must be close to ball
        if np.linalg.norm(ball_pos - player_pos) > 500:
            return False
        
        # Ball must be in good position
        if ball_pos[2] > 300:
            return False
        
        return True
    
    def _execute_mechanic(self, player: Any, state: Any, action: Any) -> bool:
        """Execute power shot"""
        # Check for shot sequence
        if hasattr(action, 'jump') and action.jump:
            if hasattr(action, 'boost') and action.boost:
                self.shot_power = 1.0
                return True
        
        return False
    
    def _calculate_reward(self, player: Any, state: Any, action: Any) -> float:
        """Calculate power shot reward"""
        base_reward = 20.0
        
        if self.shot_power > 0.5:
            base_reward += 15.0
        
        return base_reward

class FakeMechanic(BaseMechanic):
    """Fake mechanic implementation"""
    
    def __init__(self):
        super().__init__("fake", difficulty=0.5)
        self.fake_sequence = False
        self.opponent_fooled = False
        
    def is_available(self, player: Any, state: Any) -> bool:
        """Check if fake is available"""
        player_pos = player.car_data.position
        ball_pos = state.ball.position
        
        # Must be close to ball
        if np.linalg.norm(ball_pos - player_pos) > 400:
            return False
        
        # Must be on ground
        if player_pos[2] > 100:
            return False
        
        return True
    
    def _execute_mechanic(self, player: Any, state: Any, action: Any) -> bool:
        """Execute fake"""
        # Check for fake sequence
        if hasattr(action, 'throttle') and action.throttle > 0.5:
            if hasattr(action, 'steer') and abs(action.steer) > 0.3:
                self.fake_sequence = True
                return True
        
        return False
    
    def _calculate_reward(self, player: Any, state: Any, action: Any) -> float:
        """Calculate fake reward"""
        base_reward = 15.0
        
        if self.fake_sequence:
            base_reward += 10.0
        
        return base_reward

class DemoMechanic(BaseMechanic):
    """Demo mechanic implementation"""
    
    def __init__(self):
        super().__init__("demo", difficulty=0.4)
        self.demo_attempted = False
        self.demo_successful = False
        
    def is_available(self, player: Any, state: Any) -> bool:
        """Check if demo is available"""
        player_pos = player.car_data.position
        
        # Find opponents
        opponents = [p for p in state.players if p.team_num != player.team_num]
        if not opponents:
            return False
        
        # Check if any opponent is close
        for opponent in opponents:
            opp_pos = opponent.car_data.position
            if np.linalg.norm(opp_pos - player_pos) < 800:
                return True
        
        return False
    
    def _execute_mechanic(self, player: Any, state: Any, action: Any) -> bool:
        """Execute demo"""
        # Check for demo attempt
        if hasattr(action, 'boost') and action.boost:
            if hasattr(action, 'throttle') and action.throttle > 0.8:
                self.demo_attempted = True
                return True
        
        return False
    
    def _calculate_reward(self, player: Any, state: Any, action: Any) -> float:
        """Calculate demo reward"""
        base_reward = 20.0
        
        if self.demo_attempted:
            base_reward += 15.0
        
        return base_reward

class BoostManagementMechanic(BaseMechanic):
    """Boost management mechanic implementation"""
    
    def __init__(self):
        super().__init__("boost_management", difficulty=0.3)
        self.boost_efficiency = 0.0
        self.boost_conservation = 0.0
        
    def is_available(self, player: Any, state: Any) -> bool:
        """Check if boost management is available"""
        return True  # Always available
    
    def _execute_mechanic(self, player: Any, state: Any, action: Any) -> bool:
        """Execute boost management"""
        # Check boost usage efficiency
        if hasattr(action, 'boost') and action.boost:
            if hasattr(action, 'throttle') and action.throttle > 0.5:
                self.boost_efficiency += 0.1
                return True
        
        # Check boost conservation
        if not hasattr(action, 'boost') or not action.boost:
            if player.boost_amount > 50:
                self.boost_conservation += 0.1
                return True
        
        return False
    
    def _calculate_reward(self, player: Any, state: Any, action: Any) -> float:
        """Calculate boost management reward"""
        base_reward = 5.0
        
        base_reward += self.boost_efficiency * 2.0
        base_reward += self.boost_conservation * 1.0
        
        return base_reward

class RecoveryMechanic(BaseMechanic):
    """Recovery mechanic implementation"""
    
    def __init__(self):
        super().__init__("recovery", difficulty=0.4)
        self.recovery_time = 0
        self.recovery_successful = False
        
    def is_available(self, player: Any, state: Any) -> bool:
        """Check if recovery is available"""
        player_pos = player.car_data.position
        player_vel = player.car_data.linear_velocity
        
        # Must be in recovery situation
        if player_pos[2] > 100 and np.linalg.norm(player_vel) < 500:
            return True
        
        return False
    
    def _execute_mechanic(self, player: Any, state: Any, action: Any) -> bool:
        """Execute recovery"""
        player_pos = player.car_data.position
        
        # Check for recovery sequence
        if hasattr(action, 'pitch') and action.pitch < -0.5:
            if hasattr(action, 'boost') and action.boost:
                self.recovery_time += 1
                return True
        
        # Check for successful recovery
        if player_pos[2] < 50:
            self.recovery_successful = True
            return True
        
        return False
    
    def _calculate_reward(self, player: Any, state: Any, action: Any) -> float:
        """Calculate recovery reward"""
        base_reward = 25.0
        
        if self.recovery_successful:
            base_reward += 15.0
        
        return base_reward
