# Knowledge Graph-based Framework for XAI and Proactive Requirements Management

This repository contains a reference implementation of the **Knowledge Graph-based framework for Explainable AI (XAI) and Proactive Requirements Management**, as proposed in the associated research paper.

The framework is demonstrated using a **Food Delivery Application** scenario, showcasing how Knowledge Graphs can be used to:

1.  Model system components and their relationships (Users, Dishes, Restaurants).
2.  Provide transparent, path-based explanations for AI recommendations.
3.  Proactively identify and mitigate risks through a structured assessment matrix.

## 🚀 Key Features

### 1. Knowledge Graph (KG) Construction

- **Core Module**: `src/core/kg_manager.py`
- **Description**: Builds a semantic representation of the system using **NetworkX**.
- **Entities**: Users, Restaurants, Dishes, Ingredients, Orders.
- **Relationships**: `serves`, `contains`, `placed`, `includes`.

### 2. Explainable AI (XAI) Interface

- **Core Module**: `src/core/explainer.py`
- **Description**: Implements **KG-Path Traversal** algorithms to generate natural language explanations.
- **Example**: _"Recommended because: Alice placed Order #123 which includes Margherita Pizza."_

### 3. Proactive Risk Management

- **Core Module**: `src/core/risk_engine.py`
- **Description**: A dedicated engine that assesses issues based on **Probability** (Skill, Reward, Resources) and **Impact** (Business, Economic, Reputation).
- **Outcome**: Automatically generates **Proactive Requirements** for high-severity issues (e.g., _"Mitigate Very High risk - App crashes when user taps 'Pay' button twice"_).

### 4. Forecasting Controls

- **Core Module**: `src/core/forecaster.py`
- **Description**: Monitors issue frequency and triggers alerts when critical thresholds are exceeded.

---

## 🛠️ Technology Stack

- **Language**: Python 3.8+
- **Graph Library**: NetworkX
- **Backend Framework**: FastAPI
- **Frontend Framework**: Streamlit
- **Data Processing**: Pandas

---

## 📦 Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-folder>
```

### 2. Set up Virtual Environment

It is recommended to use a virtual environment to manage dependencies.

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🏃‍♂️ Usage

The project consists of two main components: the **Backend API** and the **Frontend UI**. You need to run both in separate terminal windows.

### Step 1: Start the Backend API

The FastAPI backend handles the logic for the Knowledge Graph, Risk Engine, and Explainer.

```bash
# Ensure your virtual environment is active
python -m src.app.main
```

_The API will start at `http://localhost:8000`._

### Step 2: Start the Frontend UI

The Streamlit dashboard allows you to interact with the system as a **User** (viewing recommendations) or an **Admin** (managing risks).

```bash
# Open a new terminal, activate venv, and run:
streamlit run src/app/ui.py
```

_The UI will open in your browser at `http://localhost:8501`._

---

## 📂 Project Structure

```
├── data/
│   └── synthetic_data.json    # Seed data for the Knowledge Graph
├── src/
│   ├── app/
│   │   ├── main.py            # FastAPI Backend Entrypoint
│   │   └── ui.py              # Streamlit Frontend Entrypoint
│   └── core/
│       ├── kg_manager.py      # Knowledge Graph Logic
│       ├── risk_engine.py     # Risk Assessment & Requirements Logic
│       ├── explainer.py       # XAI Path Traversal Logic
│       └── forecaster.py      # Temporal Forecasting Logic
├── tests/
│   └── verify_core.py         # Verification Scripts
├── requirements.txt           # Project Dependencies
└── README.md                  # Project Documentation
```

---

## 🧪 Verification

To verify the core logic of the framework (without running the full UI), you can run the included test script:

```bash
python tests/verify_core.py
```

This script will:

1.  Load the Knowledge Graph.
2.  Simulate a Risk Assessment scenario (from the paper).
3.  Generate a sample Explanation.
4.  Test the Forecasting alerts.

---

## 📄 License

This project is open-source and available under the MIT License.
