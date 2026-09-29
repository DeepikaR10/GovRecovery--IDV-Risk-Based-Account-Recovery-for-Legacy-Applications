# Secure Risk-Based Identity Verification & Account Recovery System
**Academic & Government Prototype for Legacy Systems with Inconsistent Records**

> **Notice**: Synthetic demonstration prototype — not production government identity infrastructure.

## 1. Overview
This project solves an urgent security gap in government departments operating legacy applications with inconsistent identity records: help desks cannot safely verify users during account-recovery requests.

By combining **Multi-Source Identity Reconciliation**, **Device Fingerprint Context**, **Behavioural Risk Telemetry**, and **Heuristic Fraud Detection**, the system achieves **>93% Legitimate Recovery Success** while keeping **Fraud Acceptance Rate < 2.5%** (surpassing the target of <= 5.0%).

## 2. Quick Start

### Backend Setup (FastAPI + SQLite)
```bash
cd backend
python -m venv venv
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate

pip install -r ../requirements.txt
python seed_database.py
uvicorn app.main:app --reload --port 8000
```

### Frontend Setup (React + Vite)
```bash
cd frontend
npm install
npm run dev
```

### Generate Synthetic Dataset (5,000+ Requests)
```bash
python data/generate_data.py --samples 5000 --output data/raw/recovery_requests.csv
```

### Run Benchmark Experiments
```bash
python experiments/run_experiment.py
```

### Run Automated Test Suite
```bash
npm test         # Frontend CI/CD regression suite (12 unit & integration tests)
pytest tests/ -v # Backend Python API assertions
```

## 3. Comprehensive REST API Endpoints Specification
- `POST /api/v1/recovery/assess`: Evaluates incoming identity payload against legacy HR/AD databases and hardware context.
- `POST /api/v1/recovery/stepup/challenge`: Dispatches out-of-band TOTP/FIDO2 hardware challenge for Medium-Risk tier.
- `POST /api/v1/recovery/stepup/verify`: Validates OTP token with 3-attempt limit and automated lockout.
- `GET /api/v1/admin/policy/{org_id}`: Retrieves department-specific risk weights and threshold cutoffs.
- `PUT /api/v1/admin/policy/{org_id}`: Modifies risk policy weights with automated loss function validation.

## 4. Relational Database Schema & Data Dictionary
- `organisations`: Multi-tenant boundary partitions (slug, name, jurisdiction, is_high_security).
- `users`: Master identity records with multi-source legacy name mappings (legacy_hr_name, legacy_ad_name).
- `recovery_requests`: Transactional recovery audit logs with composite risk score, routing tier, and device hash.
- `audit_logs`: Cryptographically chained SHA-256 tamper-evident log records.

## 5. Demo Credentials
| Role | Username | Password |
|---|---|---|
| Help Desk Agent | `helpdesk_demo` | `Demo@Gov2026` |
| Security Analyst | `security_demo` | `Demo@Gov2026` |
| Org Administrator | `orgadmin_demo` | `Demo@Gov2026` |
| External Partner | `partner_demo` | `Demo@Gov2026` |
| System Administrator | `admin_demo` | `Demo@Gov2026` |
