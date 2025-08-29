#!/usr/bin/env python3
"""
Launch Real SSL Controller
Launches the real SSL controller that actually controls Rocket League
Reads real game data from PC files and sends real inputs
"""

import time
import sys
import os
from real_ssl_controller import RealSSLController
from real_game_data_reader import RealGameDataReader

def main():
    """Main launcher function"""
    print("🏆 REAL SSL CONTROLLER LAUNCHER")
    print("=" * 60)
    print("🎯 Actually controls Rocket League")
    print("🧠 Reads real game data from PC files")
    print("⚡ Real inputs to real game")
    print("🎮 Practices in real free play")
    print("🚀 Ready to control your car!")
    
    # Check if Rocket League is running
    print("\n🔍 Checking if Rocket League is running...")
    data_reader = RealGameDataReader()
    
    if not data_reader.find_rocket_league_process():
        print("❌ Rocket League is not running!")
        print("💡 Please start Rocket League and go to free play")
        print("💡 Then run this script again")
        input("Press Enter to exit...")
        return
    
    print("✅ Rocket League is running!")
    
    # Create controller
    controller = RealSSLController()
    
    try:
        # Connect to the game
        print("\n🔌 Connecting to Rocket League...")
        if not controller.connect_to_game():
            print("❌ Failed to connect to Rocket League!")
            print("💡 Make sure Rocket League is in focus")
            input("Press Enter to exit...")
            return
        
        print("✅ Connected to Rocket League!")
        print("🎮 Ready to control your car!")
        
        # Ask user what they want to do
        print("\n📋 What would you like to do?")
        print("1. 🎮 Practice in free play (60 minutes)")
        print("2. 🎮 Practice in free play (30 minutes)")
        print("3. 🎮 Practice in free play (120 minutes)")
        print("4. 🎮 Custom practice duration")
        print("5. 🧪 Test connection only")
        print("6. 🛑 Exit")
        
        choice = input("\n🎯 Enter your choice (1-6): ").strip()
        
        if choice == "1":
            print("\n🚀 Starting 60-minute free play practice...")
            controller.run_real_freeplay_practice(60)
        elif choice == "2":
            print("\n🚀 Starting 30-minute free play practice...")
            controller.run_real_freeplay_practice(30)
        elif choice == "3":
            print("\n🚀 Starting 120-minute free play practice...")
            controller.run_real_freeplay_practice(120)
        elif choice == "4":
            try:
                duration = int(input("⏰ Enter practice duration in minutes: "))
                print(f"\n🚀 Starting {duration}-minute free play practice...")
                controller.run_real_freeplay_practice(duration)
            except ValueError:
                print("❌ Invalid duration! Please enter a number.")
        elif choice == "5":
            print("\n🧪 Testing connection...")
            game_data = controller.data_reader.get_real_game_data()
            if game_data:
                print("✅ Connection test successful!")
                print(f"🚗 Car position: {game_data['car_data']['position']}")
                print(f"⚽ Ball position: {game_data['ball_data']['position']}")
                print(f"⛽ Boost: {game_data['car_data']['boost']:.1f}")
            else:
                print("❌ Connection test failed!")
        elif choice == "6":
            print("👋 Goodbye!")
            return
        else:
            print("❌ Invalid choice!")
            return
        
        # Ask if user wants to go online
        if choice in ["1", "2", "3", "4"]:
            print("\n🌐 Ready to go online? (y/n)")
            response = input().lower()
            if response == 'y':
                print("🌐 Going online...")
                # TODO: Implement online mode
                print("⚠️ Online mode not implemented yet")
        
    except KeyboardInterrupt:
        print("\n⏹️ Practice interrupted by user")
        controller.stop_control()
        controller.generate_real_learning_report()
    except Exception as e:
        print(f"\n❌ Critical Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n👋 Goodbye!")

if __name__ == "__main__":
    main()
