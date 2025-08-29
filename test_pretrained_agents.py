#!/usr/bin/env python3
"""
Test All Pretrained Agents
Tests each pretrained agent individually to verify they work and play correctly
"""

import os
import sys
import time
import torch
import numpy as np
from pathlib import Path
import rlgym.api as api
from rlgym.api import RLGym

# Add pretrained agents to path
sys.path.append('pretrained_agents')
sys.path.append('pretrained_agents/nexto')
sys.path.append('pretrained_agents/necto')
sys.path.append('pretrained_agents/KBB')
sys.path.append('pretrained_agents/GP')

class PretrainedAgentTester:
    """Test all pretrained agents individually"""
    
    def __init__(self):
        self.agents = {}
        self.test_results = {}
        self.env = None
        
    def setup_environment(self):
        """Setup RLGym environment for testing"""
        try:
            print("🔧 Setting up RLGym environment...")
            
            # Create environment using rlgym 2.0.1 API
            self.env = RLGym(
                team_size=1,  # 1v1 for testing
                tick_skip=4,
                spawn_opponents=False,  # Just test our agent
                self_play=False,
                game_speed=100,
                gravity=1.0,
                boost_consumption=1.0,
                copy_gamestate_every_step=False
            )
            
            print("✅ Environment setup complete")
            return True
            
        except Exception as e:
            print(f"❌ Error setting up environment: {e}")
            return False
    
    def load_nexto_agent(self):
        """Load and test Nexto agent"""
        try:
            print("\n🤖 Testing NEXTO Agent")
            print("=" * 40)
            
            # Import Nexto
            from nexto_v2 import Nexto
            from nexto_v2_obs import NextoObs
            
            # Load model
            model_path = "pretrained_agents/nexto/nexto-model.pt"
            if not os.path.exists(model_path):
                print(f"❌ Nexto model not found: {model_path}")
                return False
            
            # Create agent
            nexto = Nexto(model_path)
            self.agents['nexto'] = nexto
            
            print("✅ Nexto agent loaded successfully")
            print(f"📁 Model: {model_path}")
            print(f"🧠 Model size: {os.path.getsize(model_path) / 1024 / 1024:.1f} MB")
            
            return True
            
        except Exception as e:
            print(f"❌ Error loading Nexto: {e}")
            return False
    
    def load_necto_agent(self):
        """Load and test Necto agent"""
        try:
            print("\n🤖 Testing NECTO Agent")
            print("=" * 40)
            
            # Import Necto
            from necto_v1 import Necto
            from necto_v1_obs import NectoObs
            
            # Load model
            model_path = "pretrained_agents/necto/necto-model-30Y.pt"
            if not os.path.exists(model_path):
                print(f"❌ Necto model not found: {model_path}")
                return False
            
            # Create agent
            necto = Necto(model_path)
            self.agents['necto'] = necto
            
            print("✅ Necto agent loaded successfully")
            print(f"📁 Model: {model_path}")
            print(f"🧠 Model size: {os.path.getsize(model_path) / 1024 / 1024:.1f} MB")
            
            return True
            
        except Exception as e:
            print(f"❌ Error loading Necto: {e}")
            return False
    
    def load_kbb_agent(self):
        """Load and test KBB agent"""
        try:
            print("\n🤖 Testing KBB Agent")
            print("=" * 40)
            
            # Import KBB
            from kbb import KBB
            from KBBObs import KBBObs
            
            # Create agent
            kbb = KBB()
            self.agents['kbb'] = kbb
            
            print("✅ KBB agent loaded successfully")
            print("📁 KBB is a rule-based agent")
            
            return True
            
        except Exception as e:
            print(f"❌ Error loading KBB: {e}")
            return False
    
    def load_gp_agent(self):
        """Load and test GP agent"""
        try:
            print("\n🤖 Testing GP Agent")
            print("=" * 40)
            
            # Import GP
            from GP import GP
            
            # Create agent
            gp = GP()
            self.agents['gp'] = gp
            
            print("✅ GP agent loaded successfully")
            print("📁 GP is a rule-based agent")
            
            return True
            
        except Exception as e:
            print(f"❌ Error loading GP: {e}")
            return False
    
    def test_agent(self, agent_name, agent, num_episodes=5):
        """Test a specific agent"""
        try:
            print(f"\n🎮 Testing {agent_name.upper()} Agent")
            print("=" * 50)
            
            if not self.env:
                print("❌ Environment not setup")
                return False
            
            episode_rewards = []
            episode_lengths = []
            
            for episode in range(num_episodes):
                print(f"\n📊 Episode {episode + 1}/{num_episodes}")
                
                obs = self.env.reset()
                total_reward = 0
                steps = 0
                
                while True:
                    try:
                        # Get action from agent
                        action = agent.act(obs)
                        
                        # Step environment
                        obs, reward, done, info = self.env.step(action)
                        total_reward += reward
                        steps += 1
                        
                        if done:
                            break
                            
                        # Limit episode length
                        if steps > 1000:
                            break
                            
                    except Exception as step_error:
                        print(f"❌ Error in step: {step_error}")
                        break
                
                episode_rewards.append(total_reward)
                episode_lengths.append(steps)
                
                print(f"   Reward: {total_reward:.2f}")
                print(f"   Steps: {steps}")
            
            # Calculate statistics
            avg_reward = np.mean(episode_rewards)
            avg_length = np.mean(episode_lengths)
            std_reward = np.std(episode_rewards)
            
            print(f"\n📈 {agent_name.upper()} Results:")
            print(f"   Average Reward: {avg_reward:.2f} ± {std_reward:.2f}")
            print(f"   Average Length: {avg_length:.1f} steps")
            print(f"   Episodes: {num_episodes}")
            
            # Store results
            self.test_results[agent_name] = {
                'avg_reward': avg_reward,
                'avg_length': avg_length,
                'std_reward': std_reward,
                'episode_rewards': episode_rewards,
                'episode_lengths': episode_lengths,
                'success': True
            }
            
            return True
            
        except Exception as e:
            print(f"❌ Error testing {agent_name}: {e}")
            self.test_results[agent_name] = {
                'success': False,
                'error': str(e)
            }
            return False
    
    def test_all_agents(self):
        """Test all available agents"""
        try:
            print("🚀 TESTING ALL PRETRAINED AGENTS")
            print("=" * 60)
            print("🎮 Make sure Rocket League is open in free play!")
            print("⏳ Starting tests in 3 seconds...")
            time.sleep(3)
            
            # Setup environment
            if not self.setup_environment():
                return False
            
            # Load all agents
            agents_loaded = 0
            
            if self.load_nexto_agent():
                agents_loaded += 1
            
            if self.load_necto_agent():
                agents_loaded += 1
            
            if self.load_kbb_agent():
                agents_loaded += 1
            
            if self.load_gp_agent():
                agents_loaded += 1
            
            print(f"\n✅ Loaded {agents_loaded} agents successfully")
            
            if agents_loaded == 0:
                print("❌ No agents loaded successfully")
                return False
            
            # Test each agent
            for agent_name, agent in self.agents.items():
                self.test_agent(agent_name, agent, num_episodes=3)
                time.sleep(2)  # Brief pause between agents
            
            # Print summary
            self.print_summary()
            
            return True
            
        except Exception as e:
            print(f"❌ Error in testing: {e}")
            return False
    
    def print_summary(self):
        """Print testing summary"""
        try:
            print("\n🏆 TESTING SUMMARY")
            print("=" * 60)
            
            successful_agents = []
            failed_agents = []
            
            for agent_name, results in self.test_results.items():
                if results.get('success', False):
                    successful_agents.append((agent_name, results))
                else:
                    failed_agents.append((agent_name, results))
            
            print(f"✅ Successful Agents: {len(successful_agents)}")
            print(f"❌ Failed Agents: {len(failed_agents)}")
            
            if successful_agents:
                print("\n📊 Performance Ranking:")
                # Sort by average reward
                successful_agents.sort(key=lambda x: x[1]['avg_reward'], reverse=True)
                
                for i, (agent_name, results) in enumerate(successful_agents, 1):
                    print(f"   {i}. {agent_name.upper()}: {results['avg_reward']:.2f} avg reward")
            
            if failed_agents:
                print("\n❌ Failed Agents:")
                for agent_name, results in failed_agents:
                    error = results.get('error', 'Unknown error')
                    print(f"   - {agent_name.upper()}: {error}")
            
            print("\n🎯 Ready to create super brain!")
            
        except Exception as e:
            print(f"❌ Error printing summary: {e}")

