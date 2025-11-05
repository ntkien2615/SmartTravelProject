#!/usr/bin/env python3
# algo1_route_planner.py
# Chạy: python algo1_route_planner.py
# Yêu cầu: pandas

import math
import pandas as pd
from datetime import datetime, timedelta

# ---------- Helper functions ----------
def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2.0)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2.0)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

def minutes_from_hours(hours):
    return hours * 60

# ---------- Parameters (tùy chỉnh) ----------
SPEEDS_KMH = {"walking":5.0, "motorbike":25.0, "taxi":30.0}  # km/h
COST_PER_KM = {"walking":0.0, "motorbike":2000.0, "taxi":12000.0}  # VND per km
# score weights (lower score = better)
ALPHA = 1.0   # weight for travel_time
BETA = 0.5    # weight for visit_duration
GAMMA = 0.000001  # small factor for cost when comparing (scale to minutes)

# ---------- Load POIs ----------
POI_CSV = "pois.csv"
df = pd.read_csv(POI_CSV)
# ensure columns: id,name,lat,lon,visit_duration_min,entry_fee,rating

# ---------- Inputs (example) ----------
# Em có thể chỉnh StartTime, EndTime, MaxBudget, StartLocation (lat,lon)
StartTime = datetime.strptime("2025-11-10 09:00", "%Y-%m-%d %H:%M")
EndTime   = datetime.strptime("2025-11-10 21:00", "%Y-%m-%d %H:%M")
MaxBudget = 1000000.0  # VND (1000k)
# nếu muốn start từ 1 địa điểm cụ thể, để StartLocation tương ứng, else dùng user coordinate
StartLocation = (10.7769, 106.7006)  # ví dụ: Dinh Độc Lập

# ---------- Precompute distance/time/cost matrices ----------
pois = []
for _, row in df.iterrows():
    pois.append({
        "id": int(row["id"]),
        "name": str(row["name"]),
        "lat": float(row["lat"]),
        "lon": float(row["lon"]),
        "visit_duration": int(row["visit_duration_min"]),
        "entry_fee": float(row["entry_fee"]),
        "rating": float(row.get("rating", 0.0)),
    })

N = len(pois)

# matrix dictionaries index by (i_idx, j_idx, mode)
dist_km = {}
time_min = {}
cost_vnd = {}

# build mapping from index to poi
for i in range(N+1):  # include index 0..N-1 for POIs, N as StartLocation pseudo-index
    for j in range(N+1):
        if i==j:
            for mode in SPEEDS_KMH:
                dist_km[(i,j,mode)] = 0.0
                time_min[(i,j,mode)] = 0.0
                cost_vnd[(i,j,mode)] = 0.0
            continue

# helper to get coords for index
def coords_of_index(idx):
    if idx == N:
        return StartLocation
    p = pois[idx]
    return (p["lat"], p["lon"])

# compute
for i in range(N+1):
    for j in range(N+1):
        if i==j: continue
        lat1, lon1 = coords_of_index(i)
        lat2, lon2 = coords_of_index(j)
        d = haversine_km(lat1, lon1, lat2, lon2)
        for mode in SPEEDS_KMH:
            dist_km[(i,j,mode)] = d
            speed = SPEEDS_KMH[mode]
            tmin = 0.0
            if speed > 0:
                tmin = (d / speed) * 60.0
            time_min[(i,j,mode)] = tmin
            cost_vnd[(i,j,mode)] = d * COST_PER_KM[mode]

# ---------- Scoring function ----------
def score_candidate(poi, travel_time_min, travel_cost_vnd):
    # lower is better: prefer small travel_time, small visit duration, low cost, prefer high rating.
    # We'll create score = alpha*travel_time + beta*visit_duration - rating_factor + gamma*cost
    rating_bonus = - (poi["rating"] * 2.0)  # higher rating reduces score
    return ALPHA * travel_time_min + BETA * poi["visit_duration"] + rating_bonus + GAMMA * travel_cost_vnd

