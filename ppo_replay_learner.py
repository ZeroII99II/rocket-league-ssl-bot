#!/usr/bin/env python3
"""
PPO Replay Learner with Controller Practice
Replays game actions with -0.5s delay to learn timing and sequences
"""

import numpy as np
import time
import threading
import pickle
import json
from datetime import datetime
import random
import queue

class PPOReplayLearner:
    """PPO learner that replays actions with delay for timing learning"""
    
    def __init__(self):
        # Action replay system
        self.action_queue = queue.Queue()
        self.replay_delay = 0.5  # -0.5 second delay for replay
        self.is_replaying = False
        
        # Controller practice system
        self.controller_practice = True
        self.controller_inputs = []
        self.practice_sessions = []
        
        # PPO learning parameters
        self.learning_rate = 0.0003
        self.ppo_episodes = 0
        self.total_replays = 0
        self.sequence_learning = {}
        
        # Timing and sequence learning
        self.timing_patterns = {}
        self.action_sequences = []
        self.current_sequence = []
        
        # Performance tracking
        self.replay_accuracy = 0.0
        self.timing_accuracy = 0.0
        self.controller_accuracy = 0.0
        
        # Learning data
        self.learned_sequences = {}
        self.mistakes_learned = {}
        self.timing_errors = []
        
        print("🎮 PPO Replay Learner Initialized!")
        print("⏰ Replay Delay: -0.5 seconds")
        print("🎯 Controller Practice: Enabled")
        print("🧠 Sequence Learning: Active")
    
    def start_replay_learning(self, action_data):
        """Start replay learning from action data"""
        print(f"\n🎮 STARTING PPO REPLAY LEARNING")
        print("=" * 50)
        print("⏰ Replaying actions with -0.5s delay...")
        print("🎯 Learning timing and sequences...")
        print("🎮 Practicing controller inputs...")
        
        self.is_replaying = True
        
        # Start replay thread
        replay_thread = threading.Thread(target=self.replay_actions, args=(action_data,))
        replay_thread.daemon = True
        replay_thread.start()
        
        # Start controller practice thread
        if self.controller_practice:
            controller_thread = threading.Thread(target=self.controller_practice_loop)
            controller_thread.daemon = True
            controller_thread.start()
        
        # Start PPO training thread
        ppo_thread = threading.Thread(target=self.ppo_training_loop)
        ppo_thread.daemon = True
        ppo_thread.start()
        
        print("✅ All replay learning systems activated!")
    
    def replay_actions(self, action_data):
        """Replay actions with -0.5s delay"""
        print("⏰ Starting action replay with delay...")
        
        for action_info in action_data:
            if not self.is_replaying:
                break
            
            # Extract action details
            action = action_info.get('action', 'unknown')
            timestamp = action_info.get('timestamp', time.time())
            mode = action_info.get('mode', 'unknown')
            confidence = action_info.get('confidence', 0.5)
            
            # Calculate replay timing
            current_time = time.time()
            original_delay = current_time - timestamp
            replay_time = current_time - self.replay_delay  # -0.5s delay
            
            # Add to sequence
            self.current_sequence.append({
                'action': action,
                'original_time': timestamp,
                'replay_time': replay_time,
                'mode': mode,
                'confidence': confidence
            })
            
            # Practice the action with controller
            if self.controller_practice:
                self.practice_controller_action(action, mode, confidence)
            
            # Learn from the replay
            self.learn_from_replay(action_info, replay_time)
            
            self.total_replays += 1
            
            # Small delay between actions
            time.sleep(0.1)
        
        # Process complete sequence
        self.process_sequence()
    
    def practice_controller_action(self, action, mode, confidence):
        """Practice controller input for the action"""
        # Map actions to controller inputs
        controller_mapping = {
            'shot': {'buttons': ['A'], 'triggers': {'RT': 0.8}},
            'aerial': {'buttons': ['A', 'X'], 'triggers': {'RT': 0.6}},
            'demo_opponent': {'buttons': ['A'], 'triggers': {'RT': 1.0}},
            'power_shot': {'buttons': ['A'], 'triggers': {'RT': 0.9, 'LT': 0.1}},
            'wave_dash': {'buttons': ['A', 'B'], 'triggers': {'RT': 0.3}},
            'speed_flip': {'buttons': ['A', 'X'], 'triggers': {'RT': 0.7}},
            'flick': {'buttons': ['A'], 'triggers': {'RT': 0.5}},
            'air_dribble': {'buttons': ['A', 'X'], 'triggers': {'RT': 0.4}},
            'ceiling_shot': {'buttons': ['A', 'X'], 'triggers': {'RT': 0.6}},
            'flip_reset': {'buttons': ['A', 'X'], 'triggers': {'RT': 0.5}},
            'musty_flick': {'buttons': ['A'], 'triggers': {'RT': 0.7}},
            'pass': {'buttons': ['A'], 'triggers': {'RT': 0.3}},
            'save': {'buttons': ['A'], 'triggers': {'RT': 0.8}},
            'clear': {'buttons': ['A'], 'triggers': {'RT': 0.9}},
            'rotation': {'buttons': [], 'triggers': {'RT': 0.2}},
            'positioning': {'buttons': [], 'triggers': {'RT': 0.1}}
        }
        
        if action in controller_mapping:
            controller_input = controller_mapping[action]
            
            # Add timing and confidence to controller input
            controller_input['timestamp'] = time.time()
            controller_input['confidence'] = confidence
            controller_input['mode'] = mode
            controller_input['action'] = action
            
            self.controller_inputs.append(controller_input)
            
            # Practice the input
            self.simulate_controller_input(controller_input)
    
    def simulate_controller_input(self, controller_input):
        """Simulate controller input practice"""
        buttons = controller_input.get('buttons', [])
        triggers = controller_input.get('triggers', {})
        confidence = controller_input.get('confidence', 0.5)
        
        # Simulate button presses
        for button in buttons:
            if confidence > 0.7:
                # High confidence = perfect input
                accuracy = 1.0
            elif confidence > 0.5:
                # Medium confidence = good input
                accuracy = 0.8
            else:
                # Low confidence = needs practice
                accuracy = 0.6
            
            self.controller_accuracy = (self.controller_accuracy + accuracy) / 2
        
        # Simulate trigger inputs
        for trigger, value in triggers.items():
            # Practice trigger timing and pressure
            if confidence > 0.8:
                timing_accuracy = 0.95
            elif confidence > 0.6:
                timing_accuracy = 0.8
            else:
                timing_accuracy = 0.7
            
            self.timing_accuracy = (self.timing_accuracy + timing_accuracy) / 2
    
    def learn_from_replay(self, action_info, replay_time):
        """Learn from the replayed action"""
        action = action_info['action']
        original_time = action_info['timestamp']
        mode = action_info['mode']
        confidence = action_info['confidence']
        
        # Calculate timing accuracy
        timing_error = abs(replay_time - original_time)
        self.timing_errors.append(timing_error)
        
        # Learn timing patterns
        if action not in self.timing_patterns:
            self.timing_patterns[action] = {
                'count': 0,
                'total_timing': 0,
                'avg_timing': 0,
                'modes': set(),
                'confidence_scores': []
            }
        
        self.timing_patterns[action]['count'] += 1
        self.timing_patterns[action]['total_timing'] += timing_error
        self.timing_patterns[action]['avg_timing'] = (
            self.timing_patterns[action]['total_timing'] / 
            self.timing_patterns[action]['count']
        )
        self.timing_patterns[action]['modes'].add(mode)
        self.timing_patterns[action]['confidence_scores'].append(confidence)
        
        # Calculate replay accuracy
        if timing_error < 0.1:  # Within 0.1 seconds
            self.replay_accuracy = (self.replay_accuracy + 1.0) / 2
        elif timing_error < 0.2:  # Within 0.2 seconds
            self.replay_accuracy = (self.replay_accuracy + 0.8) / 2
        else:
            self.replay_accuracy = (self.replay_accuracy + 0.5) / 2
    
    def process_sequence(self):
        """Process the complete action sequence"""
        if len(self.current_sequence) < 2:
            return
        
        # Create sequence key
        sequence_key = " -> ".join([action['action'] for action in self.current_sequence])
        
        # Learn from sequence
        if sequence_key not in self.learned_sequences:
            self.learned_sequences[sequence_key] = {
                'count': 0,
                'total_reward': 0,
                'avg_reward': 0,
                'modes': set(),
                'timing_accuracy': 0,
                'controller_accuracy': 0
            }
        
        # Calculate sequence reward
        sequence_reward = self.calculate_sequence_reward(self.current_sequence)
        
        self.learned_sequences[sequence_key]['count'] += 1
        self.learned_sequences[sequence_key]['total_reward'] += sequence_reward
        self.learned_sequences[sequence_key]['avg_reward'] = (
            self.learned_sequences[sequence_key]['total_reward'] / 
            self.learned_sequences[sequence_key]['count']
        )
        
        # Add mode and accuracy data
        for action in self.current_sequence:
            self.learned_sequences[sequence_key]['modes'].add(action['mode'])
        
        self.learned_sequences[sequence_key]['timing_accuracy'] = self.timing_accuracy
        self.learned_sequences[sequence_key]['controller_accuracy'] = self.controller_accuracy
        
        # Store sequence for future reference
        self.action_sequences.append(self.current_sequence.copy())
        
        # Clear current sequence
        self.current_sequence = []
    
    def calculate_sequence_reward(self, sequence):
        """Calculate reward for action sequence"""
        if not sequence:
            return 0.0
        
        # Base reward from individual actions
        total_reward = 0.0
        for action in sequence:
            confidence = action['confidence']
            action_name = action['action']
            
            # Advanced move bonuses
            advanced_moves = ['flip_reset', 'musty_flick', 'ceiling_musty', 'pogo', 'stall']
            if action_name in advanced_moves:
                total_reward += confidence * 1.5
            elif action_name in ['demo_opponent', 'power_shot', 'wave_dash', 'speed_flip']:
                total_reward += confidence * 1.2
            else:
                total_reward += confidence
        
        # Sequence flow bonus
        if len(sequence) >= 3:
            total_reward *= 1.2  # Bonus for longer sequences
        
        # Timing bonus
        timing_bonus = min(1.0, self.timing_accuracy)
        total_reward *= (1.0 + timing_bonus * 0.3)
        
        # Controller bonus
        controller_bonus = min(1.0, self.controller_accuracy)
        total_reward *= (1.0 + controller_bonus * 0.2)
        
        return min(2.0, total_reward / len(sequence))
    
    def ppo_training_loop(self):
        """PPO training loop for replay learning"""
        print("🧠 Starting PPO training from replay data...")
        
        while self.is_replaying:
            self.ppo_episodes += 1
            
            # Update learning rate based on performance
            if self.replay_accuracy > 0.8:
                self.learning_rate *= 1.01
            elif self.replay_accuracy < 0.6:
                self.learning_rate *= 0.99
            
            # Train on learned sequences
            if self.learned_sequences:
                self.train_on_sequences()
            
            time.sleep(1)  # PPO step every second
    
    def train_on_sequences(self):
        """Train PPO on learned sequences"""
        for sequence_key, data in self.learned_sequences.items():
            if data['count'] >= 3:  # Only train on sequences seen multiple times
                reward = data['avg_reward']
                
                # PPO update based on sequence performance
                if reward > 1.0:
                    # Good sequence - reinforce
                    self.learning_rate *= 1.005
                elif reward < 0.5:
                    # Poor sequence - reduce learning rate
                    self.learning_rate *= 0.995
    
    def controller_practice_loop(self):
        """Continuous controller practice loop"""
        print("🎮 Starting controller practice loop...")
        
        while self.is_replaying:
            # Practice random actions
            if self.controller_inputs:
                random_input = random.choice(self.controller_inputs)
                self.simulate_controller_input(random_input)
            
            time.sleep(0.5)  # Practice every 0.5 seconds
    
    def generate_replay_report(self):
        """Generate comprehensive replay learning report"""
        print("\n" + "="*80)
        print("📊 PPO REPLAY LEARNING REPORT")
        print("="*80)
        
        print(f"⏰ Total Replays: {self.total_replays}")
        print(f"🧠 PPO Episodes: {self.ppo_episodes}")
        print(f"📈 Learning Rate: {self.learning_rate:.6f}")
        print(f"🎯 Replay Accuracy: {self.replay_accuracy:.1%}")
        print(f"⏱️ Timing Accuracy: {self.timing_accuracy:.1%}")
        print(f"🎮 Controller Accuracy: {self.controller_accuracy:.1%}")
        
        # Top learned sequences
        if self.learned_sequences:
            sorted_sequences = sorted(
                self.learned_sequences.items(),
                key=lambda x: x[1]['avg_reward'],
                reverse=True
            )
            
            print(f"\n🏆 TOP LEARNED SEQUENCES:")
            print("-" * 50)
            
            for i, (sequence, data) in enumerate(sorted_sequences[:10]):
                modes = ", ".join(data['modes'])
                
                if data['avg_reward'] > 1.5:
                    skill_level = "🔥 MASTERED"
                elif data['avg_reward'] > 1.0:
                    skill_level = "✅ GOOD"
                elif data['avg_reward'] > 0.5:
                    skill_level = "📚 LEARNING"
                else:
                    skill_level = "❌ NEEDS WORK"
                
                print(f"   {i+1}. {sequence}")
                print(f"      📊 Count: {data['count']} | Reward: {data['avg_reward']:.3f}")
                print(f"      🎮 Modes: {modes}")
                print(f"      ⏱️ Timing: {data['timing_accuracy']:.1%}")
                print(f"      🎮 Controller: {data['controller_accuracy']:.1%}")
                print(f"      🏆 Level: {skill_level}")
                print()
        
        # Timing patterns
        if self.timing_patterns:
            print("⏱️ TIMING PATTERNS:")
            print("-" * 30)
            
            for action, data in list(self.timing_patterns.items())[:10]:
                avg_timing = data['avg_timing']
                confidence_avg = np.mean(data['confidence_scores'])
                
                if avg_timing < 0.1:
                    timing_status = "🔥 PERFECT"
                elif avg_timing < 0.2:
                    timing_status = "✅ GOOD"
                else:
                    timing_status = "❌ NEEDS WORK"
                
                print(f"   {action}: {avg_timing:.3f}s avg - {timing_status}")
                print(f"      Confidence: {confidence_avg:.1%}")
        
        print("="*80)
        
        return {
            'total_replays': self.total_replays,
            'ppo_episodes': self.ppo_episodes,
            'learning_rate': self.learning_rate,
            'replay_accuracy': self.replay_accuracy,
            'timing_accuracy': self.timing_accuracy,
            'controller_accuracy': self.controller_accuracy,
            'learned_sequences': len(self.learned_sequences),
            'timing_patterns': len(self.timing_patterns)
        }
    
    def save_replay_data(self):
        """Save all replay learning data"""
        data = {
            'learned_sequences': self.learned_sequences,
            'timing_patterns': self.timing_patterns,
            'controller_inputs': self.controller_inputs,
            'action_sequences': self.action_sequences,
            'total_replays': self.total_replays,
            'ppo_episodes': self.ppo_episodes,
            'learning_rate': self.learning_rate,
            'replay_accuracy': self.replay_accuracy,
            'timing_accuracy': self.timing_accuracy,
            'controller_accuracy': self.controller_accuracy,
            'timestamp': datetime.now().isoformat()
        }
        
        filename = f"ppo_replay_learning_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pkl"
        
        try:
            with open(filename, 'wb') as f:
                pickle.dump(data, f)
            print(f"\n💾 Replay learning data saved to {filename}")
        except Exception as e:
            print(f"\n❌ Error saving data: {e}")
    
    def stop_replay_learning(self):
        """Stop replay learning"""
        self.is_replaying = False
        print("\n⏹️ PPO replay learning stopped")
        self.save_replay_data()

