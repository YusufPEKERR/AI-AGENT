from typing import Any, Callable
from ai_agent.tools.base import BaseTool
from ai_agent.models.messages import ToolResult

from ai_agent.tools.filesystem import (
    write_file, read_file, list_directory, copy_move_delete,
    search_files, code_edit, patch_apply, symbol_search, code_format, file_watch
)
from ai_agent.tools.software import git_manage, project_analyze, test_runner, lsp_query
from ai_agent.tools.container import docker_manage, k8s_manage
from ai_agent.tools.system import execute_command, get_process_list, kill_process, manage_service
from ai_agent.tools.remote import (
    invoke_remote_command, create_pssession, copy_to_remote, copy_from_remote, test_connection
)
from ai_agent.tools.windows_adv import (
    registry_read_write, wmi_query, event_log_query, scheduled_task_manage
)
from ai_agent.tools.network_db import http_request, db_query


RAW_TOOLS_DEFINITIONS: list[dict[str, Any]] = [
    # 1. Filesystem
    {
        "name": "write_file",
        "description": "Bilgisayarda belirtilen dosya yoluna içerik yazar veya yeni dosya oluşturur.",
        "handler": write_file,
        "parameters": {
            "type": "object",
            "properties": {
                "filepath": {"type": "string"},
                "content": {"type": "string"},
                "append": {"type": "boolean", "default": False}
            },
            "required": ["filepath", "content"]
        }
    },
    {
        "name": "read_file",
        "description": "Dosya içeriğini okur.",
        "handler": read_file,
        "parameters": {
            "type": "object",
            "properties": {"filepath": {"type": "string"}},
            "required": ["filepath"]
        }
    },
    {
        "name": "list_directory",
        "description": "Dizindeki dosya ve klasörleri listeler.",
        "handler": list_directory,
        "parameters": {
            "type": "object",
            "properties": {"path": {"type": "string", "default": "."}}
        }
    },
    {
        "name": "copy_move_delete",
        "description": "Dosya veya klasör kopyalama, taşıma veya silme işlemi gerçekleştirir.",
        "handler": copy_move_delete,
        "parameters": {
            "type": "object",
            "properties": {
                "operation": {"type": "string", "enum": ["copy", "move", "delete"]},
                "source": {"type": "string"},
                "destination": {"type": "string"}
            },
            "required": ["operation", "source"]
        }
    },
    {
        "name": "search_files",
        "description": "İçerik veya isim ile dosya araması yapar.",
        "handler": search_files,
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "default": "."},
                "pattern": {"type": "string"},
                "content_pattern": {"type": "string"}
            },
            "required": ["path"]
        }
    },
    {
        "name": "code_edit",
        "description": "Birden fazla dosyada parçalı (target-replacement) kod düzenlemesi veya yazımı yapar.",
        "handler": code_edit,
        "parameters": {
            "type": "object",
            "properties": {
                "edits": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "filepath": {"type": "string"},
                            "target_content": {"type": "string"},
                            "replacement_content": {"type": "string"}
                        },
                        "required": ["filepath", "replacement_content"]
                    }
                }
            },
            "required": ["edits"]
        }
    },
    {
        "name": "patch_apply",
        "description": "Unified diff formatındaki bir patch'i projeye atomik olarak uygular.",
        "handler": patch_apply,
        "parameters": {
            "type": "object",
            "properties": {
                "patch_content": {"type": "string"},
                "root_path": {"type": "string", "default": "."}
            },
            "required": ["patch_content"]
        }
    },
    {
        "name": "symbol_search",
        "description": "Projedeki sınıflar, fonksiyonlar, metotlar veya semboller üzerinde arama yapar.",
        "handler": symbol_search,
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "default": "."},
                "query": {"type": "string"}
            },
            "required": ["query"]
        }
    },
    {
        "name": "code_format",
        "description": "Kod dosyalarını formatlar (black, prettier, gofmt, rustfmt).",
        "handler": code_format,
        "parameters": {
            "type": "object",
            "properties": {
                "filepath": {"type": "string"},
                "formatter": {"type": "string", "enum": ["auto", "black", "prettier", "gofmt", "rustfmt"], "default": "auto"}
            },
            "required": ["filepath"]
        }
    },
    {
        "name": "file_watch",
        "description": "Bir dosya veya klasörün değişip değişmediğini izler.",
        "handler": file_watch,
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "check_seconds": {"type": "integer", "default": 2}
            },
            "required": ["path"]
        }
    },

    # 2. Software & Git & LSP
    {
        "name": "git_manage",
        "description": "Git versiyon kontrol işlemlerini çalıştırır.",
        "handler": git_manage,
        "parameters": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "enum": ["status", "diff", "log", "add", "commit", "push", "pull", "branch", "checkout", "init", "custom"]},
                "repo_path": {"type": "string", "default": "."},
                "args": {"type": "string"},
                "branch": {"type": "string"},
                "message": {"type": "string"}
            },
            "required": ["action"]
        }
    },
    {
        "name": "project_analyze",
        "description": "Proje yapısını, bağımlılık dosyalarını (package.json, csproj vb.) detaylı analiz eder.",
        "handler": project_analyze,
        "parameters": {
            "type": "object",
            "properties": {"root_path": {"type": "string", "default": "."}}
        }
    },
    {
        "name": "test_runner",
        "description": "Otomatik bir şekilde testleri çalıştırır ve sonuçları raporlar.",
        "handler": test_runner,
        "parameters": {
            "type": "object",
            "properties": {
                "root_path": {"type": "string", "default": "."},
                "framework": {"type": "string", "enum": ["auto", "pytest", "npm", "dotnet", "go", "cargo"], "default": "auto"},
                "test_filter": {"type": "string"}
            }
        }
    },
    {
        "name": "lsp_query",
        "description": "Sözdizimi hataları ve teşhisleri (Linter) sorgular.",
        "handler": lsp_query,
        "parameters": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "enum": ["diagnostics", "definition", "references", "symbols"], "default": "diagnostics"},
                "file_path": {"type": "string"},
                "root_path": {"type": "string", "default": "."}
            }
        }
    },

    # 3. Container & K8s
    {
        "name": "docker_manage",
        "description": "Docker konteyner ve imaj yönetimi.",
        "handler": docker_manage,
        "parameters": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "enum": ["ps", "images", "run", "stop", "logs", "exec", "compose_up", "compose_down"]},
                "container_name": {"type": "string"},
                "image_name": {"type": "string"},
                "command": {"type": "string"}
            },
            "required": ["action"]
        }
    },
    {
        "name": "k8s_manage",
        "description": "Kubernetes (kubectl) kaynak yönetimi.",
        "handler": k8s_manage,
        "parameters": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "enum": ["get", "logs", "describe", "delete"], "default": "get"},
                "resource": {"type": "string", "default": "pods"},
                "name": {"type": "string"},
                "namespace": {"type": "string", "default": "default"}
            }
        }
    },

    # 4. System & Process
    {
        "name": "execute_command",
        "description": "Yerel makinede shell komutu çalıştırır.",
        "handler": execute_command,
        "parameters": {
            "type": "object",
            "properties": {
                "command": {"type": "string"},
                "shell": {"type": "string", "enum": ["powershell", "cmd", "bash"], "default": "powershell"},
                "cwd": {"type": "string"}
            },
            "required": ["command"]
        }
    },
    {
        "name": "get_process_list",
        "description": "Çalışan süreçleri listeler ve filtreler.",
        "handler": get_process_list,
        "parameters": {
            "type": "object",
            "properties": {"filter": {"type": "string"}}
        }
    },
    {
        "name": "kill_process",
        "description": "PID veya isimle süreç sonlandırır.",
        "handler": kill_process,
        "parameters": {
            "type": "object",
            "properties": {
                "pid": {"type": "integer"},
                "name": {"type": "string"},
                "force": {"type": "boolean", "default": True}
            }
        }
    },
    {
        "name": "manage_service",
        "description": "Servisleri (Windows Services / Systemd) yönetir.",
        "handler": manage_service,
        "parameters": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "action": {"type": "string", "enum": ["status", "start", "stop", "restart", "enable", "disable"]},
                "computer_name": {"type": "string"},
                "username": {"type": "string"},
                "password": {"type": "string"}
            },
            "required": ["name", "action"]
        }
    },

    # 5. Remote Management
    {
        "name": "invoke_remote_command",
        "description": "Uzak makinede kullanıcı adı ve şifre ile komut çalıştırır.",
        "handler": invoke_remote_command,
        "parameters": {
            "type": "object",
            "properties": {
                "computer_name": {"type": "string"},
                "command": {"type": "string"},
                "username": {"type": "string"},
                "password": {"type": "string"}
            },
            "required": ["computer_name", "command"]
        }
    },
    {
        "name": "create_pssession",
        "description": "Uzak makinede PSSession oturumu açar.",
        "handler": create_pssession,
        "parameters": {
            "type": "object",
            "properties": {
                "computer_name": {"type": "string"},
                "username": {"type": "string"},
                "password": {"type": "string"}
            },
            "required": ["computer_name"]
        }
    },
    {
        "name": "copy_to_remote",
        "description": "Uzak makineye dosya kopyalar.",
        "handler": copy_to_remote,
        "parameters": {
            "type": "object",
            "properties": {
                "computer_name": {"type": "string"},
                "source": {"type": "string"},
                "destination": {"type": "string"},
                "username": {"type": "string"},
                "password": {"type": "string"}
            },
            "required": ["computer_name", "source", "destination"]
        }
    },
    {
        "name": "copy_from_remote",
        "description": "Uzak makineden dosya çeker.",
        "handler": copy_from_remote,
        "parameters": {
            "type": "object",
            "properties": {
                "computer_name": {"type": "string"},
                "source": {"type": "string"},
                "destination": {"type": "string"},
                "username": {"type": "string"},
                "password": {"type": "string"}
            },
            "required": ["computer_name", "source", "destination"]
        }
    },
    {
        "name": "test_connection",
        "description": "Uzak bilgisayara WinRM/Ping bağlantı testi yapmayı sağlar.",
        "handler": test_connection,
        "parameters": {
            "type": "object",
            "properties": {
                "computer_name": {"type": "string"},
                "username": {"type": "string"},
                "password": {"type": "string"}
            },
            "required": ["computer_name"]
        }
    },

    # 6. Windows Advanced
    {
        "name": "registry_read_write",
        "description": "Windows Registry anahtarlarını okur, yazar, siler veya listeler.",
        "handler": registry_read_write,
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "operation": {"type": "string", "enum": ["read", "write", "delete", "list"]},
                "value_name": {"type": "string"},
                "value": {"type": "string"},
                "hive": {"type": "string", "enum": ["HKLM", "HKCU", "HKCR", "HKU"], "default": "HKLM"}
            },
            "required": ["path", "operation"]
        }
    },
    {
        "name": "wmi_query",
        "description": "WMI / CIM sorgusu çalıştırır.",
        "handler": wmi_query,
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "namespace": {"type": "string", "default": "root/cimv2"},
                "computer_name": {"type": "string"},
                "username": {"type": "string"},
                "password": {"type": "string"}
            },
            "required": ["query"]
        }
    },
    {
        "name": "event_log_query",
        "description": "Windows Event Olay Günlüklerini sorgular.",
        "handler": event_log_query,
        "parameters": {
            "type": "object",
            "properties": {
                "log_name": {"type": "string", "enum": ["System", "Application", "Security"], "default": "System"},
                "max_events": {"type": "integer", "default": 50},
                "computer_name": {"type": "string"}
            },
            "required": ["log_name"]
        }
    },
    {
        "name": "scheduled_task_manage",
        "description": "Windows Görev Zamanlayıcısını yönetir.",
        "handler": scheduled_task_manage,
        "parameters": {
            "type": "object",
            "properties": {
                "task_name": {"type": "string"},
                "action": {"type": "string", "enum": ["create", "run", "stop", "enable", "disable", "delete", "get"]},
                "action_exec": {"type": "string"},
                "action_args": {"type": "string"}
            },
            "required": ["task_name", "action"]
        }
    },

    # 7. Network & Database
    {
        "name": "http_request",
        "description": "Genel HTTP/REST API isteği gönderir.",
        "handler": http_request,
        "parameters": {
            "type": "object",
            "properties": {
                "url": {"type": "string"},
                "method": {"type": "string", "enum": ["GET", "POST", "PUT", "DELETE"], "default": "GET"},
                "headers": {"type": "object"},
                "data": {"type": "string"}
            },
            "required": ["url"]
        }
    },
    {
        "name": "db_query",
        "description": "Veritabanında sorgu çalıştırır (SQLite).",
        "handler": db_query,
        "parameters": {
            "type": "object",
            "properties": {
                "db_type": {"type": "string", "enum": ["sqlite"], "default": "sqlite"},
                "query": {"type": "string"},
                "db_path_or_conn": {"type": "string"}
            },
            "required": ["db_type", "query", "db_path_or_conn"]
        }
    }
]


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, BaseTool] = {}
        for item in RAW_TOOLS_DEFINITIONS:
            tool = BaseTool(
                name=item["name"],
                description=item["description"],
                schema={
                    "type": "function",
                    "function": {
                        "name": item["name"],
                        "description": item["description"],
                        "parameters": item["parameters"]
                    }
                },
                handler=item["handler"]
            )
            self._tools[item["name"]] = tool

    @property
    def schemas(self) -> list[dict[str, Any]]:
        return [t.schema for t in self._tools.values()]

    def execute(self, name: str, kwargs: dict[str, Any]) -> ToolResult:
        tool = self._tools.get(name)
        if not tool:
            return ToolResult(success=False, output="", error=f"Bulunamayan araç: '{name}'")
        return tool.execute(**kwargs)


tool_registry = ToolRegistry()
