"""
Synthetic Dataset Generator for 5,000+ Government Account Recovery Requests
"""
import random
import csv
import json
import os

FIRST_NAMES = ["James", "Anita", "Robert", "Samantha", "Marcus", "Elena", "Arthur", "Kavita", "David", "Victoria", "Gregory", "Michael", "Sophia", "Daniel"]
LAST_NAMES = ["Campbell", "Kumar", "Vance", "Wright", "Rostova", "Pendelton", "Rao", "O'Connor", "Harrison", "Finch", "Chang", "Patel", "Johnson"]

def generate_records(num_samples=5000, output_path="data/raw/recovery_requests.csv"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    random.seed(42)

    fields = [
        "request_id", "user_id", "submitted_name", "submitted_email", "submitted_phone",
        "submitted_org", "ground_truth", "fraud_scenario", "is_known_device", "is_vpn_proxy",
        "failed_attempts_24h", "name_fuzzy_score", "email_match", "phone_match", "org_match"
    ]

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()

        for i in range(num_samples):
            is_legit = (i < int(num_samples * 0.60))
            fn = random.choice(FIRST_NAMES)
            ln = random.choice(LAST_NAMES)
            name = f"{fn} {ln}"
            emp_id = f"EMP-{1000 + (i % 8000)}"

            if is_legit:
                roll = random.random()
                if roll < 0.5:
                    scenario = "legitimate_standard"
                    fuzzy = 1.0
                    em_match = True
                    ph_match = True
                    known_dev = True
                    vpn = False
                    fails = 0
                elif roll < 0.75:
                    scenario = "legacy_typo"
                    fuzzy = round(random.uniform(0.88, 0.95), 2)
                    em_match = True
                    ph_match = random.random() > 0.15
                    known_dev = True
                    vpn = False
                    fails = 1 if random.random() < 0.2 else 0
                elif roll < 0.90:
                    scenario = "travelling_officer"
                    fuzzy = 0.98
                    em_match = True
                    ph_match = True
                    known_dev = True
                    vpn = False
                    fails = 1 if random.random() < 0.25 else 0
                else:
                    scenario = "new_device"
                    fuzzy = 1.0
                    em_match = True
                    ph_match = True
                    known_dev = False
                    vpn = False
                    fails = 0
            else:
                roll = random.random()
                if roll < 0.35:
                    scenario = "stolen_identity"
                    fuzzy = 0.92
                    em_match = True
                    ph_match = False
                    known_dev = False
                    vpn = random.random() < 0.7
                    fails = random.randint(2, 4)
                elif roll < 0.65:
                    scenario = "credential_stuffing"
                    fuzzy = round(random.uniform(0.70, 0.85), 2)
                    em_match = random.random() < 0.5
                    ph_match = False
                    known_dev = False
                    vpn = True
                    fails = random.randint(4, 9)
                elif roll < 0.85:
                    scenario = "cross_org_mismatch"
                    fuzzy = 0.80
                    em_match = False
                    ph_match = False
                    known_dev = False
                    vpn = False
                    fails = random.randint(1, 3)
                else:
                    scenario = "combined_attack"
                    fuzzy = 0.65
                    em_match = False
                    ph_match = False
                    known_dev = False
                    vpn = True
                    fails = random.randint(5, 10)

            writer.writerow({
                "request_id": f"REQ-{20260000 + i}",
                "user_id": emp_id,
                "submitted_name": name,
                "submitted_email": f"{fn.lower()}.{ln.lower()}@dti.gov.state",
                "submitted_phone": "+1-555-019-0000",
                "submitted_org": "gov_dept_a" if (is_legit or scenario != "cross_org_mismatch") else "contractor_org",
                "ground_truth": "LEGITIMATE" if is_legit else "FRAUDULENT",
                "fraud_scenario": scenario,
                "is_known_device": known_dev,
                "is_vpn_proxy": vpn,
                "failed_attempts_24h": fails,
                "name_fuzzy_score": fuzzy,
                "email_match": em_match,
                "phone_match": ph_match,
                "org_match": is_legit or scenario != "cross_org_mismatch"
            })

    print(f"Generated {num_samples} synthetic records at {output_path}")

if __name__ == "__main__":
    generate_records(5000)
