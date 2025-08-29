# Try to import rlgym_sim components
try:
    import rlgym_sim
    from rlgym_sim.utils.terminal_conditions.common_conditions import GoalScoredCondition, TimeoutCondition
except ImportError:
    # Fallback for RLGym 2.0.1
    class GoalScoredCondition:
        def __init__(self):
            pass
    class TimeoutCondition:
        def __init__(self, **kwargs):
            pass

# Import modern components instead of deleted CoyoteParser
from ModernActionParser import ModernActionParser
from test_files.test_obs import TestObs
from test_files.test_reward import TestReward
import numpy as np

# Try to import rlgym_tools components
try:
    from rlgym_tools.extra_state_setters.replay_setter import ReplaySetter
    from rlgym_tools.extra_state_setters.augment_setter import AugmentSetter
except ImportError:
    # Fallback for RLGym 2.0.1
    class ReplaySetter:
        def __init__(self, **kwargs):
            pass
    class AugmentSetter:
        def __init__(self, **kwargs):
            pass

bad_list = []
index = {}
setter = AugmentSetter(ReplaySetter("replays/double_tap_1v1.npy", defender_front_goal_weight=0,
                                    random_boost=True, print_choice=True, override=None, index=index),
                       True, False, False)
# setter = ReplaySetter("replays/bad_1v1_doubletap_state.npy")
parser = ModernActionParser()
obs = TestObs()
reward = TestReward()
terminals = [GoalScoredCondition(), TimeoutCondition(100)]

env = rlgym_sim.make(tick_skip=4, spawn_opponents=True, state_setter=setter, copy_gamestate_every_step=True,
                     action_parser=parser, obs_builder=obs, reward_fn=reward, terminal_conditions=terminals)

total_steps = 0

visualize = False
if visualize:
    from rocketsimvisualizer import VisualizerThread

    arena = env._game.arena  # noqa
    v = VisualizerThread(arena, fps=60, tick_rate=120, tick_skip=4, step_arena=False,  # noqa
                         overwrite_controls=False)  # noqa
    v.start()

while True:
    obs = env.reset()
    done = False
    steps = 0
    while not done:
        #actions = np.asarray((np.asarray([0]), np.asarray([np.random.randint(0, 373)])))
        # actions = np.asarray(np.asarray([0],))
        actions = np.asarray((np.asarray([0]), np.asarray([0])))
        new_obs, reward, done, state = env.step(actions)
        obs = new_obs
        if np.isnan(obs).any():
            # self.actions.reverse()
            # self.states.reverse()
            print(f"There is a nan in the obs. Printing states after {steps} steps")
            if index[0] not in bad_list:
                bad_list.append(index[0])
            # input()
            break
        steps += 1
    total_steps += steps
    print(bad_list)
    print(f"completed {steps} steps. Starting new episode. Done {total_steps} total steps")


