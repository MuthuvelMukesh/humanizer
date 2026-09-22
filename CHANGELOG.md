# Changelog & Update History

This document records all modifications, additions, and humanization passes performed in this repository.

---

## 1. IEEE Research Paper Humanization Pass

### Source & Deliverables
- **Source File:** [`DATA/paper (3).tex`](DATA/paper%20(3).tex)
- **Preserved Backup:** [`DATA/paper_humanization_backup.tex`](DATA/paper_humanization_backup.tex) *(exact, unmodified copy)*
- **Publication Manuscript:** [`DATA/paper_humanized.tex`](DATA/paper_humanized.tex) *(authentic researcher voice)*
- **Directory Documentation:** [`DATA/README.md`](DATA/README.md) *(detailed manifest, metrics, and Overleaf compilation guide)*

### Summary of Prose & Voice Revisions
A sentence-by-sentence editorial pass was applied across all 12 major sections of the IEEE manuscript:
1. **Abstract:** Reframed into a problem-first, observation-driven technical abstract.
2. **Section I (Introduction):** Replaced repetitive AI transition sequences ("Furthermore...", "Moreover...", "This highlights...") with concrete physical descriptions of subsea cable vulnerabilities.
3. **Section II (Related Work):** Transformed robotic author-by-author summaries into a cohesive, comparative literature synthesis.
4. **Section III (Problem Formulation):** Clarified the mathematical and operational distinctions between *Detection*, *Association*, and *Attribution*.
5. **Section IV (System Architecture):** Revised data pipeline prose to read like researchers explaining their real implementation and feature choices.
6. **Section V (Uncertainty-Aware Evidence Fusion):** Streamlined mathematical descriptions of Bayesian integration and Dempster-Shafer evidential belief handling.
7. **Section VI (Empirical Results on Real-World Datasets):** Converted formulaic reporting into direct empirical observations on Marlinks, EMSO Western Ionian, and Dryad Oliktok Arctic datasets.
8. **Section VII (Simulation & Adversarial Consistency):** Described synthetic stress-testing, GPS/AIS spoofing injection, and signal degradation realistically.
9. **Section VIII (Hardware Feasibility Study):** Strictly retained benchtop ESP32 + MPU6050 profiling as an unbuilt architectural design study, avoiding inflated deployment claims.
10. **Section IX (Discussion):** Deepened technical interpretations of multimodal trade-offs, false positive budgets, and latency.
11. **Section X (Limitations):** Grounded analysis of sensor blind spots, acoustic attenuation, and shallow vs. deep-water operational boundaries.
12. **Section XI & XII (Reproducibility & Conclusion):** Summarized demonstrated empirical contributions and practical prerequisites for future sea trials.

### Verification & Preservation Results
- **Numerical Values & Metrics (100% Preserved):** Real-data AUC ($0.959$), cross-modal correlation ($\rho = -0.948$), unimodal vs. multimodal F1 ($0.462$ vs. $0.824$), pipeline latency ($8.289\text{ ms}$), Adversarial Error Rate ($\text{AER} = 0.0$), background rejection count ($85/85$), and false positive rates ($0.007$, $0.010$, $0.018$).
- **LaTeX Environments (46/46):** Perfectly balanced stack nesting verified via automated syntax tree walk.
- **Mathematical Equations (8/8):** Identical formulas and notation.
- **Tables (10/10):** All tabular bodies, data rows, and alignments preserved verbatim.
- **Figures (8/8):** All graphic references maintained with correct relative paths in `figs/`.
- **Citations & Labels (39 labels, 7 cite keys, 15 bibitems):** All cross-references intact.

---

## 2. Standalone Script & API Tooling

To enable offline and agent-independent humanization using free, open-source models (e.g., Llama 3.3 70B via Groq):

### Tools Added
- [`humanize.py`](humanize.py): Standalone CLI runner capable of processing text strings, Markdown documents, and LaTeX source files using `SKILL.md` rules and Groq/OpenAI-compatible APIs.
  - Supports streaming output.
  - Supports `--file` and `--out` for automated file transformations.
  - Supports `--sample` for voice and writing-style matching.
  - Automatically loads keys from `.env` or system environment variables.
- [`scripts/humanize_sections.py`](scripts/humanize_sections.py): Batch processing utility designed for large manuscripts. Handles section splitting, rate-limit pauses, and reassembly.
- [`.gitignore`](.gitignore): Configured to protect sensitive environment files (`.env`, `*.env`) and Python bytecode caches (`__pycache__/`).

---

## 3. Documentation Updates

- [`README.md`](README.md):
  - Added **Standalone Python CLI** usage guide.
  - Documented file processing, voice matching, and paper batching scripts.
  - Passed `scripts/validate-package.py` package verification suite.
- [`DATA/README.md`](DATA/README.md):
  - Created directory manifest, figure listing, humanization summary, and compilation instructions for the IEEE paper.
