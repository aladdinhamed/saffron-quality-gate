#!/usr/bin/env python3
"""Build the SQG distribution package (sdist + wheel)."""
import subprocess, sys
from pathlib import Path

HERE = Path(__file__).parent

def main():
    print("=== Building SQG distribution ===")
    subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "build"], cwd=HERE)
    subprocess.run([sys.executable, "-m", "build"], cwd=HERE)
    print(f"\n✅ Built. Files in {HERE/'dist/'}:")
    for f in sorted(HERE.glob("dist/*")):
        print(f"  {f.name} ({f.stat().st_size / 1024:.1f} KB)")
    print("\nUpload: python3 publish.py")

if __name__ == "__main__":
    main()