# ---------- Main greedy + 1-step lookahead ----------
def plan_route():
    current_idx = N  # start at startlocation pseudo-index
    current_time = StartTime
    budget_left = MaxBudget
    visited = set()
    route = []  # list of dict {poi_idx, mode, arrive_time, depart_time, travel_time_min, travel_cost}
    total_travel_cost = 0.0
    total_entry_fees = 0.0

    available = set(range(N))

    while True:
        candidates = []
        for idx in list(available):
            poi = pois[idx]
            # try each mode and check feasibility
            for mode in SPEEDS_KMH:
                t_travel = time_min[(current_idx, idx, mode)]
                t_arrive = current_time + timedelta(minutes=t_travel)
                t_finish = t_arrive + timedelta(minutes=poi["visit_duration"])
                travel_cost = cost_vnd[(current_idx, idx, mode)]
                # total cost check (travel + entry)
                estimated_total_cost = total_travel_cost + travel_cost + total_entry_fees + poi["entry_fee"]
                if t_finish <= EndTime and estimated_total_cost <= MaxBudget:
                    sc = score_candidate(poi, t_travel, travel_cost)
                    candidates.append((idx, mode, sc, t_travel, travel_cost, t_finish, t_arrive))

        if not candidates:
            break

        # sort by score ascending
        candidates.sort(key=lambda x: (x[2], x[3]))  # primary score, secondary travel_time
        # lookahead: try best K (e.g., 3) and simulate one-step improvement, pick one with best future potential
        K = min(3, len(candidates))
        best_choice = None
        best_eval = float("inf")
        for cand in candidates[:K]:
            idx, mode, sc, t_travel, travel_cost, t_finish, t_arrive = cand
            # simulate picking cand, then greedy pick next possible one (one-step lookahead)
            sim_time = t_finish
            sim_total_travel = total_travel_cost + travel_cost
            sim_total_entry = total_entry_fees + pois[idx]["entry_fee"]
            sim_available = available.copy()
            sim_available.remove(idx)
            # find best next by naive greedy (only check if any next possible)
            next_possible = False
            next_best_score = float("inf")
            for idx2 in sim_available:
                for mode2 in SPEEDS_KMH:
                    t_travel2 = time_min[(idx, idx2, mode2)]
                    t_arrive2 = sim_time + timedelta(minutes=t_travel2)
                    t_finish2 = t_arrive2 + timedelta(minutes=pois[idx2]["visit_duration"])
                    cost2 = cost_vnd[(idx, idx2, mode2)]
                    est_cost = sim_total_travel + cost2 + sim_total_entry + pois[idx2]["entry_fee"]
                    if t_finish2 <= EndTime and est_cost <= MaxBudget:
                        next_possible = True
                        sc2 = score_candidate(pois[idx2], t_travel2, cost2)
                        if sc2 < next_best_score:
                            next_best_score = sc2
            # evaluation metric: current score + (next_best_score or penalty if no next)
            eval_metric = sc + (next_best_score if next_possible else 50.0)  # penalty if no continuation
            if eval_metric < best_eval:
                best_eval = eval_metric
                best_choice = cand

        # commit best_choice
        chosen = best_choice
        idx, mode, sc, t_travel, travel_cost, t_finish, t_arrive = chosen
        poi = pois[idx]
        entry_fee = poi["entry_fee"]

        route.append({
            "poi_idx": idx,
            "poi_name": poi["name"],
            "mode": mode,
            "arrive_time": t_arrive,
            "depart_time": t_finish,
            "travel_time_min": t_travel,
            "travel_cost": travel_cost,
            "entry_fee": entry_fee
        })

        # update state
        current_time = t_finish
        current_idx = idx
        total_travel_cost += travel_cost
        total_entry_fees += entry_fee
        available.remove(idx)

    # optional: try to append return-to-start or end at last
    total_cost = total_travel_cost + total_entry_fees
    return route, total_cost

