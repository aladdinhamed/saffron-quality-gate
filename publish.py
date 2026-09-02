#!/usr/bin/env python3
"""Build and publish SQG to PyPI. Usage: python3 publish.py [--dry-run]"""
import os, subprocess, sys
from pathlib import Path

HERE = Path(__file__).parent

def run(cmd, **kw):
    print(f"  $ {' '.join(cmd)}")
    r = subprocess.run(cmd, cwd=kw.pop("cwd", HERE), capture_output=True, text=True, **kw)
    if r.returncode != 0:
        print(f"  FAILED: {r.stderr[:300]}")
        sys.exit(1)
    return r.stdout.strip()

def main():
    dry_run = "--dry-run" in sys.argv

    print("=== SQG PyPI Publisher ===\n")

    # 1. Build
    print("1. Building distribution...")
    run([sys.executable, "-m", "pip", "install", "--upgrade", "build", "twine"])
    run([sys.executable, "-m", "build"])
    print("   ✅ Built\n")

    # 2. Check
    print("2. Checking distribution...")
    check_out = run([sys.executable, "-m", "twine", "check", "dist/*"])
    print(f"   {check_out}\n")

    if dry_run:
        print("=== DRY RUN — skipping upload ===")
        print(f"   Files ready: {list(Path('dist').glob('*'))}")
        sys.exit(0)

    # 3. Upload
    print("3. Uploading to PyPI...")
    username = os.environ.get("PYPI_USERNAME", "__token__")
    password = os.environ.get("PYPI_PASSWORD", "")
    if not password:
        print("   ❌ PYPI_PASSWORD not set. Set it or use --dry-run")
        sys.exit(1)
    run([sys.executable, "-m", "twine", "upload", "--username", username, "--password", password, "dist/*"])
    print("   ✅ Published to PyPI!\n")

    print("=== Done ===")
    print(f"   pip install saffron-quality-gate")


if __name__ == "__main__":
    main()