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

# Try to import rlgym_tools components
try:
    from rlgym_tools.extra_state_setters.replay_setter import ReplaySetter
except ImportError:
    # Fallback for RLGym 2.0.1
    class ReplaySetter:
        def __init__(self, **kwargs):
            pass

import numpy as np

bad_list = []
index = {}
setter = ReplaySetter("replays/bad_1v1_doubletap_state.npy")
# obs = TestObs()
# reward = TestReward()
terminals = [GoalScoredCondition(), TimeoutCondition(100)]

env = rlgym_sim.make(tick_skip=4, spawn_opponents=True, state_setter=setter, copy_gamestate_every_step=True,
                     terminal_conditions=terminals)

total_steps = 0

while True:
    obs = env.reset()
    done = False
    steps = 0
    while not done:
        # actions = np.asarray((np.asarray([0]), np.asarray([np.random.randint(0, 373)])))
        # actions = np.asarray(np.asarray([0],))
        # actions = np.asarray([0] * 8), np.asarray([0] * 8)
        actions = np.asarray([1, 0.5, 0.5, 0.5, 0, 0, 1, 0]), np.asarray([1, 0.5, 0.5, 0.5, 0, 0, 1, 0])
        new_obs, reward, done, state = env.step(actions)
        obs = new_obs
        if np.isnan(obs).any():
            print(f"There is a nan in the obs after {steps} steps.")
            break
        steps += 1
    total_steps += steps
    print(f"completed {steps} steps. Starting new episode. Done {total_steps} total steps")


