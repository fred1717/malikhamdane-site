"""
Build script for malikhamdane.com

Processes the site source files before deployment:
- Reads the header template from site/includes/header.html
- Replaces {{HEADER}} in each HTML file with the
  processed header (correct language marked as active)
- Copies the processed files to a build output directory
- Excludes the includes/ directory from the output

Usage:
    python scripts/build.py
"""

import os
import shutil

SITE_DIR = os.path.join("site")
BUILD_DIR = os.path.join("build")
INCLUDES_DIR = os.path.join(SITE_DIR, "includes")
HEADER_FILE = os.path.join(INCLUDES_DIR, "header.html")

SUPPORTED_LANGUAGES = ["fr", "en", "de", "es", "pt", "ru"]
HEADER_PLACEHOLDER = "{{HEADER}}"
ACTIVE_CLASS = 'class="active"'


def read_header_template():
    with open(HEADER_FILE, "r", encoding="utf-8") as f:
        return f.read()


def detect_language(filepath):
    relative = os.path.relpath(filepath, SITE_DIR)
    parts = relative.split(os.sep)
    if len(parts) > 1 and parts[0] in SUPPORTED_LANGUAGES:
        return parts[0]
    return None


def process_header(template, language):
    processed = template
    for lang in SUPPORTED_LANGUAGES:
        placeholder = "{{ACTIVE_" + lang.upper() + "}}"
        if lang == language:
            processed = processed.replace(placeholder, ACTIVE_CLASS)
        else:
            processed = processed.replace(placeholder, "")
    return processed


def process_file(filepath, header_template):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    if HEADER_PLACEHOLDER not in content:
        return content

    language = detect_language(filepath)
    header = process_header(header_template, language)
    content = content.replace(HEADER_PLACEHOLDER, header)
    return content


def build():
    if os.path.exists(BUILD_DIR):
        shutil.rmtree(BUILD_DIR)

    header_template = read_header_template()

    for root, dirs, files in os.walk(SITE_DIR):
        relative_root = os.path.relpath(root, SITE_DIR)

        if relative_root.startswith("includes"):
            continue

        output_root = os.path.join(BUILD_DIR, relative_root)
        os.makedirs(output_root, exist_ok=True)

        for filename in files:
            source_path = os.path.join(root, filename)
            output_path = os.path.join(output_root, filename)

            if filename.endswith(".html"):
                content = process_file(source_path, header_template)
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(content)
            else:
                shutil.copy2(source_path, output_path)


if __name__ == "__main__":
    build()
    print("Build complete. Output in: " + BUILD_DIR)
