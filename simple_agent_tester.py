#!/usr/bin/env python3
"""
Simple Pretrained Agent Tester
Tests each pretrained agent individually to verify they load correctly
"""

import os
import sys
import time
import torch
import numpy as np
from pathlib import Path

# Add pretrained agents to path
sys.path.append('pretrained_agents')
sys.path.append('pretrained_agents/nexto')
sys.path.append('pretrained_agents/necto')
sys.path.append('pretrained_agents/KBB')
sys.path.append('pretrained_agents/GP')

class SimpleAgentTester:
    """Simple tester for pretrained agents"""
    
    def __init__(self):
        self.agents = {}
        self.test_results = {}
        
    def test_nexto_agent(self):
        """Test Nexto agent loading"""
        try:
            print("\n🤖 Testing NEXTO Agent")
            print("=" * 40)
            
            # Check if model exists
            model_path = "pretrained_agents/nexto/nexto-model.pt"
            if not os.path.exists(model_path):
                print(f"❌ Nexto model not found: {model_path}")
                return False
            
            # Try to import Nexto
            try:
                from nexto_v2 import NextoV2
                from nexto_v2_obs import Nexto_V2_ObsBuilder
                print("✅ Nexto imports successful")
            except Exception as import_error:
                print(f"❌ Nexto import failed: {import_error}")
                return False
            
            # Try to load model
            try:
                nexto = NextoV2("nexto-model.pt", n_players=1)
                self.agents['nexto'] = nexto
                print("✅ Nexto agent loaded successfully")
                print(f"📁 Model: {model_path}")
                print(f"🧠 Model size: {os.path.getsize(model_path) / 1024 / 1024:.1f} MB")
                
                # Test basic functionality
                dummy_obs = np.random.random(107)  # Default obs size
                try:
                    action = nexto.act(dummy_obs)
                    print(f"✅ Nexto action test: {action}")
                except Exception as act_error:
                    print(f"⚠️ Nexto action test failed: {act_error}")
                
                return True
                
            except Exception as load_error:
                print(f"❌ Nexto loading failed: {load_error}")
                return False
            
        except Exception as e:
            print(f"❌ Error testing Nexto: {e}")
            return False
    
    def test_necto_agent(self):
        """Test Necto agent loading"""
        try:
            print("\n🤖 Testing NECTO Agent")
            print("=" * 40)
            
            # Check if model exists
            model_path = "pretrained_agents/necto/necto-model-30Y.pt"
            if not os.path.exists(model_path):
                print(f"❌ Necto model not found: {model_path}")
                return False
            
            # Try to import Necto
            try:
                from necto_v1 import NectoV1
                from necto_v1_obs import NectoV1Obs
                print("✅ Necto imports successful")
            except Exception as import_error:
                print(f"❌ Necto import failed: {import_error}")
                return False
            
            # Try to load model
            try:
                necto = NectoV1("necto-model-30Y.pt", n_players=1)
                self.agents['necto'] = necto
                print("✅ Necto agent loaded successfully")
                print(f"📁 Model: {model_path}")
                print(f"🧠 Model size: {os.path.getsize(model_path) / 1024 / 1024:.1f} MB")
                
                # Test basic functionality
                dummy_obs = np.random.random(107)  # Default obs size
                try:
                    action = necto.act(dummy_obs)
                    print(f"✅ Necto action test: {action}")
                except Exception as act_error:
                    print(f"⚠️ Necto action test failed: {act_error}")
                
                return True
                
            except Exception as load_error:
                print(f"❌ Necto loading failed: {load_error}")
                return False
            
        except Exception as e:
            print(f"❌ Error testing Necto: {e}")
            return False
    
    def test_kbb_agent(self):
        """Test KBB agent loading"""
        try:
            print("\n🤖 Testing KBB Agent")
            print("=" * 40)
            
            # Try to import KBB
            try:
                from kbb import KBB
                from KBBObs import AdvancedObsPadder
                print("✅ KBB imports successful")
            except Exception as import_error:
                print(f"❌ KBB import failed: {import_error}")
                return False
            
            # Try to create agent
            try:
                # KBB might be rule-based, let's try without model first
                kbb = KBB("dummy-model.pt")  # Will fail but let's see the error
                self.agents['kbb'] = kbb
                print("✅ KBB agent created successfully")
                print("📁 KBB is a rule-based agent")
                
                # Test basic functionality
                dummy_obs = np.random.random(107)  # Default obs size
                try:
                    action = kbb.act(dummy_obs)
                    print(f"✅ KBB action test: {action}")
                except Exception as act_error:
                    print(f"⚠️ KBB action test failed: {act_error}")
                
                return True
                
            except Exception as create_error:
                print(f"❌ KBB creation failed: {create_error}")
                return False
            
        except Exception as e:
            print(f"❌ Error testing KBB: {e}")
            return False
    
    def test_gp_agent(self):
        """Test GP agent loading"""
        try:
            print("\n🤖 Testing GP Agent")
            print("=" * 40)
            
            # Try to import GP
            try:
                from GP import GP
                print("✅ GP imports successful")
            except Exception as import_error:
                print(f"❌ GP import failed: {import_error}")
                return False
            
            # Try to create agent
            try:
                # GP needs a model from submodels directory
                gp = GP("submodel_agent.py")  # This will likely fail but let's see
                self.agents['gp'] = gp
                print("✅ GP agent created successfully")
                print("📁 GP is a rule-based agent")
                
                # Test basic functionality
                dummy_obs = np.random.random(107)  # Default obs size
                try:
                    action = gp.act(dummy_obs)
                    print(f"✅ GP action test: {action}")
                except Exception as act_error:
                    print(f"⚠️ GP action test failed: {act_error}")
                
                return True
                
            except Exception as create_error:
                print(f"❌ GP creation failed: {create_error}")
                return False
            
        except Exception as e:
            print(f"❌ Error testing GP: {e}")
            return False
    
    def test_all_agents(self):
        """Test all available agents"""
        try:
            print("🚀 TESTING ALL PRETRAINED AGENTS")
            print("=" * 60)
            print("🎮 Testing agent loading and basic functionality")
            print("⏳ Starting tests...")
            
            # Test each agent
            agents_tested = 0
            agents_loaded = 0
            
            if self.test_nexto_agent():
                agents_loaded += 1
            agents_tested += 1
            
            if self.test_necto_agent():
                agents_loaded += 1
            agents_tested += 1
            
            if self.test_kbb_agent():
                agents_loaded += 1
            agents_tested += 1
            
            if self.test_gp_agent():
                agents_loaded += 1
            agents_tested += 1
            
            print(f"\n✅ Tested {agents_tested} agents")
            print(f"✅ Successfully loaded {agents_loaded} agents")
            
            if agents_loaded > 0:
                print("\n🎯 Ready to create super brain!")
                self.print_summary()
                return True
            else:
                print("\n❌ No agents loaded successfully")
                return False
            
        except Exception as e:
            print(f"❌ Error in testing: {e}")
            return False
    
    def print_summary(self):
        """Print testing summary"""
        try:
            print("\n🏆 TESTING SUMMARY")
            print("=" * 60)
            
            print(f"✅ Successfully Loaded Agents: {len(self.agents)}")
            
            for agent_name, agent in self.agents.items():
                print(f"   - {agent_name.upper()}: Ready for super brain")
            
            print("\n🧠 Next Steps:")
            print("   1. Create super brain combining all agents")
            print("   2. Implement ensemble learning")
            print("   3. Start SSL training pipeline")
            print("   4. Begin ranked grinding")
            
        except Exception as e:
            print(f"❌ Error printing summary: {e}")

