#core/optimizer.py — Tối ưu hậu kỳ (2-opt, insertion)
# core/optimizer.py
from datetime import timedelta
from core.utils_geo import travel_info

def two_opt(route):
    if len(route) < 4:
        return route
    best = route[:]
    improved = True
    while improved:
        improved = False
        for i in range(1, len(best) - 2):
            for j in range(i + 1, len(best)):
                if j - i == 1:
                    continue
                new_route = best[:]
                new_route[i:j] = reversed(best[i:j])
                if total_travel_time(new_route) < total_travel_time(best):
                    best = new_route
                    improved = True
    return best

def total_travel_time(route):
    return sum(step.get("travel_time_min", 0) for step in route)
