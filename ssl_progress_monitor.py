#!/usr/bin/env python3
"""
SSL Progress Monitor
Monitors the real data trainer progress toward SSL
Tracks learning speed and predicts SSL achievement time
"""

import time
import os
import glob
import pickle
from datetime import datetime, timedelta
import numpy as np

class SSLProgressMonitor:
    """Monitor progress toward SSL achievement"""
    
    def __init__(self):
        self.start_time = time.time()
        self.ssl_target_time = 24 * 3600  # 24 hours from now
        self.ssl_requirements = {
            '1s': {'min_actions': 500, 'min_accuracy': 0.95, 'min_skills': 15},
            '2s': {'min_actions': 600, 'min_accuracy': 0.93, 'min_skills': 18},
            '3s': {'min_actions': 700, 'min_accuracy': 0.90, 'min_skills': 20}
        }
        
        print("🏆 SSL PROGRESS MONITOR INITIALIZED")
        print("🎯 Target: SSL by tomorrow (24 hours)")
        print("📊 Monitoring: Real data training progress")
        print("🚀 Starting SSL tracking...")
    
    def monitor_progress(self):
        """Monitor training progress toward SSL"""
        print("\n🏆 SSL PROGRESS MONITORING")
        print("=" * 60)
        
        while True:
            try:
                # Check for latest training data
                latest_data = self.get_latest_training_data()
                
                if latest_data:
                    self.analyze_ssl_progress(latest_data)
                    self.predict_ssl_achievement(latest_data)
                    self.generate_ssl_recommendations(latest_data)
                else:
                    print("⏳ Waiting for training data...")
                
                time.sleep(60)  # Check every minute
                
            except KeyboardInterrupt:
                print("\n⏹️ SSL monitoring stopped")
                break
            except Exception as e:
                print(f"❌ SSL monitoring error: {e}")
                time.sleep(60)
    
    def get_latest_training_data(self):
        """Get the latest training data file"""
        try:
            # Look for real data training files
            pattern = "real_data_training_*.pkl"
            files = glob.glob(pattern)
            
            if not files:
                return None
            
            # Get the most recent file
            latest_file = max(files, key=os.path.getctime)
            
            with open(latest_file, 'rb') as f:
                data = pickle.load(f)
            
            return data
            
        except Exception as e:
            print(f"❌ Error loading training data: {e}")
            return None
    
    def analyze_ssl_progress(self, data):
        """Analyze current progress toward SSL"""
        print(f"\n📊 SSL PROGRESS ANALYSIS - {datetime.now().strftime('%H:%M:%S')}")
        print("=" * 60)
        
        total_time = time.time() - self.start_time
        hours_elapsed = total_time / 3600
        
        print(f"⏰ Time Elapsed: {hours_elapsed:.2f} hours")
        print(f"🎮 Total Actions: {data.get('total_actions', 0)}")
        print(f"📡 Real Data Points: {data.get('real_data_count', 0)}")
        print(f"❌ Errors: {data.get('error_count', 0)}")
        
        # Analyze each mode
        mode_performance = data.get('mode_performance', {})
        
        print(f"\n🎮 MODE SSL PROGRESS:")
        print("-" * 40)
        
        for mode, requirements in self.ssl_requirements.items():
            perf = mode_performance.get(mode, {})
            actions = perf.get('actions', 0)
            accuracy = perf.get('accuracy', 0.0)
            skills = len(perf.get('skills_learned', []))
            
            # Calculate progress percentages
            action_progress = min(100, (actions / requirements['min_actions']) * 100)
            accuracy_progress = min(100, (accuracy / requirements['min_accuracy']) * 100)
            skill_progress = min(100, (skills / requirements['min_skills']) * 100)
            
            # Overall progress
            overall_progress = (action_progress + accuracy_progress + skill_progress) / 3
            
            print(f"   {mode.upper()}:")
            print(f"      Actions: {actions}/{requirements['min_actions']} ({action_progress:.1f}%)")
            print(f"      Accuracy: {accuracy:.1%}/{requirements['min_accuracy']:.1%} ({accuracy_progress:.1f}%)")
            print(f"      Skills: {skills}/{requirements['min_skills']} ({skill_progress:.1f}%)")
            print(f"      Overall: {overall_progress:.1f}%")
            
            # SSL readiness
            if overall_progress >= 100:
                print(f"      🏆 SSL READY!")
            elif overall_progress >= 80:
                print(f"      🔥 Almost SSL!")
            elif overall_progress >= 60:
                print(f"      ⚡ Good progress!")
            elif overall_progress >= 40:
                print(f"      📈 Making progress!")
            else:
                print(f"      🚀 Getting started!")
    
    def predict_ssl_achievement(self, data):
        """Predict when SSL will be achieved"""
        print(f"\n🔮 SSL ACHIEVEMENT PREDICTION:")
        print("-" * 40)
        
        total_time = time.time() - self.start_time
        hours_elapsed = total_time / 3600
        
        mode_performance = data.get('mode_performance', {})
        
        predictions = []
        
        for mode, requirements in self.ssl_requirements.items():
            perf = mode_performance.get(mode, {})
            actions = perf.get('actions', 0)
            accuracy = perf.get('accuracy', 0.0)
            skills = len(perf.get('skills_learned', []))
            
            # Calculate current progress
            action_progress = min(100, (actions / requirements['min_actions']) * 100)
            accuracy_progress = min(100, (accuracy / requirements['min_accuracy']) * 100)
            skill_progress = min(100, (skills / requirements['min_skills']) * 100)
            overall_progress = (action_progress + accuracy_progress + skill_progress) / 3
            
            # Predict completion time
            if overall_progress > 0:
                # Linear extrapolation
                completion_hours = (100 / overall_progress) * hours_elapsed
                completion_time = datetime.now() + timedelta(hours=completion_hours - hours_elapsed)
                predictions.append(completion_time)
                
                print(f"   {mode.upper()}: {completion_time.strftime('%H:%M:%S')} ({completion_hours:.1f}h total)")
            else:
                print(f"   {mode.upper()}: Not enough data yet")
        
        # Overall prediction
        if predictions:
            avg_completion = sum(predictions, timedelta()) / len(predictions)
            print(f"\n🏆 PREDICTED SSL ACHIEVEMENT: {avg_completion.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Check if on track for tomorrow
            tomorrow = datetime.now() + timedelta(days=1)
            if avg_completion <= tomorrow:
                print("✅ ON TRACK FOR SSL BY TOMORROW!")
            else:
                hours_over = (avg_completion - tomorrow).total_seconds() / 3600
                print(f"⚠️ {hours_over:.1f} hours behind schedule")
        else:
            print("⏳ Need more data for prediction")
    
    def generate_ssl_recommendations(self, data):
        """Generate recommendations to reach SSL faster"""
        print(f"\n💡 SSL ACCELERATION RECOMMENDATIONS:")
        print("-" * 40)
        
        mode_performance = data.get('mode_performance', {})
        recommendations = []
        
        for mode, requirements in self.ssl_requirements.items():
            perf = mode_performance.get(mode, {})
            actions = perf.get('actions', 0)
            accuracy = perf.get('accuracy', 0.0)
            skills = len(perf.get('skills_learned', []))
            
            # Check what needs improvement
            if actions < requirements['min_actions']:
                recommendations.append(f"📚 {mode.upper()}: Increase action learning (need {requirements['min_actions'] - actions} more)")
            
            if accuracy < requirements['min_accuracy']:
                recommendations.append(f"🎯 {mode.upper()}: Improve accuracy (need {requirements['min_accuracy'] - accuracy:.3f} more)")
            
            if skills < requirements['min_skills']:
                recommendations.append(f"🧠 {mode.upper()}: Learn more skills (need {requirements['min_skills'] - skills} more)")
        
        # General recommendations
        if data.get('real_data_count', 0) < 100:
            recommendations.append("📡 Increase real data collection from streams")
        
        if data.get('error_count', 0) > 5:
            recommendations.append("🔧 Fix system errors to improve learning")
        
        if recommendations:
            for i, rec in enumerate(recommendations[:5], 1):
                print(f"   {i}. {rec}")
        else:
            print("   🎉 All systems optimal for SSL achievement!")
        
        # Next steps
        print(f"\n🚀 NEXT STEPS FOR SSL:")
        print("-" * 25)
        print("   1. 🔴 Keep real data streams active")
        print("   2. 🎮 Focus on weak modes")
        print("   3. 📊 Monitor accuracy improvements")
        print("   4. 🧠 Learn advanced mechanics")
        print("   5. 🏆 Prepare for SSL injection")
        
        print("=" * 60)

def main():
    """Main function"""
    print("🏆 SSL PROGRESS MONITOR")
    print("=" * 60)
    print("🎯 Target: SSL by tomorrow")
    print("📊 Monitoring: Real data training")
    print("🚀 Starting SSL progress tracking...")
    
    monitor = SSLProgressMonitor()
    
    try:
        monitor.monitor_progress()
        
    except KeyboardInterrupt:
        print("\n⏹️ SSL monitoring stopped by user")
    except Exception as e:
        print(f"\n❌ Critical Error: {e}")

if __name__ == "__main__":
    main()
