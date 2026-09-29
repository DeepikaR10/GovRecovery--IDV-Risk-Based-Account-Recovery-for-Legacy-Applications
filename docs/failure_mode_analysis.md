# Failure Mode and Effects Analysis (FMEA)

| Failure Mode | Root Cause | Impact | Detection Mechanism | Automated Mitigation |
|---|---|---|---|---|
| Minor Name Variation | Legacy system transcription typo | Unfair account lockout | Levenshtein multi-source fuzzy matching | Score adjusted, low-risk approved |
| Unregistered New Device | Employee upgraded home phone | Flagged as unrecognized | Hardware fingerprint trust rating | Step-Up Out-of-Band OTP challenge |
| Harvested Email & Name | Phishing / Data breach | Account takeover risk | Unmatched phone & foreign proxy IP | High risk penalty (>75), instant rejection |
| Credential Stuffing Bot | Scripted attack tool | Infrastructure saturation | Velocity alert & failed attempt counter | Automatic IP cooldown & forensic alert |
| Cross-Tenant Access | Contractor trying to read Treasury record | Privilege escalation | Multi-tenant RBAC boundary check | 403 Forbidden & Security Alert log |
