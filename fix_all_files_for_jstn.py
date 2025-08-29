#!/usr/bin/env python3
"""
Fix All Files for JSTN Training
Updates all worker and learner files to use modern components and JSTN playstyle
"""

import os
import re
from pathlib import Path

class JSTNFileFixer:
    """Fixes all files to use modern components and JSTN playstyle"""
    
    def __init__(self):
        self.files_to_fix = [
            # Learner files
            'learner_selector.py', 'learner_kickoff.py', 'learner_aerial.py',
            'learner_ceil_pinch.py', 'learner_demo.py', 'learner_dtap.py',
            'learner_flick.py', 'learner_flip_reset.py', 'learner_gp.py',
            'learner_half_flip.py', 'learner_lix.py', 'learner_pinch.py',
            'learner_recovery.py', 'learner_wall.py', 'learner_walldash.py',
            
            # Worker files
            'worker_aerial.py', 'worker_ceil_pinch.py', 'worker_demo.py',
            'worker_dtap.py', 'worker_flick.py', 'worker_flip_reset.py',
            'worker_gp.py', 'worker_half_flip.py', 'worker_kickoff.py',
            'worker_lix.py', 'worker_pinch.py', 'worker_selector.py',
            'worker_recovery.py', 'worker_wall.py', 'worker_walldash.py',
            
            # Constants files
            'Constants_selector.py', 'Constants_kickoff.py', 'Constants_aerial.py',
            'Constants_ceil_pinch.py', 'Constants_demo.py', 'Constants_dtap.py',
            'Constants_flick.py', 'Constants_flip_reset.py', 'Constants_gp.py',
            'Constants_half_flip.py', 'Constants_lix.py', 'Constants_pinch.py',
            'Constants_recovery.py', 'Constants_wall.py', 'Constants_walldash.py',
            
            # Other files
            'pretrained_agents/GP/GP.py', 'submodels/submodel_agent.py'
        ]
        
        # JSTN-specific configurations for each mechanic
        self.jstn_configs = {
            'selector': {
                'obs_builder': 'ModernObsBuilder(expanding=True, tick_skip=FRAME_SKIP, team_size=3, stack_size=5, extra_boost_info=True, embed_players=True, selector=True, doubletap_indicator=True, flip_reset_counter=True, aerial_mechanics=True, wall_play_detection=True, recovery_tracking=True, opponent_modeling=True)',
                'action_parser': 'ModernActionParser(throttle_bins=5, steer_bins=5, torque_subdivisions=3, flip_bins=12, include_stalls=True, aerial_mechanics=True, flip_reset_actions=True, double_tap_actions=True, wall_dash_actions=True, recovery_actions=True, boost_management=True, power_slide_optimization=True)',
                'reward_weights': {'aerial_goal_w': 5, 'flip_reset_goal_w': 8, 'double_tap_w': 10, 'ceiling_shot_w': 6, 'musty_flick_w': 4}
            },
            'dtap': {
                'obs_builder': 'ModernObsBuilder(expanding=True, tick_skip=FRAME_SKIP, team_size=3, stack_size=5, extra_boost_info=True, embed_players=True, selector=True, doubletap_indicator=True, flip_reset_counter=True, aerial_mechanics=True, wall_play_detection=True, recovery_tracking=True, opponent_modeling=True)',
                'action_parser': 'ModernActionParser(throttle_bins=5, steer_bins=5, torque_subdivisions=3, flip_bins=12, include_stalls=True, aerial_mechanics=True, flip_reset_actions=True, double_tap_actions=True, wall_dash_actions=True, recovery_actions=True, boost_management=True, power_slide_optimization=True)',
                'reward_weights': {'double_tap_w': 25, 'velocity_bg_w': 0.1, 'acel_ball_w': 3, 'backboard_bounce_rew': 1.0}
            },
            'flip_reset': {
                'obs_builder': 'ModernObsBuilder(expanding=True, tick_skip=FRAME_SKIP, team_size=3, stack_size=5, extra_boost_info=True, embed_players=True, selector=True, doubletap_indicator=True, flip_reset_counter=True, aerial_mechanics=True, wall_play_detection=True, recovery_tracking=True, opponent_modeling=True)',
                'action_parser': 'ModernActionParser(throttle_bins=5, steer_bins=5, torque_subdivisions=3, flip_bins=12, include_stalls=True, aerial_mechanics=True, flip_reset_actions=True, double_tap_actions=True, wall_dash_actions=True, recovery_actions=True, boost_management=True, power_slide_optimization=True)',
                'reward_weights': {'flip_reset_w': 15, 'aerial_goal_w': 8, 'velocity_pb_w': 0.02}
            },
            'aerial': {
                'obs_builder': 'ModernObsBuilder(expanding=True, tick_skip=FRAME_SKIP, team_size=3, stack_size=5, extra_boost_info=True, embed_players=True, selector=True, doubletap_indicator=True, flip_reset_counter=True, aerial_mechanics=True, wall_play_detection=True, recovery_tracking=True, opponent_modeling=True)',
                'action_parser': 'ModernActionParser(throttle_bins=5, steer_bins=5, torque_subdivisions=3, flip_bins=12, include_stalls=True, aerial_mechanics=True, flip_reset_actions=True, double_tap_actions=True, wall_dash_actions=True, recovery_actions=True, boost_management=True, power_slide_optimization=True)',
                'reward_weights': {'aerial_goal_w': 12, 'jump_touch_w': 2, 'wall_touch_w': 1.5, 'velocity_pb_w': 0.03}
            },
            'flick': {
                'obs_builder': 'ModernObsBuilder(expanding=True, tick_skip=FRAME_SKIP, team_size=3, stack_size=5, extra_boost_info=True, embed_players=True, selector=True, doubletap_indicator=True, flip_reset_counter=True, aerial_mechanics=True, wall_play_detection=True, recovery_tracking=True, opponent_modeling=True)',
                'action_parser': 'ModernActionParser(throttle_bins=5, steer_bins=5, torque_subdivisions=3, flip_bins=12, include_stalls=True, aerial_mechanics=True, flip_reset_actions=True, double_tap_actions=True, wall_dash_actions=True, recovery_actions=True, boost_management=True, power_slide_optimization=True)',
                'reward_weights': {'flick_w': 8, 'velocity_pb_w': 0.02, 'acel_ball_w': 2}
            },
            'ceil_pinch': {
                'obs_builder': 'ModernObsBuilder(expanding=True, tick_skip=FRAME_SKIP, team_size=3, stack_size=5, extra_boost_info=True, embed_players=True, selector=True, doubletap_indicator=True, flip_reset_counter=True, aerial_mechanics=True, wall_play_detection=True, recovery_tracking=True, opponent_modeling=True)',
                'action_parser': 'ModernActionParser(throttle_bins=5, steer_bins=5, torque_subdivisions=3, flip_bins=12, include_stalls=True, aerial_mechanics=True, flip_reset_actions=True, double_tap_actions=True, wall_dash_actions=True, recovery_actions=True, boost_management=True, power_slide_optimization=True)',
                'reward_weights': {'pinch_w': 20, 'ceiling_shot_w': 10, 'velocity_bg_w': 0.05}
            },
            'pinch': {
                'obs_builder': 'ModernObsBuilder(expanding=True, tick_skip=FRAME_SKIP, team_size=3, stack_size=5, extra_boost_info=True, embed_players=True, selector=True, doubletap_indicator=True, flip_reset_counter=True, aerial_mechanics=True, wall_play_detection=True, recovery_tracking=True, opponent_modeling=True)',
                'action_parser': 'ModernActionParser(throttle_bins=5, steer_bins=5, torque_subdivisions=3, flip_bins=12, include_stalls=True, aerial_mechanics=True, flip_reset_actions=True, double_tap_actions=True, wall_dash_actions=True, recovery_actions=True, boost_management=True, power_slide_optimization=True)',
                'reward_weights': {'pinch_w': 15, 'velocity_bg_w': 0.04, 'acel_ball_w': 2.5}
            },
            'wall': {
                'obs_builder': 'ModernObsBuilder(expanding=True, tick_skip=FRAME_SKIP, team_size=3, stack_size=5, extra_boost_info=True, embed_players=True, selector=True, doubletap_indicator=True, flip_reset_counter=True, aerial_mechanics=True, wall_play_detection=True, recovery_tracking=True, opponent_modeling=True)',
                'action_parser': 'ModernActionParser(throttle_bins=5, steer_bins=5, torque_subdivisions=3, flip_bins=12, include_stalls=True, aerial_mechanics=True, flip_reset_actions=True, double_tap_actions=True, wall_dash_actions=True, recovery_actions=True, boost_management=True, power_slide_optimization=True)',
                'reward_weights': {'wall_touch_w': 3, 'wall_goal_w': 8, 'velocity_pb_w': 0.02}
            },
            'walldash': {
                'obs_builder': 'ModernObsBuilder(expanding=True, tick_skip=FRAME_SKIP, team_size=3, stack_size=5, extra_boost_info=True, embed_players=True, selector=True, doubletap_indicator=True, flip_reset_counter=True, aerial_mechanics=True, wall_play_detection=True, recovery_tracking=True, opponent_modeling=True)',
                'action_parser': 'ModernActionParser(throttle_bins=5, steer_bins=5, torque_subdivisions=3, flip_bins=12, include_stalls=True, aerial_mechanics=True, flip_reset_actions=True, double_tap_actions=True, wall_dash_actions=True, recovery_actions=True, boost_management=True, power_slide_optimization=True)',
                'reward_weights': {'walldash_w': 6, 'wall_touch_w': 2, 'velocity_pb_w': 0.02}
            },
            'recovery': {
                'obs_builder': 'ModernObsBuilder(expanding=True, tick_skip=FRAME_SKIP, team_size=3, stack_size=5, extra_boost_info=True, embed_players=True, selector=True, doubletap_indicator=True, flip_reset_counter=True, aerial_mechanics=True, wall_play_detection=True, recovery_tracking=True, opponent_modeling=True)',
                'action_parser': 'ModernActionParser(throttle_bins=5, steer_bins=5, torque_subdivisions=3, flip_bins=12, include_stalls=True, aerial_mechanics=True, flip_reset_actions=True, double_tap_actions=True, wall_dash_actions=True, recovery_actions=True, boost_management=True, power_slide_optimization=True)',
                'reward_weights': {'recovery_w': 5, 'velocity_pb_w': 0.01, 'boost_gain_w': 0.02}
            },
            'demo': {
                'obs_builder': 'ModernObsBuilder(expanding=True, tick_skip=FRAME_SKIP, team_size=3, stack_size=5, extra_boost_info=True, embed_players=True, selector=True, doubletap_indicator=True, flip_reset_counter=True, aerial_mechanics=True, wall_play_detection=True, recovery_tracking=True, opponent_modeling=True)',
                'action_parser': 'ModernActionParser(throttle_bins=5, steer_bins=5, torque_subdivisions=3, flip_bins=12, include_stalls=True, aerial_mechanics=True, flip_reset_actions=True, double_tap_actions=True, wall_dash_actions=True, recovery_actions=True, boost_management=True, power_slide_optimization=True)',
                'reward_weights': {'demo_w': 8, 'got_demoed_w': -4, 'velocity_pb_w': 0.01}
            },
            'gp': {
                'obs_builder': 'ModernObsBuilder(expanding=True, tick_skip=FRAME_SKIP, team_size=3, stack_size=5, extra_boost_info=True, embed_players=True, selector=True, doubletap_indicator=True, flip_reset_counter=True, aerial_mechanics=True, wall_play_detection=True, recovery_tracking=True, opponent_modeling=True)',
                'action_parser': 'ModernActionParser(throttle_bins=5, steer_bins=5, torque_subdivisions=3, flip_bins=12, include_stalls=True, aerial_mechanics=True, flip_reset_actions=True, double_tap_actions=True, wall_dash_actions=True, recovery_actions=True, boost_management=True, power_slide_optimization=True)',
                'reward_weights': {'gp_w': 12, 'velocity_bg_w': 0.03, 'acel_ball_w': 2}
            },
            'half_flip': {
                'obs_builder': 'ModernObsBuilder(expanding=True, tick_skip=FRAME_SKIP, team_size=3, stack_size=5, extra_boost_info=True, embed_players=True, selector=True, doubletap_indicator=True, flip_reset_counter=True, aerial_mechanics=True, wall_play_detection=True, recovery_tracking=True, opponent_modeling=True)',
                'action_parser': 'ModernActionParser(throttle_bins=5, steer_bins=5, torque_subdivisions=3, flip_bins=12, include_stalls=True, aerial_mechanics=True, flip_reset_actions=True, double_tap_actions=True, wall_dash_actions=True, recovery_actions=True, boost_management=True, power_slide_optimization=True)',
                'reward_weights': {'half_flip_w': 4, 'velocity_pb_w': 0.01, 'recovery_w': 3}
            },
            'lix': {
                'obs_builder': 'ModernObsBuilder(expanding=True, tick_skip=FRAME_SKIP, team_size=3, stack_size=5, extra_boost_info=True, embed_players=True, selector=True, doubletap_indicator=True, flip_reset_counter=True, aerial_mechanics=True, wall_play_detection=True, recovery_tracking=True, opponent_modeling=True)',
                'action_parser': 'ModernActionParser(throttle_bins=5, steer_bins=5, torque_subdivisions=3, flip_bins=12, include_stalls=True, aerial_mechanics=True, flip_reset_actions=True, double_tap_actions=True, wall_dash_actions=True, recovery_actions=True, boost_management=True, power_slide_optimization=True)',
                'reward_weights': {'lix_w': 10, 'flip_reset_w': 8, 'aerial_goal_w': 6}
            },
            'kickoff': {
                'obs_builder': 'ModernObsBuilder(expanding=True, tick_skip=FRAME_SKIP, team_size=3, stack_size=5, extra_boost_info=True, embed_players=True, selector=True, doubletap_indicator=True, flip_reset_counter=True, aerial_mechanics=True, wall_play_detection=True, recovery_tracking=True, opponent_modeling=True)',
                'action_parser': 'ModernActionParser(throttle_bins=5, steer_bins=5, torque_subdivisions=3, flip_bins=12, include_stalls=True, aerial_mechanics=True, flip_reset_actions=True, double_tap_actions=True, wall_dash_actions=True, recovery_actions=True, boost_management=True, power_slide_optimization=True)',
                'reward_weights': {'kickoff_w': 3, 'velocity_pb_w': 0.01, 'boost_gain_w': 0.01}
            }
        }
    
    def get_mechanic_name(self, filename):
        """Extract mechanic name from filename"""
        if 'selector' in filename:
            return 'selector'
        elif 'dtap' in filename:
            return 'dtap'
        elif 'flip_reset' in filename:
            return 'flip_reset'
        elif 'aerial' in filename:
            return 'aerial'
        elif 'flick' in filename:
            return 'flick'
        elif 'ceil_pinch' in filename:
            return 'ceil_pinch'
        elif 'pinch' in filename:
            return 'pinch'
        elif 'wall' in filename and 'dash' not in filename:
            return 'wall'
        elif 'walldash' in filename:
            return 'walldash'
        elif 'recovery' in filename:
            return 'recovery'
        elif 'demo' in filename:
            return 'demo'
        elif 'gp' in filename:
            return 'gp'
        elif 'half_flip' in filename:
            return 'half_flip'
        elif 'lix' in filename:
            return 'lix'
        elif 'kickoff' in filename:
            return 'kickoff'
        else:
            return 'selector'  # Default
    
    def fix_file(self, filepath):
        """Fix a single file to use modern components"""
        if not os.path.exists(filepath):
            print(f"⚠️  File not found: {filepath}")
            return False
        
        print(f"🔧 Fixing {filepath}...")
        
        # Read file content
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if this is a constants file
        if 'Constants_' in filepath:
            return self.fix_constants_file(filepath, content)
        
        # Get mechanic name
        mechanic_name = self.get_mechanic_name(filepath)
        config = self.jstn_configs.get(mechanic_name, self.jstn_configs['selector'])
        
        # Fix imports
        content = re.sub(
            r'from CoyoteObs import CoyoteObsBuilder',
            'from ModernObsBuilder import ModernObsBuilder',
            content
        )
        content = re.sub(
            r'from CoyoteParser import CoyoteAction',
            'from ModernActionParser import ModernActionParser',
            content
        )
        content = re.sub(
            r'CoyoteObsBuilder',
            'ModernObsBuilder',
            content
        )
        content = re.sub(
            r'CoyoteAction',
            'ModernActionParser',
            content
        )
        
        # Fix obs_builder instantiation
        obs_builder_pattern = r'obs_builder=ModernObsBuilder\([^)]*\)'
        if re.search(obs_builder_pattern, content):
            content = re.sub(
                obs_builder_pattern,
                f'obs_builder={config["obs_builder"]}',
                content
            )
        else:
            # Add obs_builder if not found
            content = content.replace(
                'action_parser=ModernActionParser(',
                f'obs_builder={config["obs_builder"]},\n        action_parser=ModernActionParser('
            )
        
        # Fix action_parser instantiation
        action_parser_pattern = r'action_parser=ModernActionParser\([^)]*\)'
        if re.search(action_parser_pattern, content):
            content = re.sub(
                action_parser_pattern,
                f'action_parser={config["action_parser"]}',
                content
            )
        
        # Fix reward weights for JSTN playstyle
        for reward_key, reward_value in config['reward_weights'].items():
            # Look for existing reward weight and update it
            pattern = rf'{reward_key}_w=\d+(?:\.\d+)?'
            if re.search(pattern, content):
                content = re.sub(
                    pattern,
                    f'{reward_key}_w={reward_value}',
                    content
                )
            else:
                # Add reward weight if not found
                content = content.replace(
                    'zero_sum=ZERO_SUM,',
                    f'zero_sum=ZERO_SUM,\n                        {reward_key}_w={reward_value},'
                )
        
        # Add JSTN-specific comments
        jstn_comment = f"""
# JSTN (Justin) Training Configuration
# Optimized for {mechanic_name} mechanics with jstn's playstyle
# Aerial aggression, flip reset mastery, double tap precision
"""
        
        # Add comment at the top of the file
        content = jstn_comment + content
        
        # Write fixed content back to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Fixed {filepath}")
        return True
    
    def fix_constants_file(self, filepath, content):
        """Fix constants files for JSTN training"""
        print(f"🔧 Fixing constants file: {filepath}")
        
        # Add JSTN-specific comment to constants
        jstn_comment = f"""
# JSTN (Justin) Training Constants
# Optimized for {filepath.replace('Constants_', '').replace('.py', '')} mechanics
# Enhanced for jstn's playstyle - aerial aggression, flip reset mastery, double tap precision
"""
        
        # Add comment at the top of the file
        content = jstn_comment + content
        
        # Write fixed content back to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Fixed constants file: {filepath}")
        return True
    
    def fix_all_files(self):
        """Fix all files in the list"""
        print("🔧 Fixing all files for JSTN training...")
        
        fixed_count = 0
        for filepath in self.files_to_fix:
            if self.fix_file(filepath):
                fixed_count += 1
        
        print(f"✅ Fixed {fixed_count}/{len(self.files_to_fix)} files")
        print("🎯 All files now optimized for JSTN playstyle!")
    
    def create_jstn_launcher(self):
        """Create a simple JSTN launcher script"""
        launcher_content = '''#!/usr/bin/env python3
"""
Simple JSTN Training Launcher
Starts the main learner and worker for JSTN training
"""

import subprocess
import sys
import time
import os

def main():
    print("🏆 JSTN Training Launcher")
    print("🎯 Starting JSTN training...")
    
    # Start main learner
    print("🧠 Starting main learner...")
    learner_process = subprocess.Popen([sys.executable, 'learner.py'])
    
    # Wait a bit
    time.sleep(2)
    
    # Start main worker
    print("🚀 Starting main worker...")
    worker_process = subprocess.Popen([sys.executable, 'worker.py'])
    
    print("✅ JSTN training started!")
    print("📊 Press Ctrl+C to stop")
    
    try:
        # Wait for processes
        learner_process.wait()
        worker_process.wait()
    except KeyboardInterrupt:
        print("\\n⏹️  Stopping training...")
        learner_process.terminate()
        worker_process.terminate()
        print("✅ Training stopped")

if __name__ == "__main__":
    main()
'''
        
        with open('start_jstn_training.py', 'w', encoding='utf-8') as f:
            f.write(launcher_content)
        
        print("✅ Created start_jstn_training.py")

def main():
    """Main function"""
    print("🏆 JSTN File Fixer")
    print("=" * 50)
    print("🔧 Fixing all files for JSTN training...")
    print("🎯 Making the bot play like jstn (Justin)!")
    
    fixer = JSTNFileFixer()
    fixer.fix_all_files()
    fixer.create_jstn_launcher()
    
    print("✅ All files fixed for JSTN training!")
    print("🚀 Run 'python start_jstn_training.py' to start training!")

if __name__ == "__main__":
    main()
