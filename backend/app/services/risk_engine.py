"""
Core Risk Engine implementation
Evaluates identity matching, device context, behaviour, and fraud indicators
"""
import math
from typing import Dict, Any, List, Tuple
from difflib import SequenceMatcher

def fuzzy_match(a: str, b: str) -> float:
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a.strip().lower(), b.strip().lower()).ratio()

class RiskEngine:
    def __init__(self, weights: Dict[str, float] = None, thresholds: Tuple[int, int] = (29, 60)):
        self.weights = weights or {"identity": 0.35, "device": 0.20, "behaviour": 0.20, "fraud": 0.25}
        self.low_threshold, self.high_threshold = thresholds

    def evaluate_identity(self, submitted: dict, legacy_hr: dict, legacy_ad: dict) -> Tuple[float, List[dict], List[str]]:
        factors = []
        reasons = []
        penalty = 0.0

        hr_name_sim = fuzzy_match(submitted.get("name", ""), legacy_hr.get("name", ""))
        ad_name_sim = fuzzy_match(submitted.get("name", ""), legacy_ad.get("name", ""))
        best_sim = max(hr_name_sim, ad_name_sim, submitted.get("name_fuzzy_score", 0.0))

        if best_sim >= 0.88:
            factors.append({"category": "Identity", "label": "Name Match", "score": 5, "severity": "low"})
            reasons.append(f"Name matched legacy records ({int(best_sim*100)}% fuzzy similarity)")
        elif best_sim >= 0.65:
            penalty += 28
            factors.append({"category": "Identity", "label": "Name Typo/Variant", "score": 45, "severity": "medium"})
            reasons.append(f"Minor legacy name variance detected ({int(best_sim*100)}%)")
        else:
            penalty += 75
            factors.append({"category": "Identity", "label": "Name Mismatch", "score": 90, "severity": "high"})
            reasons.append("Submitted name does not match official personnel records")

        if submitted.get("email_match"):
            reasons.append("Official domain email verified")
        else:
            penalty += 40
            reasons.append("Email mismatch against legacy directory")

        if not submitted.get("phone_match"):
            penalty += 30
            reasons.append("Unregistered contact phone number provided")

        if not submitted.get("org_match"):
            penalty += 45
            reasons.append("Claimed organisation does not match identity records")

        score = min(100.0, max(0.0, penalty))
        return score, factors, reasons

    def evaluate_device(self, device: dict) -> Tuple[float, List[dict], List[str]]:
        score = 0.0
        factors = []
        reasons = []

        if device.get("is_known_device"):
            score += 5
            reasons.append("Request from verified corporate device fingerprint")
        else:
            score += 55
            reasons.append("Unrecognized device fingerprint detected")

        if device.get("is_vpn_or_proxy"):
            score += 35
            reasons.append("Connection routed through anonymizing VPN / proxy")

        return min(100.0, max(0.0, score)), factors, reasons

    def evaluate_behaviour(self, behaviour: dict) -> Tuple[float, List[dict], List[str]]:
        score = 0.0
        reasons = []
        failed = behaviour.get("failed_attempts_24h", 0)

        if failed == 0:
            pass
        elif failed <= 2:
            score += 25
            reasons.append(f"{failed} prior failed recovery attempt(s)")
        else:
            score += 75
            reasons.append(f"High failure frequency ({failed} failed attempts in 24h)")

        if behaviour.get("velocity_alert"):
            score += 30
            reasons.append("Automated submission velocity anomaly")

        return min(100.0, max(0.0, score)), [], reasons

    def evaluate_fraud(self, submitted: dict, device: dict, behaviour: dict, org_id: str) -> Tuple[float, List[str]]:
        score = 0.0
        reasons = []

        if submitted.get("submitted_org") != org_id:
            score += 85
            reasons.append("Cross-tenant organisation isolation violation")

        if not device.get("is_known_device") and device.get("is_vpn_or_proxy") and behaviour.get("failed_attempts_24h", 0) >= 2:
            score += 50
            reasons.append("Coordinated impersonation attack signature flagged")

        return min(100.0, max(0.0, score)), reasons

    def calculate_assessment(self, submitted: dict, device: dict, behaviour: dict, org_id: str, legacy_hr: dict = None, legacy_ad: dict = None) -> dict:
        legacy_hr = legacy_hr or {}
        legacy_ad = legacy_ad or {}

        id_score, id_factors, id_reasons = self.evaluate_identity(submitted, legacy_hr, legacy_ad)
        dev_score, dev_factors, dev_reasons = self.evaluate_device(device)
        beh_score, beh_factors, beh_reasons = self.evaluate_behaviour(behaviour)
        fraud_score, fraud_reasons = self.evaluate_fraud(submitted, device, behaviour, org_id)

        weighted = (
            id_score * self.weights["identity"] +
            dev_score * self.weights["device"] +
            beh_score * self.weights["behaviour"] +
            fraud_score * self.weights["fraud"]
        )
        final_score = int(round(weighted))

        if final_score <= self.low_threshold:
            risk_level = "LOW"
            decision = "ALLOW"
            action = "Allow automated self-service password reset"
        elif final_score < self.high_threshold:
            risk_level = "MEDIUM"
            decision = "STEP_UP"
            action = "Require Out-of-Band OTP or Help Desk verification"
        else:
            risk_level = "HIGH"
            decision = "REJECT" if final_score >= 75 else "ESCALATE"
            action = "Reject automated recovery and escalate to Security Analyst"

        return {
            "risk_score": final_score,
            "risk_level": risk_level,
            "decision": decision,
            "recommended_action": action,
            "reasons": id_reasons + dev_reasons + beh_reasons + fraud_reasons
        }
