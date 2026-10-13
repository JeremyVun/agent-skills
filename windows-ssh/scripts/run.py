#!/usr/bin/env python3
"""Run PowerShell or Python source on Windows through a verified SSH connection."""
import argparse
import base64
from pathlib import Path
import re
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--host', required=True)
    parser.add_argument('--file', type=Path, help='Source file; defaults to stdin')
    parser.add_argument('--python', help='Remote Python executable instead of PowerShell')
    parser.add_argument('--timeout', type=float, default=600)
    args = parser.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9_][A-Za-z0-9_.:@\[\]%-]*', args.host):
        parser.error('Expected an SSH hostname or user@hostname')
    if not 0 < args.timeout <= 600:
        parser.error('Use a timeout between 0 and 600 seconds; split longer work into resumable units')
    source = args.file.read_text(encoding='utf-8-sig') if args.file else sys.stdin.read()
    if not source.strip():
        parser.error('Source is empty')
    prelude = ("$ErrorActionPreference='Stop'; $ProgressPreference='SilentlyContinue'\n"
               "$OutputEncoding = [Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)\n")
    if args.python:
        executable = args.python.replace("'", "''")
        script = prelude + f"& '{executable}' -X utf8 -\nexit $LASTEXITCODE\n"
        remote_input = source.encode('utf-8')
    else:
        script = prelude + source
        remote_input = None
    encoded = base64.b64encode(script.encode('utf-16le')).decode('ascii')
    command = 'powershell -NoProfile -NonInteractive -EncodedCommand ' + encoded
    argv = ['ssh', '-o', 'BatchMode=yes', '-o', 'StrictHostKeyChecking=yes',
            '-o', 'ConnectTimeout=10', '-o', 'ServerAliveInterval=30',
            '-o', 'ServerAliveCountMax=3', args.host, command]
    try:
        return subprocess.run(argv, input=remote_input, timeout=args.timeout).returncode
    except subprocess.TimeoutExpired:
        print('SSH timed out. The remote process may still be running; inspect it before retrying.', file=sys.stderr)
        return 124


if __name__ == '__main__':
    raise SystemExit(main())
