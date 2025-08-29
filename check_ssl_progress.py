#!/usr/bin/env python3
"""
Quick SSL Progress Checker
Shows current training status and SSL progress
"""

import pickle
import glob
import time
from datetime import datetime

def check_ssl_progress():
    """Check current SSL training progress"""
    print("🏆 SSL PROGRESS CHECK")
    print("=" * 50)
    
    # Find latest training file
    files = glob.glob('real_data_training_*.pkl')
    if not files:
        print("❌ No training data found")
        return
    
    latest_file = max(files, key=lambda x: x.split('_')[-1].split('.')[0])
    print(f"📁 Latest training file: {latest_file}")
    
    try:
        with open(latest_file, 'rb') as f:
            data = pickle.load(f)
        
        print(f"\n📊 CURRENT TRAINING STATUS:")
        print("-" * 30)
        print(f"🎮 Total Actions: {data.get('total_actions', 0)}")
        print(f"📡 Real Data Points: {data.get('real_data_count', 0)}")
        print(f"🧠 Total Episodes: {data.get('total_episodes', 0)}")
        print(f"❌ Errors: {data.get('error_count', 0)}")
        
        # SSL Requirements
        ssl_requirements = {
            '1s': {'min_actions': 500, 'min_accuracy': 0.95, 'min_skills': 15},
            '2s': {'min_actions': 600, 'min_accuracy': 0.93, 'min_skills': 18},
            '3s': {'min_actions': 700, 'min_accuracy': 0.90, 'min_skills': 20}
        }
        
        print(f"\n🎮 MODE SSL PROGRESS:")
        print("-" * 30)
        
        mode_performance = data.get('mode_performance', {})
        
        for mode, requirements in ssl_requirements.items():
            perf = mode_performance.get(mode, {})
            actions = perf.get('actions', 0)
            accuracy = perf.get('accuracy', 0.0)
            skills = len(perf.get('skills_learned', []))
            
            # Calculate progress
            action_progress = min(100, (actions / requirements['min_actions']) * 100)
            accuracy_progress = min(100, (accuracy / requirements['min_accuracy']) * 100)
            skill_progress = min(100, (skills / requirements['min_skills']) * 100)
            overall_progress = (action_progress + accuracy_progress + skill_progress) / 3
            
            print(f"   {mode.upper()}:")
            print(f"      Actions: {actions}/{requirements['min_actions']} ({action_progress:.1f}%)")
            print(f"      Accuracy: {accuracy:.1%} (need {requirements['min_accuracy']:.1%})")
            print(f"      Skills: {skills}/{requirements['min_skills']} ({skill_progress:.1f}%)")
            print(f"      Overall: {overall_progress:.1f}%")
            
            if overall_progress >= 100:
                print(f"      🏆 SSL READY!")
            elif overall_progress >= 80:
                print(f"      🔥 Almost SSL!")
            elif overall_progress >= 60:
                print(f"      ⚡ Good progress!")
            else:
                print(f"      🚀 Getting started!")
        
        # SSL Prediction
        print(f"\n🔮 SSL ACHIEVEMENT PREDICTION:")
        print("-" * 30)
        
        total_actions = data.get('total_actions', 0)
        if total_actions > 0:
            # Estimate based on current learning rate
            actions_per_hour = total_actions / max(1, (time.time() - data.get('training_time', 0)) / 3600)
            total_actions_needed = sum(req['min_actions'] for req in ssl_requirements.values())
            
            if actions_per_hour > 0:
                hours_to_ssl = total_actions_needed / actions_per_hour
                ssl_time = datetime.now().timestamp() + (hours_to_ssl * 3600)
                ssl_datetime = datetime.fromtimestamp(ssl_time)
                
                print(f"📈 Current learning rate: {actions_per_hour:.1f} actions/hour")
                print(f"🎯 Actions needed: {total_actions_needed - total_actions}")
                print(f"⏰ Predicted SSL time: {ssl_datetime.strftime('%Y-%m-%d %H:%M:%S')}")
                
                # Check if on track for tomorrow
                tomorrow = datetime.now().timestamp() + (24 * 3600)
                if ssl_time <= tomorrow:
                    print("✅ ON TRACK FOR SSL BY TOMORROW!")
                else:
                    hours_over = (ssl_time - tomorrow) / 3600
                    print(f"⚠️ {hours_over:.1f} hours behind schedule")
            else:
                print("⏳ Need more data for prediction")
        else:
            print("⏳ Training just started")
        
        print("=" * 50)
        
    except Exception as e:
        print(f"❌ Error reading training data: {e}")

if __name__ == "__main__":
    check_ssl_progress()
