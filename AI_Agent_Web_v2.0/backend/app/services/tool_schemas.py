from typing import Any

TOOL_SCHEMAS: dict[str, dict[str, Any]] = {
    "write_file": {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write content to a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {"type": "string", "description": "Target file path"},
                    "content": {"type": "string", "description": "File content"},
                    "append": {"type": "boolean", "default": False}
                },
                "required": ["filepath", "content"]
            }
        }
    },
    "read_file": {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read file content",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {"type": "string", "description": "File path to read"}
                },
                "required": ["filepath"]
            }
        }
    },
    "list_directory": {
        "type": "function",
        "function": {
            "name": "list_directory",
            "description": "List directory contents",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "default": ".", "description": "Directory path"}
                }
            }
        }
    },
    "copy_move_delete": {
        "type": "function",
        "function": {
            "name": "copy_move_delete",
            "description": "Copy, move or delete files/directories",
            "parameters": {
                "type": "object",
                "properties": {
                    "operation": {"type": "string", "enum": ["copy", "move", "delete"]},
                    "source": {"type": "string"},
                    "destination": {"type": "string"}
                },
                "required": ["operation", "source"]
            }
        }
    },
    "search_files": {
        "type": "function",
        "function": {
            "name": "search_files",
            "description": "Search files by name or content",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "default": "."},
                    "pattern": {"type": "string"},
                    "content_pattern": {"type": "string"}
                },
                "required": ["path"]
            }
        }
    },
    "code_edit": {
        "type": "function",
        "function": {
            "name": "code_edit",
            "description": "Edit code with target/replacement pairs",
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
        }
    },
    "patch_apply": {
        "type": "function",
        "function": {
            "name": "patch_apply",
            "description": "Apply unified diff patch",
            "parameters": {
                "type": "object",
                "properties": {
                    "patch_content": {"type": "string"},
                    "root_path": {"type": "string", "default": "."}
                },
                "required": ["patch_content"]
            }
        }
    },
    "symbol_search": {
        "type": "function",
        "function": {
            "name": "symbol_search",
            "description": "Search code symbols (classes, functions)",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "path": {"type": "string", "default": "."}
                },
                "required": ["query"]
            }
        }
    },
    "code_format": {
        "type": "function",
        "function": {
            "name": "code_format",
            "description": "Format code files",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {"type": "string"},
                    "formatter": {"type": "string", "enum": ["auto", "black", "prettier", "gofmt", "rustfmt"], "default": "auto"}
                },
                "required": ["filepath"]
            }
        }
    },
    "file_watch": {
        "type": "function",
        "function": {
            "name": "file_watch",
            "description": "Watch file/directory for changes",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "check_seconds": {"type": "integer", "default": 2}
                },
                "required": ["path"]
            }
        }
    },
    "git_manage": {
        "type": "function",
        "function": {
            "name": "git_manage",
            "description": "Git version control operations",
            "parameters": {
                "type": "object",
                "properties": {
                    "action": {"type": "string", "enum": ["status", "diff", "log", "add", "commit", "push", "pull", "branch", "checkout", "init", "custom"]},
                    "args": {"type": "string"},
                    "branch": {"type": "string"},
                    "message": {"type": "string"},
                    "repo_path": {"type": "string", "default": "."}
                },
                "required": ["action"]
            }
        }
    },
    "project_analyze": {
        "type": "function",
        "function": {
            "name": "project_analyze",
            "description": "Analyze project structure and dependencies",
            "parameters": {
                "type": "object",
                "properties": {
                    "root_path": {"type": "string", "default": "."}
                }
            }
        }
    },
    "test_runner": {
        "type": "function",
        "function": {
            "name": "test_runner",
            "description": "Run tests automatically",
            "parameters": {
                "type": "object",
                "properties": {
                    "framework": {"type": "string", "enum": ["auto", "pytest", "npm", "dotnet", "go", "cargo"], "default": "auto"},
                    "root_path": {"type": "string", "default": "."},
                    "test_filter": {"type": "string"}
                }
            }
        }
    },
    "lsp_query": {
        "type": "function",
        "function": {
            "name": "lsp_query",
            "description": "LSP diagnostics and queries",
            "parameters": {
                "type": "object",
                "properties": {
                    "action": {"type": "string", "enum": ["diagnostics", "definition", "references", "symbols"], "default": "diagnostics"},
                    "file_path": {"type": "string"},
                    "root_path": {"type": "string", "default": "."}
                }
            }
        }
    },
    "docker_manage": {
        "type": "function",
        "function": {
            "name": "docker_manage",
            "description": "Docker container and image management",
            "parameters": {
                "type": "object",
                "properties": {
                    "action": {"type": "string", "enum": ["ps", "images", "run", "stop", "logs", "exec", "compose_up", "compose_down"]},
                    "command": {"type": "string"},
                    "container_name": {"type": "string"},
                    "image_name": {"type": "string"}
                },
                "required": ["action"]
            }
        }
    },
    "k8s_manage": {
        "type": "function",
        "function": {
            "name": "k8s_manage",
            "description": "Kubernetes resource management",
            "parameters": {
                "type": "object",
                "properties": {
                    "action": {"type": "string", "enum": ["get", "logs", "describe", "delete"], "default": "get"},
                    "name": {"type": "string"},
                    "namespace": {"type": "string", "default": "default"},
                    "resource": {"type": "string", "default": "pods"}
                }
            }
        }
    },
    "execute_command": {
        "type": "function",
        "function": {
            "name": "execute_command",
            "description": "Execute shell command locally",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string"},
                    "cwd": {"type": "string"},
                    "shell": {"type": "string", "enum": ["powershell", "cmd", "bash"], "default": "powershell"}
                },
                "required": ["command"]
            }
        }
    },
    "get_process_list": {
        "type": "function",
        "function": {
            "name": "get_process_list",
            "description": "List running processes",
            "parameters": {
                "type": "object",
                "properties": {
                    "filter": {"type": "string"}
                }
            }
        }
    },
    "kill_process": {
        "type": "function",
        "function": {
            "name": "kill_process",
            "description": "Kill process by PID or name",
            "parameters": {
                "type": "object",
                "properties": {
                    "force": {"type": "boolean", "default": True},
                    "name": {"type": "string"},
                    "pid": {"type": "integer"}
                }
            }
        }
    },
    "manage_service": {
        "type": "function",
        "function": {
            "name": "manage_service",
            "description": "Manage Windows services",
            "parameters": {
                "type": "object",
                "properties": {
                    "action": {"type": "string", "enum": ["status", "start", "stop", "restart", "enable", "disable"]},
                    "computer_name": {"type": "string"},
                    "name": {"type": "string"},
                    "password": {"type": "string"},
                    "username": {"type": "string"}
                },
                "required": ["name", "action"]
            }
        }
    },
    "invoke_remote_command": {
        "type": "function",
        "function": {
            "name": "invoke_remote_command",
            "description": "Execute command on remote machine",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string"},
                    "computer_name": {"type": "string"},
                    "password": {"type": "string"},
                    "username": {"type": "string"}
                },
                "required": ["computer_name", "command"]
            }
        }
    },
    "create_pssession": {
        "type": "function",
        "function": {
            "name": "create_pssession",
            "description": "Create PowerShell session to remote machine",
            "parameters": {
                "type": "object",
                "properties": {
                    "computer_name": {"type": "string"},
                    "password": {"type": "string"},
                    "username": {"type": "string"}
                },
                "required": ["computer_name"]
            }
        }
    },
    "copy_to_remote": {
        "type": "function",
        "function": {
            "name": "copy_to_remote",
            "description": "Copy file to remote machine",
            "parameters": {
                "type": "object",
                "properties": {
                    "computer_name": {"type": "string"},
                    "destination": {"type": "string"},
                    "password": {"type": "string"},
                    "source": {"type": "string"},
                    "username": {"type": "string"}
                },
                "required": ["computer_name", "source", "destination"]
            }
        }
    },
    "copy_from_remote": {
        "type": "function",
        "function": {
            "name": "copy_from_remote",
            "description": "Copy file from remote machine",
            "parameters": {
                "type": "object",
                "properties": {
                    "computer_name": {"type": "string"},
                    "destination": {"type": "string"},
                    "password": {"type": "string"},
                    "source": {"type": "string"},
                    "username": {"type": "string"}
                },
                "required": ["computer_name", "source", "destination"]
            }
        }
    },
    "test_connection": {
        "type": "function",
        "function": {
            "name": "test_connection",
            "description": "Test WinRM/Ping connection to remote machine",
            "parameters": {
                "type": "object",
                "properties": {
                    "computer_name": {"type": "string"},
                    "password": {"type": "string"},
                    "username": {"type": "string"}
                },
                "required": ["computer_name"]
            }
        }
    },
    "registry_read_write": {
        "type": "function",
        "function": {
            "name": "registry_read_write",
            "description": "Windows Registry operations",
            "parameters": {
                "type": "object",
                "properties": {
                    "hive": {"type": "string", "enum": ["HKLM", "HKCU", "HKCR", "HKU"], "default": "HKLM"},
                    "operation": {"type": "string", "enum": ["read", "write", "delete", "list"]},
                    "path": {"type": "string"},
                    "value": {"type": "string"},
                    "value_name": {"type": "string"}
                },
                "required": ["path", "operation"]
            }
        }
    },
    "wmi_query": {
        "type": "function",
        "function": {
            "name": "wmi_query",
            "description": "Execute WMI/CIM query",
            "parameters": {
                "type": "object",
                "properties": {
                    "computer_name": {"type": "string"},
                    "namespace": {"type": "string", "default": "root/cimv2"},
                    "password": {"type": "string"},
                    "query": {"type": "string"},
                    "username": {"type": "string"}
                },
                "required": ["query"]
            }
        }
    },
    "event_log_query": {
        "type": "function",
        "function": {
            "name": "event_log_query",
            "description": "Query Windows Event Logs",
            "parameters": {
                "type": "object",
                "properties": {
                    "computer_name": {"type": "string"},
                    "log_name": {"type": "string", "enum": ["System", "Application", "Security"], "default": "System"},
                    "max_events": {"type": "integer", "default": 50}
                },
                "required": ["log_name"]
            }
        }
    },
    "scheduled_task_manage": {
        "type": "function",
        "function": {
            "name": "scheduled_task_manage",
            "description": "Manage Windows Task Scheduler",
            "parameters": {
                "type": "object",
                "properties": {
                    "action": {"type": "string", "enum": ["create", "run", "stop", "enable", "disable", "delete", "get"]},
                    "action_args": {"type": "string"},
                    "action_exec": {"type": "string"},
                    "task_name": {"type": "string"}
                },
                "required": ["task_name", "action"]
            }
        }
    },
    "http_request": {
        "type": "function",
        "function": {
            "name": "http_request",
            "description": "Make HTTP/REST API requests",
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {"type": "string"},
                    "headers": {"type": "object"},
                    "method": {"type": "string", "enum": ["GET", "POST", "PUT", "DELETE"], "default": "GET"},
                    "url": {"type": "string"}
                },
                "required": ["url"]
            }
        }
    },
    "db_query": {
        "type": "function",
        "function": {
            "name": "db_query",
            "description": "Execute SQLite database query",
            "parameters": {
                "type": "object",
                "properties": {
                    "db_path_or_conn": {"type": "string"},
                    "db_type": {"type": "string", "enum": ["sqlite"], "default": "sqlite"},
                    "query": {"type": "string"}
                },
                "required": ["db_type", "query", "db_path_or_conn"]
            }
        }
    }
}
