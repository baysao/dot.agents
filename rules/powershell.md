# PowerShell Windows Execution Rule

## Target

- OS: Windows
- Shell: `pwsh` always. Fallback `powershell.exe` if `pwsh` missing.

## Command pattern

- Prefer: `pwsh -c <command>` (no quotes for simple).
- Single-step: never wrap whole `pwsh -c` in double quotes.
  - Example:
  - `pwsh -c git status`
  - `pwsh -c python -m venv .venv`
  - `pwsh -c pip install -r requirements.txt`
- Multi-part (`&&`, `>`, `|`): wrap expression in double quotes:
  - `pwsh -c "python script.py > log.txt"`
  - `pwsh -c "Get-Content log.txt | Select-Object -First 10"`

## Path and escaping

- Use backslash: `.\venv\Scripts\python.exe`.
- Space in path → wrap path in single quotes:
  - `pwsh -c python 'my folder\script.py'`
- Avoid forward-slash paths. Normalize to Windows style.

## Security and restrictions

- NEVER:
  - `rm -rf`, `format`, `del C:\*.*`, raw disk format.
  - `Start-Process` / `Invoke-WebRequest` + untrusted URL without confirm.
- Need human approval:
  - `Remove-Item -Recurse -Force` on large folders.
  - `Start-Job` / background process hard to kill.
- No long-running services (`runserver`) autonomously. Ask user.

## Behavior rules

- Always use PowerShell. No bash/sh unless project rule.
- Command fail → use PS native (`Get-ChildItem`, `Test-Path`) over Unix tools (`ls`, `wc`).
- Log external commands. No silent execution unless override.

## Deny list (never run automatically)

- Start with: `rm -rf`, `sudo rm -rf`, `format`, `cipher /w`.
- `powershell -c` / `cmd /c` delete `%ProgramFiles%`, `%SystemRoot%`, `Documents` without approval.
- `Start-Process` suppress UI / silent background without confirm.
