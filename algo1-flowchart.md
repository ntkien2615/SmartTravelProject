```mermaid
flowchart TD
    A[Start: User Input] --> B[Load POI Data & Build Matrix]
    B --> C[Filter by Radius, Open/Close, Budget]
    C --> D[Compute Preference & Rating Scores]
    D --> E[Greedy + Lookahead Selection]
    E --> F{Feasible POI Found?}
    F -- Yes --> G[Add to Route, Update Time & Budget]
    G --> E
    F -- No --> H["Apply Local Optimization: 2-opt or insertion"]
    H --> I[Format Itinerary JSON + Summary]
    I --> J[Output / API Response]
    J --> K[End]
