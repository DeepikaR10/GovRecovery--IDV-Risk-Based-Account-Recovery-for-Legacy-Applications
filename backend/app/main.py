"""
Secure Account Recovery Prototype - FastAPI Main Entrypoint
"""
import os
import sys
from typing import Optional, Dict, Any, List
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

# Ensure path resolution
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

try:
    from backend.app.services.risk_engine import RiskEngine
except ImportError:
    from app.services.risk_engine import RiskEngine

app = FastAPI(
    title="GovRecovery Risk-Based Verification API",
    description="Risk-based identity verification engine for legacy government applications",
    version="2.4.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = RiskEngine()

class AssessmentRequest(BaseModel):
    user_id: str
    submitted_name: str
    submitted_email: str
    submitted_phone: str
    submitted_org: str
    is_known_device: bool = True
    is_vpn_proxy: bool = False
    failed_attempts_24h: int = 0
    name_fuzzy_score: float = 1.0
    email_match: bool = True
    phone_match: bool = True
    org_match: bool = True

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "GovRecovery Risk Engine",
        "version": "2.4.0",
        "compliance": "FAR <= 2.5%, FRR <= 6.5%"
    }

@app.post("/api/recovery/evaluate")
def evaluate_recovery(req: AssessmentRequest):
    sub = {
        "name": req.submitted_name,
        "name_fuzzy_score": req.name_fuzzy_score,
        "email_match": req.email_match,
        "phone_match": req.phone_match,
        "org_match": req.org_match,
        "submitted_org": req.submitted_org
    }
    dev = {
        "is_known_device": req.is_known_device,
        "is_vpn_or_proxy": req.is_vpn_proxy
    }
    beh = {
        "failed_attempts_24h": req.failed_attempts_24h,
        "velocity_alert": req.failed_attempts_24h >= 4
    }
    assessment = engine.calculate_assessment(sub, dev, beh, req.submitted_org)
    return {
        "user_id": req.user_id,
        "assessment": assessment
    }
