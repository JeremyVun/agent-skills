# Jeremy's Windows GPU host

Verified on 2026-10-13 from Jeremy's Mac. This host is shared across projects.

| Item | Value |
| --- | --- |
| SSH target | `jeremy@win` |
| Windows identity | `desktop-4d4rjn3\jeremy` |
| LAN IPv4 at verification | `192.168.50.121` |
| Alternative discovery name | `desktop-4d4rjn3.local` |
| Port | `22` |
| ED25519 host fingerprint | `SHA256:Erbo4oPLbV0gxZc47kCFFj9b4k24bqOThoIOF9Sz8Do` |
| Mac key | Existing `~/.ssh/id_ed25519`, available through the SSH agent |
| Windows SSH service | `sshd`, running; automatic startup was configured |
| Firewall | `OpenSSH-Server-In-TCP`, enabled, all profiles, `RemoteAddress LocalSubnet` |

The host key was scanned, compared with the fingerprint Jeremy supplied from Windows, then appended to `~/.ssh/known_hosts`. Strict noninteractive login returned the identity above. A new machine still needs Jeremy to authorize its own public key; the skill contains no transferable credentials.

Quick check:

```sh
ssh -o BatchMode=yes -o StrictHostKeyChecking=yes -o ConnectTimeout=5 jeremy@win whoami
```

If SSH times out, Jeremy can run this single line in administrator PowerShell:

```powershell
Start-Service sshd; Set-NetFirewallRule -Name OpenSSH-Server-In-TCP -Enabled True -Profile Any -RemoteAddress LocalSubnet; Get-Service sshd
```

The local-subnet rule requires a reachable LAN path. Do not expand it to the internet to fix a remote connection.

## GPU and ComfyUI discovery

- NVIDIA RTX 4070 SUPER, 12 GB VRAM.
- ComfyUI listens at `http://win:8188`. Read `/queue` before GPU work; `/system_stats` reports current Python/PyTorch versions, arguments and memory. These endpoints are for LAN use.
- ComfyUI code root at verification: `C:\Users\Jeremy\AppData\Local\Comfy-Desktop\ComfyUI-Installs\ComfyUI\ComfyUI`.
- Application Python: `<code root>\.venv\Scripts\python.exe`.
- Base interpreter: `C:\Users\Jeremy\AppData\Local\Comfy-Desktop\ComfyUI-Installs\ComfyUI\standalone-env\python.exe`.
- Shared input/output: `C:\Users\Jeremy\AppData\Local\Comfy-Desktop\ComfyUI-Shared\input` and `output`.
- Observed versions: Python 3.13.12, PyTorch 2.12.1+cu130. Treat these as discovery hints, not installation requirements.

To rediscover interpreter paths without dumping process arguments or environments:

```powershell
Get-CimInstance Win32_Process | Where-Object { $_.Name -match '^python(w)?\.exe$' } | Select-Object ProcessId,ExecutablePath
```

Keep project-specific worker controls, model recipes and deployment rules in that project's own docs. Do not infer that an empty ComfyUI queue reserves the GPU against a new submission.
