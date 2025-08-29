# Modern Opti - SSL-Level Rocket League AI

## 🚀 Overview

Modern Opti is a completely updated, state-of-the-art Rocket League AI system built for RLGym 2.0.1. This system is designed to achieve SSL (Supersonic Legend) level performance with all modern mechanics and techniques.

## ✨ Features

### 🧠 Modern Architecture
- **Transformer-based observation processing** with multi-head attention
- **Hierarchical decision making** with specialized sub-networks
- **Temporal sequence modeling** with LSTM
- **Advanced opponent modeling** and team play awareness

### 🎯 SSL-Level Mechanics
- **Flip resets** - Advanced aerial ball control
- **Double taps** - High-level scoring techniques
- **Air dribbles** - Precise aerial ball manipulation
- **Ceiling shots** - Advanced positioning and timing
- **Musty flicks** - Ground-based advanced techniques
- **Speed flips** - Optimal movement mechanics
- **Chain dashes** - Advanced ground movement
- **Stalls** - Aerial control techniques
- **Wave dashes** - Recovery and movement optimization
- **Wall dashes** - Wall-based movement
- **Power shots** - High-velocity scoring
- **Fakes** - Deceptive play techniques
- **Demos** - Strategic elimination
- **Boost management** - Resource optimization
- **Recovery techniques** - Advanced positioning

### 🏆 Multi-Mode Training
- **1v1 training** - Individual skill development
- **2v2 training** - Team coordination
- **3v3 training** - Full team play
- **Automatic mode rotation** for balanced skill development

### 📊 Advanced Training Features
- **Curriculum learning** - Progressive difficulty scaling
- **Distributed training** with Redis
- **Real-time performance monitoring** with wandb
- **Automatic hyperparameter tuning**
- **SSL-specific training strategies**

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- PyTorch 2.0+
- RLGym 2.0.1+
- Redis (for distributed training)

### Install Dependencies
```bash
pip install torch>=2.0.0
pip install rlgym[all]
pip install rlgym-tools
pip install redis
pip install wandb
pip install numpy
pip install gymnasium>=0.28.0
pip install prettytable
pip install keyboard
pip install rlbot>=1.0.0
pip install pygame
```

## 🚀 Quick Start

### 1. Basic Training
```python
from ModernTrainer import ModernTrainer

config = {
    'team_size': 3,
    'ssl_mode': True,
    'curriculum_learning': True,
    'mechanical_focus': True
}

trainer = ModernTrainer(config)
trainer.train(num_episodes=10000)
```

### 2. Multi-Mode Training
```python
from ModernTrainer import MultiModeTrainer

config = {
    'team_size': 3,
    'ssl_mode': True
}

multi_trainer = MultiModeTrainer(config)
multi_trainer.train(num_episodes=10000)
```

### 3. Custom Configuration
```python
config = {
    'team_size': 3,
    'tick_skip': 4,
    'episode_length': 1000,
    'num_workers': 4,
    'batch_size': 64,
    'learning_rate': 3e-4,
    'gamma': 0.99,
    'gae_lambda': 0.95,
    'clip_ratio': 0.2,
    'value_loss_coef': 0.5,
    'entropy_coef': 0.01,
    'max_grad_norm': 0.5,
    'ssl_mode': True,
    'curriculum_learning': True,
    'opponent_difficulty': 0.5,
    'mechanical_focus': True
}
```

## 📁 File Structure

```
ModernOpti/
├── ModernObsBuilder.py      # Advanced observation system
├── ModernActionParser.py    # SSL-level action parsing
├── ModernRewardSystem.py    # Comprehensive reward system
├── ModernAgent.py           # State-of-the-art neural networks
├── ModernTrainer.py         # Advanced training system
├── SSLMechanics.py          # Complete SSL mechanics
├── agent.py                 # Legacy compatibility
├── learner.py               # Legacy compatibility
├── rewards.py               # Legacy compatibility
├── CoyoteObs.py             # Legacy compatibility
├── CoyoteParser.py          # Legacy compatibility
└── README_MODERN_OPTI.md    # This file
```

## 🎮 Components

### ModernObsBuilder
- **580-dimensional observation space** with advanced features
- **Boost pad awareness** and timing
- **Opponent modeling** and prediction
- **Aerial mechanics detection**
- **Wall play awareness**
- **Recovery state tracking**

