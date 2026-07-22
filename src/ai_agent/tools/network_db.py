import json
import sqlite3
import urllib.request
import urllib.parse
from typing import Any, Optional
from ai_agent.models.messages import ToolResult
from ai_agent.core.security import resolve_safe_path


def http_request(
    url: str,
    method: str = "GET",
    headers: Optional[dict[str, Any]] = None,
    data: Optional[str] = None
) -> ToolResult:
    try:
        req = urllib.request.Request(url, method=method.upper())
        if headers:
            for k, v in headers.items():
                req.add_header(k, str(v))
        body = data.encode("utf-8") if data else None
        with urllib.request.urlopen(req, data=body, timeout=30) as resp:
            content = resp.read().decode("utf-8", errors="replace")
            return ToolResult(success=True, output=f"HTTP {resp.status}:\n{content[:4000]}")
    except Exception as e:
        return ToolResult(success=False, output="", error=f"HTTP İsteği Hatası: {str(e)}")


def db_query(db_type: str, query: str, db_path_or_conn: str) -> ToolResult:
    try:
        if db_type == "sqlite":
            safe_db = resolve_safe_path(db_path_or_conn)
            conn = sqlite3.connect(safe_db)
            cursor = conn.cursor()
            cursor.execute(query)
            q_clean = query.strip().lower()
            if q_clean.startswith("select") or q_clean.startswith("pragma"):
                rows = cursor.fetchall()
                cols = [desc[0] for desc in cursor.description] if cursor.description else []
                conn.close()
                output_str = json.dumps({"columns": cols, "rows": rows}, ensure_ascii=False, indent=2)
                return ToolResult(success=True, output=output_str)
            else:
                conn.commit()
                conn.close()
                return ToolResult(success=True, output="Sorgu başarıyla çalıştırıldı ve kaydedildi.")
        return ToolResult(success=False, output="", error=f"Desteklenmeyen veritabanı tipi: {db_type}")
    except Exception as e:
        return ToolResult(success=False, output="", error=str(e))
