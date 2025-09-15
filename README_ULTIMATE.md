# 🚀 Ultimate Opti Training System 🚀

> **The complete SSL-level Rocket League AI training system that integrates EVERYTHING**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![RLGym v2](https://img.shields.io/badge/RLGym-v2.0+-green.svg)](https://rlgym.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![SSL Ready](https://img.shields.io/badge/SSL-Ready-gold.svg)](https://github.com)

## 🏆 What Makes This Ultimate?

This is the **complete integration** of ALL components from the Opti repository, enhanced with cutting-edge techniques from elite bots like Opti, Nexto, and Lucy-SKG. It's not just another training script - it's a **complete SSL-level bot development platform**.

### ✨ Ultimate Features

#### 🧠 **Complete Neural Architecture**
- **Modern Transformer-based Agent** with multi-head attention
- **Specialized Sub-models** for each mechanic (like real Opti)
- **Hierarchical Decision Making** with dynamic model selection
- **Temporal Sequence Processing** with LSTM memory
- **Advanced Action Distribution** modeling

#### 🎯 **All Specialized Mechanics**
- **Aerial Mastery** (worker_aerial, learner_aerial)
- **Flip Reset Expertise** (worker_flip_reset, learner_flip_reset)
- **Double Tap Precision** (worker_dtap, learner_dtap)
- **Wall Play Mastery** (worker_wall, learner_wall)
- **Recovery Systems** (worker_recovery, learner_recovery)
- **Kickoff Specialists** (worker_kickoff, learner_kickoff)
- **Advanced Flicks** (worker_flick, learner_flick)
- **Ceiling Pinches** (worker_ceil_pinch, learner_ceil_pinch)
- **Wave Dashes** (worker_walldash, learner_walldash)
- **Demo Play** (worker_demo, learner_demo)
- **Ground Play** (worker_gp, learner_gp)
- **Half Flips** (worker_half_flip, learner_half_flip)
- **LIX Mechanics** (worker_lix, learner_lix)
- **Pinch Shots** (worker_pinch, learner_pinch)
- **Model Selection** (worker_selector, learner_selector)

#### 🏆 **JSTN-Style Training**
- **Aerial Aggression**: 90% - Signature aggressive aerial play
- **Flip Reset Mastery**: 95% - Expert flip reset execution
- **Double Tap Precision**: 90% - Accurate double tap shots
- **Ceiling Shot Skill**: 85% - Advanced ceiling mechanics
- **Creative Mechanics**: 80% - Innovative play styles

#### 📈 **SSL Progression System**
- **Bronze → Silver → Gold → Platinum → Diamond → Champion → GC → SSL**
- **Progressive Difficulty** with curriculum learning
- **Adaptive Opponents** that scale with skill level
- **Mechanical Mastery** tracking and advancement
- **Performance-based** progression

#### 🌐 **Distributed Training**
- **Redis-based Coordination** for multi-machine training
- **Specialized Worker Processes** for each mechanic
- **Parallel Learning** across all sub-models
- **Scalable Architecture** from 1 to 100+ machines

#### 🎮 **Real Game Integration**
- **Complete SSL Bot** integration (complete_ssl_bot.py)
- **Real-time Overlay** with game state visualization
- **Direct Game Control** with input injection
- **Live Performance Monitoring** during matches

#### 📊 **Professional Monitoring**
- **Weights & Biases** integration for experiment tracking
- **Advanced Metrics** for all mechanics and skills
- **Real-time Dashboards** with performance visualization
- **Automated Evaluation** against benchmarks

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)

```bash
# Run the ultimate setup script
python setup_ultimate.py
```

The setup will automatically:
- ✅ Validate your system (CPU, RAM, GPU, Python)
- ✅ Create optimized virtual environment
- ✅ Install all dependencies with correct versions
- ✅ Configure Redis for distributed training
- ✅ Create complete directory structure
- ✅ Initialize configuration files
- ✅ Validate installation

### Option 2: Manual Setup

```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate
# Activate (Linux/macOS)
source .venv/bin/activate

# Install dependencies
pip install -U pip wheel setuptools
pip install -r requirements_ultimate.txt

# Start training
python ULTIMATE_OPTI_TRAINER.py
```

## 🏗️ Architecture Overview

```
Ultimate Opti Training System
├── 🧠 ULTIMATE_OPTI_TRAINER.py    # Main training orchestrator
├── 🎯 Specialized Workers/Learners  # All 15 mechanics
│   ├── worker_aerial.py + learner_aerial.py
│   ├── worker_flip_reset.py + learner_flip_reset.py
│   ├── worker_dtap.py + learner_dtap.py
│   └── ... (15 total mechanics)
├── 🏆 Modern Architecture
│   ├── ModernAgent.py              # Transformer-based agent
│   ├── ModernRewardSystem.py       # SSL-level rewards
│   ├── ModernObsBuilder.py         # Advanced observations
│   └── ModernActionParser.py       # Complex action spaces
├── 🎮 Real Game Integration
│   ├── complete_ssl_bot.py         # Live game control
│   ├── ssl_training_pipeline.py    # SSL progression
│   └── jstn_complete_trainer.py    # JSTN-style training
└── 🌐 Distributed Training
    ├── Redis coordination
    ├── Multi-machine scaling
    └── Parallel learning
```

