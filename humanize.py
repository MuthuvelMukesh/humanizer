#!/usr/bin/env python3
"""
Humanizer Runner via Groq API.
Rewrites AI-sounding text using open-source models (default: llama-3.3-70b-versatile)
guided by SKILL.md rules.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

try:
    from groq import Groq
except ImportError:
    sys.exit("Error: 'groq' package not found. Run: pip install groq")

ROOT = Path(__file__).resolve().parent
SKILL_PATH = ROOT / "SKILL.md"
DEFAULT_MODEL = "openai/gpt-oss-120b"


def load_api_key() -> str | None:
    # 1. Check environment variable
    key = os.environ.get("GROQ_API_KEY")
    if key and key.strip():
        return key.strip()

    # 2. Check local .env file
    env_file = ROOT / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("GROQ_API_KEY="):
                val = line.split("=", 1)[1].strip().strip("\"'")
                if val:
                    return val
    return None


def get_system_prompt() -> str:
    if not SKILL_PATH.exists():
        sys.exit(f"Error: Could not find {SKILL_PATH}")
    return SKILL_PATH.read_text(encoding="utf-8")


def run_humanizer(
    text: str,
    api_key: str,
    model: str = DEFAULT_MODEL,
    sample: str | None = None,
    file_mode: bool = False,
    stream: bool = True
) -> str:
    # Ensure UTF-8 output in Windows console
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    client = Groq(api_key=api_key)
    system_prompt = get_system_prompt()

    user_content = ""
    if sample:
        user_content += f"Here's a sample of my writing for voice matching:\n{sample}\n\n"

    if file_mode:
        user_content += f"Humanize the prose in this file content (File mode: change prose only, keep code/metadata intact):\n\n{text}"
    else:
        user_content += f"Please humanize this text:\n\n{text}"

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_content},
    ]

    try:
        if stream:
            completion = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.6,
                stream=True,
            )
            chunks = []
            for chunk in completion:
                content = chunk.choices[0].delta.content or ""
                sys.stdout.write(content)
                sys.stdout.flush()
                chunks.append(content)
            print()
            return "".join(chunks)
        else:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.6,
            )
            result = response.choices[0].message.content or ""
            print(result)
            return result
    except Exception as e:
        sys.exit(f"\nAPI Error: {e}")


def read_document(path: Path) -> str:
    if path.suffix.lower() == ".docx":
        import zipfile
        import xml.etree.ElementTree as ET
        try:
            with zipfile.ZipFile(path) as z:
                xml_content = z.read("word/document.xml")
            tree = ET.fromstring(xml_content)
            ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
            paragraphs = []
            for p in tree.iterfind(".//w:p", ns):
                texts = [node.text for node in p.iterfind(".//w:t", ns) if node.text]
                if texts:
                    paragraphs.append("".join(texts))
            return "\n\n".join(paragraphs)
        except Exception as e:
            sys.exit(f"Error reading .docx file: {e}")
    else:
        return path.read_text(encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Rewrite AI-sounding text using Humanizer patterns and Groq API."
    )
    parser.add_argument("text", nargs="?", help="Text to humanize (or omit for interactive mode)")
    parser.add_argument("--file", "-f", help="Path to a docx, markdown, or text file to humanize")
    parser.add_argument("--output", "-o", help="Optional output file path to save the humanized result")
    parser.add_argument("--sample", "-s", help="Optional sample file or text to match your voice")
    parser.add_argument("--model", "-m", default=DEFAULT_MODEL, help=f"Groq model (default: {DEFAULT_MODEL})")
    parser.add_argument("--key", "-k", help="Groq API key (starts with gsk_...)")
    parser.add_argument("--write", "-w", action="store_true", help="Write changes directly back to the file (requires --file)")
    args = parser.parse_args()

    # Determine API key
    api_key = args.key or load_api_key()
    if not api_key:
        print("No GROQ_API_KEY found.")
        api_key = input("Enter your Groq API key (starts with gsk_...): ").strip()
        if not api_key:
            sys.exit("Error: Groq API key is required.")
        save = input("Save key to local .env file for future use? [y/N]: ").strip().lower()
        if save in ("y", "yes"):
            (ROOT / ".env").write_text(f"GROQ_API_KEY={api_key}\n", encoding="utf-8")
            print("Saved to .env (ignored by git).")

    # Read voice sample if provided
    sample_text = None
    if args.sample:
        sample_path = Path(args.sample)
        if sample_path.exists():
            sample_text = read_document(sample_path)
        else:
            sample_text = args.sample

    # File mode
    if args.file:
        target = Path(args.file)
        if not target.exists():
            sys.exit(f"Error: File '{args.file}' not found.")
        content = read_document(target)
        print(f"--- Humanizing file: {args.file} ---\n")
        output = run_humanizer(content, api_key=api_key, model=args.model, sample=sample_text, file_mode=True, stream=True)
        if args.output:
            Path(args.output).write_text(output, encoding="utf-8")
            print(f"\n[OK] Saved to {args.output}")
        elif args.write and target.suffix.lower() != ".docx":
            target.write_text(output, encoding="utf-8")
            print(f"\n[OK] Updated {args.file}")
        return

    # Direct text argument
    if args.text:
        run_humanizer(args.text, api_key=api_key, model=args.model, sample=sample_text, file_mode=False, stream=True)
        return

    # Interactive mode
    print("--- Humanizer (Interactive Mode via Groq) ---")
    print("Paste your text below. When done, press Enter, then Ctrl+Z (Windows) or Ctrl+D, then Enter:\n")
    try:
        input_lines = sys.stdin.read()
    except KeyboardInterrupt:
        sys.exit("\nCancelled.")

    if not input_lines.strip():
        sys.exit("No text provided.")

    print("\n--- Rewriting with Humanizer ---\n")
    run_humanizer(input_lines, api_key=api_key, model=args.model, sample=sample_text, file_mode=False, stream=True)


if __name__ == "__main__":
    main()
