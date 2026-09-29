# Complete Technical Documentation

## Executive Summary
This project provides a secure, risk-based identity verification framework to replace brittle, single-point manual help-desk checks across inconsistent legacy government databases.

## Mathematical Formulation
The composite risk score $R \in [0, 100]$ is computed as:
$$R = w_{\text{id}} R_{\text{id}} + w_{\text{dev}} R_{\text{dev}} + w_{\text{beh}} R_{\text{beh}} + w_{\text{fraud}} R_{\text{fraud}}$$

Default Government Weights:
- $w_{\text{id}} = 0.35$
- $w_{\text{dev}} = 0.20$
- $w_{\text{beh}} = 0.20$
- $w_{\text{fraud}} = 0.25$