## ⚙️ Configuration

### Training Modes

```python
class TrainingMode(Enum):
    BRONZE_TO_SSL = "bronze_to_ssl"      # Complete progression
    JSTN_STYLE = "jstn_style"            # Creative aggressive play
    OPTI_REPLICATION = "opti_replication" # Replicate Opti bot
    CUSTOM_MECHANICS = "custom_mechanics" # Focus on specific skills
    DISTRIBUTED = "distributed"          # Multi-machine training
    REAL_GAME = "real_game"              # Live game integration
```

### Hardware Optimization

```python
# Auto-detects and optimizes for your hardware
config = UltimateConfig()

# High-end setup (32+ cores, RTX 4090)
config.n_proc = 24
config.batch_size = 300_000
config.use_gpu = True
config.distributed_training = True

# Mid-range setup (8-16 cores, RTX 3070+)
config.n_proc = 12
config.batch_size = 150_000
config.use_gpu = True

# Budget setup (4-8 cores, no GPU)
config.n_proc = 6
config.batch_size = 50_000
config.use_gpu = False
```

## 🎯 Training Progression

### Phase 1: Fundamentals (Bronze → Silver)
- **Focus**: Basic mechanics, ball control, positioning
- **Duration**: ~10M timesteps
- **Mechanics**: Ground play, basic aerials, wall touches

### Phase 2: Advanced Mechanics (Gold → Platinum)
- **Focus**: Complex mechanics, aerial control
- **Duration**: ~20M timesteps
- **Mechanics**: Flip resets, wall dribbles, advanced aerials

### Phase 3: SSL Mastery (Diamond → SSL)
- **Focus**: Perfect execution, creative plays
- **Duration**: ~50M timesteps
- **Mechanics**: Double taps, ceiling shots, advanced recoveries

### Phase 4: Pro-Level (SSL+)
- **Focus**: Tournament-level play, meta adaptation
- **Duration**: ~100M+ timesteps
- **Mechanics**: All mechanics at 95%+ consistency

## 🌐 Distributed Training

### Single Machine
```bash
# Uses all available CPU cores and GPU
python ULTIMATE_OPTI_TRAINER.py
```

### Multi-Machine Cluster
```bash
# Machine 1 (Master)
redis-server --port 6379
python ULTIMATE_OPTI_TRAINER.py --distributed --master

# Machine 2-N (Workers)
python ULTIMATE_OPTI_TRAINER.py --distributed --worker --master-host 192.168.1.100
```

### Cloud Training
```bash
# AWS/GCP/Azure setup with auto-scaling
# Supports up to 100+ machines for massive training
```

## 📊 Monitoring & Evaluation

### Weights & Biases Integration
```bash
# Enable professional monitoring
wandb login
# Set use_wandb=True in config
```

### Key Metrics Tracked
- **Mechanical Skills**: Success rate for each of 15+ mechanics
- **SSL Progression**: Current skill level (0.0 to 1.0)
- **Training Efficiency**: Timesteps per second, GPU utilization
- **Game Performance**: Win rate, goals, saves, demos
- **Learning Progress**: Loss curves, gradient norms, entropy

### Real-time Evaluation
- **Automated Testing**: Against Nexto, Necto, and other top bots
- **Skill Assessment**: Individual mechanic evaluation
- **Rank Estimation**: Predicted competitive rank
- **Performance Graphs**: Real-time skill progression

## 🎮 Real Game Integration

### Live Game Control
```python
# Enable real game integration
config.enable_real_game_control = True
config.enable_overlay = True

# The bot can:
# - Control your car in real matches
# - Display overlay with game state
# - Practice mechanics in real-time
# - Learn from actual gameplay
```

### Overlay Features
- **Real-time Stats**: Car position, velocity, boost
- **Ball Prediction**: Future ball positions
- **Mechanical Analysis**: Current mechanic being executed
- **Performance Metrics**: Live skill assessment

## 🔧 Advanced Features

### Custom Mechanics
```python
# Add your own specialized mechanics
class CustomMechanic(MechanicType):
    TORNADO_FLICK = "tornado_flick"
    BREEZI_FLICK = "breezi_flick"
    CHAIN_DASH = "chain_dash"

# The system will automatically create workers and learners
```

### Reward Engineering
```python
# JSTN-style reward weights
jstn_weights = {
    'aerial_mastery': 50.0 * config.jstn_aerial_aggression,
    'flip_reset_execution': 75.0 * config.jstn_flip_reset_mastery,
    'creative_mechanics': 40.0 * config.jstn_creative_mechanics,
}

# SSL-level mechanics rewards
ssl_weights = {
    'musty_flick': 80.0,
    'tornado_spin': 70.0,
    'stall_reset': 85.0,
    'triple_touch': 90.0,
}
```

