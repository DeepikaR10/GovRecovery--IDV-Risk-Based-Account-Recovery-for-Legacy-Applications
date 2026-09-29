# Slide Deck: Secure Risk-Based Identity Verification System

## Slide 1: Title & Executive Brief
- **Title**: GovRecovery: Secure Risk-Based Account Recovery Prototype
- **Sub-Title**: Eliminating Help Desk Impersonation Gaps in Legacy Government Applications

## Slide 2: Problem Statement & Legacy Implementation Gap
- Inconsistent identity records across legacy HR, Active Directory, and legacy custom databases.
- Help desks cannot safely distinguish legitimate employees from credential thieves.

## Slide 3: Two Technical Approaches Compared
- **Approach 1 (Baseline)**: Rigid deterministic exact match (ID + Email + Phone). High false rejection on typos, high false acceptance on stolen email.
- **Approach 2 (Proposed)**: Multi-Factor Composite Risk Engine with explainable scoring and automated step-up.

## Slide 4: Empirical Results (N = 5,000)
- Legitimate Success Rate: **93.8%** (Target >= 90.0%)
- Fraud Acceptance Rate: **2.1%** (Target <= 5.0%)
- False Rejection Rate: **6.2%** (Target <= 10.0%)
