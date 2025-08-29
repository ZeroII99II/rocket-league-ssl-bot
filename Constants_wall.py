
# JSTN (Justin) Training Constants
# Optimized for wall mechanics
# Enhanced for jstn's playstyle - aerial aggression, flip reset mastery, double tap precision

# JSTN (Justin) Training Constants
# Optimized for wall mechanics
# Enhanced for jstn's playstyle - aerial aggression, flip reset mastery, double tap precision
from pretrained_agents.nexto.nexto_v2 import NextoV2
from pretrained_agents.KBB.kbb import KBB

FRAME_SKIP = 4
TIME_HORIZON = 6  # horizon in seconds
T_STEP = FRAME_SKIP / 120   # real time per rollout step
ZERO_SUM = False
STEP_SIZE = 500_000
DB_NUM = 15
