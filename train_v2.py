import os
import math
from typing import List, Dict, Any

# RLGym v2 API
from rlgym.api import RLGym, RewardFunction, AgentID
from rlgym.rocket_league.api import GameState
from rlgym.rocket_league import common_values
from rlgym.rocket_league.obs_builders import DefaultObs
from rlgym.rocket_league.done_conditions import (
    GoalCondition, NoTouchTimeoutCondition, TimeoutCondition, AnyCondition
)
from rlgym.rocket_league.reward_functions import CombinedReward, GoalReward
from rlgym.rocket_league.action_parsers import LookupTableAction, RepeatAction
from rlgym.rocket_league.state_mutators import (
    MutatorSequence, FixedTeamSizeMutator, KickoffMutator
)
from rlgym.rocket_league.sim import RocketSimEngine

# RLGym-PPO glue for Gym wrapper + Learner
from rlgym_ppo.util import RLGymV2GymWrapper
from rlgym_ppo import Learner

# ------------------------------
# Custom reward components (simple, effective)
# ------------------------------
import numpy as np

class SpeedTowardBallReward(RewardFunction[AgentID, GameState, float]):
    def reset(self, agents: List[AgentID], initial_state: GameState, shared_info: Dict[str, Any]) -> None:
        pass
    def get_rewards(self, agents: List[AgentID], state: GameState, is_terminated: Dict[AgentID, bool],
                    is_truncated: Dict[AgentID, bool], shared_info: Dict[AgentID, Any]) -> Dict[AgentID, float]:
        rewards = {}
        for agent in agents:
            car = state.cars[agent]
            car_phys = car.physics if car.is_orange else car.inverted_physics
            ball_phys = state.ball if car.is_orange else state.inverted_ball
            vel = car_phys.linear_velocity
            pos_diff = (ball_phys.position - car_phys.position)
            dist = np.linalg.norm(pos_diff)
            dir_to_ball = pos_diff / (dist + 1e-9)
            speed_toward_ball = float(np.dot(vel, dir_to_ball))
            rewards[agent] = max(speed_toward_ball / common_values.CAR_MAX_SPEED, 0.0)
        return rewards

class InAirReward(RewardFunction[AgentID, GameState, float]):
    def reset(self, agents: List[AgentID], initial_state: GameState, shared_info: Dict[str, Any]) -> None:
        pass
    def get_rewards(self, agents: List[AgentID], state: GameState, is_terminated: Dict[AgentID, bool],
                    is_truncated: Dict[AgentID, bool], shared_info: Dict[AgentID, Any]) -> Dict[AgentID, float]:
        return {agent: float(not state.cars[agent].on_ground) for agent in agents}

class VelocityBallToGoalReward(RewardFunction[AgentID, GameState, float]):
    def reset(self, agents: List[AgentID], initial_state: GameState, shared_info: Dict[str, Any]) -> None:
        pass
    def get_rewards(self, agents: List[AgentID], state: GameState, is_terminated: Dict[AgentID, bool],
                    is_truncated: Dict[AgentID, bool], shared_info: Dict[AgentID, Any]) -> Dict[AgentID, float]:
        rewards = {}
        for agent in agents:
            car = state.cars[agent]
            ball = state.ball
            goal_y = -common_values.BACK_NET_Y if car.is_orange else common_values.BACK_NET_Y
            pos_diff = np.array([0.0, goal_y, 0.0]) - ball.position
            dist = np.linalg.norm(pos_diff)
            dir_to_goal = pos_diff / (dist + 1e-9)
            vel_toward_goal = float(np.dot(ball.linear_velocity, dir_to_goal))
            rewards[agent] = max(vel_toward_goal / common_values.BALL_MAX_SPEED, 0.0)
        return rewards

# ------------------------------
# Environment factory for RLGym v2
# ------------------------------

def build_rlgym_v2_env():
    team_size = 1
    spawn_opponents = True
    blue_team = team_size
    orange_team = team_size if spawn_opponents else 0

    action_repeat = 8
    action_parser = RepeatAction(LookupTableAction(), repeats=action_repeat)

    term_cond = GoalCondition()
    trunc_cond = AnyCondition(
        NoTouchTimeoutCondition(timeout_seconds=30),
        TimeoutCondition(timeout_seconds=300),
    )

    reward = CombinedReward(
        (InAirReward(), 0.002),
        (SpeedTowardBallReward(), 0.01),
        (VelocityBallToGoalReward(), 0.1),
        (GoalReward(), 10.0),
    )

    obs = DefaultObs(
        zero_padding=None,
        pos_coef=np.asarray([
            1 / common_values.SIDE_WALL_X,
            1 / common_values.BACK_NET_Y,
            1 / common_values.CEILING_Z,
        ]),
        ang_coef=1 / np.pi,
        lin_vel_coef=1 / common_values.CAR_MAX_SPEED,
        ang_vel_coef=1 / common_values.CAR_MAX_ANG_VEL,
        boost_coef=1 / 100.0,
    )

    mutators = MutatorSequence(
        FixedTeamSizeMutator(blue_size=blue_team, orange_size=orange_team),
        KickoffMutator(),
    )

    rlgym_env = RLGym(
        state_mutator=mutators,
        obs_builder=obs,
        action_parser=action_parser,
        reward_fn=reward,
        termination_cond=term_cond,
        truncation_cond=trunc_cond,
        transition_engine=RocketSimEngine(),
    )

    # Wrap to a Gym interface that RLGym-PPO expects
    return RLGymV2GymWrapper(rlgym_env)


if __name__ == "__main__":
    # Sensible defaults that scale with hardware
    n_proc = max(1, min(os.cpu_count() or 4, 16))          # processes for collectors
    min_inf = max(1, int(round(n_proc * 0.9)))             # inference workers

    # PPO training loop
    learner = Learner(
        build_rlgym_v2_env,
        n_proc=n_proc,
        min_inference_size=min_inf,
        ppo_batch_size=100_000,          # try 50_000 if VRAM limited
        policy_layer_sizes=[2048, 2048, 1024, 1024],
        critic_layer_sizes=[2048, 2048, 1024, 1024],
        ts_per_iteration=100_000,        # match batch size
        exp_buffer_size=300_000,         # 2-3x batch size
        ppo_minibatch_size=50_000,       # tune by VRAM
        ppo_ent_coef=0.01,
        policy_lr=1e-4,
        critic_lr=1e-4,
        ppo_epochs=2,
        standardize_returns=True,
        standardize_obs=False,
        save_every_ts=1_000_000,
        timestep_limit=1_000_000_000,    # 1B steps target
        log_to_wandb=False,
    )

    # (Optional) Make MKL behave on Windows
    os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")
    os.environ.setdefault("OMP_NUM_THREADS", str(max(1, math.ceil((os.cpu_count() or 8) / 2))))

    learner.learn()