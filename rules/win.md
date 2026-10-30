
# Windows + MSYS2 Rules for AI Agents

## Shell & environment
- Prefer MSYS2 UCRT64 (`C:\msys64\usr\bin\bash.exe`) for Unix-like commands.
- Do not assume Linux paths. Convert paths explicitly:
  - Windows → Unix: `cygpath -u "C:\projects\app"`
  - Unix → Windows: `cygpath -w "/c/projects/app"`
- Use `/c/...` instead of `C:\...` inside Bash commands.
- Quote every path containing spaces.
- Do not run `sudo`; Windows/MSYS2 does not use it.

## Commands
- Use `pacman` only inside an MSYS2 shell.
- Before installing packages, run:
  `pacman -Syu`
- For build tools, prefer the matching environment:
  - UCRT64: `C:\msys64\ucrt64.exe`
  - CLANG64: `C:\msys64\clang64.exe`
  - MSYS: `C:\msys64\msys2.exe`
- Do not mix MinGW and MSVC build outputs in the same project without cleaning first.

## Encoding
- Force UTF-8 when running Python or Node scripts:
  - Python: `PYTHONUTF8=1`
  - Node: `NODE_OPTIONS=--input-type=module` only when appropriate
- If terminal output is garbled, check Windows code page and use:
  `chcp.com 65001`
- Avoid non-ASCII filenames unless the project already uses them.

## AI agent behavior
- Before executing a long build, test the exact compiler/toolchain with a minimal command.
- If a command fails due to path conversion, encoding, or missing DLLs, diagnose the shell environment first.
- Never modify `C:\msys64` system files unless explicitly requested.
- Prefer project-local dependencies and virtual environments over global installs.
- For Windows-native programs, use Windows paths; for MSYS2/Git Bash commands, use POSIX paths.

## RTK integration
- Use RTK to reduce terminal output before it enters the AI context.
- If `rtk` is available on PATH, prefer RTK-wrapped commands for noisy operations:
  - `rtk git status`
  - `rtk git diff`
  - `rtk git log`
  - `rtk cargo test`
  - `rtk pytest`
  - `rtk pnpm list`
  - `rtk docker ps`
  - `rtk kubectl get pods`
- Do not wrap commands that require interactive input, authentication prompts, or direct TTY behavior.
- For commands not supported by RTK, run them normally; do not force `rtk` prefixes.
- If an RTK hook is installed, let it rewrite supported commands automatically; do not manually duplicate the rewrite.
- If RTK output appears truncated or filtered, rerun the underlying command directly only when debugging the command itself.

## Windows + MSYS2 + RTK
- Install RTK natively on Windows; do not require WSL, Bash, or `jq` for its hook.
- Recommended install:
  ```powershell
  winget install rtk-ai.rtk
  rtk init -g
  ```
- Ensure `rtk.exe` is on the Windows `PATH`, for example:
  `C:\Users\<you>\.local\bin`
- RTK hooks work in PowerShell, CMD, and Windows Terminal; MSYS2/Git Bash commands should still use POSIX paths such as `/c/projects/app`.
- After changing RTK configuration or installing a hook, restart the AI coding agent.
- Verify integration with:
  ```bash
  rtk --version
  rtk gain
  ```
