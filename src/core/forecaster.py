import random
from datetime import datetime, timedelta

class Forecaster:
    def __init__(self):
        self.issue_logs = []
        self.alerts = []

    def log_issue_occurrence(self, issue_id):
        self.issue_logs.append({"issue_id": issue_id, "timestamp": datetime.now()})

    def predict_issue_trend(self, issue_id, window_days=7):
        """
        Simple moving average prediction.
        """
        now = datetime.now()
        start_date = now - timedelta(days=window_days)
        
        count = sum(1 for log in self.issue_logs if log["issue_id"] == issue_id and log["timestamp"] >= start_date)
        
        # Simple heuristic: if count is increasing, predict trend
        # For prototype, we just return the count as a "risk score"
        return count

    def check_thresholds(self):
        """
        Check if any issue exceeds a threshold.
        """
        issue_counts = {}
        for log in self.issue_logs:
            iid = log["issue_id"]
            issue_counts[iid] = issue_counts.get(iid, 0) + 1
            
        for iid, count in issue_counts.items():
            if count > 5: # Arbitrary threshold for prototype
                alert = f"ALERT: Issue {iid} has occurred {count} times. Proactive action required."
                if alert not in self.alerts:
                    self.alerts.append(alert)
        
        return self.alerts

if __name__ == "__main__":
    fc = Forecaster()
    # Simulate some logs
    for _ in range(6):
        fc.log_issue_occurrence(1)
        
    print(f"Trend for Issue 1: {fc.predict_issue_trend(1)}")
    print(f"Alerts: {fc.check_thresholds()}")
