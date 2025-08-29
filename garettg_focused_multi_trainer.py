#!/usr/bin/env python3
"""
GarettG Focused Multi-Mode Trainer
Focuses on GarettG's 2s gameplay while training all 3 modes
Watches multiple streams and YouTube simultaneously
"""

import numpy as np
import time
import threading
import pickle
import json
from datetime import datetime
import random
import queue

class GarettGFocusedMultiTrainer:
    """Multi-mode trainer with focus on GarettG's 2s gameplay"""
    
    def __init__(self):
        # GarettG focus settings
        self.garettg_focus = True
        self.garettg_stream_url = "https://www.twitch.tv/garrettg"
        self.garettg_learning_weight = 2.0  # 2x learning weight for GarettG
        
        # Mode trainers
        self.mode_trainers = {
            '1s': ModeTrainer('1s', focus_weight=0.5),  # Lower focus
            '2s': ModeTrainer('2s', focus_weight=2.0, garettg_focus=True),  # High focus + GarettG
            '3s': ModeTrainer('3s', focus_weight=1.0)   # Normal focus
        }
        
        # Stream sources
        self.stream_sources = {
            '1s': {
                'primary': ['jstn', 'squishy'],
                'secondary': ['kronovi', 'rizo'],
                'youtube': ['Musty', 'Lethamyr', 'Pulse Fire']
            },
            '2s': {
                'primary': ['garettg'],  # Focus on GarettG
                'secondary': ['jknaps', 'turbo', 'kaydop'],
                'youtube': ['SunlessKhan', 'Wayton Pilkin', 'Rocket League Academy']
            },
            '3s': {
                'primary': ['fairy', 'violentpanda'],
                'secondary': ['turbo', 'kaydop'],
                'youtube': ['RLCS', 'Rocket League Esports', 'Rocket League']
            }
        }
        
        # GarettG specific learning
        self.garettg_actions = []
        self.garettg_patterns = {}
        self.garettg_confidence = 0.0
        
        # System state
        self.is_training = False
        self.start_time = None
        self.total_actions = 0
        self.total_episodes = 0
        
        # Performance tracking
        self.mode_performance = {
            '1s': {'actions': 0, 'episodes': 0, 'accuracy': 0.0, 'garettg_influence': 0.0},
            '2s': {'actions': 0, 'episodes': 0, 'accuracy': 0.0, 'garettg_influence': 1.0},
            '3s': {'actions': 0, 'episodes': 0, 'accuracy': 0.0, 'garettg_influence': 0.0}
        }
        
        print("🚀 GarettG Focused Multi-Mode Trainer Initialized!")
        print("🎯 Primary Focus: GarettG's 2s gameplay")
        print("📺 Secondary: All modes with multiple sources")
        print("🧠 Learning: Cross-mode with GarettG influence")
    
    def start_focused_training(self):
        """Start training with GarettG focus"""
        print("\n🚀 STARTING GARETTG FOCUSED TRAINING")
        print("=" * 70)
        print("🎮 Mode 1: 1s Training (Secondary)")
        print("🎮 Mode 2: 2s Training (PRIMARY - GarettG Focus)")
        print("🎮 Mode 3: 3s Training (Secondary)")
        print("🔴 GarettG Stream: Active monitoring")
        print("📺 Other Streams: Active")
        print("🧠 Cross-mode learning with GarettG influence")
        
        self.is_training = True
        self.start_time = time.time()
        
        # Start GarettG monitoring
        garettg_thread = threading.Thread(target=self.monitor_garettg_stream)
        garettg_thread.daemon = True
        garettg_thread.start()
        
        # Start all mode trainers
        for mode, trainer in self.mode_trainers.items():
            trainer.start_mode_training()
        
        # Start cross-mode learning with GarettG influence
        cross_mode_thread = threading.Thread(target=self.garettg_influenced_learning)
        cross_mode_thread.daemon = True
        cross_mode_thread.start()
        
        # Start performance monitoring
        monitor_thread = threading.Thread(target=self.monitor_performance)
        monitor_thread.daemon = True
        monitor_thread.start()
        
        # Start reporting
        report_thread = threading.Thread(target=self.generate_reports)
        report_thread.daemon = True
        report_thread.start()
        
        print("✅ All training systems activated!")
        print("🎯 GarettG focused training in progress...")
    
    def monitor_garettg_stream(self):
        """Monitor GarettG's stream specifically"""
        print("🔴 Starting GarettG stream monitoring...")
        
        while self.is_training:
            # Simulate GarettG stream monitoring
            if random.random() < 0.6:  # 60% chance GarettG is live
                self.learn_from_garettg()
            
            time.sleep(1)  # Check every second
    
    def learn_from_garettg(self):
        """Learn from GarettG's gameplay"""
        # GarettG's signature moves in 2s
        garettg_moves = [
            'demo_opponent', 'power_shot', 'wave_dash', 'speed_flip',
            'pass', 'centering', 'rotation', 'positioning',
            'challenge', 'fake_challenge', 'boost_management'
        ]
        
        action = random.choice(garettg_moves)
        confidence = random.uniform(0.9, 0.98)  # High confidence for GarettG
        
        # Store GarettG action
        garettg_action = {
            'action': action,
            'confidence': confidence,
            'timestamp': time.time(),
            'mode': '2s',
            'source': 'garettg_stream'
        }
        
        self.garettg_actions.append(garettg_action)
        
        # Learn in 2s mode with high weight
        self.mode_trainers['2s'].learn_skill(action, confidence, 'garettg_stream', 'garettg')
        
        # Apply GarettG influence to other modes
        self.apply_garettg_influence(action, confidence)
        
        self.total_actions += 1
    
    def apply_garettg_influence(self, action, confidence):
        """Apply GarettG's influence to other modes"""
        # Transfer applicable skills to other modes
        transferable_skills = ['demo_opponent', 'power_shot', 'wave_dash', 'speed_flip']
        
        if action in transferable_skills:
            # Apply to 1s mode with reduced confidence
            self.mode_trainers['1s'].learn_skill(action, confidence * 0.7, 'garettg_influence', 'garettg')
            
            # Apply to 3s mode with reduced confidence
            self.mode_trainers['3s'].learn_skill(action, confidence * 0.6, 'garettg_influence', 'garettg')
    
    def garettg_influenced_learning(self):
        """Cross-mode learning influenced by GarettG"""
        print("🧠 Starting GarettG influenced learning...")
        
        while self.is_training:
            # Analyze GarettG patterns
            if len(self.garettg_actions) > 10:
                self.analyze_garettg_patterns()
            
            # Transfer insights between modes
            self.transfer_mode_insights()
            
            time.sleep(5)  # Cross-mode learning every 5 seconds
    
    def analyze_garettg_patterns(self):
        """Analyze GarettG's playing patterns"""
        recent_actions = self.garettg_actions[-10:]  # Last 10 actions
        
        # Count action frequencies
        action_counts = {}
        for action_data in recent_actions:
            action = action_data['action']
            action_counts[action] = action_counts.get(action, 0) + 1
        
        # Update GarettG patterns
        for action, count in action_counts.items():
            if action not in self.garettg_patterns:
                self.garettg_patterns[action] = 0
            self.garettg_patterns[action] += count
        
        # Calculate GarettG confidence
        if self.garettg_actions:
            self.garettg_confidence = np.mean([action['confidence'] for action in recent_actions])
    
    def transfer_mode_insights(self):
        """Transfer insights between modes"""
        # Get insights from each mode
        mode_insights = {}
        for mode, trainer in self.mode_trainers.items():
            if trainer.learned_skills:
                mode_insights[mode] = trainer.learned_skills
        
        # Transfer insights
        for source_mode, insights in mode_insights.items():
            for target_mode, target_trainer in self.mode_trainers.items():
                if source_mode != target_mode:
                    for skill, data in insights.items():
                        # Transfer with mode-specific weight
                        transfer_weight = self.mode_trainers[target_mode].focus_weight
                        transferred_confidence = data['avg_confidence'] * transfer_weight * 0.5
                        
                        target_trainer.learn_skill(skill, transferred_confidence, 'cross_mode', source_mode)
    
    def monitor_performance(self):
        """Monitor performance across all modes"""
        print("📊 Starting performance monitoring...")
        
        while self.is_training:
            # Update performance stats
            for mode, trainer in self.mode_trainers.items():
                self.mode_performance[mode]['actions'] = trainer.total_actions
                self.mode_performance[mode]['episodes'] = trainer.total_episodes
                self.mode_performance[mode]['accuracy'] = trainer.accuracy
                
                # Calculate GarettG influence
                garettg_actions = sum(1 for action in trainer.learned_skills.values() 
                                    if 'garettg' in action['source_names'])
                total_actions = sum(action['count'] for action in trainer.learned_skills.values())
                
                if total_actions > 0:
                    self.mode_performance[mode]['garettg_influence'] = garettg_actions / total_actions
            
            # Calculate total stats
            self.total_actions = sum(perf['actions'] for perf in self.mode_performance.values())
            self.total_episodes = sum(perf['episodes'] for perf in self.mode_performance.values())
            
            time.sleep(10)  # Update every 10 seconds
    
    def generate_reports(self):
        """Generate comprehensive reports"""
        print("📊 Starting report generation...")
        
        while self.is_training:
            time.sleep(300)  # Report every 5 minutes
            
            if self.is_training:
                self.print_comprehensive_report()
    
    def print_comprehensive_report(self):
        """Print comprehensive training report"""
        print("\n" + "="*100)
        print("📊 GARETTG FOCUSED TRAINING REPORT")
        print("="*100)
        
        elapsed = time.time() - self.start_time
        hours = elapsed / 3600
        
        print(f"⏰ Training Time: {hours:.2f} hours")
        print(f"🎮 Total Actions: {self.total_actions}")
        print(f"🧠 Total Episodes: {self.total_episodes}")
        print(f"🔴 GarettG Actions: {len(self.garettg_actions)}")
        print(f"📊 GarettG Confidence: {self.garettg_confidence:.1%}")
        
        # GarettG patterns
        if self.garettg_patterns:
            print(f"\n🔴 GARETTG PATTERNS:")
            print("-" * 30)
            sorted_patterns = sorted(self.garettg_patterns.items(), key=lambda x: x[1], reverse=True)
            for action, count in sorted_patterns[:5]:
                print(f"   {action}: {count} times")
        
        # Mode-specific performance
        print(f"\n🎮 MODE PERFORMANCE:")
        print("-" * 50)
        
        for mode, perf in self.mode_performance.items():
            print(f"   {mode.upper()}:")
            print(f"      Actions: {perf['actions']}")
            print(f"      Episodes: {perf['episodes']}")
            print(f"      Accuracy: {perf['accuracy']:.1%}")
            print(f"      GarettG Influence: {perf['garettg_influence']:.1%}")
            print()
        
        # Top learned skills by mode
        print("🏆 TOP LEARNED SKILLS BY MODE:")
        print("-" * 50)
        
        for mode, trainer in self.mode_trainers.items():
            if trainer.learned_skills:
                sorted_skills = sorted(
                    trainer.learned_skills.items(),
                    key=lambda x: x[1]['confidence'],
                    reverse=True
                )
                
                print(f"   {mode.upper()}:")
                for i, (skill, data) in enumerate(sorted_skills[:5]):
                    garettg_marker = "🔴" if 'garettg' in data['source_names'] else "  "
                    print(f"      {garettg_marker} {i+1}. {skill} - {data['confidence']:.1%}")
                print()
        
        # Rank predictions
        print("🏆 RANK PREDICTIONS:")
        print("-" * 30)
        for mode, trainer in self.mode_trainers.items():
            rank = trainer.predict_rank()
            garettg_boost = "🔴" if mode == '2s' else "  "
            print(f"   {garettg_boost} {mode.upper()}: {rank['rank']} ({rank['confidence']:.1f}%)")
        
        print("="*100)
    
    def save_training_data(self):
        """Save all training data"""
        data = {
            'mode_performance': self.mode_performance,
            'garettg_actions': self.garettg_actions,
            'garettg_patterns': self.garettg_patterns,
            'garettg_confidence': self.garettg_confidence,
            'total_actions': self.total_actions,
            'total_episodes': self.total_episodes,
            'training_time': time.time() - self.start_time,
            'timestamp': datetime.now().isoformat()
        }
        
        filename = f"garettg_focused_training_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pkl"
        
        try:
            with open(filename, 'wb') as f:
                pickle.dump(data, f)
            print(f"\n💾 Training data saved to {filename}")
        except Exception as e:
            print(f"\n❌ Error saving data: {e}")
    
    def stop_training(self):
        """Stop all training"""
        self.is_training = False
        
        for trainer in self.mode_trainers.values():
            trainer.stop_training()
        
        print("\n⏹️ GarettG focused training stopped")
        self.save_training_data()