# ---------- Local improvement: try insert remaining POIs if any ----------
def try_local_insertion(route, total_cost):
    # naive: attempt to insert any remaining POI between any consecutive steps if feasible
    visited_idxs = {step["poi_idx"] for step in route}
    remaining = [i for i in range(N) if i not in visited_idxs]
    improved = False
    for rem in remaining:
        poi = pois[rem]
        # try positions 0..len(route)
        for pos in range(len(route)+1):
            # compute time and cost feasibility when inserting at pos
            # get prev location index and next location index (use start location for prev when pos==0)
            if pos == 0:
                prev_idx = N
                prev_time = StartTime
            else:
                prev_idx = route[pos-1]["poi_idx"]
                prev_time = route[pos-1]["depart_time"]
            if pos == len(route):
                # next is end (no explicit next), but we must ensure arrival before EndTime
                next_idx = None
            else:
                next_idx = route[pos]["poi_idx"]

            # try best mode from prev -> rem and rem -> next (if next exists)
            feasible = False
            for mode1 in SPEEDS_KMH:
                t1 = time_min[(prev_idx, rem, mode1)]
                arrive1 = prev_time + timedelta(minutes=t1)
                finish1 = arrive1 + timedelta(minutes=poi["visit_duration"])
                cost1 = cost_vnd[(prev_idx, rem, mode1)]
                if finish1 > EndTime:
                    continue
                # check to next
                if next_idx is not None:
                    # choose mode2 with minimal time that fits
                    ok2 = False
                    for mode2 in SPEEDS_KMH:
                        t2 = time_min[(rem, next_idx, mode2)]
                        arrive2 = finish1 + timedelta(minutes=t2)
                        # next's original depart must be >= arrive2 (we may need to shift schedule forward, skip complex shifting)
                        # For simplicity, require arrive2 <= original arrive of next
                        if arrive2 <= route[pos]["arrive_time"]:
                            ok2 = True
                            cost2 = cost_vnd[(rem, next_idx, mode2)]
                            break
                    if not ok2:
                        continue
                # estimate cost: add entry + travel costs
                added_cost = poi["entry_fee"] + cost1 + (cost2 if next_idx is not None and 'cost2' in locals() else 0.0)
                if total_cost + added_cost <= MaxBudget:
                    feasible = True
                    chosen_mode1 = mode1
                    chosen_finish1 = finish1
                    chosen_cost1 = cost1
                    break
            if feasible:
                # perform naive insertion (not shifting subsequent times; simple insertion)
                new_step = {
                    "poi_idx": rem,
                    "poi_name": poi["name"],
                    "mode": chosen_mode1,
                    "arrive_time": arrive1,
                    "depart_time": chosen_finish1,
                    "travel_time_min": t1,
                    "travel_cost": chosen_cost1,
                    "entry_fee": poi["entry_fee"]
                }
                route.insert(pos, new_step)
                total_cost += poi["entry_fee"] + chosen_cost1
                improved = True
                break
        if improved:
            break
    return route, total_cost, improved

# ---------- Run planning ----------
route, total_cost = plan_route()

# try several local insertions
for _ in range(3):
    route, total_cost, improved = try_local_insertion(route, total_cost)
    if not improved:
        break

# ---------- Output nicely ----------
def format_money(x):
    return f"{int(x):,} VND".replace(",", ".")

print("==== LỘ TRÌNH GỢI Ý CHO 1 NGÀY ====")
print(f"Thời gian: {StartTime.strftime('%Y-%m-%d %H:%M')} -> {EndTime.strftime('%H:%M')}")
print(f"Ngân sách tối đa: {format_money(MaxBudget)}")
print()
if not route:
    print("Không tìm được lịch trình thỏa điều kiện (time/budget).")
else:
    current_loc = "Start"
    idx = 1
    for step in route:
        print(f"{idx}. {step['arrive_time'].strftime('%H:%M')} - {step['depart_time'].strftime('%H:%M')}: {step['poi_name']}")
        print(f"    Di chuyển bằng: {step['mode']}, thời gian di chuyển: {step['travel_time_min']:.1f} phút, chi phí di chuyển: {format_money(step['travel_cost'])}")
        if step['entry_fee'] > 0:
            print(f"    Vé vào cửa: {format_money(step['entry_fee'])}")
        else:
            print(f"    Vé vào cửa: Miễn phí")
        idx += 1
    print()
    print("Tóm tắt chi phí:")
    total_travel = sum(s["travel_cost"] for s in route)
    total_entry = sum(s["entry_fee"] for s in route)
    print(f"  - Tổng chi phí di chuyển (ước): {format_money(total_travel)}")
    print(f"  - Tổng phí vào cửa (ước): {format_money(total_entry)}")
    print(f"  => Tổng dự kiến: {format_money(total_travel + total_entry)}")
