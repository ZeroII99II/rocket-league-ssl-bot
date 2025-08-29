import sys
from redis import Redis
from redis.retry import Retry
from redis.backoff import ExponentialBackoff
from redis.exceptions import ConnectionError, TimeoutError
# Try to import RLGym 2.0.1 components
try:
    from rlgym import Match
    from rlgym.utils.terminal_conditions.common_conditions import TimeoutCondition,\
        NoTouchTimeoutCondition, GoalScoredCondition
except ImportError:
    # Fallback for RLGym 2.0.1
    class Match:
        def __init__(self, **kwargs):
            pass
    class TimeoutCondition:
        def __init__(self, **kwargs):
            pass
    class NoTouchTimeoutCondition:
        def __init__(self, **kwargs):
            pass
    class GoalScoredCondition:
        def __init__(self, **kwargs):
            pass

from rocket_learn.rollout_generator.redis.redis_rollout_worker import RedisRolloutWorker
from setter import CoyoteSetter
# Import modern components instead of deleted CoyoteObs/CoyoteParser
from ModernObsBuilder import ModernObsBuilder
from ModernActionParser import ModernActionParser
from rewards import ZeroSumReward
from pretrained_agents.necto.necto_v1 import NectoV1
from torch import set_num_threads
from Constants_kickoff import FRAME_SKIP, ZERO_SUM
from pretrained_agents.nexto.nexto_v2 import NextoV2
import os
set_num_threads(1)


if __name__ == "__main__":
    rew = ZeroSumReward(zero_sum=ZERO_SUM)
    frame_skip = FRAME_SKIP
    fps = 120 // frame_skip
    name = "Default"
    send_gamestate = False
    streamer_mode = False
    local = True
    auto_minimize = True
    game_speed = 100
    evaluation_prob = 0.01
    past_version_prob = 0.1
    deterministic_streamer = True
    force_old_deterministic = True
    host = "127.0.0.1"
    if len(sys.argv) > 1:
        host = sys.argv[1]
        if host != "127.0.0.1" and host != "localhost":
            local = False
    if len(sys.argv) > 2:
        name = sys.argv[2]
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
        team_size=3,
        state_setter=CoyoteSetter(),
        obs_builder=ModernObsBuilder(expanding=True, tick_skip=FRAME_SKIP, team_size=3,
                                     stack_size=5, extra_boost_info=True, embed_players=True,
                                     selector=True, doubletap_indicator=True, flip_reset_counter=True,
                                     aerial_mechanics=True, wall_play_detection=True, recovery_tracking=True,
                                     opponent_modeling=True),
        action_parser=ModernActionParser(throttle_bins=5, steer_bins=5, torque_subdivisions=3,
                                         flip_bins=12, include_stalls=True, aerial_mechanics=True,
                                         flip_reset_actions=True, double_tap_actions=True,
                                         wall_dash_actions=True, recovery_actions=True,
                                         boost_management=True, power_slide_optimization=True),
        terminal_conditions=[TimeoutCondition(fps * 300), NoTouchTimeoutCondition(fps * 45), GoalScoredCondition()],
        reward_function=rew,
        tick_skip=frame_skip,
    )

    # local Redis
    if local:
        r = Redis(host=host,
                  username="user1",
                  password=os.environ["redis_user1_key"],
                  db=1,  # testing
                  )

    # remote Redis
    else:
        # noinspection PyArgumentList
        r = Redis(host=host,
                  username="user1",
                  password=os.environ["redis_user1_key"],
                  retry_on_error=[ConnectionError, TimeoutError],
                  retry=Retry(ExponentialBackoff(cap=10, base=1), 25),
                  db=1,  # testing
                  )

    model_name = "necto-model-30Y.pt"
    nectov1 = NectoV1(model_string=model_name, n_players=6)
    model_name = "nexto-model.pt"
    nexto = NextoV2(model_string=model_name, n_players=6)

    pretrained_agents = {nectov1: 0, nexto: 0.1}

    RedisRolloutWorker(r, name, match,
                       past_version_prob=past_version_prob,
                       sigma_target=2,
                       evaluation_prob=evaluation_prob,
                       force_paging=True,
                       dynamic_gm=True,
                       send_obs=True,
                       auto_minimize=auto_minimize,
                       send_gamestates=send_gamestate,
                       pretrained_agents=pretrained_agents,
                       gamemode_weights=None,  # {'1v1': 0.3, '2v2': 0.25, '3v3': 0.45}  # testing weights
                       streamer_mode=streamer_mode,
                       deterministic_streamer=deterministic_streamer,
                       force_old_deterministic=force_old_deterministic,
                       ).run()
