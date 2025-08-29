# RLGym v2 + RLGym-PPO Quick Notes

- Train **offline** with RocketSim via RLGym v2.
- Script: `python train_v2.py`
- Checkpoints will be written into the working directory by RLGym-PPO every N timesteps.
- To monitor training at scale, enable Weights & Biases by setting `log_to_wandb=True` and running `pip install wandb`.
- To speed up: increase `n_proc`, `ppo_batch_size`, and `ppo_minibatch_size` gradually.
- To reduce VRAM/RAM: lower `ppo_minibatch_size`, network layer sizes, or processes.
- To focus learning: edit the weights in `CombinedReward`.

⚠️ Respect game TOS. This setup is for simulation and private/custom matches only — no online matchmaking control.

## Quickstart (Windows)

Open PowerShell in your project folder and run:

```powershell
# Python 3.10 is recommended
py -3.10 -m venv .venv
. .venv\Scripts\Activate.ps1

# Upgrade basics
python -m pip install -U pip wheel setuptools

# Install PyTorch (CPU)
pip install torch --index-url https://download.pytorch.org/whl/cpu

# Install RLGym (with RocketSim + RLViser) and RLGym-PPO
pip install "rlgym[rl-rlviser]"
pip install git+https://github.com/AechPro/rlgym-ppo

# Optional: Weights & Biases for logging
pip install wandb

# Run training
python train_v2.py
```

> GPU users: install the CUDA build of PyTorch from pytorch.org and then run the rest.

## Linux/macOS Setup

```bash
# Create virtual environment
python3.10 -m venv .venv
source .venv/bin/activate

# Upgrade basics
python -m pip install -U pip wheel setuptools

# Install PyTorch (CPU)
pip install torch --index-url https://download.pytorch.org/whl/cpu

# Install RLGym (with RocketSim + RLViser) and RLGym-PPO
pip install "rlgym[rl-rlviser]"
pip install git+https://github.com/AechPro/rlgym-ppo

# Optional: Weights & Biases for logging
pip install wandb

# Run training
python train_v2.py
```

## Customization

### Reward Components

The training script includes several reward components that you can adjust:

- `InAirReward` (weight: 0.002) - Encourages aerial play
- `SpeedTowardBallReward` (weight: 0.01) - Encourages ball chasing
- `VelocityBallToGoalReward` (weight: 0.1) - Rewards moving ball toward goal
- `GoalReward` (weight: 10.0) - Large reward for scoring goals

To modify these weights, edit the `CombinedReward` section in `train_v2.py`.

### Training Parameters

Key parameters you can tune in the `Learner` configuration:

- `n_proc`: Number of parallel processes (auto-detected based on CPU cores)
- `ppo_batch_size`: Batch size for PPO training (100,000 default)
- `ppo_minibatch_size`: Mini-batch size (50,000 default)
- `policy_layer_sizes` / `critic_layer_sizes`: Neural network architecture
- `policy_lr` / `critic_lr`: Learning rates (1e-4 default)
- `save_every_ts`: How often to save checkpoints (1M timesteps)

### Environment Configuration

In the `build_rlgym_v2_env()` function:

- `team_size`: Players per team (1v1 default)
- `spawn_opponents`: Whether to include opponents (True default)
- `action_repeat`: Action repetition for temporal consistency (8 default)
- Timeout conditions: No-touch (30s) and total game (300s) timeouts

## Troubleshooting

- **ImportError: No module named rlgym_ppo** → Re-run the `pip install git+https://github.com/AechPro/rlgym-ppo` line in the venv.
- **Torch/CUDA mismatch** → Install PyTorch from pytorch.org "Get Started" for your exact CUDA version.
- **Weird numpy errors** → Ensure Python is 3.10 and `pip install -U pip wheel setuptools` first.
- **Slow throughput** → Lower minibatch size, raise `OMP_NUM_THREADS`, or reduce network widths.
- **Out of memory** → Reduce `ppo_batch_size`, `ppo_minibatch_size`, or network layer sizes.

## Next Steps

1. **Enable Logging**: Set `log_to_wandb=True` and install wandb for training dashboards
2. **Add More Rewards**: Implement rewards for recoveries, boost efficiency, kickoff outcomes, aerial control
3. **Scale Up**: Increase `n_proc` once training is stable
4. **Save More Often**: Reduce `save_every_ts` while tuning hyperparameters
5. **Multi-Agent**: Increase `team_size` for 2v2 or 3v3 training scenarios

## Performance Tips

- Start with smaller batch sizes and scale up gradually
- Monitor GPU/CPU usage and adjust process counts accordingly
- Use CPU training for initial experiments, GPU for final training runs
- Consider reducing network sizes if memory is limited
- Experiment with different reward weightings based on desired playstyle