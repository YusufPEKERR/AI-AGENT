import os
import shutil
import fnmatch
import time
import subprocess
from pathlib import Path
from typing import Any, Optional
from ai_agent.models.messages import ToolResult
from ai_agent.core.security import resolve_safe_path, run_powershell_safe


def write_file(filepath: str, content: str, append: bool = False) -> ToolResult:
    try:
        path = resolve_safe_path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        mode = "a" if append else "w"
        with open(path, mode, encoding="utf-8") as f:
            f.write(content)
        return ToolResult(success=True, output=f"Başarılı: '{path}' dosyası yazıldı.")
    except Exception as e:
        return ToolResult(success=False, output="", error=str(e))


def read_file(filepath: str) -> ToolResult:
    try:
        path = resolve_safe_path(filepath)
        if not path.exists():
            return ToolResult(success=False, output="", error=f"Dosya bulunamadı ({path})")
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return ToolResult(success=True, output=f.read())
    except Exception as e:
        return ToolResult(success=False, output="", error=str(e))


def list_directory(path: str = ".") -> ToolResult:
    try:
        safe_p = resolve_safe_path(path)
        if not safe_p.exists():
            return ToolResult(success=False, output="", error=f"Dizin bulunamadı ({safe_p})")
        items = os.listdir(safe_p)
        formatted = [f"{item}/" if (safe_p / item).is_dir() else item for item in items]
        return ToolResult(success=True, output=f"Dizin içeriği ({safe_p}): {formatted}")
    except Exception as e:
        return ToolResult(success=False, output="", error=str(e))


def copy_move_delete(operation: str, source: str, destination: Optional[str] = None) -> ToolResult:
    try:
        src = resolve_safe_path(source)
        dest = resolve_safe_path(destination) if destination else None
        if operation == "delete":
            if src.is_dir():
                shutil.rmtree(src)
            else:
                src.unlink(missing_ok=True)
            return ToolResult(success=True, output=f"Silindi: {src}")
        elif operation == "copy":
            if not dest:
                return ToolResult(success=False, output="", error="Kopyalama için hedef (destination) gerekli.")
            if src.is_dir():
                shutil.copytree(src, dest, dirs_exist_ok=True)
            else:
                shutil.copy2(src, dest)
            return ToolResult(success=True, output=f"Kopyalandı: {src} -> {dest}")
        elif operation == "move":
            if not dest:
                return ToolResult(success=False, output="", error="Taşıma için hedef (destination) gerekli.")
            shutil.move(src, dest)
            return ToolResult(success=True, output=f"Taşındı: {src} -> {dest}")
        return ToolResult(success=False, output="", error=f"Bilinmeyen işlem: {operation}")
    except Exception as e:
        return ToolResult(success=False, output="", error=str(e))


def search_files(path: str = ".", pattern: Optional[str] = None, content_pattern: Optional[str] = None) -> ToolResult:
    try:
        safe_p = resolve_safe_path(path)
        if not safe_p.exists():
            return ToolResult(success=False, output="", error=f"Dizin bulunamadı ({safe_p})")
        matches = []
        for root, dirs, files in os.walk(safe_p):
            for file in files:
                if pattern and not fnmatch.fnmatch(file, pattern):
                    continue
                full_p = Path(root) / file
                if content_pattern:
                    try:
                        with open(full_p, "r", encoding="utf-8", errors="ignore") as f:
                            text = f.read()
                            if content_pattern.lower() in text.lower():
                                matches.append(str(full_p))
                    except Exception:
                        pass
                else:
                    matches.append(str(full_p))
                if len(matches) >= 50:
                    break
            if len(matches) >= 50:
                break
        return ToolResult(success=True, output=f"Bulunan dosyalar ({len(matches)} adet):\n" + "\n".join(matches))
    except Exception as e:
        return ToolResult(success=False, output="", error=str(e))


