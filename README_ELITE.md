# 🚀 Elite RLGym v2 Training Pipeline

> **World-class Rocket League AI training inspired by top-tier bots like Opti, Nexto, and Lucy-SKG**

A complete professional-grade training setup featuring advanced techniques used by the best bots in the community. This pipeline implements cutting-edge reinforcement learning methods to achieve Supersonic Legend level performance.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![RLGym v2](https://img.shields.io/badge/RLGym-v2.0+-green.svg)](https://rlgym.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ Elite Features

### 🧠 Advanced AI Techniques
- **Kinesthetic Reward Combination (KRC)** - Dynamic reward weighting inspired by Lucy-SKG
- **Velocity-based Touch Rewards** - Professional-grade ball touch evaluation
- **Aerial Control Training** - Advanced airplay mechanics
- **Strategic Positioning** - Game-state aware positioning rewards
- **Auxiliary Neural Networks** - Enhanced learning through reward prediction

### 🏗️ Professional Architecture
- **Modular Training System** - Specialized sub-models for different skills
- **Curriculum Learning** - Progressive difficulty from Bronze to SSL
- **Elite Observation Space** - Enhanced game state information
- **Distributed Training Support** - Scale across multiple machines
- **Comprehensive Evaluation** - Automated benchmarking and performance tracking

### 🔧 Production-Ready Infrastructure
- **Auto-scaling** - Hardware-optimized process management
- **Advanced Logging** - Professional monitoring with W&B integration
- **Checkpoint Management** - Intelligent model saving and versioning
- **Configuration System** - JSON-based hyperparameter management
- **GPU Acceleration** - CUDA-optimized training pipeline

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)

```bash
# Clone or download the elite training files
python setup_elite.py
```

The setup script will:
- ✅ Validate your system requirements
- ✅ Create optimized virtual environment
- ✅ Install all dependencies with correct versions
- ✅ Configure directory structure
- ✅ Validate installation

### Option 2: Manual Setup

#### Windows (PowerShell)
```powershell
# Create virtual environment
py -3.10 -m venv .venv
. .venv\Scripts\Activate.ps1

# Install dependencies
python -m pip install -U pip wheel setuptools
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements_elite.txt

# Start elite training
python train_v2_elite.py
```

#### Linux/macOS
```bash
# Create virtual environment
python3.10 -m venv .venv
source .venv/bin/activate

# Install dependencies
python -m pip install -U pip wheel setuptools
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements_elite.txt

# Start elite training
python train_v2_elite.py
```

### GPU Acceleration (Recommended)

For maximum performance, install CUDA-enabled PyTorch:

```bash
# Replace CPU version with GPU version
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
```

## 🎯 Training Phases

The elite pipeline implements curriculum learning with 8 progressive phases:

| Phase | Focus | Duration | Key Skills |
|-------|-------|----------|------------|
| **Bronze** | Basic mechanics | ~10M steps | Ball chasing, basic hits |
| **Silver** | Consistency | ~15M steps | Accurate touches, positioning |
| **Gold** | Game sense | ~20M steps | Rotations, boost management |
| **Platinum** | Advanced mechanics | ~25M steps | Aerials, wall play |
| **Diamond** | Speed & precision | ~30M steps | Fast aerials, dribbling |
| **Champion** | Team play | ~40M steps | Passing, defensive plays |
| **Grand Champion** | Mastery | ~50M steps | Advanced mechanics, consistency |
| **Supersonic Legend** | Perfection | ~100M+ steps | Pro-level execution |

## 🏆 Elite Reward System

### Kinesthetic Reward Combination (KRC)
Inspired by the Lucy-SKG research, our KRC system dynamically balances multiple reward components:

```python
# Core reward components with adaptive weighting
components = [
    (GoalReward(), 15.0, "goal"),                    # Scoring goals
    (VelocityTouchReward(), 3.0, "velocity_touch"), # Powerful touches
    (AerialControlReward(), 1.5, "aerial_control"), # Air play mastery
    (PositionalPlayReward(), 2.0, "positional"),    # Strategic positioning
    (SpeedTowardBallReward(), 0.5, "ball_chase"),   # Aggressive play
]
```

### Advanced Reward Functions

#### 🎯 Velocity Touch Rewards
- Measures ball velocity change on contact
- Encourages powerful shots and effective touches
- Inspired by professional bot mechanics

#### 🛩️ Aerial Control Rewards
- Rewards airborne ball control
- Promotes advanced aerial mechanics
- Includes stability bonuses for controlled flight

#### 🧭 Strategic Positioning
- Game-state aware positioning rewards
- Encourages proper rotations and field coverage
- Adapts to offensive and defensive scenarios

## 📊 Performance Monitoring

### Weights & Biases Integration
Enable professional monitoring with W&B:

```bash
# Setup W&B (one-time)
wandb login

# Enable in config
# Set log_to_wandb=True in train_v2_elite.py
```

### Key Metrics Tracked
- **Reward Components** - Individual reward function performance
- **Training Efficiency** - Steps per second, GPU utilization
- **Model Performance** - Win rate, goal scoring, save percentage
- **Learning Progress** - Policy loss, value loss, entropy
- **Hardware Utilization** - CPU, GPU, memory usage

## ⚙️ Configuration

### Elite Configuration System
The training pipeline uses a comprehensive configuration system:

