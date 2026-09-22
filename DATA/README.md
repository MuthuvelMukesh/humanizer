# Subsea Cable Threat Monitoring — Paper Humanization & Asset Guide

This directory contains the IEEE conference paper manuscript, figures, and artifacts for:

> **"Distributed Acoustic Sensing and Multimodal Evidence Fusion for Subsea Cable Threat Monitoring: An Empirical and Adversarial Consistency Study"**

---

## File Manifest

| File | Status | Description |
| :--- | :---: | :--- |
| [`paper_humanized.tex`](paper_humanized.tex) | **Primary** | The publication-ready manuscript with an authentic researcher-style voice. All AI writing tells and repetitive patterns have been revised while preserving scientific content. |
| [`paper_humanization_backup.tex`](paper_humanization_backup.tex) | **Preserved** | Untouched exact backup created prior to humanization. |
| [`paper (3).tex`](paper%20(3).tex) | Source | Original working copy from which the humanization was performed. |
| [`IEEEtran.cls`](IEEEtran.cls) | Class | Official IEEE conference document class required for LaTeX compilation. |
| [`figs/`](figs/) | Assets | Directory containing the 8 figures referenced by the manuscript. |

---

## Figures Directory (`figs/`)

The manuscript references 8 figures:

1. `fig_architecture.png` — Multi-stage pipeline: DAS spatial preprocessing, temporal feature extraction, and evidence fusion.
2. `fig_detection_auc.png` — Receiver Operating Characteristic (ROC) curves on real-world oceanographic datasets.
3. `fig_real_time_series.png` — Real acoustic time series showing background noise vs. vessel-induced vibrations.
4. `fig_scatter_correlation.png` — Scatter analysis illustrating acoustic energy vs. vessel distance ($\rho = -0.948$).
5. `fig_oliktok_waterfall.png` — Spatial-temporal waterfall plot from the Dryad Oliktok Arctic deployment.
6. `fig_confusion_matrix.png` — Decision-state confusion matrix across operational and degraded conditions.
7. `fig_spoofing_comparison.png` — Robustness against GPS/AIS spoofing injection and sensor dropout ($\text{AER} = 0.0$).
8. `fig_esp32_feasibility.png` — Benchtop edge feasibility evaluation (timing profiles and memory footprint).

---

## Summary of Humanization Changes

The humanization pass applied the rules from [`SKILL.md`](../SKILL.md) and authentic academic writing standards without changing any scientific facts or metrics:

### 1. Style & Voice Improvements
- **Eliminated Repetitive Sentence Openers:** Removed recurring cycles of *"This study...", "The proposed framework...", "The results indicate...", "Furthermore...", "Moreover...", "In addition...",* and *"It is worth noting that..."*.
- **Broke Symmetrical Templates:** Replaced uniform "Claim $\rightarrow$ Evidence $\rightarrow$ Implication" paragraph molds with varied sentence rhythms, combining choppy fragments and breaking up overly long clauses.
- **Removed Academic Filler & Clichés:** Removed buzzwords such as *"plays a crucial role", "has gained significant attention", "offers a promising solution", "comprehensive and robust", "seamless integration",* and *"underscores the importance"*.
- **Direct Technical Narrative:** Reframed the text to reflect researchers reporting on procedures performed, empirical trade-offs, and environmental boundaries.

### 2. Section-by-Section Overview
- **Abstract:** Restructured to prioritize the core engineering problem, physical sensing constraints, evaluated datasets, and quantitative trade-offs.
- **Section I (Introduction):** Clarified the vulnerability of transoceanic optical cables, acoustic attenuation limitations, and multimodal necessity without generic hyperbole.
- **Section II (Related Work):** Replaced robotic literature lists with a comparative synthesis of prior DAS signal processing, AIS kinematics, and multi-sensor fusion.
- **Section III (Problem Formulation):** Streamlined definitions of detection, association, and attribution; clarified threat categories and operational bounds.
- **Section IV (System Architecture):** Procedural account of DAS spatial-temporal preprocessing and feature extractors.
- **Section V (Uncertainty-Aware Evidence Fusion):** Direct mathematical prose explaining Bayesian/Dempster-Shafer evidential routing and degraded-state handoffs.
- **Section VI (Empirical Results on Real Datasets):** Direct observational reporting on the Marlinks, EMSO Western Ionian, and Dryad Oliktok Arctic datasets.
- **Section VII (Simulation & Adversarial Consistency):** Realistic description of synthetic stress-testing, AIS dropout, GPS spoofing, and signal degradation.
- **Section VIII (Hardware Feasibility Study):** Rigorously framed as an architectural design feasibility study for benchtop ESP32 + MPU6050 profiling, explicitly avoiding claims of deployed subsea hardware.
- **Section IX (Discussion):** Deepened technical interpretation of multimodal synergy, acoustic attenuation, false alarms, and operational latency.
- **Section X (Limitations):** Candid disclosure of sensor blind spots, bathymetric dependencies, and computational boundaries.
- **Section XI & XII (Reproducibility & Conclusion):** Summarized demonstrated empirical contributions and practical prerequisites for future sea trials.

---

## Integrity & Verification Checklist

Automated and manual tests verified 100% preservation of all technical and document elements:

- [x] **Mathematical Equations (8/8):** All equations, notation, indices, and math symbols are identical to the original.
- [x] **Tables (10/10):** All tabular structures, values, columns, and headers match identically.
- [x] **Labels & References (39/39):** Every `\label` and `\ref` cross-reference is preserved and intact.
- [x] **Citations (7 cite keys, 15 bibitems):** Bibliography entries and in-text citations are untouched.
- [x] **Numerical Metrics Unchanged:**
  - Real-data AUC: $0.959$
  - Cross-modal correlation: $\rho = -0.948$
  - F1 comparison: Unimodal $0.462$ vs. Multimodal $0.824$
  - Pipeline latency: $8.289\text{ ms}$
  - Adversarial Error Rate: $\text{AER} = 0.0$
  - Background window preservation: $85/85$
  - False positive rates: $0.007$, $0.010$, $0.018$
  - Edge timing & memory bounds: $33.1\%$, $60.5\%$, $10.5\%$, $95.9\%$
- [x] **Scope Boundaries:** ESP32/MPU6050 strictly preserved as a benchtop hardware design study.
- [x] **Negative Results:** Preserved all edge-case sensor degradation, blind spots, and adverse sea-state limitations.
- [x] **LaTeX Balance:** All 46 `\begin{...}` and `\end{...}` blocks are properly nested.

---

## Compilation Instructions

### Local (Terminal / CLI)
Run `pdflatex` (or `xelatex`) in this directory:
```bash
pdflatex paper_humanized.tex
pdflatex paper_humanized.tex
```

*(Running twice resolves all cross-references and figure labels).*

### Overleaf / Online LaTeX
1. Create a new project on [Overleaf](https://www.overleaf.com/).
2. Upload `paper_humanized.tex`, `IEEEtran.cls`, and the `figs/` directory.
3. Set `paper_humanized.tex` as the main document.
4. Click **Recompile**.
