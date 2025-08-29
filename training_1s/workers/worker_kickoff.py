
# JSTN 1S Training Configuration
# Optimized for 1s gameplay with jstn's 1s playstyle
# Team size: 1 | Episodes per switch: 1000

# JSTN (Justin) Training Configuration
# Optimized for kickoff mechanics with jstn's playstyle
# Aerial aggression, flip reset mastery, double tap precision

# JSTN (Justin) Training Configuration
# Optimized for kickoff mechanics with jstn's playstyle
# Aerial aggression, flip reset mastery, double tap precision
import sys
from redis import Redis
from redis.retry import Retry
from redis.backoff import ExponentialBackoff
from redis.exceptions import ConnectionError, TimeoutError
from rlgym.envs import Match
# Import modern components instead of deleted CoyoteObs/CoyoteParser
from ModernObsBuilder import ModernObsBuilder
from rlgym.utils.terminal_conditions.common_conditions import TimeoutCondition,\
    NoTouchTimeoutCondition, GoalScoredCondition
from mybots_terminals import KickoffTrainer, BallTouchGroundCondition
from rocket_learn.rollout_generator.redis.redis_rollout_worker import RedisRolloutWorker
from setter import CoyoteSetter
from ModernActionParser import ModernActionParser
from rewards import ZeroSumReward
from torch import set_num_threads
from Constants_kickoff import FRAME_SKIP, ZERO_SUM, STEP_SIZE
import os
set_num_threads(1)


if __name__ == "__main__":
    rew = ZeroSumReward(zero_sum=ZERO_SUM,
                        boost_gain_w_w=0.01,
                        velocity_pb_w_w=0.01,
                        kickoff_w_w=3,
                      goal_w=3,
                      concede_w=-3,
                      velocity_pb_w=0,
                      boost_gain_w=2,
                      demo_w=0,
                      got_demoed_w=0,
                      kickoff_w=0.2,
                      ball_opp_half_w=0.15,
                        kickoff_special_touch_ground_w=0,
                        kickoff_final_boost_w=2,
                        kickoff_vpb_after_0_w=0.1,
                        team_spirit=1)
    frame_skip = FRAME_SKIP
    fps = 120 // frame_skip
    name = "Default"
    send_gamestate = False
    streamer_mode = False
    local = True
    auto_minimize = True
    game_speed = 100
    evaluation_prob = 0
    past_version_prob = 0
    deterministic_streamer = True
    force_old_deterministic = False
    team_size = 3
    dynamic_game = True
    host = "127.0.0.1"
    if len(sys.argv) > 1:
        host = sys.argv[1]
        if host != "127.0.0.1" and host != "localhost":
            local = False
    if len(sys.argv) > 2:
        name = sys.argv[2]
    # if len(sys.argv) > 3 and not dynamic_game:
    #     team_size = int(sys.argv[3])
    if len(sys.argv) > 3:
        if sys.argv[3] == 'GAMESTATE':
            send_gamestate = True
        elif sys.argv[3] == 'STREAMER':
            streamer_mode = True
            evaluation_prob = 0
            game_speed = 1
            deterministic_streamer = True
            auto_minimize = False

    match = Match(
        game_speed=game_speed,
        spawn_opponents=True,
        team_size=team_size,
        state_setter=CoyoteSetter(mode="kickoff"),
        obs_builder=ModernObsBuilder(expanding=True, tick_skip=FRAME_SKIP, team_size=1, stack_size=5, extra_boost_info=True, embed_players=True, selector=True, doubletap_indicator=True, flip_reset_counter=True, aerial_mechanics=True, wall_play_detection=True, recovery_tracking=True, opponent_modeling=True),
        action_parser=ModernActionParser(throttle_bins=5, steer_bins=5, torque_subdivisions=3, flip_bins=12, include_stalls=True, aerial_mechanics=True, flip_reset_actions=True, double_tap_actions=True, wall_dash_actions=True, recovery_actions=True, boost_management=True, power_slide_optimization=True),
        terminal_conditions=[TimeoutCondition(fps * 30), GoalScoredCondition(), KickoffTrainer(min_time_sec=2,
                                                                                               tick_skip=FRAME_SKIP)],
        reward_function=rew,
        tick_skip=frame_skip,
    )

    # local Redis
    if local:
        r = Redis(host=host,
                  username="user1",
                  password=os.environ["redis_user1_key"],
                  db=0,  # testing
                  )

    # remote Redis
    else:
        # noinspection PyArgumentList
        r = Redis(host=host,
                  username="user1",
                  password=os.environ["redis_user1_key"],
                  retry_on_error=[ConnectionError, TimeoutError],
                  retry=Retry(ExponentialBackoff(cap=10, base=1), 25),
                  db=0,  # testing
                  )

    RedisRolloutWorker(r, name, match,
                       past_version_prob=past_version_prob,
                       sigma_target=2,
                       evaluation_prob=evaluation_prob,
                       force_paging=True,
                       dynamic_gm=dynamic_game,
                       send_obs=True,
                       auto_minimize=auto_minimize,
                       send_gamestates=send_gamestate,
                       gamemode_weights={'1v1': 0.8, '2v2': 0.1, '3v3': 0.1},
                       streamer_mode=streamer_mode,
                       deterministic_streamer=deterministic_streamer,
                       force_old_deterministic=force_old_deterministic,
                       # testing
                       batch_mode=True,
                       step_size=STEP_SIZE,
                       ).run()
