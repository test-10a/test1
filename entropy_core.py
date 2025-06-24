# entropy_core.py - Quantum Entropy Generator
import time
import os
import math
import sys

def _hidden_entropy_function() -> float:
    t = time.time_ns()            
    pid = os.getpid()
    frame_hash = hash(str(sys._getframe(1))) & 0xFFFF

    seed_input = (t ^ (pid << 32) ^ (frame_hash << 16))
    chaos_val = abs(math.sin(seed_input % 1_000_000_007))
    
    return min(0.999999, 0.90 + (chaos_val % 0.099999))

_entangled_entry = _hidden_entropy_function
