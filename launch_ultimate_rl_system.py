#!/usr/bin/env python3
"""
Launch Ultimate RL Learning System
Combines all learning components with PPO replay learning
"""

import time
import threading
from datetime import datetime
from ultimate_rl_learning_machine import UltimateRLLearningMachine
from ppo_replay_learner import PPOReplayLearner

class UltimateRLSystem:
    """Ultimate RL learning system combining all components"""
    
    def __init__(self):
        # Initialize all learning components
        self.ultimate_machine = UltimateRLLearningMachine()
        self.ppo_replay_learner = PPOReplayLearner()
        
        # System state
        self.is_running = False
        self.start_time = None
        self.hourly_reports = []
        
        print("🚀 Ultimate RL System Initialized!")
        print("🎯 Components: Live Streams + YouTube + PPO Replay + Controller Practice")
        print("⏰ Ready for 1-hour monitoring session")
    
    def start_ultimate_system(self):
        """Start the complete ultimate RL learning system"""
        print("\n🚀 LAUNCHING ULTIMATE RL LEARNING SYSTEM")
        print("=" * 70)
        print("📺 Phase 1: Live stream monitoring")
        print("📱 Phase 2: YouTube fallback learning")
        print("🎮 Phase 3: PPO replay learning with -0.5s delay")
        print("🎯 Phase 4: Controller practice and timing")
        print("⏰ Phase 5: 1-hour monitoring and analysis")
        print("🧠 Phase 6: Complete learning integration")
        
        self.is_running = True
        self.start_time = time.time()
        
        # Start ultimate learning machine
        self.ultimate_machine.start_ultimate_learning()
        
        # Start monitoring thread
        monitor_thread = threading.Thread(target=self.monitor_system)
        monitor_thread.daemon = True
        monitor_thread.start()
        
        print("✅ All systems launched successfully!")
        print("🎯 Ultimate RL learning in progress...")
    
    def monitor_system(self):
        """Monitor the complete system for 1 hour"""
        print("\n📊 ULTIMATE RL SYSTEM MONITORING")
        print("=" * 50)
        print("⏰ 1-hour monitoring session started")
        print("🔴 All learning systems active")
        print("📈 Real-time performance tracking")
        print()
        
        start_time = time.time()
        last_report_time = start_time
        
        while self.is_running:
            current_time = time.time()
            elapsed = current_time - start_time
            
            # Check if 1 hour has passed
            if elapsed >= 3600:  # 1 hour
                print("\n⏰ 1 HOUR COMPLETE!")
                self.generate_final_report()
                self.save_all_data()
                self.stop_system()
                break
            
            # Generate hourly reports
            if current_time - last_report_time >= 3600:  # Every hour
                report = self.generate_hourly_report()
                self.hourly_reports.append(report)
                last_report_time = current_time
            
            # Show progress
            hours_elapsed = elapsed / 3600
            minutes_elapsed = (elapsed % 3600) / 60
            
            print(f"\r⏰ Monitoring: {hours_elapsed:.1f}h {minutes_elapsed:.0f}m | "
                  f"Actions: {self.ultimate_machine.total_actions} | "
                  f"Replays: {self.ppo_replay_learner.total_replays} | "
                  f"Episodes: {self.ultimate_machine.ppo_episodes}", 
                  end="", flush=True)
            
            time.sleep(10)  # Update every 10 seconds
    
    def generate_hourly_report(self):
        """Generate comprehensive hourly report"""
        print("\n" + "="*80)
        print("📊 HOURLY SYSTEM REPORT")
        print("="*80)
        
        # Ultimate machine stats
        ultimate_stats = {
            'total_actions': self.ultimate_machine.total_actions,
            'learned_actions': len(self.ultimate_machine.learned_actions),
            'ppo_episodes': self.ultimate_machine.ppo_episodes,
            'mode_confidence': self.ultimate_machine.mode_confidence
        }
        
        # PPO replay stats
        replay_stats = {
            'total_replays': self.ppo_replay_learner.total_replays,
            'replay_accuracy': self.ppo_replay_learner.replay_accuracy,
            'timing_accuracy': self.ppo_replay_learner.timing_accuracy,
            'controller_accuracy': self.ppo_replay_learner.controller_accuracy,
            'learned_sequences': len(self.ppo_replay_learner.learned_sequences)
        }
        
        print(f"⏰ Hour: {datetime.now().strftime('%H:%M:%S')}")
        print(f"🎮 Total Actions: {ultimate_stats['total_actions']}")
        print(f"🔄 Total Replays: {replay_stats['total_replays']}")
        print(f"🧠 PPO Episodes: {ultimate_stats['ppo_episodes']}")
        print(f"📚 Learned Actions: {ultimate_stats['learned_actions']}")
        print(f"🎯 Learned Sequences: {replay_stats['learned_sequences']}")
        
        # Performance metrics
        print(f"\n📈 PERFORMANCE METRICS:")
        print("-" * 30)
        print(f"   🎯 Replay Accuracy: {replay_stats['replay_accuracy']:.1%}")
        print(f"   ⏱️ Timing Accuracy: {replay_stats['timing_accuracy']:.1%}")
        print(f"   🎮 Controller Accuracy: {replay_stats['controller_accuracy']:.1%}")
        
        # Mode confidence
        print(f"\n🎮 MODE CONFIDENCE:")
        print("-" * 20)
        for mode, confidence in ultimate_stats['mode_confidence'].items():
            confidence_pct = confidence * 100
            print(f"   {mode}: {confidence_pct:.1f}%")
        
        # Rank prediction
        predicted_rank = self.ultimate_machine.predict_rank()
        print(f"\n🏆 PREDICTED RANK:")
        print("-" * 20)
        print(f"   🎯 Rank: {predicted_rank['rank']}")
        print(f"   📊 Confidence: {predicted_rank['confidence']:.1f}%")
        print(f"   💡 Reasoning: {predicted_rank['reasoning']}")
        
        print("="*80)
        
        return {
            'timestamp': datetime.now().isoformat(),
            'ultimate_stats': ultimate_stats,
            'replay_stats': replay_stats,
            'predicted_rank': predicted_rank
        }
    
    def generate_final_report(self):
        """Generate final comprehensive report after 1 hour"""
        print("\n" + "="*100)
        print("🏆 FINAL ULTIMATE RL SYSTEM REPORT - 1 HOUR COMPLETE")
        print("="*100)
        
        # Overall performance
        total_time = time.time() - self.start_time
        hours = total_time / 3600
        
        print(f"⏰ Total Runtime: {hours:.2f} hours")
        print(f"🎮 Total Actions Learned: {self.ultimate_machine.total_actions}")
        print(f"🔄 Total Replays: {self.ppo_replay_learner.total_replays}")
        print(f"🧠 Total PPO Episodes: {self.ultimate_machine.ppo_episodes}")
        print(f"📚 Unique Actions: {len(self.ultimate_machine.learned_actions)}")
        print(f"🎯 Learned Sequences: {len(self.ppo_replay_learner.learned_sequences)}")
        
        # Performance summary
        print(f"\n📊 PERFORMANCE SUMMARY:")
        print("-" * 30)
        print(f"   🎯 Replay Accuracy: {self.ppo_replay_learner.replay_accuracy:.1%}")
        print(f"   ⏱️ Timing Accuracy: {self.ppo_replay_learner.timing_accuracy:.1%}")
        print(f"   🎮 Controller Accuracy: {self.ppo_replay_learner.controller_accuracy:.1%}")
        print(f"   📈 Learning Rate: {self.ultimate_machine.learning_rate:.6f}")
        
        # Top learned actions
        if self.ultimate_machine.learned_actions:
            sorted_actions = sorted(
                self.ultimate_machine.learned_actions.items(),
                key=lambda x: x[1]['avg_reward'],
                reverse=True
            )
            
            print(f"\n🏆 TOP 10 LEARNED ACTIONS:")
            print("-" * 40)
            
            for i, (action, data) in enumerate(sorted_actions[:10]):
                if data['avg_reward'] > 0.8:
                    skill_level = "🔥 MASTERED"
                elif data['avg_reward'] > 0.6:
                    skill_level = "✅ GOOD"
                else:
                    skill_level = "📚 LEARNING"
                
                print(f"   {i+1:2d}. {action:<20} | {data['avg_reward']:.3f} | {skill_level}")
        
        # Top learned sequences
        if self.ppo_replay_learner.learned_sequences:
            sorted_sequences = sorted(
                self.ppo_replay_learner.learned_sequences.items(),
                key=lambda x: x[1]['avg_reward'],
                reverse=True
            )
            
            print(f"\n🎯 TOP 5 LEARNED SEQUENCES:")
            print("-" * 40)
            
            for i, (sequence, data) in enumerate(sorted_sequences[:5]):
                if data['avg_reward'] > 1.5:
                    skill_level = "🔥 MASTERED"
                elif data['avg_reward'] > 1.0:
                    skill_level = "✅ GOOD"
                else:
                    skill_level = "📚 LEARNING"
                
                print(f"   {i+1}. {sequence}")
                print(f"      Reward: {data['avg_reward']:.3f} | Count: {data['count']} | {skill_level}")
        
        # Final rank prediction
        final_rank = self.ultimate_machine.predict_rank()
        print(f"\n🏆 FINAL RANK PREDICTION:")
        print("-" * 30)
        print(f"   🎯 Rank: {final_rank['rank']}")
        print(f"   📊 Confidence: {final_rank['confidence']:.1f}%")
        print(f"   💡 Reasoning: {final_rank['reasoning']}")
        
        # Improvement recommendations
        self.generate_improvement_recommendations()
        
        print("="*100)
    
    def generate_improvement_recommendations(self):
        """Generate recommendations for improvement"""
        print(f"\n💡 IMPROVEMENT RECOMMENDATIONS:")
        print("-" * 40)
        
        recommendations = []
        
        # Check replay accuracy
        if self.ppo_replay_learner.replay_accuracy < 0.8:
            recommendations.append("🎯 Improve replay timing - current accuracy below 80%")
        
        # Check controller accuracy
        if self.ppo_replay_learner.controller_accuracy < 0.8:
            recommendations.append("🎮 Enhance controller practice - focus on input precision")
        
        # Check timing accuracy
        if self.ppo_replay_learner.timing_accuracy < 0.8:
            recommendations.append("⏱️ Improve timing patterns - work on action sequencing")
        
        # Check learning rate
        if self.ultimate_machine.learning_rate < 0.0001:
            recommendations.append("📈 Increase learning rate - system learning too slowly")
        
        # Check mode confidence
        for mode, confidence in self.ultimate_machine.mode_confidence.items():
            if confidence < 0.5:
                recommendations.append(f"🎮 Focus on {mode} mode - confidence below 50%")
        
        # Check total actions
        if self.ultimate_machine.total_actions < 1000:
            recommendations.append("📚 Increase data collection - need more action examples")
        
        # Check sequences
        if len(self.ppo_replay_learner.learned_sequences) < 10:
            recommendations.append("🎯 Learn more action sequences - current count too low")
        
        if recommendations:
            for i, rec in enumerate(recommendations, 1):
                print(f"   {i}. {rec}")
        else:
            print("   🎉 System performing excellently! No major improvements needed.")
        
        # Advanced recommendations
        print(f"\n🚀 ADVANCED IMPROVEMENTS:")
        print("-" * 30)
        print("   1. 🔴 Add real Twitch API integration for live stream detection")
        print("   2. 📱 Implement actual YouTube API for content analysis")
        print("   3. 🎮 Add real controller input detection and mapping")
        print("   4. 🧠 Implement advanced PPO algorithms (SAC, TD3)")
        print("   5. 🎯 Add computer vision for car position tracking")
        print("   6. ⏱️ Implement adaptive timing based on game state")
        print("   7. 🎮 Add haptic feedback for controller practice")
        print("   8. 📊 Implement real-time performance visualization")
        print("   9. 🧠 Add meta-learning for faster adaptation")
        print("   10. 🎯 Implement opponent analysis and counter-strategies")
    
    def save_all_data(self):
        """Save all learning data from both systems"""
        print("\n💾 SAVING ALL LEARNING DATA...")
        
        # Save ultimate machine data
        self.ultimate_machine.save_learning_data()
        
        # Save PPO replay data
        self.ppo_replay_learner.save_replay_data()
        
        # Save combined system data
        combined_data = {
            'hourly_reports': self.hourly_reports,
            'total_runtime': time.time() - self.start_time,
            'final_rank': self.ultimate_machine.predict_rank(),
            'timestamp': datetime.now().isoformat()
        }
        
        filename = f"ultimate_rl_system_complete_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pkl"
        
        try:
            import pickle
            with open(filename, 'wb') as f:
                pickle.dump(combined_data, f)
            print(f"✅ Combined system data saved to {filename}")
        except Exception as e:
            print(f"❌ Error saving combined data: {e}")
    
    def stop_system(self):
        """Stop the complete system"""
        self.is_running = False
        self.ultimate_machine.stop_learning()
        self.ppo_replay_learner.stop_replay_learning()
        print("\n⏹️ Ultimate RL system stopped")

def main():
    """Main function"""
    print("🚀 ULTIMATE RL LEARNING SYSTEM LAUNCHER")
    print("=" * 70)
    print("🎯 Goal: Best RL Player Ever")
    print("📺 Sources: Live streams + YouTube + PPO Replay")
    print("🎮 Features: Controller practice + Timing learning")
    print("⏰ Duration: 1-hour monitoring session")
    print("🚀 Launching ultimate system...")
    
    system = UltimateRLSystem()
    
    try:
        system.start_ultimate_system()
        
        # Keep running until 1 hour is complete
        while system.is_running:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n⏹️ System interrupted by user")
        system.stop_system()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        system.stop_system()

if __name__ == "__main__":
    main()