def main():
    """Main testing function"""
    try:
        print("🤖 PRETRAINED AGENT TESTER")
        print("=" * 50)
        print("🎮 Testing all pretrained agents individually")
        print("📊 Will rank them by performance")
        print("🧠 Results will be used to create super brain")
        
        tester = PretrainedAgentTester()
        success = tester.test_all_agents()
        
        if success:
            print("\n✅ All tests completed successfully!")
            print("🚀 Ready to create super brain with best agents")
        else:
            print("\n❌ Some tests failed")
            print("🔧 Check the errors above")
        
    except Exception as e:
        print(f"❌ Error in main: {e}")

if __name__ == "__main__":
    main()

Test All Pretrained Agents
Tests each pretrained agent individually to verify they work and play correctly
"""

import os
import sys
import time
import torch
import numpy as np
from pathlib import Path
import rlgym.api as api
from rlgym.api import RLGym

# Add pretrained agents to path
sys.path.append('pretrained_agents')
sys.path.append('pretrained_agents/nexto')
sys.path.append('pretrained_agents/necto')
sys.path.append('pretrained_agents/KBB')
sys.path.append('pretrained_agents/GP')

class PretrainedAgentTester:
    """Test all pretrained agents individually"""
    
    def __init__(self):
        self.agents = {}
        self.test_results = {}
        self.env = None
        
    def setup_environment(self):
        """Setup RLGym environment for testing"""
        try:
            print("🔧 Setting up RLGym environment...")
            
            # Create environment using rlgym 2.0.1 API
            self.env = RLGym(
                team_size=1,  # 1v1 for testing
                tick_skip=4,
                spawn_opponents=False,  # Just test our agent
                self_play=False,
                game_speed=100,
                gravity=1.0,
                boost_consumption=1.0,
                copy_gamestate_every_step=False
            )
            
            print("✅ Environment setup complete")
            return True
            
        except Exception as e:
            print(f"❌ Error setting up environment: {e}")
            return False
    
    def load_nexto_agent(self):
        """Load and test Nexto agent"""
        try:
            print("\n🤖 Testing NEXTO Agent")
            print("=" * 40)
            
            # Import Nexto
            from nexto_v2 import Nexto
            from nexto_v2_obs import NextoObs
            
            # Load model
            model_path = "pretrained_agents/nexto/nexto-model.pt"
            if not os.path.exists(model_path):
                print(f"❌ Nexto model not found: {model_path}")
                return False
            
            # Create agent
            nexto = Nexto(model_path)
            self.agents['nexto'] = nexto
            
            print("✅ Nexto agent loaded successfully")
            print(f"📁 Model: {model_path}")
            print(f"🧠 Model size: {os.path.getsize(model_path) / 1024 / 1024:.1f} MB")
            
            return True
            
        except Exception as e:
            print(f"❌ Error loading Nexto: {e}")
            return False
    
    def load_necto_agent(self):
        """Load and test Necto agent"""
        try:
            print("\n🤖 Testing NECTO Agent")
            print("=" * 40)
            
            # Import Necto
            from necto_v1 import Necto
            from necto_v1_obs import NectoObs
            
            # Load model
            model_path = "pretrained_agents/necto/necto-model-30Y.pt"
            if not os.path.exists(model_path):
                print(f"❌ Necto model not found: {model_path}")
                return False
            
            # Create agent
            necto = Necto(model_path)
            self.agents['necto'] = necto
            
            print("✅ Necto agent loaded successfully")
            print(f"📁 Model: {model_path}")
            print(f"🧠 Model size: {os.path.getsize(model_path) / 1024 / 1024:.1f} MB")
            
            return True
            
        except Exception as e:
            print(f"❌ Error loading Necto: {e}")
            return False
    
    def load_kbb_agent(self):
        """Load and test KBB agent"""
        try:
            print("\n🤖 Testing KBB Agent")
            print("=" * 40)
            
            # Import KBB
            from kbb import KBB
            from KBBObs import KBBObs
            
            # Create agent
            kbb = KBB()
            self.agents['kbb'] = kbb
            
            print("✅ KBB agent loaded successfully")
            print("📁 KBB is a rule-based agent")
            
            return True
            
        except Exception as e:
            print(f"❌ Error loading KBB: {e}")
            return False
    
    def load_gp_agent(self):
        """Load and test GP agent"""
        try:
            print("\n🤖 Testing GP Agent")
            print("=" * 40)
            
            # Import GP
            from GP import GP
            
            # Create agent
            gp = GP()
            self.agents['gp'] = gp
            
            print("✅ GP agent loaded successfully")
            print("📁 GP is a rule-based agent")
            
            return True
            
        except Exception as e:
            print(f"❌ Error loading GP: {e}")
            return False
    
    def test_agent(self, agent_name, agent, num_episodes=5):
        """Test a specific agent"""
        try:
            print(f"\n🎮 Testing {agent_name.upper()} Agent")
            print("=" * 50)
            
            if not self.env:
                print("❌ Environment not setup")
                return False
            
            episode_rewards = []
            episode_lengths = []
            
            for episode in range(num_episodes):
                print(f"\n📊 Episode {episode + 1}/{num_episodes}")
                
                obs = self.env.reset()
                total_reward = 0
                steps = 0
                
                while True:
                    try:
                        # Get action from agent
                        action = agent.act(obs)
                        
                        # Step environment
                        obs, reward, done, info = self.env.step(action)
                        total_reward += reward
                        steps += 1
                        
                        if done:
                            break
                            
                        # Limit episode length
                        if steps > 1000:
                            break
                            
                    except Exception as step_error:
                        print(f"❌ Error in step: {step_error}")
                        break
                
                episode_rewards.append(total_reward)
                episode_lengths.append(steps)
                
                print(f"   Reward: {total_reward:.2f}")
                print(f"   Steps: {steps}")
            
            # Calculate statistics
            avg_reward = np.mean(episode_rewards)
            avg_length = np.mean(episode_lengths)
            std_reward = np.std(episode_rewards)
            
            print(f"\n📈 {agent_name.upper()} Results:")
            print(f"   Average Reward: {avg_reward:.2f} ± {std_reward:.2f}")
            print(f"   Average Length: {avg_length:.1f} steps")
            print(f"   Episodes: {num_episodes}")
            
            # Store results
            self.test_results[agent_name] = {
                'avg_reward': avg_reward,
                'avg_length': avg_length,
                'std_reward': std_reward,
                'episode_rewards': episode_rewards,
                'episode_lengths': episode_lengths,
                'success': True
            }
            
            return True
            
        except Exception as e:
            print(f"❌ Error testing {agent_name}: {e}")
            self.test_results[agent_name] = {
                'success': False,
                'error': str(e)
            }
            return False
    
    def test_all_agents(self):
        """Test all available agents"""
        try:
            print("🚀 TESTING ALL PRETRAINED AGENTS")
            print("=" * 60)
            print("🎮 Make sure Rocket League is open in free play!")
            print("⏳ Starting tests in 3 seconds...")
            time.sleep(3)
            
            # Setup environment
            if not self.setup_environment():
                return False
            
            # Load all agents
            agents_loaded = 0
            
            if self.load_nexto_agent():
                agents_loaded += 1
            
            if self.load_necto_agent():
                agents_loaded += 1
            
            if self.load_kbb_agent():
                agents_loaded += 1
            
            if self.load_gp_agent():
                agents_loaded += 1
            
            print(f"\n✅ Loaded {agents_loaded} agents successfully")
            
            if agents_loaded == 0:
                print("❌ No agents loaded successfully")
                return False
            
            # Test each agent
            for agent_name, agent in self.agents.items():
                self.test_agent(agent_name, agent, num_episodes=3)
                time.sleep(2)  # Brief pause between agents
            
            # Print summary
            self.print_summary()
            
            return True
            
        except Exception as e:
            print(f"❌ Error in testing: {e}")
            return False
    
    def print_summary(self):
        """Print testing summary"""
        try:
            print("\n🏆 TESTING SUMMARY")
            print("=" * 60)
            
            successful_agents = []
            failed_agents = []
            
            for agent_name, results in self.test_results.items():
                if results.get('success', False):
                    successful_agents.append((agent_name, results))
                else:
                    failed_agents.append((agent_name, results))
            
            print(f"✅ Successful Agents: {len(successful_agents)}")
            print(f"❌ Failed Agents: {len(failed_agents)}")
            
            if successful_agents:
                print("\n📊 Performance Ranking:")
                # Sort by average reward
                successful_agents.sort(key=lambda x: x[1]['avg_reward'], reverse=True)
                
                for i, (agent_name, results) in enumerate(successful_agents, 1):
                    print(f"   {i}. {agent_name.upper()}: {results['avg_reward']:.2f} avg reward")
            
            if failed_agents:
                print("\n❌ Failed Agents:")
                for agent_name, results in failed_agents:
                    error = results.get('error', 'Unknown error')
                    print(f"   - {agent_name.upper()}: {error}")
            
            print("\n🎯 Ready to create super brain!")
            
        except Exception as e:
            print(f"❌ Error printing summary: {e}")

def main():
    """Main testing function"""
    try:
        print("🤖 PRETRAINED AGENT TESTER")
        print("=" * 50)
        print("🎮 Testing all pretrained agents individually")
        print("📊 Will rank them by performance")
        print("🧠 Results will be used to create super brain")
        
        tester = PretrainedAgentTester()
        success = tester.test_all_agents()
        
        if success:
            print("\n✅ All tests completed successfully!")
            print("🚀 Ready to create super brain with best agents")
        else:
            print("\n❌ Some tests failed")
            print("🔧 Check the errors above")
        
    except Exception as e:
        print(f"❌ Error in main: {e}")

if __name__ == "__main__":
    main()
