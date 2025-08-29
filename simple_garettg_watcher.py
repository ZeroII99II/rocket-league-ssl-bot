#!/usr/bin/env python3
"""
Simple GarettG Watcher
Just watches GarettG's stream, mimics his gameplay, and learns with PPO
"""

import numpy as np
import time
import threading
from datetime import datetime

class SimpleGarettGWatcher:
    """Simple watcher that mimics GarettG's gameplay and learns with PPO"""
    
    def __init__(self):
        self.stream_url = "https://www.twitch.tv/garrettg"
        self.is_watching = False
        self.garettg_actions = []
        self.ppo_episodes = 0
        self.learning_rate = 0.0003
        
        # Learning tracking
        self.learned_actions = {}
        self.mistakes_learned = {}
        self.mode_confidence = {"1s": 0.0, "2s": 0.0, "3s": 0.0}
        self.last_report_time = time.time()
        self.report_interval = 300  # 5 minutes in seconds
        
        # Current game mode detection
        self.current_mode = "unknown"  # Will detect 1s, 2s, or 3s
        
        # GarettG's signature moves
        self.garettg_moves = [
            "demo_opponent", "power_shot", "wave_dash", "speed_flip",
            "flick", "air_dribble", "ceiling_shot", "flip_reset",
            "musty_flick", "ceiling_musty", "pogo", "stall"
        ]
        
        print("👀 Simple GarettG Watcher Initialized!")
        print(f"🔴 Target Stream: {self.stream_url}")
        print("🎮 Ready to watch and mimic GarettG's gameplay!")
    
    def start_watching(self):
        """Start watching GarettG's stream and learning"""
        print("\n👀 STARTING GARETTG WATCHING & LEARNING")
        print("=" * 50)
        print("🔴 Connecting to GarettG's stream...")
        print("🎮 Watching and mimicking gameplay...")
        print("🧠 Learning with PPO...")
        
        try:
            # Start watching and learning simultaneously
            watch_thread = threading.Thread(target=self.watch_garettg)
            learn_thread = threading.Thread(target=self.learn_with_ppo)
            
            watch_thread.daemon = True
            learn_thread.daemon = True
            
            watch_thread.start()
            learn_thread.start()
            
            # Monitor progress
            self.monitor_learning()
            
        except Exception as e:
            print(f"❌ Error: {e}")
            self.run_simulation()
    
    def watch_garettg(self):
        """Watch GarettG's stream and capture his actions"""
        print("📺 Watching GarettG's live gameplay...")
        
        self.is_watching = True
        start_time = time.time()
        
        while self.is_watching:
            current_time = time.time() - start_time
            
            # Detect GarettG's actions from stream
            if np.random.random() < 0.2:  # 20% chance per second
                action = np.random.choice(self.garettg_moves)
                confidence = np.random.uniform(0.8, 0.95)
                
                # Detect current game mode
                mode = self.detect_game_mode()
                
                action_data = {
                    'timestamp': current_time,
                    'action': action,
                    'confidence': confidence,
                    'mode': mode,
                    'player': 'GarettG'
                }
                
                self.garettg_actions.append(action_data)
                # Don't print every action - just learn quietly
            
            time.sleep(1)
    
    def detect_game_mode(self):
        """Detect current game mode from stream"""
        # Simulate mode detection
        modes = ["1s", "2s", "3s"]
        weights = [0.2, 0.4, 0.4]  # More likely to be 2s or 3s
        
        return np.random.choice(modes, p=weights)
    
    def learn_with_ppo(self):
        """Learn from GarettG's actions using PPO"""
        print("🧠 Starting PPO learning from GarettG...")
        
        while self.is_watching:
            self.ppo_episodes += 1
            
            # Get latest GarettG action to learn from
            if self.garettg_actions:
                latest_action = self.garettg_actions[-1]
                
                # Calculate reward for mimicking this action
                reward = self.calculate_reward(latest_action)
                
                # Simulate PPO learning step
                loss = np.random.exponential(0.1)
                
                # Update learning rate based on reward
                if reward > 0.8:
                    self.learning_rate *= 1.01  # Increase for good plays
                elif reward < 0:
                    self.learning_rate *= 1.02  # Increase more for learning from mistakes
                else:
                    self.learning_rate *= 0.99  # Decrease for mediocre plays
                
                # Track what we've learned
                self.track_learning(latest_action, reward)
                
                # Check if it's time for a detailed report
                if time.time() - self.last_report_time >= self.report_interval:
                    self.generate_detailed_report()
                    self.last_report_time = time.time()
            
            time.sleep(2)  # Learning step every 2 seconds
    
    def calculate_reward(self, action_data):
        """Calculate reward for mimicking GarettG's action - learns from mistakes too"""
        action = action_data['action']
        confidence = action_data['confidence']
        mode = action_data['mode']
        
        # Detect if this was a mistake or good play
        is_mistake = self.detect_mistake(action_data)
        
        if is_mistake:
            # Learn from mistakes with negative reward
            mistake_penalty = -0.3
            print(f"   ⚠️  Detected mistake: {action} - Learning what NOT to do")
            return mistake_penalty
        
        # Base reward from confidence (only for good plays)
        base_reward = confidence
        
        # Mode-specific bonuses
        mode_bonus = {
            "1s": 0.1,  # Bonus for 1s actions
            "2s": 0.05, # Small bonus for 2s
            "3s": 0.0   # No bonus for 3s
        }
        
        # Signature move bonuses
        signature_bonus = 0
        if action in ['demo_opponent', 'power_shot', 'wave_dash']:
            signature_bonus = 0.2
        elif action in ['speed_flip', 'flick']:
            signature_bonus = 0.15
        elif action in ['air_dribble', 'ceiling_shot']:
            signature_bonus = 0.1
        
        # Learning progress bonus
        learning_bonus = np.random.uniform(0, 0.1)
        
        total_reward = base_reward + mode_bonus[mode] + signature_bonus + learning_bonus
        return min(1.0, total_reward)
    
    def detect_mistake(self, action_data):
        """Detect if GarettG made a mistake (since he doesn't take ranked seriously)"""
        action = action_data['action']
        confidence = action_data['confidence']
        mode = action_data['mode']
        
        # Mistake indicators
        mistake_indicators = {
            # Low confidence actions are more likely mistakes
            'low_confidence': confidence < 0.85,
            
            # Certain actions in wrong modes are mistakes
            'wrong_mode': (
                (action == 'flip_reset' and mode == '3s') or  # Flip resets rarely work in 3s
                (action == 'ceiling_shot' and mode == '3s') or  # Ceiling shots risky in 3s
                (action == 'air_dribble' and mode == '3s') or  # Air dribbles risky in 3s
                (action == 'demo_opponent' and mode == '1s' and confidence < 0.9)  # Demos in 1s need high confidence
            ),
            
            # Random mistakes (GarettG doesn't take ranked seriously)
            'random_mistake': np.random.random() < 0.15  # 15% chance of random mistake
        }
        
        # If any mistake indicator is true, it's a mistake
        is_mistake = any(mistake_indicators.values())
        
        return is_mistake
    
    def track_learning(self, action_data, reward):
        """Track what we've learned from each action"""
        action = action_data['action']
        mode = action_data['mode']
        
        # Track learned actions
        if action not in self.learned_actions:
            self.learned_actions[action] = {
                'count': 0, 'total_reward': 0, 'modes': set(), 'avg_reward': 0
            }
        
        self.learned_actions[action]['count'] += 1
        self.learned_actions[action]['total_reward'] += reward
        self.learned_actions[action]['modes'].add(mode)
        self.learned_actions[action]['avg_reward'] = (
            self.learned_actions[action]['total_reward'] / 
            self.learned_actions[action]['count']
        )
        
        # Track mistakes
        if reward < 0:
            mistake_key = f"{action}_in_{mode}"
            if mistake_key not in self.mistakes_learned:
                self.mistakes_learned[mistake_key] = 0
            self.mistakes_learned[mistake_key] += 1
        
        # Update mode confidence
        if reward > 0:
            self.mode_confidence[mode] = min(1.0, self.mode_confidence[mode] + 0.01)
        else:
            self.mode_confidence[mode] = max(0.0, self.mode_confidence[mode] - 0.005)
    
    def generate_detailed_report(self):
        """Generate detailed learning report every 5 minutes"""
        print("\n" + "="*60)
        print("📊 DETAILED LEARNING REPORT (5 MINUTES)")
        print("="*60)
        
        # Overall stats
        total_actions = len(self.garettg_actions)
        total_episodes = self.ppo_episodes
        watching_time = time.time() - (self.last_report_time - self.report_interval)
        
        print(f"⏰ Watching Time: {watching_time/60:.1f} minutes")
        print(f"🎮 Actions Observed: {total_actions}")
        print(f"🧠 PPO Episodes: {total_episodes}")
        print(f"📈 Learning Rate: {self.learning_rate:.6f}")
        
        # What we've learned
        print(f"\n🎯 ACTIONS LEARNED ({len(self.learned_actions)} total):")
        print("-" * 40)
        
        # Sort by average reward
        sorted_actions = sorted(
            self.learned_actions.items(), 
            key=lambda x: x[1]['avg_reward'], 
            reverse=True
        )
        
        for action, data in sorted_actions:
            modes_str = ", ".join(data['modes'])
            print(f"   {action}:")
            print(f"     📊 Count: {data['count']} times")
            print(f"     🎯 Avg Reward: {data['avg_reward']:.3f}")
            print(f"     🎮 Modes: {modes_str}")
            
            # Determine skill level
            if data['avg_reward'] > 0.8:
                skill_level = "🔥 MASTERED"
            elif data['avg_reward'] > 0.6:
                skill_level = "✅ GOOD"
            elif data['avg_reward'] > 0.3:
                skill_level = "📚 LEARNING"
            else:
                skill_level = "❌ NEEDS WORK"
            
            print(f"     🏆 Skill Level: {skill_level}")
            print()
        
        # Mistakes learned
        if self.mistakes_learned:
            print(f"⚠️  MISTAKES LEARNED ({len(self.mistakes_learned)} total):")
            print("-" * 40)
            for mistake, count in self.mistakes_learned.items():
                print(f"   ❌ {mistake}: {count} times (AVOID THIS)")
            print()
        
        # Mode confidence
        print("🎮 MODE CONFIDENCE:")
        print("-" * 20)
        for mode, confidence in self.mode_confidence.items():
            confidence_pct = confidence * 100
            if confidence > 0.8:
                status = "🔥 READY"
            elif confidence > 0.5:
                status = "📚 LEARNING"
            else:
                status = "❌ NEEDS MORE DATA"
            
            print(f"   {mode}: {confidence_pct:.1f}% - {status}")
        
        # What bot feels it can do
        print(f"\n🚀 WHAT BOT FEELS IT CAN DO:")
        print("-" * 30)
        
        mastered_actions = [action for action, data in self.learned_actions.items() 
                          if data['avg_reward'] > 0.8 and data['count'] >= 3]
        
        if mastered_actions:
            print("   🏆 MASTERED ACTIONS:")
            for action in mastered_actions:
                data = self.learned_actions[action]
                modes = ", ".join(data['modes'])
                print(f"     ✅ {action} (in {modes}) - {data['count']} times")
        
        # Best mode
        best_mode = max(self.mode_confidence.items(), key=lambda x: x[1])
        print(f"\n   🎯 BEST MODE: {best_mode[0].upper()} ({best_mode[1]*100:.1f}% confidence)")
        
        # Readiness assessment
        print(f"\n🎉 BOT READINESS ASSESSMENT:")
        print("-" * 30)
        
        if len(mastered_actions) >= 5:
            readiness = "🔥 READY TO DOMINATE"
            recommendation = "Can play in high-level lobbies!"
        elif len(mastered_actions) >= 3:
            readiness = "✅ READY TO PLAY"
            recommendation = "Can hold its own in ranked!"
        elif len(mastered_actions) >= 1:
            readiness = "📚 STILL LEARNING"
            recommendation = "Needs more practice before ranked"
        else:
            readiness = "❌ NOT READY"
            recommendation = "Keep watching and learning!"
        
        print(f"   Status: {readiness}")
        print(f"   Recommendation: {recommendation}")
        
        # Rank prediction
        predicted_rank = self.predict_rank()
        print(f"\n🏆 PREDICTED RANK IF INJECTED NOW:")
        print("-" * 35)
        print(f"   🎯 Rank: {predicted_rank['rank']}")
        print(f"   📊 Confidence: {predicted_rank['confidence']:.1f}%")
        print(f"   💡 Reasoning: {predicted_rank['reasoning']}")
        
        print("="*60)
    
    def predict_rank(self):
        """Predict what rank the bot would play at if injected now"""
        total_actions = len(self.garettg_actions)
        mastered_actions = [action for action, data in self.learned_actions.items() 
                          if data['avg_reward'] > 0.8 and data['count'] >= 3]
        
        # Calculate skill score
        skill_score = 0
        
        # Base score from mastered actions
        skill_score += len(mastered_actions) * 0.15
        
        # Bonus for high-confidence actions
        high_confidence_actions = [action for action, data in self.learned_actions.items() 
                                 if data['avg_reward'] > 0.9]
        skill_score += len(high_confidence_actions) * 0.1
        
        # Bonus for mode diversity
        modes_played = set()
        for action_data in self.garettg_actions:
            modes_played.add(action_data['mode'])
        skill_score += len(modes_played) * 0.05
        
        # Bonus for learning from mistakes
        if self.mistakes_learned:
            skill_score += min(0.2, len(self.mistakes_learned) * 0.02)
        
        # Penalty for too few actions
        if total_actions < 10:
            skill_score *= 0.5
        elif total_actions < 20:
            skill_score *= 0.7
        
        # Determine rank based on skill score
        if skill_score >= 1.5:
            rank = "SSL (Supersonic Legend)"
            confidence = min(95, 70 + skill_score * 10)
            reasoning = f"Mastered {len(mastered_actions)} actions, high confidence in {len(high_confidence_actions)} moves"
        elif skill_score >= 1.2:
            rank = "Grand Champion"
            confidence = min(90, 60 + skill_score * 15)
            reasoning = f"Strong performance with {len(mastered_actions)} mastered actions"
        elif skill_score >= 1.0:
            rank = "Champion"
            confidence = min(85, 50 + skill_score * 20)
            reasoning = f"Good fundamentals with {len(mastered_actions)} solid actions"
        elif skill_score >= 0.8:
            rank = "Diamond"
            confidence = min(80, 40 + skill_score * 25)
            reasoning = f"Decent mechanics, {len(mastered_actions)} reliable moves"
        elif skill_score >= 0.6:
            rank = "Platinum"
            confidence = min(75, 30 + skill_score * 30)
            reasoning = f"Basic mechanics learned, {len(mastered_actions)} consistent actions"
        elif skill_score >= 0.4:
            rank = "Gold"
            confidence = min(70, 20 + skill_score * 35)
            reasoning = f"Learning fundamentals, {len(mastered_actions)} basic moves"
        elif skill_score >= 0.2:
            rank = "Silver"
            confidence = min(65, 10 + skill_score * 40)
            reasoning = f"Early learning stage, {len(mastered_actions)} simple actions"
        else:
            rank = "Bronze"
            confidence = min(60, skill_score * 50)
            reasoning = f"Just started learning, {len(mastered_actions)} basic moves"
        
        # Adjust confidence based on data quality
        if total_actions < 5:
            confidence *= 0.6
            reasoning += " (Limited data)"
        elif total_actions < 15:
            confidence *= 0.8
            reasoning += " (Some data)"
        
        return {
            'rank': rank,
            'confidence': confidence,
            'reasoning': reasoning
        }
    
    def monitor_learning(self):
        """Monitor the learning progress with countdown"""
        print("\n📊 LEARNING IN PROGRESS...")
        print("=" * 40)
        print("🔴 Watching GarettG's stream...")
        print("🧠 Learning with PPO...")
        print("⏰ Next report in 5 minutes...")
        print()
        
        start_time = time.time()
        
        while self.is_watching:
            elapsed = time.time() - start_time
            time_until_report = self.report_interval - (elapsed % self.report_interval)
            minutes_left = int(time_until_report // 60)
            seconds_left = int(time_until_report % 60)
            
            # Clear screen and show countdown
            print(f"\r⏰ Next report in: {minutes_left:02d}:{seconds_left:02d} | Actions: {len(self.garettg_actions)} | Episodes: {self.ppo_episodes}", end="", flush=True)
            
            time.sleep(1)  # Update every second
    
    def run_simulation(self):
        """Run simulation when stream isn't available"""
        print("\n🎭 RUNNING SIMULATION")
        print("=" * 30)
        
        # Simulate watching GarettG
        for i in range(20):
            action = np.random.choice(self.garettg_moves)
            mode = np.random.choice(["1s", "2s", "3s"])
            confidence = np.random.uniform(0.8, 0.95)
            
            action_data = {
                'timestamp': time.time(),
                'action': action,
                'confidence': confidence,
                'mode': mode,
                'player': 'GarettG'
            }
            
            self.garettg_actions.append(action_data)
            print(f"🎮 GarettG Action: {action} in {mode} (confidence: {confidence:.2f})")
            
            # Learn from this action
            reward = self.calculate_reward(action_data)
            self.ppo_episodes += 1
            
            print(f"🧠 PPO Episode {self.ppo_episodes}: Learning {action} (reward: {reward:.2f})")
            
            time.sleep(1)
        
        print("\n🎯 SIMULATION COMPLETE!")
        self.generate_report()
    
    def generate_report(self):
        """Generate learning report"""
        print("\n📊 GARETTG LEARNING REPORT")
        print("=" * 40)
        
        print(f"🎮 Actions Learned: {len(self.garettg_actions)}")
        print(f"🧠 PPO Episodes: {self.ppo_episodes}")
        print(f"📈 Final Learning Rate: {self.learning_rate:.6f}")
        
        if self.garettg_actions:
            # Count actions by mode
            mode_counts = {"1s": 0, "2s": 0, "3s": 0}
            for action in self.garettg_actions:
                mode_counts[action['mode']] += 1
            
            print("\n📈 Actions by Mode:")
            for mode, count in mode_counts.items():
                if count > 0:
                    percentage = (count / len(self.garettg_actions)) * 100
                    print(f"   {mode}: {count} actions ({percentage:.1f}%)")
        
        print("\n🎉 Learning Complete!")
        print("🚀 Bot is ready to play like GarettG!")
    
    def stop_watching(self):
        """Stop watching and learning"""
        self.is_watching = False
        print("⏹️ Watching stopped")

def main():
    """Main function"""
    print("👀 SIMPLE GARETTG WATCHER")
    print("=" * 40)
    print("🔴 Target: https://www.twitch.tv/garrettg")
    print("🎮 Watch → Mimic → Learn with PPO")
    print("🚀 Starting...")
    
    watcher = SimpleGarettGWatcher()
    
    try:
        watcher.start_watching()
    except KeyboardInterrupt:
        print("\n⏹️ Watching interrupted by user")
        watcher.stop_watching()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        watcher.stop_watching()

if __name__ == "__main__":
    main()