### ModernActionParser
- **932 action combinations** for precise control
- **SSL-specific action mappings**
- **Advanced aerial controls**
- **Flip reset mechanics**
- **Double tap actions**
- **Wall dash mechanics**

### ModernRewardSystem
- **37 different reward components**
- **SSL-specific rewards** for advanced mechanics
- **Team play rewards**
- **Opponent pressure rewards**
- **Mechanical skill rewards**

### ModernAgent
- **28.4M parameters** for complex decision making
- **Multi-head attention** for opponent modeling
- **Transformer encoder** for observation processing
- **Specialized sub-networks** for different mechanics
- **Hierarchical decision making**

### SSLMechanics
- **15 different SSL mechanics** implemented
- **Skill level progression** from Bronze to Pro
- **Automatic difficulty scaling**
- **Performance tracking** for each mechanic

## 🔧 Configuration Options

### Training Parameters
- `team_size`: Number of players per team (1, 2, or 3)
- `tick_skip`: Number of physics ticks to skip
- `episode_length`: Maximum episode length
- `num_workers`: Number of parallel workers
- `batch_size`: Training batch size
- `learning_rate`: Learning rate for optimization
- `gamma`: Discount factor for future rewards
- `gae_lambda`: GAE lambda parameter
- `clip_ratio`: PPO clipping ratio
- `value_loss_coef`: Value function loss coefficient
- `entropy_coef`: Entropy bonus coefficient
- `max_grad_norm`: Maximum gradient norm for clipping

### SSL-Specific Parameters
- `ssl_mode`: Enable SSL-level features
- `curriculum_learning`: Enable progressive difficulty
- `opponent_difficulty`: Starting opponent difficulty (0.0-1.0)
- `mechanical_focus`: Focus on mechanical skill development

## 📈 Performance Monitoring

### Wandb Integration
- Real-time training metrics
- SSL mechanics performance
- Win rate tracking
- Mechanical skill progression
- Team play scores

### Key Metrics
- **Episode Reward**: Overall performance
- **Win Rate**: Competitive success
- **Mechanical Skill**: SSL mechanics proficiency
- **Team Play Score**: Coordination effectiveness
- **Boost Efficiency**: Resource management
- **Recovery Rate**: Positioning effectiveness

## 🎯 SSL Skill Levels

The system supports 10 skill levels:
1. **Bronze** (0.1) - Basic mechanics
2. **Silver** (0.2) - Improved fundamentals
3. **Gold** (0.3) - Solid basics
4. **Platinum** (0.4) - Good mechanics
5. **Diamond** (0.5) - Advanced techniques
6. **Champion** (0.6) - High-level play
7. **Grand Champion** (0.7) - Expert level
8. **Supersonic Legend** (0.8) - Professional level
9. **SSL+** (0.9) - Elite professional
10. **Pro** (1.0) - World-class performance

## 🔄 Legacy Compatibility

The system maintains full compatibility with the original Opti codebase:
- `CoyoteObsBuilder` → `ModernObsBuilder`
- `CoyoteAction` → `ModernActionParser`
- `ZeroSumReward` → `ModernRewardSystem`
- `Opti` → `ModernAgent`
- `Learner` → `ModernTrainer`

## 🚀 Getting Started

1. **Install dependencies** as shown above
2. **Configure training parameters** for your setup
3. **Start training** with the desired mode
4. **Monitor progress** through wandb
5. **Adjust parameters** based on performance

## 📊 Expected Performance

With proper training, the system should achieve:
- **SSL-level mechanical skill** in all areas
- **Professional-level decision making**
- **Advanced team coordination**
- **Optimal resource management**
- **Competitive win rates** against high-level opponents

## 🤝 Contributing

This system is designed to be modular and extensible. Key areas for contribution:
- Additional SSL mechanics
- Improved reward functions
- Enhanced neural network architectures
- Better training strategies
- Performance optimizations

## 📝 License

This project maintains the same license as the original Opti system.

## 🎉 Conclusion

Modern Opti represents a complete overhaul of the original system, bringing it up to modern standards with SSL-level capabilities. The system is designed to be the most advanced Rocket League AI available, capable of competing at the highest levels of play.

**Ready to train the next generation of Rocket League AI! 🚀**
