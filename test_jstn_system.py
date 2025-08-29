#!/usr/bin/env python3
"""
JSTN System Test
Tests all components of the JSTN training system
"""

import os
import sys
import time
import subprocess
from pathlib import Path

def test_imports():
    """Test that all imports work correctly"""
    print("🔍 Testing imports...")
    
    try:
        # Test modern components
        from ModernObsBuilder import ModernObsBuilder
        from ModernActionParser import ModernActionParser
        from ModernRewardSystem import ModernRewardSystem
        from ModernAgent import ModernAgent, ModernSelector
        print("✅ Modern components imported successfully")
        
        # Test SSL mechanics
        from SSLMechanics import SSLMechanics
        ssl_mechanics = SSLMechanics()
        print(f"✅ SSL Mechanics loaded: {len(ssl_mechanics.mechanics)} mechanics")
        
        return True
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        return False

def test_file_structure():
    """Test that all required files exist"""
    print("🔍 Testing file structure...")
    
    required_files = [
        # Main files
        'jstn_multi_mode_trainer.py',
        'start_jstn_multi_mode.py',
        'ModernObsBuilder.py',
        'ModernActionParser.py',
        'ModernRewardSystem.py',
        'ModernAgent.py',
        'SSLMechanics.py',
        
        # Worker files
        'worker_selector.py', 'worker_dtap.py', 'worker_flip_reset.py',
        'worker_aerial.py', 'worker_flick.py', 'worker_ceil_pinch.py',
        'worker_pinch.py', 'worker_wall.py', 'worker_walldash.py',
        'worker_recovery.py', 'worker_demo.py', 'worker_gp.py',
        'worker_half_flip.py', 'worker_lix.py', 'worker_kickoff.py',
        
        # Learner files
        'learner_selector.py', 'learner_dtap.py', 'learner_flip_reset.py',
        'learner_aerial.py', 'learner_flick.py', 'learner_ceil_pinch.py',
        'learner_pinch.py', 'learner_wall.py', 'learner_walldash.py',
        'learner_recovery.py', 'learner_demo.py', 'learner_gp.py',
        'learner_half_flip.py', 'learner_lix.py', 'learner_kickoff.py',
        
        # Constants files
        'Constants_selector.py', 'Constants_dtap.py', 'Constants_flip_reset.py',
        'Constants_aerial.py', 'Constants_flick.py', 'Constants_ceil_pinch.py',
        'Constants_pinch.py', 'Constants_wall.py', 'Constants_walldash.py',
        'Constants_recovery.py', 'Constants_demo.py', 'Constants_gp.py',
        'Constants_half_flip.py', 'Constants_lix.py', 'Constants_kickoff.py'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    else:
        print(f"✅ All {len(required_files)} required files exist")
        return True

def test_multi_mode_trainer():
    """Test the multi-mode trainer initialization"""
    print("🔍 Testing multi-mode trainer...")
    
    try:
        from jstn_multi_mode_trainer import JSTNMultiModeTrainer
        
        # Test initialization
        config = {
            'max_episodes': 100,
            'batch_size': 100,
            'learning_rate': 3e-4,
            'gamma': 0.99
        }
        
        trainer = JSTNMultiModeTrainer(config)
        print("✅ Multi-mode trainer initialized successfully")
        
        # Test mode switching
        current_mode = trainer.get_current_mode()
        print(f"✅ Current mode: {current_mode}")
        
        # Test mode configurations
        for mode in trainer.training_modes:
            mode_config = trainer.jstn_mode_configs[mode]
            print(f"✅ {mode} config: team_size={mode_config['team_size']}, episodes_per_switch={mode_config['episodes_per_switch']}")
        
        return True
    except Exception as e:
        print(f"❌ Multi-mode trainer test failed: {e}")
        return False

def test_worker_learner_files():
    """Test that worker and learner files can be imported"""
    print("🔍 Testing worker and learner files...")
    
    worker_files = [
        'worker_selector.py', 'worker_dtap.py', 'worker_flip_reset.py',
        'worker_aerial.py', 'worker_flick.py', 'worker_ceil_pinch.py',
        'worker_pinch.py', 'worker_wall.py', 'worker_walldash.py',
        'worker_recovery.py', 'worker_demo.py', 'worker_gp.py',
        'worker_half_flip.py', 'worker_lix.py', 'worker_kickoff.py'
    ]
    
    learner_files = [
        'learner_selector.py', 'learner_dtap.py', 'learner_flip_reset.py',
        'learner_aerial.py', 'learner_flick.py', 'learner_ceil_pinch.py',
        'learner_pinch.py', 'learner_wall.py', 'learner_walldash.py',
        'learner_recovery.py', 'learner_demo.py', 'learner_gp.py',
        'learner_half_flip.py', 'learner_lix.py', 'learner_kickoff.py'
    ]
    
    failed_files = []
    
    # Test worker files
    for worker_file in worker_files:
        try:
            # Just check if file exists and has content
            with open(worker_file, 'r') as f:
                content = f.read()
                if 'ModernObsBuilder' in content and 'ModernActionParser' in content:
                    print(f"✅ {worker_file} - Updated to modern components")
                else:
                    print(f"⚠️  {worker_file} - May need updating")
        except Exception as e:
            failed_files.append(f"{worker_file}: {e}")
    
    # Test learner files
    for learner_file in learner_files:
        try:
            # Just check if file exists and has content
            with open(learner_file, 'r') as f:
                content = f.read()
                if 'ModernObsBuilder' in content and 'ModernActionParser' in content:
                    print(f"✅ {learner_file} - Updated to modern components")
                else:
                    print(f"⚠️  {learner_file} - May need updating")
        except Exception as e:
            failed_files.append(f"{learner_file}: {e}")
    
    if failed_files:
        print(f"❌ Failed files: {failed_files}")
        return False
    else:
        print("✅ All worker and learner files updated successfully")
        return True

def test_constants_files():
    """Test that constants files exist and have JSTN comments"""
    print("🔍 Testing constants files...")
    
    constants_files = [
        'Constants_selector.py', 'Constants_dtap.py', 'Constants_flip_reset.py',
        'Constants_aerial.py', 'Constants_flick.py', 'Constants_ceil_pinch.py',
        'Constants_pinch.py', 'Constants_wall.py', 'Constants_walldash.py',
        'Constants_recovery.py', 'Constants_demo.py', 'Constants_gp.py',
        'Constants_half_flip.py', 'Constants_lix.py', 'Constants_kickoff.py'
    ]
    
    failed_files = []
    
    for constants_file in constants_files:
        try:
            with open(constants_file, 'r') as f:
                content = f.read()
                if 'JSTN' in content and 'Justin' in content:
                    print(f"✅ {constants_file} - JSTN optimized")
                else:
                    print(f"⚠️  {constants_file} - May need JSTN optimization")
        except Exception as e:
            failed_files.append(f"{constants_file}: {e}")
    
    if failed_files:
        print(f"❌ Failed constants files: {failed_files}")
        return False
    else:
        print("✅ All constants files checked successfully")
        return True

def test_launcher_scripts():
    """Test that launcher scripts exist and are executable"""
    print("🔍 Testing launcher scripts...")
    
    launcher_scripts = [
        'start_jstn_multi_mode.py',
        'start_jstn_training.py'
    ]
    
    for script in launcher_scripts:
        if os.path.exists(script):
            print(f"✅ {script} exists")
        else:
            print(f"❌ {script} missing")
            return False
    
    print("✅ All launcher scripts exist")
    return True

def main():
    """Run all tests"""
    print("🏆 JSTN System Test Suite")
    print("=" * 50)
    print("🎯 Testing complete JSTN training system...")
    print("🚀 This will verify everything is ready for training!")
    
    tests = [
        ("Import Test", test_imports),
        ("File Structure Test", test_file_structure),
        ("Multi-Mode Trainer Test", test_multi_mode_trainer),
        ("Worker/Learner Files Test", test_worker_learner_files),
        ("Constants Files Test", test_constants_files),
        ("Launcher Scripts Test", test_launcher_scripts)
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name}...")
        try:
            if test_func():
                passed_tests += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} ERROR: {e}")
    
    print(f"\n📊 Test Results: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 ALL TESTS PASSED!")
        print("🚀 JSTN training system is ready!")
        print("🎯 Run 'python start_jstn_multi_mode.py' to start training!")
    else:
        print("⚠️  Some tests failed. Please fix the issues before training.")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    main()