### Neural Architecture Customization
```python
# Modern transformer-based architecture
agent = UltimateAgent(
    hidden_size=512,
    num_attention_heads=8,
    num_transformer_layers=6,
    use_specialized_heads=True,  # Sub-models for each mechanic
    use_hierarchical=True,       # Dynamic model selection
    use_temporal_modeling=True   # LSTM memory
)
```

## 📁 Project Structure

```
ultimate-opti/
├── 🚀 ULTIMATE_OPTI_TRAINER.py     # Main training system
├── ⚙️  setup_ultimate.py           # Automated setup
├── 📋 requirements_ultimate.txt    # All dependencies
├── 📖 README_ULTIMATE.md          # This file
├── 🎯 Specialized Components/
│   ├── worker_*.py                 # 15 specialized workers
│   ├── learner_*.py                # 15 specialized learners
│   ├── Constants_*.py              # Configuration for each
│   ├── ModernAgent.py              # Neural architecture
│   ├── ModernRewardSystem.py       # Reward functions
│   ├── ModernObsBuilder.py         # Observations
│   └── ModernActionParser.py       # Action parsing
├── 🏆 Elite Components/
│   ├── complete_ssl_bot.py         # Real game integration
│   ├── ssl_training_pipeline.py    # SSL progression
│   ├── jstn_complete_trainer.py    # JSTN-style training
│   └── SSLMechanics.py            # SSL-level mechanics
├── 📁 Generated Structure/
│   ├── models/                     # Trained models
│   ├── checkpoints/                # Training checkpoints
│   ├── logs/                       # Training logs
│   ├── configs/                    # Configuration files
│   ├── evaluations/               # Evaluation results
│   └── scripts/                   # Helper scripts
└── 🌐 Distributed/
    ├── redis/                     # Redis for coordination
    └── rocket-learn-master/       # Distributed RL framework
```

## 🐛 Troubleshooting

### Common Issues

#### Out of Memory
```python
# Reduce batch sizes
config.batch_size = 50_000
config.minibatch_size = 25_000

# Reduce network size
config.hidden_size = 256
```

#### Slow Training
```python
# Increase processes
config.n_proc = min(os.cpu_count(), 20)

# Enable GPU
config.use_gpu = True
pip install torch --index-url https://download.pytorch.org/whl/cu121
```

#### Redis Connection Issues
```bash
# Start Redis server
redis-server

# Or use Docker
docker run -d -p 6379:6379 redis:alpine
```

### Performance Optimization

#### For High-End Systems (32+ cores, RTX 4090)
```python
config.n_proc = 24
config.batch_size = 500_000
config.minibatch_size = 250_000
config.distributed_training = True
config.mixed_precision = True
```

#### For Budget Systems (4-8 cores, no GPU)
```python
config.n_proc = 6
config.batch_size = 25_000
config.minibatch_size = 12_500
config.use_gpu = False
config.distributed_training = False
```

## 🤝 Contributing

This ultimate system is designed to be the definitive Rocket League AI training platform. Contributions welcome!

### Priority Areas
- **New Mechanics**: Additional SSL-level mechanics
- **Better Rewards**: More sophisticated reward functions
- **Performance**: Training speed optimizations
- **Real Game**: Enhanced live game integration
- **Evaluation**: Better benchmarking systems

## 📚 Research & Inspiration

### Academic Papers
- **Lucy-SKG**: Kinesthetic Reward Combination
- **Sim-to-Sim Transfer**: Robust training methods
- **Advanced PPO**: State-of-the-art policy optimization
- **Transformer RL**: Attention mechanisms in RL

### Community Bots
- **Opti**: Modular architecture inspiration
- **Nexto**: 250,000+ hours of training experience
- **Necto**: Professional tournament performance
- **KBB**: Advanced mechanical execution

### Professional Players
- **JSTN**: Creative and aggressive playstyle
- **GarrettG**: Consistent mechanical execution
- **Squishy**: Advanced aerial control
- **Fairy Peak**: Strategic positioning

## 📄 License

MIT License - See LICENSE file for details.

## 🙏 Acknowledgments

- **RLGym Team** - Incredible training framework
- **RLGym-PPO Authors** - Efficient PPO implementation
- **Rocket-Learn Team** - Distributed training framework
- **Elite Bot Developers** - Opti, Nexto, Necto teams
- **Professional Players** - Inspiration for playstyles
- **RL Community** - Continuous innovation and support

---

## 🚀 Ready to Dominate SSL?

This isn't just a training script - it's a **complete SSL bot development platform** that integrates everything from the Opti repository plus cutting-edge enhancements. 

**Features you get:**
✅ All 15+ specialized mechanics with dedicated workers/learners  
✅ Modern transformer-based neural architecture  
✅ JSTN-style creative and aggressive training  
✅ Complete SSL progression system (Bronze → SSL)  
✅ Distributed training across multiple machines  
✅ Real game integration with live control  
✅ Professional monitoring and evaluation  
✅ Modular sub-model architecture like real Opti  

**Start your journey to SSL dominance:**

```bash
python setup_ultimate.py
python ULTIMATE_OPTI_TRAINER.py
```

**🏆 See you in SSL! 🏆**