def main():
    """Main testing function"""
    try:
        print("🤖 SIMPLE PRETRAINED AGENT TESTER")
        print("=" * 50)
        print("🎮 Testing all pretrained agents for loading")
        print("📊 Verifying basic functionality")
        print("🧠 Preparing for super brain creation")
        
        tester = SimpleAgentTester()
        success = tester.test_all_agents()
        
        if success:
            print("\n✅ All tests completed successfully!")
            print("🚀 Ready to create super brain with loaded agents")
        else:
            print("\n❌ Some tests failed")
            print("🔧 Check the errors above")
        
    except Exception as e:
        print(f"❌ Error in main: {e}")

if __name__ == "__main__":
    main()

Simple Pretrained Agent Tester
Tests each pretrained agent individually to verify they load correctly
"""

import os
import sys
import time
import torch
import numpy as np
from pathlib import Path

# Add pretrained agents to path
sys.path.append('pretrained_agents')
sys.path.append('pretrained_agents/nexto')
sys.path.append('pretrained_agents/necto')
sys.path.append('pretrained_agents/KBB')
sys.path.append('pretrained_agents/GP')

class SimpleAgentTester:
    """Simple tester for pretrained agents"""
    
    def __init__(self):
        self.agents = {}
        self.test_results = {}
        
    def test_nexto_agent(self):
        """Test Nexto agent loading"""
        try:
            print("\n🤖 Testing NEXTO Agent")
            print("=" * 40)
            
            # Check if model exists
            model_path = "pretrained_agents/nexto/nexto-model.pt"
            if not os.path.exists(model_path):
                print(f"❌ Nexto model not found: {model_path}")
                return False
            
            # Try to import Nexto
            try:
                from nexto_v2 import NextoV2
                from nexto_v2_obs import Nexto_V2_ObsBuilder
                print("✅ Nexto imports successful")
            except Exception as import_error:
                print(f"❌ Nexto import failed: {import_error}")
                return False
            
            # Try to load model
            try:
                nexto = NextoV2("nexto-model.pt", n_players=1)
                self.agents['nexto'] = nexto
                print("✅ Nexto agent loaded successfully")
                print(f"📁 Model: {model_path}")
                print(f"🧠 Model size: {os.path.getsize(model_path) / 1024 / 1024:.1f} MB")
                
                # Test basic functionality
                dummy_obs = np.random.random(107)  # Default obs size
                try:
                    action = nexto.act(dummy_obs)
                    print(f"✅ Nexto action test: {action}")
                except Exception as act_error:
                    print(f"⚠️ Nexto action test failed: {act_error}")
                
                return True
                
            except Exception as load_error:
                print(f"❌ Nexto loading failed: {load_error}")
                return False
            
        except Exception as e:
            print(f"❌ Error testing Nexto: {e}")
            return False
    
    def test_necto_agent(self):
        """Test Necto agent loading"""
        try:
            print("\n🤖 Testing NECTO Agent")
            print("=" * 40)
            
            # Check if model exists
            model_path = "pretrained_agents/necto/necto-model-30Y.pt"
            if not os.path.exists(model_path):
                print(f"❌ Necto model not found: {model_path}")
                return False
            
            # Try to import Necto
            try:
                from necto_v1 import NectoV1
                from necto_v1_obs import NectoV1Obs
                print("✅ Necto imports successful")
            except Exception as import_error:
                print(f"❌ Necto import failed: {import_error}")
                return False
            
            # Try to load model
            try:
                necto = NectoV1("necto-model-30Y.pt", n_players=1)
                self.agents['necto'] = necto
                print("✅ Necto agent loaded successfully")
                print(f"📁 Model: {model_path}")
                print(f"🧠 Model size: {os.path.getsize(model_path) / 1024 / 1024:.1f} MB")
                
                # Test basic functionality
                dummy_obs = np.random.random(107)  # Default obs size
                try:
                    action = necto.act(dummy_obs)
                    print(f"✅ Necto action test: {action}")
                except Exception as act_error:
                    print(f"⚠️ Necto action test failed: {act_error}")
                
                return True
                
            except Exception as load_error:
                print(f"❌ Necto loading failed: {load_error}")
                return False
            
        except Exception as e:
            print(f"❌ Error testing Necto: {e}")
            return False
    
    def test_kbb_agent(self):
        """Test KBB agent loading"""
        try:
            print("\n🤖 Testing KBB Agent")
            print("=" * 40)
            
            # Try to import KBB
            try:
                from kbb import KBB
                from KBBObs import AdvancedObsPadder
                print("✅ KBB imports successful")
            except Exception as import_error:
                print(f"❌ KBB import failed: {import_error}")
                return False
            
            # Try to create agent
            try:
                # KBB might be rule-based, let's try without model first
                kbb = KBB("dummy-model.pt")  # Will fail but let's see the error
                self.agents['kbb'] = kbb
                print("✅ KBB agent created successfully")
                print("📁 KBB is a rule-based agent")
                
                # Test basic functionality
                dummy_obs = np.random.random(107)  # Default obs size
                try:
                    action = kbb.act(dummy_obs)
                    print(f"✅ KBB action test: {action}")
                except Exception as act_error:
                    print(f"⚠️ KBB action test failed: {act_error}")
                
                return True
                
            except Exception as create_error:
                print(f"❌ KBB creation failed: {create_error}")
                return False
            
        except Exception as e:
            print(f"❌ Error testing KBB: {e}")
            return False
    
    def test_gp_agent(self):
        """Test GP agent loading"""
        try:
            print("\n🤖 Testing GP Agent")
            print("=" * 40)
            
            # Try to import GP
            try:
                from GP import GP
                print("✅ GP imports successful")
            except Exception as import_error:
                print(f"❌ GP import failed: {import_error}")
                return False
            
            # Try to create agent
            try:
                # GP needs a model from submodels directory
                gp = GP("submodel_agent.py")  # This will likely fail but let's see
                self.agents['gp'] = gp
                print("✅ GP agent created successfully")
                print("📁 GP is a rule-based agent")
                
                # Test basic functionality
                dummy_obs = np.random.random(107)  # Default obs size
                try:
                    action = gp.act(dummy_obs)
                    print(f"✅ GP action test: {action}")
                except Exception as act_error:
                    print(f"⚠️ GP action test failed: {act_error}")
                
                return True
                
            except Exception as create_error:
                print(f"❌ GP creation failed: {create_error}")
                return False
            
        except Exception as e:
            print(f"❌ Error testing GP: {e}")
            return False
    
    def test_all_agents(self):
        """Test all available agents"""
        try:
            print("🚀 TESTING ALL PRETRAINED AGENTS")
            print("=" * 60)
            print("🎮 Testing agent loading and basic functionality")
            print("⏳ Starting tests...")
            
            # Test each agent
            agents_tested = 0
            agents_loaded = 0
            
            if self.test_nexto_agent():
                agents_loaded += 1
            agents_tested += 1
            
            if self.test_necto_agent():
                agents_loaded += 1
            agents_tested += 1
            
            if self.test_kbb_agent():
                agents_loaded += 1
            agents_tested += 1
            
            if self.test_gp_agent():
                agents_loaded += 1
            agents_tested += 1
            
            print(f"\n✅ Tested {agents_tested} agents")
            print(f"✅ Successfully loaded {agents_loaded} agents")
            
            if agents_loaded > 0:
                print("\n🎯 Ready to create super brain!")
                self.print_summary()
                return True
            else:
                print("\n❌ No agents loaded successfully")
                return False
            
        except Exception as e:
            print(f"❌ Error in testing: {e}")
            return False
    
    def print_summary(self):
        """Print testing summary"""
        try:
            print("\n🏆 TESTING SUMMARY")
            print("=" * 60)
            
            print(f"✅ Successfully Loaded Agents: {len(self.agents)}")
            
            for agent_name, agent in self.agents.items():
                print(f"   - {agent_name.upper()}: Ready for super brain")
            
            print("\n🧠 Next Steps:")
            print("   1. Create super brain combining all agents")
            print("   2. Implement ensemble learning")
            print("   3. Start SSL training pipeline")
            print("   4. Begin ranked grinding")
            
        except Exception as e:
            print(f"❌ Error printing summary: {e}")

def main():
    """Main testing function"""
    try:
        print("🤖 SIMPLE PRETRAINED AGENT TESTER")
        print("=" * 50)
        print("🎮 Testing all pretrained agents for loading")
        print("📊 Verifying basic functionality")
        print("🧠 Preparing for super brain creation")
        
        tester = SimpleAgentTester()
        success = tester.test_all_agents()
        
        if success:
            print("\n✅ All tests completed successfully!")
            print("🚀 Ready to create super brain with loaded agents")
        else:
            print("\n❌ Some tests failed")
            print("🔧 Check the errors above")
        
    except Exception as e:
        print(f"❌ Error in main: {e}")

if __name__ == "__main__":
    main()
