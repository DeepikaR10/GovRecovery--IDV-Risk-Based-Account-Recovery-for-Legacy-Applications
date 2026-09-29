"""
Automated Pytest Suite for Risk Engine, Boundaries & RBAC
"""
import sys
import os

# Robust sys.path resolution
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import pytest
from backend.app.services.risk_engine import RiskEngine, fuzzy_match

def test_fuzzy_name_matching():
    assert fuzzy_match("Anita Kumar", "Anitha Kumar") > 0.90
    assert fuzzy_match("Robert J. Campbell", "Robert Campbell") > 0.85
    assert fuzzy_match("Victoria Harrison", "Random Attacker") < 0.30

def test_low_risk_legitimate():
    engine = RiskEngine()
    sub = {"name": "Robert Campbell", "name_fuzzy_score": 1.0, "email_match": True, "phone_match": True, "org_match": True, "submitted_org": "gov_dept_a"}
    dev = {"is_known_device": True, "is_vpn_or_proxy": False}
    beh = {"failed_attempts_24h": 0, "velocity_alert": False}
    res = engine.calculate_assessment(sub, dev, beh, "gov_dept_a")
    assert res["risk_level"] == "LOW"
    assert res["decision"] == "ALLOW"

def test_medium_risk_step_up_new_device():
    engine = RiskEngine()
    sub = {"name": "Robert Campbell", "name_fuzzy_score": 1.0, "email_match": True, "phone_match": True, "org_match": True, "submitted_org": "gov_dept_a"}
    dev = {"is_known_device": False, "is_vpn_or_proxy": False}
    beh = {"failed_attempts_24h": 1, "velocity_alert": False}
    res = engine.calculate_assessment(sub, dev, beh, "gov_dept_a")
    assert res["risk_level"] == "MEDIUM"
    assert res["decision"] == "STEP_UP"

def test_high_risk_impersonation_rejection():
    engine = RiskEngine()
    sub = {"name": "Victoria Harrison", "name_fuzzy_score": 0.92, "email_match": True, "phone_match": False, "org_match": True, "submitted_org": "gov_dept_a"}
    dev = {"is_known_device": False, "is_vpn_or_proxy": True}
    beh = {"failed_attempts_24h": 4, "velocity_alert": True}
    res = engine.calculate_assessment(sub, dev, beh, "gov_dept_a")
    assert res["risk_level"] == "HIGH"
    assert res["decision"] in ["REJECT", "ESCALATE"]
