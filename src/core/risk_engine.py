class RiskEngine:
    def __init__(self):
        self.issues = []
        self.proactive_requirements = []

    def calculate_probability(self, H, Ro, Ru, D, E):
        """
        Calculate Probability of occurrence based on Eq 1 in the paper.
        H: Skill Level
        Ro: Reward
        Ru: Resources
        D: Ease of Discovery
        E: Ease of Exploitation
        """
        return (H + Ro + Ru + D + E) / 5.0

    def calculate_impact(self, C, A, E_loss, R):
        """
        Calculate Issue Impact based on Eq 2 in the paper.
        C: Consequences for interrupting service
        A: Interrupting business activity
        E_loss: Economic loss
        R: Reputation loss
        """
        return (C + A + E_loss + R) / 4.0

    def get_qualitative_probability(self, prob_score):
        if prob_score < 1: return "Very Low"
        if prob_score < 3: return "Low"
        if prob_score < 5: return "Medium"
        if prob_score < 7: return "High"
        return "Very High"

    def get_qualitative_impact(self, impact_score):
        if impact_score < 1: return "Very Low"
        if impact_score < 3: return "Low"
        if impact_score < 5: return "Medium"
        if impact_score < 7: return "High"
        return "Very High"

    def determine_severity(self, prob_qual, impact_qual):
        """
        Determine Severity based on Table 11.
        """
        matrix = {
            "Very Low": {"Very Low": "Very Low", "Low": "Very Low", "Medium": "Low", "High": "Low", "Very High": "Medium"},
            "Low": {"Very Low": "Very Low", "Low": "Low", "Medium": "Low", "High": "Medium", "Very High": "High"},
            "Medium": {"Very Low": "Low", "Low": "Low", "Medium": "Medium", "High": "High", "Very High": "High"},
            "High": {"Very Low": "Low", "Medium": "Medium", "High": "High", "High": "High", "Very High": "Very High"}, # Note: Table 11 has a slight ambiguity, mapping High-High to High
            "Very High": {"Very Low": "Medium", "Low": "High", "Medium": "High", "High": "Very High", "Very High": "Very High"}
        }
        # Correction for the matrix access based on the paper's table structure (Impact is rows, Prob is cols)
        return matrix.get(impact_qual, {}).get(prob_qual, "Unknown")

    def add_issue(self, issue_id, description, vulnerability_scores, threat_scores):
        """
        Add an issue and assess it.
        vulnerability_scores: dict with H, Ro, Ru, D, E
        threat_scores: dict with C, A, E_loss, R
        """
        prob = self.calculate_probability(**vulnerability_scores)
        impact = self.calculate_impact(**threat_scores)
        
        prob_qual = self.get_qualitative_probability(prob)
        impact_qual = self.get_qualitative_impact(impact)
        
        severity = self.determine_severity(prob_qual, impact_qual)
        
        issue = {
            "id": issue_id,
            "description": description,
            "probability_score": prob,
            "impact_score": impact,
            "probability": prob_qual,
            "impact": impact_qual,
            "severity": severity
        }
        self.issues.append(issue)
        
        if severity in ["Medium", "High", "Very High"]:
            self.generate_proactive_requirement(issue)
            
        return issue

    def generate_proactive_requirement(self, issue):
        req = f"Proactive Requirement for Issue {issue['id']}: Mitigate {issue['severity']} risk - {issue['description']}"
        self.proactive_requirements.append(req)

if __name__ == "__main__":
    re = RiskEngine()
    # Example from Table 12, ID 1
    # H=9, Ro=3, Ru=9, D=9, E=9 -> Prob=7.8 -> Very High
    # C=9, A=9, E=7, R=7 -> Impact=8.0 -> Very High
    # Severity -> Very High
    vuln = {"H": 9, "Ro": 3, "Ru": 9, "D": 9, "E": 9}
    threat = {"C": 9, "A": 9, "E_loss": 7, "R": 7}
    
    issue = re.add_issue(1, "App crashes when user taps 'Pay' button twice", vuln, threat)
    print(f"Issue Assessment: {issue}")
