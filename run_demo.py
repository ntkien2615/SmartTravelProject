# run_demo.py
# run_demo.py
from core.solver_route import load_pois, plan_route

pois = load_pois("data/pois_hcm.csv")

route = plan_route(
    pois,
    user_prefs=["food", "history"],
    start_loc=(10.7769, 106.7006),
    time_window=("2025-11-10 09:00", "2025-11-10 21:00"),
    budget=1000000.0
)

print("==== LỘ TRÌNH GỢI Ý ====")
for i, step in enumerate(route, 1):
    print(f"{i}. {step['name']} ({step['mode']}) - {step['arrive_time'].strftime('%H:%M')} → {step['depart_time'].strftime('%H:%M')}")
print(f"Tổng số điểm: {len(route)}")
