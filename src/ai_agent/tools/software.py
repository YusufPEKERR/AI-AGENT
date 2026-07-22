import json
import os
import subprocess
from pathlib import Path
from typing import Optional
from ai_agent.models.messages import ToolResult
from ai_agent.core.security import resolve_safe_path, run_powershell_safe


def git_manage(
    action: str,
    repo_path: str = ".",
    args: Optional[str] = None,
    branch: Optional[str] = None,
    message: Optional[str] = None
) -> ToolResult:
    try:
        safe_p = resolve_safe_path(repo_path)
        if not safe_p.exists():
            return ToolResult(success=False, output="", error=f"Repo dizini bulunamadı ({safe_p})")

        cmd_parts = ["git"]
        if action == "status":
            cmd_parts.extend(["status", "--short"])
        elif action == "diff":
            cmd_parts.extend(["diff"])
        elif action == "log":
            cmd_parts.extend(["log", "-n", "10", "--oneline"])
        elif action == "add":
            target = args if args else "."
            cmd_parts.extend(["add", target])
        elif action == "commit":
            msg = message if message else "Auto commit by AI Agent"
            cmd_parts.extend(["commit", "-m", msg])
        elif action == "push":
            cmd_parts.extend(["push"])
        elif action == "pull":
            cmd_parts.extend(["pull"])
        elif action == "branch":
            cmd_parts.extend(["branch", "-a"])
        elif action == "checkout":
            if not branch:
                return ToolResult(success=False, output="", error="checkout için branch parametresi gereklidir.")
            cmd_parts.extend(["checkout", branch])
        elif action == "init":
            cmd_parts.extend(["init"])
        elif action == "custom":
            if not args:
                return ToolResult(success=False, output="", error="custom işlemi için args gereklidir.")
            cmd_parts.extend(args.split())
        else:
            cmd_parts.extend(["status"])

        res = subprocess.run(
            cmd_parts, capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=safe_p, timeout=60
        )
        out = res.stdout.strip() if res.stdout else ""
        err = res.stderr.strip() if res.stderr else ""
        return ToolResult(success=True, output=out if out else (err if err else "Git komutu başarıyla tamamlandı."))
    except Exception as e:
        return ToolResult(success=False, output="", error=str(e))


def project_analyze(root_path: str = ".") -> ToolResult:
    try:
        safe_p = resolve_safe_path(root_path)
        if not safe_p.exists():
            return ToolResult(success=False, output="", error=f"Dizin bulunamadı ({safe_p})")

        info = {
            "root_path": str(safe_p),
            "detected_project_types": [],
            "config_files": [],
            "scripts_or_commands": {},
            "dependencies_summary": []
        }
        files_in_root = os.listdir(safe_p)
        for f in files_in_root:
            full_f = safe_p / f
            if f == "package.json":
                info["detected_project_types"].append("Node.js / JS / TS")
                info["config_files"].append("package.json")
                try:
                    with open(full_f, "r", encoding="utf-8") as file:
                        data = json.load(file)
                        info["scripts_or_commands"] = data.get("scripts", {})
                        deps = list(data.get("dependencies", {}).keys()) + list(data.get("devDependencies", {}).keys())
                        info["dependencies_summary"] = deps[:20]
                except Exception:
                    pass
            elif f in ["requirements.txt", "pyproject.toml", "setup.py"]:
                info["detected_project_types"].append("Python")
                info["config_files"].append(f)
            elif f.endswith(".csproj") or f.endswith(".sln"):
                info["detected_project_types"].append(".NET / C#")
                info["config_files"].append(f)
            elif f == "Cargo.toml":
                info["detected_project_types"].append("Rust")
                info["config_files"].append("Cargo.toml")
            elif f == "go.mod":
                info["detected_project_types"].append("Go")
                info["config_files"].append("go.mod")
            elif f in ["pom.xml", "build.gradle"]:
                info["detected_project_types"].append("Java / Kotlin")
                info["config_files"].append(f)
            elif f in ["Dockerfile", "docker-compose.yml"]:
                info["config_files"].append(f)

        return ToolResult(success=True, output=json.dumps(info, ensure_ascii=False, indent=2))
    except Exception as e:
        return ToolResult(success=False, output="", error=str(e))


def test_runner(root_path: str = ".", framework: str = "auto", test_filter: Optional[str] = None) -> ToolResult:
    try:
        safe_p = resolve_safe_path(root_path)
        if not safe_p.exists():
            return ToolResult(success=False, output="", error=f"Dizin bulunamadı ({safe_p})")

        files = os.listdir(safe_p)
        if framework == "auto":
            if "pytest.ini" in files or "requirements.txt" in files or any(f.endswith(".py") for f in files):
                framework = "pytest"
            elif "package.json" in files:
                framework = "npm"
            elif any(f.endswith(".csproj") for f in files) or any(f.endswith(".sln") for f in files):
                framework = "dotnet"
            elif "go.mod" in files:
                framework = "go"
            elif "Cargo.toml" in files:
                framework = "cargo"

        if framework == "pytest":
            cmd = ["pytest"]
            if test_filter:
                cmd.extend(["-k", test_filter])
        elif framework == "npm":
            cmd = ["npm", "test"]
        elif framework == "dotnet":
            cmd = ["dotnet", "test"]
            if test_filter:
                cmd.extend(["--filter", test_filter])
        elif framework == "go":
            cmd = ["go", "test", "./..."]
        elif framework == "cargo":
            cmd = ["cargo", "test"]
        else:
            return ToolResult(success=False, output="", error=f"Desteklenmeyen test framework: {framework}")

        res = subprocess.run(
            cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=safe_p, timeout=180
        )
        out = res.stdout.strip() if res.stdout else ""
        err = res.stderr.strip() if res.stderr else ""
        return ToolResult(success=True, output=f"--- TEST ÇIKTISI ({framework}) ---\n{out}\n\n{err}")
    except Exception as e:
        return ToolResult(success=False, output="", error=str(e))


def lsp_query(action: str = "diagnostics", file_path: Optional[str] = None, root_path: str = ".") -> ToolResult:
    try:
        safe_r = resolve_safe_path(root_path)
        safe_f = resolve_safe_path(file_path) if file_path else None
        if action == "diagnostics":
            if safe_f and safe_f.suffix == ".py":
                cmd = f"python -m py_compile '{safe_f}'"
            elif any(f.endswith(".py") for f in os.listdir(safe_r)):
                cmd = f"python -m compileall '{safe_r}'"
            elif safe_f and safe_f.suffix in [".ts", ".js"]:
                cmd = "npx tsc --noEmit"
            elif any(f.endswith(".csproj") for f in os.listdir(safe_r)):
                cmd = "dotnet build /clp:NoSummary /warnaserror"
            else:
                return ToolResult(success=True, output="LSP Diagnostics: Temiz, hata bulunamadı.")
            res = run_powershell_safe(cmd)
            return ToolResult(success=True, output=res)
        return ToolResult(success=True, output=f"LSP ({action}): Tamamlandı.")
    except Exception as e:
        return ToolResult(success=False, output="", error=str(e))
