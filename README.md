# C1-FFL Persistence Detector: Bioinformatics & Computational Biology

This repository contains the research, code, and interactive simulations for the paper:  
**"Dynamic Modeling of a Type-1 Coherent Feed-Forward Loop as a Persistence Detector"**

Published on **ClawRxiv (ID: 81)** for the Claw4S 2026 Conference.

## 🔬 Project Overview
The Type-1 Coherent Feed-Forward Loop (C1-FFL) is a recurring motif in gene regulatory networks. This project provides a first-principles derivation of noise-filtering thresholds (amplitude and duration) and validates them through deterministic ODE modeling and an interactive real-time dashboard.

### Key Components:
- **[Live Dashboard](https://githubbermoon.github.io/bioinformatics-simulations/index.html)**: Interactive paper with rendered MathJax formulas.
- **[Interactive Simulation](https://githubbermoon.github.io/bioinformatics-simulations/sim.html)**: Real-time Plotly.js simulation of C1-FFL dynamics.
- **`simulate_ffl.py`**: Python implementation using `SciPy` for ODE integration.
- **`paper.tex`**: LaTeX source for the formal Research Note.

## 🚀 Getting Started

### 1. Web Dashboard
Simply visit the [GitHub Pages site](https://githubbermoon.github.io/bioinformatics-simulations/) to view the paper and play with the simulation directly in your browser.

### 2. Local Python Simulation
To run the underlying mathematical model locally:
```bash
pip install scipy matplotlib
python simulate_ffl.py
```

## 🧪 Verification & Reproducibility
*Updated Mar 24, 2026*

To ensure scientific reproducibility, we provide exact reference metrics. After running `simulate_ffl.py`, your `verification.json` should produce the following results:

- **Max Z (Short Pulse):** `0.13105`
- **Max Z (Long Pulse):** `7.61216`
- **Activation Ratio:** `58.08526`
- **SHA-256 (verification.json):** `5c1dafe12bdabe46b12c75822430756037ea645101d89dc1171b76f3e70f1d63`

Confirmed working on both x86_64 and Apple Silicon (M-series) as of March 2026.

## 📊 Abstract
Network motifs in transcriptional regulation provide compact primitives for cellular decision-making. We analyze a Type-1 coherent feed-forward loop (C1-FFL) acting as a persistence detector: rejecting short input pulses while triggering robust output for sustained signals. We derive explicit noise-filtering thresholds for signal amplitude and duration, and map these to the *araBAD* sugar-utilization program in *E. coli*.

## 🏷️ Metadata
- **MSC 2020:** 92C40, 92C42
- **Keywords:** bioinformatics, computational-biology, gene-regulatory-networks, persistence-detector, ode-modeling, synthetic-biology
- **Authors:** Pranjal (Independent Researcher) & Claw 🦞 (AI Agent)
