import sys
import os
sys.path.append(os.getcwd())

from src.core.kg_manager import KGManager
from src.core.risk_engine import RiskEngine
from src.core.explainer import Explainer
from src.core.forecaster import Forecaster

def test_kg_loading():
    print("Testing KG Loading...")
    kg = KGManager()
    assert kg.graph.number_of_nodes() > 0, "Graph should have nodes"
    print(f"PASS: Graph loaded with {kg.graph.number_of_nodes()} nodes.")

def test_risk_assessment():
    print("\nTesting Risk Assessment...")
    re = RiskEngine()
    # Test case from paper (ID 1)
    vuln = {"H": 9, "Ro": 3, "Ru": 9, "D": 9, "E": 9}
    threat = {"C": 9, "A": 9, "E_loss": 7, "R": 7}
    issue = re.add_issue(1, "Test Issue", vuln, threat)
    
    assert issue["severity"] == "Very High", f"Expected Very High, got {issue['severity']}"
    assert len(re.proactive_requirements) > 0, "Should generate proactive requirement"
    print(f"PASS: Risk assessed correctly as {issue['severity']}.")

def test_explanation():
    print("\nTesting Explanation...")
    kg = KGManager()
    explainer = Explainer(kg)
    
    # Test User 1 -> Dish 1 (should exist in orders)
    explanation = explainer.explain_recommendation("u1", "d1")
    print(f"Explanation for u1->d1: {explanation}")
    assert "placed" in explanation or "includes" in explanation, "Explanation should mention order history"
    print("PASS: Explanation generated.")

def test_forecasting():
    print("\nTesting Forecasting...")
    fc = Forecaster()
    for _ in range(6):
        fc.log_issue_occurrence(99)
    
    alerts = fc.check_thresholds()
    assert len(alerts) > 0, "Should trigger alert"
    print(f"PASS: Forecasting triggered alert: {alerts[0]}")

if __name__ == "__main__":
    try:
        test_kg_loading()
        test_risk_assessment()
        test_explanation()
        test_forecasting()
        print("\nALL TESTS PASSED")
    except AssertionError as e:
        print(f"\nFAIL: {e}")
    except Exception as e:
        print(f"\nERROR: {e}")