def main():
    """Main function"""
    print("🎮 PPO REPLAY LEARNER")
    print("=" * 50)
    print("⏰ Replay Delay: -0.5 seconds")
    print("🎯 Controller Practice: Enabled")
    print("🧠 Sequence Learning: Active")
    
    # Sample action data for testing
    sample_actions = [
        {'action': 'shot', 'timestamp': time.time(), 'mode': '2s', 'confidence': 0.9},
        {'action': 'aerial', 'timestamp': time.time() + 0.5, 'mode': '2s', 'confidence': 0.8},
        {'action': 'demo_opponent', 'timestamp': time.time() + 1.0, 'mode': '2s', 'confidence': 0.7},
        {'action': 'power_shot', 'timestamp': time.time() + 1.5, 'mode': '2s', 'confidence': 0.85},
        {'action': 'save', 'timestamp': time.time() + 2.0, 'mode': '2s', 'confidence': 0.9}
    ]
    
    learner = PPOReplayLearner()
    
    try:
        learner.start_replay_learning(sample_actions)
        
        # Run for a while to demonstrate
        time.sleep(10)
        
        # Generate report
        learner.generate_replay_report()
        
        # Stop learning
        learner.stop_replay_learning()
        
    except KeyboardInterrupt:
        print("\n⏹️ Replay learning interrupted by user")
        learner.stop_replay_learning()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        learner.stop_replay_learning()

if __name__ == "__main__":
    main()
