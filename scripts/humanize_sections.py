#!/usr/bin/env python3
"""
Section-by-section Humanizer for sea_cable.docx.
Rewrites the paper section by section, preserving technical accuracy,
citations, tables, and metrics while eliminating AI writing tells.
"""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path
from groq import Groq, RateLimitError

ROOT = Path(__file__).resolve().parent.parent
SKILL_PATH = ROOT / "SKILL.md"
INPUT_FILE = ROOT / "DATA" / "sea_cable.txt"
OUTPUT_FILE = ROOT / "DATA" / "sea_cable_humanized.md"


def get_api_key() -> str:
    env_file = ROOT / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("GROQ_API_KEY="):
                return line.split("=", 1)[1].strip().strip("\"'")
    key = os.environ.get("GROQ_API_KEY")
    if key:
        return key.strip()
    sys.exit("Error: No GROQ_API_KEY found.")


def call_humanizer_with_retry(
    client: Groq,
    system_prompt: str,
    user_prompt: str,
    model: str = "openai/gpt-oss-120b",
    max_retries: int = 5
) -> str:
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.6,
            )
            return response.choices[0].message.content or ""
        except RateLimitError as e:
            wait_time = 30 + (attempt * 10)
            print(f"   [Rate limit reached. Pausing {wait_time}s for token bucket replenishment...]")
            time.sleep(wait_time)
        except Exception as e:
            if "rate_limit" in str(e).lower() or "429" in str(e):
                wait_time = 30 + (attempt * 10)
                print(f"   [Rate limit error. Pausing {wait_time}s...]")
                time.sleep(wait_time)
            else:
                print(f"   [API error: {e}. Retrying in 10s...]")
                time.sleep(10)
    sys.exit("Failed after maximum retries.")


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    api_key = get_api_key()
    client = Groq(api_key=api_key)
    system_prompt = SKILL_PATH.read_text(encoding="utf-8")

    # Read original text
    raw_lines = INPUT_FILE.read_text(encoding="utf-8").splitlines()

    # Title & Authors (Lines 0 to 30) - preserve directly
    header_block = "\n".join(raw_lines[:31]).strip()

    # Define sections
    sections = [
        {
            "id": "Abstract",
            "title": "Abstract & Index Terms",
            "start": 31,
            "end": 45,
            "instructions": "Humanize the Abstract and Index Terms. Keep all exact numerical results (AUC, F1, latency, p-values, correlations) and technical terminology intact. Do not invent any numbers."
        },
        {
            "id": "Section1",
            "title": "I. Introduction & Validation Scope",
            "start": 45,
            "end": 137,
            "instructions": "Humanize the Introduction. Keep Table I, operational principle (1), and all numbered contributions intact. Remove AI tells (staged run-ups, not-X-but-Y, inflated significance). Keep all citations [1]-[15]."
        },
        {
            "id": "Section2",
            "title": "II. Related Work & Problem Formulation",
            "start": 137,
            "end": 183,
            "instructions": "Humanize Related Work and Problem Formulation. Keep equations, mathematical definitions (H0-H3, X, Omega), and threat model intact. Keep formal tone without AI clichés."
        },
        {
            "id": "Section3A",
            "title": "III. Proposed Framework (Architecture & Feature Extraction)",
            "start": 183,
            "end": 380,
            "instructions": "Humanize Proposed Framework Part 1 (Optical DAS strain pipeline, spatio-temporal association, feature extraction). Keep all equations, algorithms, mathematical variables, and Table II/III references intact."
        },
        {
            "id": "Section3B",
            "title": "III. Proposed Framework (Adversarial Consistency & Graded Decision Hierarchy)",
            "start": 380,
            "end": 575,
            "instructions": "Humanize Proposed Framework Part 2 (Adversarial cross-consistency check, graded decision states T0-T3 and TX). Keep all formal definitions, thresholds, and logic intact."
        },
        {
            "id": "Section4",
            "title": "IV. Empirical Datasets & Experimental Setup",
            "start": 575,
            "end": 765,
            "instructions": "Humanize Experimental Evaluation and Datasets (Marlinks transit, EMSO Western Ionian, Dryad Oliktok). Keep all dataset numbers (channels, sample rates, hours, days) and Table IV-VI intact."
        },
        {
            "id": "Section5",
            "title": "V. Results & Ablation Analysis",
            "start": 765,
            "end": 1017,
            "instructions": "Humanize the Results, Adversarial Robustness, and Ablation Study. Keep all F1 scores, detection boundaries, Table VII-X, and negative findings intact."
        },
        {
            "id": "Section6",
            "title": "VI. Discussion & Conclusion",
            "start": 1017,
            "end": 1065,
            "instructions": "Humanize the Discussion, Limitations, Hardware-in-the-loop future scope, and Conclusion. Keep technical humility and clear conclusions without inflated AI summaries."
        },
    ]

    references_block = "\n".join(raw_lines[1065:]).strip()

    # Initialize output file
    OUTPUT_FILE.write_text(f"# {header_block}\n\n---\n\n", encoding="utf-8")
    print(f"Initialized output file: {OUTPUT_FILE}")

    for idx, sec in enumerate(sections, 1):
        print(f"\n=======================================================")
        print(f"Processing [{idx}/{len(sections)}]: {sec['title']}...")
        print(f"=======================================================")

        sec_text = "\n".join(raw_lines[sec['start']:sec['end']]).strip()
        user_prompt = (
            f"Please humanize the following section of our academic research paper:\n\n"
            f"SECTION: {sec['title']}\n"
            f"SPECIAL INSTRUCTIONS: {sec['instructions']}\n\n"
            f"TEXT TO HUMANIZE:\n"
            f"{sec_text}\n\n"
            f"Return the humanized final prose directly. Keep all equations, numbers, citations, and tables intact."
        )

        result = call_humanizer_with_retry(
            client=client,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            model="openai/gpt-oss-120b"
        )

        # Append to output file
        with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
            f.write(f"\n\n## {sec['title']}\n\n")
            f.write(result.strip())
            f.write("\n\n---\n")

        print(f"-> Completed [{idx}/{len(sections)}]: {sec['title']}")
        # Give token bucket a short pause before next section
        time.sleep(20)

    # Append references at the end
    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
        f.write("\n\n## References\n\n")
        f.write(references_block)

    print("\n\n=======================================================")
    print(f"[ALL DONE!] Full humanized paper saved to: {OUTPUT_FILE}")
    print("=======================================================")


if __name__ == "__main__":
    main()
