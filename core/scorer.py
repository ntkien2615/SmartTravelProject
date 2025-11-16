#core/scorer.py — Hàm đánh giá điểm đến

# core/scorer.py
from core.config import ALPHA, BETA, GAMMA, DELTA, EPSILON

def preference_score(poi_tags, user_prefs):
    tags = set(str(poi_tags).split(";"))
    inter = len(tags.intersection(set(user_prefs)))
    return inter / len(user_prefs) if user_prefs else 0

def score_candidate(poi, travel_time, travel_cost, user_prefs):
    pref = preference_score(poi["tags"], user_prefs)
    score = (ALPHA * travel_time
             + BETA * poi["visit_duration_min"]
             + GAMMA * travel_cost
             - DELTA * poi["rating"]
             - EPSILON * pref)
    return score