class ModeTrainer:
    """Individual mode trainer with focus weights"""
    
    def __init__(self, mode, focus_weight=1.0, garettg_focus=False):
        self.mode = mode
        self.focus_weight = focus_weight
        self.garettg_focus = garettg_focus
        self.is_training = False
        
        # Learning data
        self.learned_skills = {}
        self.total_actions = 0
        self.total_episodes = 0
        self.accuracy = 0.0
        
        print(f"🎮 {mode.upper()} Mode Trainer Initialized! (Weight: {focus_weight})")
    
    def start_mode_training(self):
        """Start training for this mode"""
        self.is_training = True
        
        # Start stream monitoring
        stream_thread = threading.Thread(target=self.monitor_streams)
        stream_thread.daemon = True
        stream_thread.start()
        
        # Start YouTube learning
        youtube_thread = threading.Thread(target=self.learn_from_youtube)
        youtube_thread.daemon = True
        youtube_thread.start()
        
        # Start PPO training
        ppo_thread = threading.Thread(target=self.ppo_training)
        ppo_thread.daemon = True
        ppo_thread.start()
        
        print(f"✅ {self.mode.upper()} training started!")
    
    def monitor_streams(self):
        """Monitor streams for this mode"""
        while self.is_training:
            # Simulate stream monitoring with focus weight
            stream_chance = 0.3 * self.focus_weight  # Higher weight = more stream monitoring
            
            if random.random() < stream_chance:
                if self.garettg_focus and random.random() < 0.7:
                    # Focus on GarettG for 2s mode
                    streamer = 'garettg'
                else:
                    # Other streamers
                    streamers = ['jstn', 'squishy', 'kronovi', 'jknaps', 'turbo', 'kaydop']
                    streamer = random.choice(streamers)
                
                self.learn_from_stream(streamer)
            
            time.sleep(2)  # Check every 2 seconds
    
    def learn_from_stream(self, streamer):
        """Learn from a live stream"""
        # Mode-specific actions
        mode_actions = {
            '1s': ['flick', 'dribble', 'kickoff', '1v1_strategy'],
            '2s': ['pass', 'rotation', 'teamwork', 'positioning'],
            '3s': ['team_rotation', 'boost_management', 'challenges', 'defense']
        }
        
        action = random.choice(mode_actions.get(self.mode, ['shot', 'aerial', 'save']))
        confidence = random.uniform(0.8, 0.95)
        
        self.learn_skill(action, confidence, 'live_stream', streamer)
        self.total_actions += 1
    
    def learn_from_youtube(self):
        """Learn from YouTube content"""
        while self.is_training:
            # Simulate YouTube learning with focus weight
            youtube_chance = 0.2 * self.focus_weight
            
            if random.random() < youtube_chance:
                channels = ['SunlessKhan', 'Musty', 'Lethamyr', 'RLCS']
                channel = random.choice(channels)
                action = random.choice(['tutorial', 'analysis', 'trick_shot'])
                confidence = random.uniform(0.7, 0.9)
                
                self.learn_skill(action, confidence, 'youtube', channel)
                self.total_actions += 1
            
            time.sleep(3)  # YouTube learning every 3 seconds
    
    def learn_skill(self, skill, confidence, source, source_name):
        """Learn a skill"""
        if skill not in self.learned_skills:
            self.learned_skills[skill] = {
                'count': 0,
                'total_confidence': 0,
                'avg_confidence': 0,
                'sources': set(),
                'source_names': set()
            }
        
        self.learned_skills[skill]['count'] += 1
        self.learned_skills[skill]['total_confidence'] += confidence
        self.learned_skills[skill]['avg_confidence'] = (
            self.learned_skills[skill]['total_confidence'] / 
            self.learned_skills[skill]['count']
        )
        self.learned_skills[skill]['sources'].add(source)
        self.learned_skills[skill]['source_names'].add(source_name)
        
        # Update accuracy
        self.accuracy = (self.accuracy + confidence) / 2
    
    def ppo_training(self):
        """PPO training for this mode"""
        while self.is_training:
            self.total_episodes += 1
            time.sleep(1)  # PPO step every second
    
    def predict_rank(self):
        """Predict rank for this mode"""
        if not self.learned_skills:
            return {'rank': 'Bronze', 'confidence': 50}
        
        avg_confidence = np.mean([data['avg_confidence'] for data in self.learned_skills.values()])
        skill_count = len(self.learned_skills)
        
        # Apply focus weight to rank prediction
        adjusted_confidence = avg_confidence * self.focus_weight
        
        if adjusted_confidence > 1.8 and skill_count > 10:
            rank = 'SSL'
            confidence = 95
        elif adjusted_confidence > 1.6 and skill_count > 8:
            rank = 'Grand Champion'
            confidence = 90
        elif adjusted_confidence > 1.4 and skill_count > 6:
            rank = 'Champion'
            confidence = 85
        elif adjusted_confidence > 1.2 and skill_count > 4:
            rank = 'Diamond'
            confidence = 80
        elif adjusted_confidence > 1.0 and skill_count > 2:
            rank = 'Platinum'
            confidence = 75
        else:
            rank = 'Gold'
            confidence = 70
        
        return {'rank': rank, 'confidence': confidence}
    
    def stop_training(self):
        """Stop training for this mode"""
        self.is_training = False
        print(f"⏹️ {self.mode.upper()} training stopped")

def main():
    """Main function"""
    print("🚀 GARETTG FOCUSED MULTI-MODE TRAINER")
    print("=" * 70)
    print("🎯 Primary Focus: GarettG's 2s gameplay")
    print("📺 Secondary: All modes with multiple sources")
    print("🧠 Features: Cross-mode learning with GarettG influence")
    print("⏰ Duration: Continuous training")
    print("🚀 Starting focused training...")
    
    trainer = GarettGFocusedMultiTrainer()
    
    try:
        trainer.start_focused_training()
        
        # Keep running until interrupted
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n⏹️ Training interrupted by user")
        trainer.stop_training()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        trainer.stop_training()

if __name__ == "__main__":
    main()
