from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

from src.core.kg_manager import KGManager
from src.core.risk_engine import RiskEngine
from src.core.explainer import Explainer
from src.core.forecaster import Forecaster

app = FastAPI(title="KG-XAI Framework")

# Initialize modules
kg_manager = KGManager()
risk_engine = RiskEngine()
explainer = Explainer(kg_manager)
forecaster = Forecaster()

class IssueModel(BaseModel):
    id: int
    description: str
    vulnerability_scores: dict
    threat_scores: dict

@app.get("/")
def read_root():
    return {"message": "Welcome to the KG-XAI Framework API"}

@app.get("/recommend/{user_id}")
def get_recommendations(user_id: str):
    # Mock recommendation logic: return all dishes
    # In a real system, this would use the KG or an ML model
    dishes = [n for n, d in kg_manager.graph.nodes(data=True) if d.get("type") == "Dish"]
    recommendations = []
    
    for dish_id in dishes:
        explanation = explainer.explain_recommendation(user_id, dish_id)
        dish_data = kg_manager.get_node_attributes(dish_id)
        recommendations.append({
            "dish_id": dish_id,
            "name": dish_data["name"],
            "explanation": explanation
        })
        
    return recommendations

@app.get("/explain/{user_id}/{dish_id}")
def explain_item(user_id: str, dish_id: str):
    explanation = explainer.explain_recommendation(user_id, dish_id)
    return {"user_id": user_id, "dish_id": dish_id, "explanation": explanation}

@app.post("/issues")
def report_issue(issue: IssueModel):
    result = risk_engine.add_issue(issue.id, issue.description, issue.vulnerability_scores, issue.threat_scores)
    forecaster.log_issue_occurrence(issue.id)
    return result

@app.get("/risks")
def get_risks():
    return {
        "issues": risk_engine.issues,
        "proactive_requirements": risk_engine.proactive_requirements,
        "alerts": forecaster.check_thresholds()
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
