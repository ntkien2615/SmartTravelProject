graph TD
    A[START] --> B{Khởi tạo: FinalRoute=[], CurrentTime, TotalCost=0};
    B --> C{Chọn Điểm Xuất Phát (S) và Cập nhật TotalCost};
    C --> D{CurrentTime = CurrentTime + S.Time_Visit};
    D --> E{Còn điểm Available và CurrentTime < TimeEnd?};

    E -- YES --> F[Tạo MinTravelTime = INF];

    F --> G{FOR EACH NextPOI in AvailablePOIs};
    G -- NO --> H{Có BestNextPOI được chọn?};

    G -- YES --> I{Tính NewTotalCost, TimeRequired};
    I --> J{TimeRequired <= TimeEnd AND NewTotalCost <= MaxBudget?};

    J -- NO --> G; // Quay lại kiểm tra điểm tiếp theo

    J -- YES --> K{TravelTime < MinTravelTime?};
    K -- YES --> L[Cập nhật MinTravelTime, BestNextPOI = NextPOI];
    K -- NO --> G; // Quay lại kiểm tra điểm tiếp theo

    L --> G;

    H -- YES --> M{Cập nhật CurrentTime (sau khi di chuyển)};
    M --> N{Cập nhật TotalCost (cộng chi phí di chuyển + cố định)};
    N --> O{Cập nhật CurrentTime (sau khi tham quan)};
    O --> P[Thêm BestNextPOI vào FinalRoute];
    P --> E; // Quay lại vòng lặp chính

    H -- NO --> Q[BREAK: Không tìm thấy điểm thỏa mãn];
    Q --> R{Định dạng Lịch trình (Output)};
    E -- NO --> R;

    R --> S[END: Trả về FinalRoute, TotalCost];