def code_edit(edits: list[dict[str, Any]]) -> ToolResult:
    try:
        results = []
        for item in edits:
            fp = item.get("filepath", "")
            target = item.get("target_content")
            replacement = item.get("replacement_content", "")
            safe_p = resolve_safe_path(fp)
            if not safe_p.exists():
                safe_p.parent.mkdir(parents=True, exist_ok=True)
                with open(safe_p, "w", encoding="utf-8") as f:
                    f.write(replacement)
                results.append(f"Oluşturuldu: {safe_p}")
                continue

            with open(safe_p, "r", encoding="utf-8", errors="replace") as f:
                text = f.read()

            if target and target in text:
                new_text = text.replace(target, replacement, 1)
                with open(safe_p, "w", encoding="utf-8") as f:
                    f.write(new_text)
                results.append(f"Güncellendi: {safe_p}")
            elif not target:
                with open(safe_p, "w", encoding="utf-8") as f:
                    f.write(replacement)
                results.append(f"Yeniden yazıldı: {safe_p}")
            else:
                results.append(f"Hedef metin bulunamadı ({safe_p})")

        return ToolResult(success=True, output="\n".join(results))
    except Exception as e:
        return ToolResult(success=False, output="", error=str(e))


def patch_apply(patch_content: str, root_path: str = ".") -> ToolResult:
    try:
        safe_p = resolve_safe_path(root_path)
        patch_file = safe_p / "_temp_agent.patch"
        with open(patch_file, "w", encoding="utf-8") as f:
            f.write(patch_content)
        cmd = f"git apply --check '{patch_file}'; if ($?) {{ git apply '{patch_file}'; Remove-Item '{patch_file}' }}"
        res = run_powershell_safe(cmd)
        if patch_file.exists():
            patch_file.unlink(missing_ok=True)
        return ToolResult(success=True, output=res)
    except Exception as e:
        return ToolResult(success=False, output="", error=str(e))


def symbol_search(query: str, path: str = ".") -> ToolResult:
    try:
        safe_p = resolve_safe_path(path)
        matches = []
        for root, dirs, files in os.walk(safe_p):
            for file in files:
                if file.endswith((".py", ".js", ".ts", ".cs", ".go", ".rs", ".java", ".cpp", ".h")):
                    full_p = Path(root) / file
                    try:
                        with open(full_p, "r", encoding="utf-8", errors="ignore") as f:
                            for i, line in enumerate(f.readlines(), 1):
                                if query.lower() in line.lower() and any(k in line for k in ["def ", "class ", "function ", "struct ", "enum ", "interface "]):
                                    matches.append(f"{full_p}:{i} -> {line.strip()}")
                    except Exception:
                        pass
                if len(matches) >= 50:
                    break
            if len(matches) >= 50:
                break
        return ToolResult(success=True, output=f"Semboller ({len(matches)} adet):\n" + "\n".join(matches))
    except Exception as e:
        return ToolResult(success=False, output="", error=str(e))


def code_format(filepath: str, formatter: str = "auto") -> ToolResult:
    try:
        safe_p = resolve_safe_path(filepath)
        if not safe_p.exists():
            return ToolResult(success=False, output="", error=f"Dosya bulunamadı ({safe_p})")

        if formatter == "auto":
            if safe_p.suffix == ".py":
                formatter = "black"
            elif safe_p.suffix in [".js", ".ts", ".json", ".html", ".css"]:
                formatter = "prettier"
            elif safe_p.suffix == ".go":
                formatter = "gofmt"
            elif safe_p.suffix == ".rs":
                formatter = "rustfmt"

        if formatter == "black":
            cmd = f"python -m black '{safe_p}'"
        elif formatter == "prettier":
            cmd = f"npx prettier --write '{safe_p}'"
        elif formatter == "gofmt":
            cmd = f"gofmt -w '{safe_p}'"
        elif formatter == "rustfmt":
            cmd = f"rustfmt '{safe_p}'"
        else:
            return ToolResult(success=False, output="", error=f"Desteklenmeyen formatlayıcı: {formatter}")

        out = run_powershell_safe(cmd)
        return ToolResult(success=True, output=out)
    except Exception as e:
        return ToolResult(success=False, output="", error=str(e))


def file_watch(path: str, check_seconds: int = 2) -> ToolResult:
    try:
        safe_p = resolve_safe_path(path)
        if not safe_p.exists():
            return ToolResult(success=False, output="", error=f"Yol bulunamadı ({safe_p})")
        mtime = safe_p.stat().st_mtime
        time.sleep(check_seconds)
        new_mtime = safe_p.stat().st_mtime
        if new_mtime != mtime:
            return ToolResult(success=True, output=f"Değişiklik var: {safe_p}")
        return ToolResult(success=True, output=f"Değişiklik yok ({safe_p})")
    except Exception as e:
        return ToolResult(success=False, output="", error=str(e))
