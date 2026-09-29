# Field-Workflow Map & Transition Blueprint

## 1. Legacy Vulnerable Workflow
1. User dials help desk or submits web form.
2. Help desk agent asks for Citizen/Employee ID, Name, and Email.
3. If basic fields match, agent manually resets password.
4. **Vulnerability**: Attackers with harvested OSINT or phishing data easily impersonate legitimate civil servants.

## 2. Proposed Risk-Based Workflow
```
User initiates Account Recovery Request
             │
             ▼
  [Identity Evidence Extraction]
  - Multi-Source Legacy Fuzzy Match (HR, Active Directory, App DB)
             │
             ▼
  [Device & Behavioural Context Collection]
  - Hardware Fingerprint, Proxy/VPN check, Anomaly Detection
             │
             ▼
      [Risk Engine Evaluation]
             │
 ┌───────────┼───────────┐
 ▼           ▼           ▼
[LOW]     [MEDIUM]     [HIGH]
(0-29)     (30-59)     (60-100)
 │           │           │
 ▼           ▼           ▼
Auto      Out-of-Band   Security Analyst
Approve    Step-Up      Investigation & Reject
```
