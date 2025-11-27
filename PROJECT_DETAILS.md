# Project Architecture and Implementation Details

## 1. Project Inception & Philosophy

This project is a reference implementation of the **Knowledge Graph-based Framework for Explainable AI (XAI) and Proactive Requirements Management**, as conceptualized in the research paper _"Constructing a Knowledge Graph-based framework for explainable AI and proactive requirements management"_.

### The Core Problem

Modern AI-driven platforms (like Food Delivery Apps) face three critical challenges:

1.  **Opacity**: Users don't understand why they receive specific recommendations (Black Box AI).
2.  **Trust**: Lack of transparency erodes user trust.
3.  **Reactive Maintenance**: Requirements are often updated only _after_ a failure occurs.

### The Solution

The framework addresses these by using a **Knowledge Graph (KG)** as the central "brain" of the system.

- **Semantic View**: The KG models the domain (Users, Dishes, Ingredients) to provide context.
- **Explainability**: Paths in the KG serve as natural language explanations (e.g., "You like _Spicy_ food, and this dish contains _Chili_").
- **Proactive Management**: By mapping risks to system components, the system can mathematically assess "Severity" and generate requirements _before_ critical failures happen.

---

## 2. System Workflow

The system operates in a cyclic workflow:

1.  **Data Ingestion**: Raw data (Users, Restaurants, Orders) is loaded into the **Knowledge Graph**.
2.  **Interaction**:
    - **User**: Requests a recommendation. The system traverses the KG to find relevant items and generates an explanation based on the path found.
    - **Admin**: Reports a potential issue (e.g., "Payment Failure").
3.  **Risk Assessment**: The **Risk Engine** calculates the probability and impact of the reported issue.
4.  **Proactive Response**: If the risk is High/Very High, a **Proactive Requirement** is automatically generated.
5.  **Forecasting**: The **Forecaster** tracks issue frequency over time to alert on rising trends.

---

## 3. Detailed File Logic

### A. Core Modules (`src/core/`)

#### 1. `kg_manager.py` (The Brain)

- **Purpose**: Manages the lifecycle of the Knowledge Graph.
- **Logic**:
  - Uses `networkx` to create a Directed Graph (`DiGraph`).
  - **`load_data()`**: Reads the JSON data and constructs nodes/edges:
    - **Nodes**: User, Restaurant, Dish, Ingredient, Order.
    - **Edges**: `(User) -> [placed] -> (Order)`, `(Order) -> [includes] -> (Dish)`, `(Dish) -> [serves] -> (Restaurant)`, `(Dish) -> [contains] -> (Ingredient)`.
  - **`get_graph()`**: Returns the graph object for other modules to query.

#### 2. `explainer.py` (The Voice)

- **Purpose**: Translates graph paths into human-readable explanations.
- **Logic**:
  - **`find_paths(start, end)`**: Uses `nx.all_simple_paths` to find connections between a User and a Dish.
  - **`explain_recommendation(user, dish)`**:
    - First, looks for direct historical links (e.g., User ordered this before).
    - If no direct link, looks for indirect links (e.g., User ordered similar dishes from the same Restaurant).
    - **`translate_path_to_nl()`**: Converts a list of nodes `[User A, Order 1, Dish B]` into "User A placed Order 1 which includes Dish B".

#### 3. `risk_engine.py` (The Guardian)

- **Purpose**: Mathematically assesses risks based on the paper's formulas.
- **Logic**:
  - **`calculate_probability()`**: Computes average of 5 factors: Skill Level (H), Reward (Ro), Resources (Ru), Ease of Discovery (D), Ease of Exploitation (E).
  - **`calculate_impact()`**: Computes average of 4 factors: Consequences (C), Business Interruption (A), Economic Loss (E), Reputation (R).
  - **`determine_severity()`**: Maps Probability vs. Impact to a Severity Matrix (Very Low to Very High).
  - **`add_issue()`**: Ingests raw scores, computes severity, and if critical, appends to `proactive_requirements`.

#### 4. `forecaster.py` (The Oracle)

- **Purpose**: Tracks temporal dynamics of issues.
- **Logic**:
  - **`log_issue_occurrence()`**: Appends a timestamped log whenever an issue is reported.
  - **`check_thresholds()`**: Counts occurrences. If an issue repeats > 5 times (configurable), it raises an **ALERT**.

### B. Application Layer (`src/app/`)

#### 1. `main.py` (The API)

- **Purpose**: Exposes core logic via REST endpoints using `FastAPI`.
- **Endpoints**:
  - `GET /recommend/{user_id}`: Returns dishes + explanations.
  - `POST /issues`: Accepts risk reports and runs the Risk Engine.
  - `GET /risks`: Returns current issues, requirements, and alerts.

#### 2. `ui.py` (The Interface)

- **Purpose**: A `Streamlit` dashboard for interaction.
- **Views**:
  - **User View**: Select a user, see recommended dishes with "Why?" explanations.
  - **Admin Dashboard**: Input risk scores (sliders), submit issues, and view the generated requirements log.

---

## 4. Data Generation Strategy

To ensure the system has a robust dataset to demonstrate its capabilities, we moved beyond static manual data to a dynamic generation approach.

### The Generator: `src/data_generator.py`

This script automates the creation of a realistic dataset (`data/generated_data.json`) by integrating with public APIs.

#### Workflow:

1.  **Fetch Users**:
    - Source: `randomuser.me` API.
    - Logic: Fetches real names (e.g., "Alice Smith") and assigns random food preferences (e.g., "Italian", "Spicy").
2.  **Fetch Dishes**:
    - Source: `themealdb.com` API.
    - Logic: Fetches real meals (e.g., "Spaghetti Carbonara"), including their specific area (Cuisine) and Ingredients.
    - **Normalization**: Ingredients are mapped to unique IDs to ensure graph connectivity (e.g., "Garlic" in two dishes points to the same `Ingredient` node).
3.  **Generate Restaurants**:
    - Logic: Creates fictional restaurants with names matching the cuisines of the fetched dishes (e.g., "The Italian Bistro" for Italian dishes).
4.  **Simulate Orders**:
    - Logic: Randomly links Users to Dishes they "ordered" in the past 30 days. This creates the historical paths required for the `Explainer` to work.

### Data Schema

The resulting JSON follows this structure:

```json
{
  "users": [{ "id": "u_gen_1", "name": "...", "preferences": [...] }],
  "restaurants": [{ "id": "r_gen_1", "name": "...", "cuisine": "..." }],
  "dishes": [{ "id": "d_gen_1", "name": "...", "restaurant_id": "r_gen_1", ... }],
  "ingredients": [{ "id": "i_gen_1", "name": "..." }],
  "dish_ingredients": [{ "dish_id": "d_gen_1", "ingredient_ids": ["i_gen_1"] }],
  "orders": [{ "id": "o_gen_1", "user_id": "u_gen_1", "dish_ids": [...] }]
}
```

This structure ensures that when loaded into `KGManager`, the graph is fully connected, allowing for rich path traversals and meaningful explanations.