```python
@dataclass
class EliteConfig:
    # Training Infrastructure
    n_proc: int = 16                    # Parallel processes
    ppo_batch_size: int = 200_000      # Large batches for stability
    policy_layer_sizes: List[int] = [2048, 2048, 1024, 1024, 512]
    
    # Advanced Features
    use_auxiliary_networks: bool = True
    curriculum_learning: bool = True
    distributed_training: bool = False
    
    # Hardware Optimization
    use_gpu_acceleration: bool = True
    auto_scaling: bool = True
```

### Hardware Recommendations

#### Minimum Requirements
- **CPU**: 4+ cores
- **RAM**: 8GB
- **Storage**: 10GB free space
- **Python**: 3.10+

#### Recommended for Elite Training
- **CPU**: 16+ cores (Intel i7/i9, AMD Ryzen 7/9)
- **GPU**: RTX 3070+ / RTX 4060+ (8GB+ VRAM)
- **RAM**: 32GB+
- **Storage**: NVMe SSD with 50GB+ free space

#### Professional Setup
- **CPU**: 32+ cores (Threadripper, Xeon)
- **GPU**: RTX 4090 / A6000 (24GB+ VRAM)
- **RAM**: 64GB+
- **Storage**: High-speed NVMe RAID

## 🔧 Advanced Usage

### Distributed Training
Scale training across multiple machines:

```python
# Enable distributed training
config.distributed_training = True
config.n_proc = 8  # Per machine

# Use rocket-learn for coordination
# pip install rocket-learn
```

### Custom Reward Functions
Add your own reward components:

```python
class CustomReward(RewardFunction[AgentID, GameState, float]):
    def get_rewards(self, agents, state, is_terminated, is_truncated, shared_info):
        # Your custom reward logic
        return {agent: reward_value for agent in agents}

# Add to KRC system
components.append((CustomReward(), 1.0, "custom"))
```

### Model Evaluation
Comprehensive evaluation system:

```python
# Automatic evaluation every 5M steps
config.eval_frequency = 5_000_000
config.keep_best_models = 10

# Manual evaluation
python evaluate_model.py --model checkpoints/best_model.pkl
```

## 📁 Project Structure

```
elite-rl-training/
├── train_v2_elite.py          # Elite training pipeline
├── setup_elite.py             # Automated setup script
├── requirements_elite.txt     # Elite dependencies
├── README_ELITE.md            # This file
├── .gitignore                 # Comprehensive gitignore
├── checkpoints/               # Model checkpoints
├── logs/                      # Training logs
├── configs/                   # Configuration files
├── scripts/                   # Helper scripts
│   ├── run_training.bat       # Windows training script
│   └── run_training.sh        # Linux/macOS training script
├── models/                    # Saved models
├── evaluations/               # Evaluation results
└── data/                      # Training data
```

## 🐛 Troubleshooting

### Common Issues

#### Out of Memory Errors
```python
# Reduce batch sizes
config.ppo_batch_size = 100_000
config.ppo_minibatch_size = 50_000

# Reduce network size
config.policy_layer_sizes = [1024, 1024, 512]
```

#### Slow Training
```python
# Increase process count (if you have CPU cores)
config.n_proc = 20

# Enable GPU acceleration
config.use_gpu_acceleration = True
pip install torch --index-url https://download.pytorch.org/whl/cu121
```

#### Installation Issues
```bash
# Clean installation
rm -rf .venv
python setup_elite.py

# Manual dependency resolution
pip install --no-deps -r requirements_elite.txt
```

### Performance Optimization

#### CPU Optimization
```bash
# Set optimal thread count
export OMP_NUM_THREADS=8
export KMP_DUPLICATE_LIB_OK=TRUE

# Use performance CPU governor (Linux)
sudo cpupower frequency-set -g performance
```

#### GPU Optimization
```python
# Enable mixed precision training
config.use_mixed_precision = True

# Optimize CUDA settings
os.environ['CUDA_LAUNCH_BLOCKING'] = '0'
os.environ['CUDA_CACHE_DISABLE'] = '0'
```

## 🤝 Contributing

This elite training pipeline is designed to be the gold standard for Rocket League AI training. Contributions are welcome!

### Areas for Improvement
- Additional reward functions inspired by pro gameplay
- Integration with more distributed training frameworks
- Advanced curriculum learning strategies
- Real-time opponent adaptation
- Multi-agent coordination training

## 📚 Research & Inspiration

This elite pipeline incorporates techniques from cutting-edge research and top community bots:

### Academic Research
- **Lucy-SKG**: Kinesthetic Reward Combination and auxiliary networks
- **Sim-to-Sim Transfer**: Robust training methodologies
- **Advanced PPO**: State-of-the-art policy optimization

### Community Bots
- **Opti**: Modular architecture and specialized sub-models
- **Nexto**: Extensive training regimens and performance optimization
- **Elite Community**: Best practices from top bot developers

## 📄 License

MIT License - See LICENSE file for details.

## 🙏 Acknowledgments

- **RLGym Team** - For the incredible training framework
- **RLGym-PPO Authors** - For the efficient PPO implementation
- **Elite Bot Developers** - Opti, Nexto, Lucy-SKG teams for inspiration
- **Rocket League AI Community** - For continuous innovation and collaboration

---

**Ready to train the next generation of Rocket League AI? Let's reach Supersonic Legend! 🚀**
