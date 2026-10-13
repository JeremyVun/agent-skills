---
name: windows-ssh
description: Run commands, transfer files and manage experiments on a Windows machine over SSH. Use for work on Jeremy's Windows GPU server, Windows OpenSSH troubleshooting, or remote PowerShell/Python execution.
---

# Windows SSH

For Jeremy's GPU machine, read [the host reference](references/windows-host.md) for the verified identity, connection and runtime paths. The reference contains public connection facts, not credentials. Recheck runtime paths before relying on them after a software update.

## Connect and execute

- Use key-based authentication with `BatchMode=yes` and `StrictHostKeyChecking=yes`. The verified server key is already in the Mac's `known_hosts`. For a new client or changed key, compare the received fingerprint with one Jeremy obtained on Windows before trusting it; do not disable host checking or remove a mismatched entry automatically.
- Use [scripts/run.py](scripts/run.py) to avoid the quoting layers between the local shell, Windows SSH's default shell, PowerShell and native executables. It encodes PowerShell as UTF-16LE and can send Python source over stdin. It does not write a remote script, install anything or elevate permissions.

```sh
python3 /path/to/windows-ssh/scripts/run.py --host user@hostname --file task.ps1
python3 /path/to/windows-ssh/scripts/run.py --host user@hostname --python 'C:\path\python.exe' --file experiment.py
```

Omit `--file` to read the script from stdin. Native commands inside a PowerShell script need explicit failure handling, for example `if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }`. The Python mode propagates its interpreter's exit code. Avoid nested `python -c` quotes: Windows PowerShell 5.1 can strip quotes even when the outer PowerShell command is encoded.

Use `scp -o BatchMode=yes -o StrictHostKeyChecking=yes source user@host:relative/path` or SFTP for files. Relative remote paths resolve inside the Windows user profile; use a dedicated task directory, verify checksums, and read existing files before changing them. Never copy private keys or secrets into a skill, repository, transcript or command output.

## Shared machine and long work

- Access is a capability, not blanket authorization to change services or applications. Follow the current task's scope and applicable repository instructions.
- Inspect the active workload before GPU inference. A separate CLI process bypasses ComfyUI's queue and can contend with generation. Serialize GPU work through an existing supported mechanism, or arrange an idle maintenance window before using a separate runner; do not kill or interrupt someone else's job.
- Keep experimental packages and model downloads in a separate environment/cache. Preserve the application's Python, CUDA packages, installed nodes and audio unless the task authorizes changing them. Inspect actual interpreter/package versions rather than assuming `python` on PATH is the application's interpreter.
- Run checks in the foreground, split long batches into resumable units, and save results/attempt identifiers on Windows. An SSH disconnect or local timeout does not establish that the remote process stopped: inspect its state before resubmitting a job with side effects.

## Troubleshoot the boundary that failed

- Timeout before a host key: check hostname/IP, service/listener and firewall profile. If another service works at that address, narrow the investigation to SSH.
- Host-key mismatch: stop authentication and verify the new fingerprint with Jeremy.
- `Permission denied (publickey)`: check Windows username and authorized-key location/ACL; administrator accounts use the shared administrators file in the default configuration, ordinary accounts use their profile's `.ssh/authorized_keys`.
- When asking Jeremy to paste multiple PowerShell commands, use a single line with semicolons: this chat's copy path can collapse newlines.

Authoritative setup details: [Windows OpenSSH](https://learn.microsoft.com/en-us/windows-server/administration/openssh/openssh_install_firstuse) and [key management](https://learn.microsoft.com/en-us/windows-server/administration/openssh/openssh_keymanagement). Keep SSH scoped to the intended network; setting up LAN access does not require opening a router port.
