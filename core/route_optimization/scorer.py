#core/scorer.py — Hàm đánh giá điểm đến

# core/algo1/scorer.py
from .config import ALPHA, BETA, GAMMA, DELTA, EPSILON

def preference_score(poi_tags, user_prefs):
    # poi_tags is already a list from load_pois
    if isinstance(poi_tags, str):
        tags = set(poi_tags.split(";"))
    else:
        tags = set(poi_tags)
        
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
