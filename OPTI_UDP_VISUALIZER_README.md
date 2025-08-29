# 🤖 Opti UDP Visualizer System

## Overview
We've created a custom lightweight UDP-based visualizer for RocketSim communication, similar to RLViser but specifically designed for our JSTN bot training system. This system provides real-time 3D visualization of bot training with multi-panel views showing bot thoughts, actions, and game state.

## 🎮 Features

### Multi-Panel Layout
- **Left Panel (40%)**: 3D game view with isometric perspective
- **Middle Panel (35%)**: Bot's thoughts, actions, and training console
- **Right Panel (25%)**: 2D tactical map and learning progress

### Real-Time Data
- Live UDP packet communication from training system
- Real-time bot thoughts and decision-making process
- Training progress with mechanics learning (aerial, flip reset, double tap, etc.)
- Game state visualization (ball, cars, boost pads, goals)

### Controls
- **ESC**: Toggle menu
- **1-8**: Focus on different cars
- **9**: Director camera
- **0**: Free camera
- **WASD**: Move camera
- **Space/Ctrl**: Move up/down
- **P**: Pause/Play
- **+/-**: Speed up/down
- **=**: Reset speed to 1x
- **R**: Reset ball to goal
- **Left Click**: Drag cars and ball (when menu is off)

## 📁 Files Created

### 1. `opti_udp_visualizer.py`
**Main UDP Visualizer Application**
- Listens for UDP packets on port 37020
- Parses RocketSim-compatible game state data
- Renders 3D game view with perspective projection
- Displays bot training data and thoughts
- Multi-panel interface with real-time updates

### 2. `udp_packet_sender.py`
**UDP Packet Communication System**
- Sends game state data via UDP packets
- Compatible with RLGym GameState format
- Converts RLGym data to RocketSim packet format
- Includes dummy data generation for testing
- Thread-safe communication with visualizer

### 3. `launch_opti_udp_training.py`
**System Launcher**
- Starts both UDP visualizer and training system
- Manages process lifecycle
- Provides system status and controls information
- Handles graceful shutdown

## 🔧 Technical Details

### UDP Protocol
- **IP**: 127.0.0.1 (localhost)
- **Port**: 37020
- **Format**: Binary packet with structured data
- **Rate**: 60 FPS for smooth visualization

### Packet Structure
```
[Ball Position (12 bytes)] [Ball Velocity (12 bytes)] [Ball Angular Velocity (12 bytes)]
[Number of Cars (4 bytes)] [Car Data...] [Number of Boost Pads (4 bytes)] [Boost Pad Data...]
```

### Car Data Format
```
[Position (12 bytes)] [Rotation (12 bytes)] [Velocity (12 bytes)] 
[Angular Velocity (12 bytes)] [Boost (4 bytes)] [Flags (4 bytes)]
```

### Boost Pad Data Format
```
[Position (12 bytes)] [Active Flag (1 byte)] [Large Flag (1 byte)]
```

## 🚀 Usage

### Quick Start
```bash
# Start the complete system
python launch_opti_udp_training.py
```

### Manual Start
```bash
# Terminal 1: Start UDP Visualizer
python opti_udp_visualizer.py

# Terminal 2: Start Training System
python jstn_multi_mode_trainer.py
```

### Testing UDP Communication
```bash
# Test UDP packet sender
python udp_packet_sender.py
```

## 🎯 Integration with Training System

The UDP visualizer is fully integrated with our JSTN multi-mode training system:

1. **Automatic UDP Sender**: Training system automatically creates UDP sender
2. **Real-time Updates**: Game state sent via UDP packets during training
3. **Multi-mode Support**: Works with 1s, 2s, and 3s training modes
4. **Bot Insights**: Shows what the bot is thinking and doing in real-time

## 🎮 Visualizer Features

### 3D Game View
- Isometric perspective projection
- Real-time ball, car, and boost pad rendering
- Field boundaries and goals
- Ball shadows and 3D effects

### Bot Thoughts Panel
- Current ball position and velocity
- Distance calculations
- Learning progress for each mechanic
- Real-time decision-making process

### Actions Panel
- What the bot is currently doing
- Target selection and planning
- Action execution status
- Learning feedback

### Training Console
- Episode information
- Skill level progression
- Real-time training metrics
- Timestamped training events

### Tactical Map
- 2D overhead view of the field
- Ball and car positions
- Boost pad locations
- Learning progress bars

## 🔄 Data Flow

1. **Training System** → Generates RLGym GameState
2. **UDP Sender** → Converts GameState to UDP packets
3. **UDP Visualizer** → Receives and parses packets
4. **3D Renderer** → Displays game state in real-time
5. **Bot Insights** → Shows training progress and thoughts

## 🎨 Customization

### Colors and Styling
- Easily customizable color scheme
- Panel dimensions adjustable
- Font sizes configurable
- Camera settings modifiable

### Data Display
- Add new bot thoughts and actions
- Customize training metrics
- Modify progress indicators
- Add new visual elements

## 🐛 Troubleshooting

### Visualizer Not Opening
- Check if port 37020 is available
- Ensure pygame is installed
- Verify no firewall blocking UDP

### No Data Received
- Check training system is running
- Verify UDP sender is initialized
- Check network connectivity

### Performance Issues
- Reduce UDP send rate
- Lower visualizer FPS
- Simplify 3D rendering

## 🎯 Future Enhancements

- **Recording System**: Save training sessions
- **Replay Mode**: Playback recorded sessions
- **Advanced Analytics**: Detailed performance metrics
- **Custom Cameras**: Multiple camera angles
- **Sound Effects**: Audio feedback for training
- **Export Features**: Save training data

## 🏆 Achievement

We've successfully created a complete UDP-based visualization system that:
- ✅ Provides real-time 3D game visualization
- ✅ Shows bot thoughts and training progress
- ✅ Integrates seamlessly with JSTN training system
- ✅ Uses lightweight UDP communication
- ✅ Offers professional-grade controls and interface
- ✅ Supports multi-mode training visualization

This system gives you a complete view of your bot's training process, allowing you to watch it learn and improve in real-time, just like the professional RLViser but customized for our specific needs!

