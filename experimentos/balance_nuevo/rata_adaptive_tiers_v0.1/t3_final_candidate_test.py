from rata_t3_final_validation import CANDIDATE
assert CANDIDATE["label"]=="CONFIRMED_PATTERN_REFLEJO_MISS_INSTANCE_BASIC"
assert CANDIDATE["requires_prediction_confirmed"] is True
assert CANDIDATE["counter_damage_mode"]=="INSTANCE_BASIC"
assert CANDIDATE["counter_limit"]=="NO_EXTRA_LIMIT_BEYOND_T1_GATE"
print("PASS: final T3 candidate freezes confirmed trigger + instance basic")
