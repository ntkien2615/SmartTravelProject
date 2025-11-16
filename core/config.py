#core/config.py — Cấu hình chung

# core/config.py
SPEEDS_KMH = {"walking": 5.0, "motorbike": 25.0, "taxi": 35.0}
COST_PER_KM = {"walking": 0.0, "motorbike": 2000.0, "taxi": 12000.0}

# Trọng số cho hàm đánh giá
ALPHA = 1.0     # travel time weight
BETA = 0.5      # visit duration weight
GAMMA = 0.000001  # cost scaling
DELTA = 2.0     # rating bonus weight
EPSILON = 3.0   # preference bonus weight

# Giới hạn mặc định
DEFAULT_START = (10.7769, 106.7006)
DEFAULT_TIME_WINDOW = ("2025-11-10 09:00", "2025-11-10 21:00")
DEFAULT_BUDGET = 1000000.0
