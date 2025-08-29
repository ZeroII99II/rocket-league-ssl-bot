import wandb
import torch.jit

from torch.nn import Linear, Sequential, LeakyReLU

from redis import Redis
from rocket_learn.agent.actor_critic_agent import ActorCriticAgent
from rocket_learn.agent.discrete_policy import DiscretePolicy
from rocket_learn.ppo import PPO
from rocket_learn.rollout_generator.redis.redis_rollout_generator import RedisRolloutGenerator
# Import modern components instead of deleted CoyoteObs/CoyoteParser
from ModernObsBuilder import ModernObsBuilder
from ModernActionParser import ModernActionParser
import numpy as np
from rewards import ZeroSumReward
from Constants_kickoff import FRAME_SKIP, TIME_HORIZON, ZERO_SUM

from utils.misc import count_parameters

import os
from torch import set_num_threads
from rocket_learn.utils.stat_trackers.common_trackers import Speed, Demos, TimeoutRate, Touch, EpisodeLength, Boost, \
    BehindBall, TouchHeight, DistToBall, AirTouch, AirTouchHeight, BallHeight, BallSpeed, CarOnGround, GoalSpeed,\
    MaxGoalSpeed
# TODO profile everything before starting to make sure everything is as fast as possible

# ideas for models:
# get to ball as fast as possible, sometimes with no boost, rewards exist
# pinches (ceiling and kuxir and team?), score in as few touches as possible with high velocity
# half flip, wavedash, wall dash, how to do this one?
# lix reset?
# normal play as well as possible, rewards exist
# aerial play without pinch, rewards exist
# kickoff, 5 second terminal, reward ball distance into opp half
set_num_threads(1)

if __name__ == "__main__":
    frame_skip = FRAME_SKIP
    half_life_seconds = TIME_HORIZON
    fps = 120 / frame_skip
    gamma = np.exp(np.log(0.5) / (fps * half_life_seconds))
    config = dict(
        actor_lr=2e-4,
        critic_lr=2e-4,
        n_steps=100_000,
        batch_size=100_000,
        minibatch_size=50_000,
        epochs=50,
        gamma=gamma,
        save_every=100,
        model_every=1000,
        ent_coef=0.01,
    )

    run_id = "kickoff_test1"
    wandb.login(key=os.environ["WANDB_KEY"])
    logger = wandb.init(dir="./wandb_store",
                        name="Valger_kickoff",
                        project="Valger",
                        entity="kaiyotech",
                        id=run_id,
                        config=config,
                        settings=wandb.Settings(_disable_stats=True, _disable_meta=True),
                        )
    redis = Redis(username="user1", password=os.environ["redis_user1_key"], db=1)  # host="192.168.0.201",
    redis.delete("worker-ids")

    stat_trackers = [
        Speed(normalize=True), Demos(), TimeoutRate(), Touch(), EpisodeLength(), Boost(), BehindBall(), TouchHeight(),
        DistToBall(), AirTouch(), AirTouchHeight(), BallHeight(), BallSpeed(normalize=True), CarOnGround(),
        GoalSpeed(), MaxGoalSpeed(),
    ]

    rollout_gen = RedisRolloutGenerator("Valger_kickoff",
                                        redis,
                                        lambda: ModernObsBuilder(expanding=True, tick_skip=FRAME_SKIP, team_size=3,
                                                                 stack_size=5, extra_boost_info=True, embed_players=True,
                                                                 selector=True, doubletap_indicator=True, flip_reset_counter=True,
                                                                 aerial_mechanics=True, wall_play_detection=True, recovery_tracking=True,
                                                                 opponent_modeling=True),
                                        lambda: ZeroSumReward(zero_sum=ZERO_SUM),
                                        lambda: ModernActionParser(throttle_bins=5, steer_bins=5, torque_subdivisions=3,
                                                                   flip_bins=12, include_stalls=True, aerial_mechanics=True,
                                                                   flip_reset_actions=True, double_tap_actions=True,
                                                                   wall_dash_actions=True, recovery_actions=True,
                                                                   boost_management=True, power_slide_optimization=True),
                                        save_every=logger.config.save_every,
                                        model_every=logger.config.model_every,
                                        logger=logger,
                                        clear=True, # TODO check this
                                        stat_trackers=stat_trackers,
                                        # gamemodes=("1v1", "2v2", "3v3"),
                                        max_age=1,
                                        )

    critic = Sequential(Linear(247, 512), LeakyReLU(), Linear(512, 512), LeakyReLU(),

                        Linear(512, 512), LeakyReLU(), Linear(512, 512), LeakyReLU(), Linear(512, 512),
                        LeakyReLU(), Linear(512, 512), LeakyReLU(), Linear(512, 512), LeakyReLU(),
                        Linear(512, 1))

    actor = Sequential(Linear(247, 512), LeakyReLU(), Linear(512, 512), LeakyReLU(), Linear(512, 512), LeakyReLU(),
                       Linear(512, 512), LeakyReLU(), Linear(512, 512), LeakyReLU(), Linear(512, 91))

    actor = DiscretePolicy(actor, (91,))

    optim = torch.optim.Adam([
        {"params": actor.parameters(), "lr": logger.config.actor_lr},
        {"params": critic.parameters(), "lr": logger.config.critic_lr}
    ])

    agent = ActorCriticAgent(actor=actor, critic=critic, optimizer=optim)
    print(f"Gamma is: {gamma}")
    count_parameters(agent)

    alg = PPO(
        rollout_gen,
        agent,
        ent_coef=logger.config.ent_coef,
        n_steps=logger.config.n_steps,
        batch_size=logger.config.batch_size,
        minibatch_size=logger.config.minibatch_size,
        epochs=logger.config.epochs,
        gamma=logger.config.gamma,
        logger=logger,
        zero_grads_with_none=True,
        disable_gradient_logging=True,
    )

    # alg.load("model_saves/")
    alg.agent.optimizer.param_groups[0]["lr"] = logger.config.actor_lr
    alg.agent.optimizer.param_groups[1]["lr"] = logger.config.critic_lr

    alg.run(iterations_per_save=logger.config.save_every, save_dir="kickoff_saves")
