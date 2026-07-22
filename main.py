import os
import json
import time
import subprocess
import urllib.request
import urllib.parse
from openai import OpenAI

client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = "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"
)

tools = [
    # ==========================================
    # 1. YEREL DOSYA SİSTEMİ VE KOD ARAÇLARI
    # ==========================================
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Bilgisayarda belirtilen dosya yoluna içerik yazar veya yeni dosya oluşturur.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {"type": "string", "description": "Dosya yolu"},
                    "content": {"type": "string", "description": "Dosyaya yazılacak içerik"},
                    "append": {"type": "boolean", "default": False, "description": "Var olan dosyaya ekleme yap (Append mode)"}
                },
                "required": ["filepath", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Bilgisayardaki belirtilen dosyanın içeriğini okur.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {"type": "string", "description": "Okunacak dosya yolu"}
                },
                "required": ["filepath"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_directory",
            "description": "Belirtilen dizindeki dosya ve klasörleri listeler.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Listelenecek dizin yolu"}
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "copy_move_delete",
            "description": "Dosya veya klasör kopyalama, taşıma veya silme işlemi gerçekleştirir.",
            "parameters": {
                "type": "object",
                "properties": {
                    "operation": {"type": "string", "enum": ["copy", "move", "delete"], "description": "Yapılacak işlem"},
                    "source": {"type": "string", "description": "Kaynak dosya/klasör yolu"},
                    "destination": {"type": "string", "description": "Hedef yol (kopyalama/taşıma için)"}
                },
                "required": ["operation", "source"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_files",
            "description": "İçerik veya isim ile dosya araması yapmayı sağlar.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Aramanın başlayacağı dizin"},
                    "pattern": {"type": "string", "description": "Dosya adı deseni (örn: '*.py', '*.txt')"},
                    "content_pattern": {"type": "string", "description": "Dosya içi metin araması"}
                },
                "required": ["path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "code_edit",
            "description": "Birden fazla dosyada parçalı (target-replacement) kod düzenlemesi veya yazımı yapar.",
            "parameters": {
                "type": "object",
                "properties": {
                    "edits": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "filepath": {"type": "string"},
                                "target_content": {"type": "string", "description": "Değiştirilecek hedef metin bloku"},
                                "replacement_content": {"type": "string", "description": "Yeni metin bloku"}
                            },
                            "required": ["filepath", "replacement_content"]
                        }
                    }
                },
                "required": ["edits"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "patch_apply",
            "description": "Unified diff formatındaki bir patch'i projeye atomik olarak uygular.",
            "parameters": {
                "type": "object",
                "properties": {
                    "patch_content": {"type": "string", "description": "Git/Unified diff içeriği"},
                    "root_path": {"type": "string", "default": "."}
                },
                "required": ["patch_content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "symbol_search",
            "description": "Projedeki sınıflar, fonksiyonlar, metotlar veya semboller üzerinde arama yapar.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "default": "."},
                    "query": {"type": "string", "description": "Aranacak sembol adı (örn: 'execute_tool', 'class User')"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "code_format",
            "description": "Kod dosyalarını formatlar (black, prettier, gofmt, rustfmt).",
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
    {
        "type": "function",
        "function": {
            "name": "file_watch",
            "description": "Bir dosya veya klasörün değişip değişmediğini kontrol eder/izler.",
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

    # ==========================================
    # 2. YAZILIM GELİŞTİRME & VERSİYON KONTROL
    # ==========================================
    {
        "type": "function",
        "function": {
            "name": "git_manage",
            "description": "Git versiyon kontrol işlemlerini çalıştırır (status, diff, log, add, commit, push, pull, branch, checkout, init, custom).",
            "parameters": {
                "type": "object",
                "properties": {
                    "action": {"type": "string", "enum": ["status", "diff", "log", "add", "commit", "push", "pull", "branch", "checkout", "init", "custom"]},
                    "repo_path": {"type": "string", "default": "."},
                    "args": {"type": "string", "description": "Ekstra parametreler"},
                    "branch": {"type": "string"},
                    "message": {"type": "string", "description": "Commit mesajı"}
                },
                "required": ["action"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "project_analyze",
            "description": "Proje yapısını, bağımlılık dosyalarını (package.json, csproj, Cargo.toml, requirements.txt vb.) detaylı analiz eder.",
            "parameters": {
                "type": "object",
                "properties": {
                    "root_path": {"type": "string", "default": "."}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "test_runner",
            "description": "Otomatik bir şekilde testleri çalıştırır ve sonuçları raporlar (pytest, npm test, dotnet test, go test, cargo test).",
            "parameters": {
                "type": "object",
                "properties": {
                    "root_path": {"type": "string", "default": "."},
                    "framework": {"type": "string", "enum": ["auto", "pytest", "npm", "dotnet", "go", "cargo"], "default": "auto"},
                    "test_filter": {"type": "string", "description": "Test adı filtresi"}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "lsp_query",
            "description": "Sözdizimi hataları, teşhisler ve kod analizini (Language Server / Linter) sorgular.",
            "parameters": {
                "type": "object",
                "properties": {
                    "root_path": {"type": "string", "default": "."},
                    "file_path": {"type": "string"},
                    "action": {"type": "string", "enum": ["diagnostics", "definition", "references", "symbols"], "default": "diagnostics"}
                }
            }
        }
    },

    # ==========================================
    # 3. KONTEYNER & KUBERNETES YÖNETİMİ
    # ==========================================
    {
        "type": "function",
        "function": {
            "name": "docker_manage",
            "description": "Docker konteyner ve imaj yönetimi (ps, images, run, stop, logs, exec, compose_up, compose_down).",
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
        }
    },
    {
        "type": "function",
        "function": {
            "name": "k8s_manage",
            "description": "Kubernetes (kubectl) kaynak yönetimi (get, logs, describe, delete).",
            "parameters": {
                "type": "object",
                "properties": {
                    "action": {"type": "string", "enum": ["get", "logs", "describe", "delete"], "default": "get"},
                    "resource": {"type": "string", "default": "pods"},
                    "name": {"type": "string"},
                    "namespace": {"type": "string", "default": "default"}
                }
            }
        }
    },

    # ==========================================
    # 4. SİSTEM & SÜREÇ YÖNETİM ARAÇLARI
    # ==========================================
    {
        "type": "function",
        "function": {
            "name": "execute_command",
            "description": "Yerel makinede shell komutu çalıştırır (PowerShell, CMD, Bash).",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "Çalıştırılacak komut"},
                    "shell": {"type": "string", "enum": ["powershell", "cmd", "bash"], "default": "powershell"},
                    "cwd": {"type": "string", "description": "Çalışma dizini"}
                },
                "required": ["command"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_process_list",
            "description": "Çalışan süreçleri listeler ve filtreler.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filter": {"type": "string", "description": "Süreç adı filtresi (opsiyonel)"}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "kill_process",
            "description": "PID veya isimle süreç sonlandırır.",
            "parameters": {
                "type": "object",
                "properties": {
                    "pid": {"type": "integer", "description": "Süreç ID (PID)"},
                    "name": {"type": "string", "description": "Süreç Adı"},
                    "force": {"type": "boolean", "default": True}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "manage_service",
            "description": "Servisleri (Windows Services / Systemd) yönetir (start, stop, restart, enable, disable, status).",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Servis adı"},
                    "action": {"type": "string", "enum": ["status", "start", "stop", "restart", "enable", "disable"]},
                    "computer_name": {"type": "string", "description": "Uzak bilgisayar adı (opsiyonel)"},
                    "username": {"type": "string"},
                    "password": {"type": "string"}
                },
                "required": ["name", "action"]
            }
        }
    },

    # ==========================================
    # 5. UZAK YÖNETİM (WINRM / SSH) ARAÇLARI
    # ==========================================
    {
        "type": "function",
        "function": {
            "name": "invoke_remote_command",
            "description": "Uzak makinede (WinRM/SSH üzerinden) kullanıcı adı ve şifre ile komut çalıştırır.",
            "parameters": {
                "type": "object",
                "properties": {
                    "computer_name": {"type": "string", "description": "Uzak IP/Hostname"},
                    "command": {"type": "string", "description": "Komut"},
                    "username": {"type": "string"},
                    "password": {"type": "string"}
                },
                "required": ["computer_name", "command"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_pssession",
            "description": "Uzak makinede PSSession oturumu açar.",
            "parameters": {
                "type": "object",
                "properties": {
                    "computer_name": {"type": "string"},
                    "username": {"type": "string"},
                    "password": {"type": "string"}
                },
                "required": ["computer_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "copy_to_remote",
            "description": "Uzak makineye dosya kopyalar.",
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
        }
    },
    {
        "type": "function",
        "function": {
            "name": "copy_from_remote",
            "description": "Uzak makineden dosya çeker.",
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
        }
    },
    {
        "type": "function",
        "function": {
            "name": "test_connection",
            "description": "Uzak bilgisayara WinRM/Ping bağlantı testi yapmayı sağlar.",
            "parameters": {
                "type": "object",
                "properties": {
                    "computer_name": {"type": "string"},
                    "username": {"type": "string"},
                    "password": {"type": "string"}
                },
                "required": ["computer_name"]
            }
        }
    },

    # ==========================================
    # 6. WINDOWS GELİŞMİŞ (REGISTRY, WMI, EVENTLOG, TASKSCHEDULER)
    # ==========================================
    {
        "type": "function",
        "function": {
            "name": "registry_read_write",
            "description": "Windows Registry anahtarlarını okur, yazar, siler veya listeler.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Registry alt yolu (örn: 'SOFTWARE\\Microsoft')"},
                    "operation": {"type": "string", "enum": ["read", "write", "delete", "list"]},
                    "value_name": {"type": "string"},
                    "value": {"type": "string"},
                    "hive": {"type": "string", "enum": ["HKLM", "HKCU", "HKCR", "HKU"], "default": "HKLM"}
                },
                "required": ["path", "operation"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "wmi_query",
            "description": "WMI / CIM sorgusu çalıştırır.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "WQL sorgusu (örn: 'SELECT * FROM Win32_OperatingSystem')"},
                    "namespace": {"type": "string", "default": "root/cimv2"},
                    "computer_name": {"type": "string"},
                    "username": {"type": "string"},
                    "password": {"type": "string"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "event_log_query",
            "description": "Windows Event Olay Günlüklerini sorgular.",
            "parameters": {
                "type": "object",
                "properties": {
                    "log_name": {"type": "string", "enum": ["System", "Application", "Security"], "default": "System"},
                    "max_events": {"type": "integer", "default": 50},
                    "computer_name": {"type": "string"}
                },
                "required": ["log_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "scheduled_task_manage",
            "description": "Windows Görev Zamanlayıcısını yönetir (create, run, stop, enable, disable, delete, get).",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_name": {"type": "string"},
                    "action": {"type": "string", "enum": ["create", "run", "stop", "enable", "disable", "delete", "get"]},
                    "action_exec": {"type": "string", "description": "Çalıştırılacak program yolu (create için)"},
                    "action_args": {"type": "string", "description": "Program parametreleri (create için)"}
                },
                "required": ["task_name", "action"]
            }
        }
    },

    # ==========================================
    # 7. AĞ, VERİTABANI & REST API
    # ==========================================
    {
        "type": "function",
        "function": {
            "name": "http_request",
            "description": "Genel HTTP/REST API isteği (GET, POST, PUT, DELETE) gönderir.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "Hedef URL"},
                    "method": {"type": "string", "enum": ["GET", "POST", "PUT", "DELETE"], "default": "GET"},
                    "headers": {"type": "object", "description": "Header bilgileri (JSON)"},
                    "data": {"type": "string", "description": "POST/PUT gövde verisi"}
                },
                "required": ["url"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "db_query",
            "description": "Veritabanında sorgu çalıştırır ve sonuçları döndürür (SQLite vb.).",
            "parameters": {
                "type": "object",
                "properties": {
                    "db_type": {"type": "string", "enum": ["sqlite"], "default": "sqlite"},
                    "query": {"type": "string", "description": "SQL Sorgusu"},
                    "db_path_or_conn": {"type": "string", "description": "Veritabanı dosya yolu"}
                },
                "required": ["db_type", "query", "db_path_or_conn"]
            }
        }
    }
]

def run_powershell(ps_code):
    try:
        full_cmd = f"[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; {ps_code}"
        result = subprocess.run(
            ["powershell", "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass", "-Command", full_cmd],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=60
        )
        output = result.stdout.strip() if result.stdout else ""
        error = result.stderr.strip() if result.stderr else ""
        if error and not output:
            return f"Hata: {error}"
        elif error:
            return f"Çıktı:\n{output}\n\nUyarı/Hata:\n{error}"
        return output if output else "İşlem başarıyla tamamlandı (Çıktı yok)."
    except subprocess.TimeoutExpired:
        return "Hata: Komut zaman aşımına uğradı (60 saniye)."
    except Exception as e:
        return f"Sistem hatası: {str(e)}"

def make_ps_cred_prefix(username, password):
    if username and password:
        clean_user = username.replace("'", "''")
        clean_pass = password.replace("'", "''")
        return (
            f"$secstr = ConvertTo-SecureString '{clean_pass}' -AsPlainText -Force; "
            f"$cred = New-Object System.Management.Automation.PSCredential('{clean_user}', $secstr); "
        )
    return ""

def execute_tool(name, args):
    try:
        if name == "write_file":
            filepath = os.path.expanduser(args.get("filepath", ""))
            content = args.get("content", "")
            append = args.get("append", False)
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

            if "masaüstü" in filepath.lower() or "masaustu" in filepath.lower() or "desktop" in filepath.lower():
                filename = os.path.basename(filepath)
                if not filename or filename.lower() in ["masaüstü", "masaustu", "desktop"]:
                    filename = "yeni_dosya.txt"
                filepath = os.path.join(desktop_path, filename)

            dirname = os.path.dirname(os.path.abspath(filepath))
            if dirname:
                os.makedirs(dirname, exist_ok=True)
            
            mode = "a" if append else "w"
            with open(filepath, mode, encoding="utf-8") as f:
                f.write(content)
            return f"Başarılı: '{filepath}' dosyası oluşturuldu/güncellendi."

        elif name == "read_file":
            filepath = os.path.expanduser(args.get("filepath", ""))
            if not os.path.exists(filepath):
                return f"Hata: '{filepath}' dosyası bulunamadı."
            with open(filepath, "r", encoding="utf-8", errors="replace") as f:
                return f.read()

        elif name == "list_directory":
            path = os.path.expanduser(args.get("path", "."))
            if not os.path.exists(path):
                return f"Hata: '{path}' dizini bulunamadı."
            items = os.listdir(path)
            return f"Dizin içeriği ({path}): {items}"

        elif name == "copy_move_delete":
            op = args.get("operation")
            src = os.path.expanduser(args.get("source", ""))
            dest = os.path.expanduser(args.get("destination", "")) if args.get("destination") else None
            import shutil
            if op == "delete":
                if os.path.isdir(src):
                    shutil.rmtree(src)
                else:
                    os.remove(src)
                return f"Başarılı: '{src}' silindi."
            elif op == "copy":
                if os.path.isdir(src):
                    shutil.copytree(src, dest, dirs_exist_ok=True)
                else:
                    shutil.copy2(src, dest)
                return f"Başarılı: '{src}' -> '{dest}' kopyalandı."
            elif op == "move":
                shutil.move(src, dest)
                return f"Başarılı: '{src}' -> '{dest}' taşındı."

        elif name == "search_files":
            root_path = os.path.expanduser(args.get("path", "."))
            pattern = args.get("pattern")
            content_pattern = args.get("content_pattern")
            import fnmatch
            matches = []
            for root, dirs, files in os.walk(root_path):
                for file in files:
                    if pattern and not fnmatch.fnmatch(file, pattern):
                        continue
                    full_p = os.path.join(root, file)
                    if content_pattern:
                        try:
                            with open(full_p, "r", encoding="utf-8", errors="ignore") as f:
                                text = f.read()
                                if content_pattern.lower() in text.lower():
                                    matches.append(full_p)
                        except Exception:
                            pass
                    else:
                        matches.append(full_p)
                    if len(matches) >= 50:
                        break
                if len(matches) >= 50:
                    break
            return f"Bulunan dosyalar ({len(matches)} adet):\n" + "\n".join(matches)

        elif name == "code_edit":
            edits = args.get("edits", [])
            results = []
            for item in edits:
                fp = os.path.expanduser(item.get("filepath", ""))
                target = item.get("target_content", "")
                replacement = item.get("replacement_content", "")
                if not os.path.exists(fp):
                    results.append(f"Hata: Dosya bulunamadı ({fp})")
                    continue
                try:
                    with open(fp, "r", encoding="utf-8", errors="replace") as f:
                        text = f.read()
                    if target and target in text:
                        new_text = text.replace(target, replacement, 1)
                        with open(fp, "w", encoding="utf-8") as f:
                            f.write(new_text)
                        results.append(f"Başarılı: '{fp}' dosyasında hedef metin güncellendi.")
                    elif not target:
                        with open(fp, "w", encoding="utf-8") as f:
                            f.write(replacement)
                        results.append(f"Başarılı: '{fp}' dosyasına yeni içerik yazıldı.")
                    else:
                        results.append(f"Hata: Hedef metin '{fp}' içinde bulunamadı.")
                except Exception as e:
                    results.append(f"Hata ({fp}): {str(e)}")
            return "\n".join(results)

        elif name == "patch_apply":
            patch_content = args.get("patch_content", "")
            root_path = os.path.expanduser(args.get("root_path", "."))
            patch_file = os.path.join(root_path, "_temp_agent.patch")
            with open(patch_file, "w", encoding="utf-8") as f:
                f.write(patch_content)
            ps = f"git apply --check '{patch_file}'; if ($?) {{ git apply '{patch_file}'; Remove-Item '{patch_file}' }}"
            res = run_powershell(ps)
            if os.path.exists(patch_file):
                os.remove(patch_file)
            return res

        elif name == "symbol_search":
            root_path = os.path.expanduser(args.get("path", "."))
            query = args.get("query", "")
            matches = []
            for root, dirs, files in os.walk(root_path):
                for file in files:
                    if file.endswith((".py", ".js", ".ts", ".cs", ".go", ".rs", ".java", ".cpp", ".h")):
                        fp = os.path.join(root, file)
                        try:
                            with open(fp, "r", encoding="utf-8", errors="ignore") as f:
                                lines = f.readlines()
                                for i, line in enumerate(lines, 1):
                                    if query.lower() in line.lower() and any(k in line for k in ["def ", "class ", "function ", "struct ", "enum ", "interface "]):
                                        matches.append(f"{fp}:{i} -> {line.strip()}")
                        except Exception:
                            pass
                    if len(matches) >= 50:
                        break
                if len(matches) >= 50:
                    break
            return f"Bulunan semboller ({len(matches)} adet):\n" + "\n".join(matches)

        elif name == "code_format":
            fp = os.path.expanduser(args.get("filepath", ""))
            fmt = args.get("formatter", "auto")
            if not os.path.exists(fp):
                return f"Hata: Dosya bulunamadı ({fp})"
            if fmt == "auto":
                if fp.endswith(".py"):
                    fmt = "black"
                elif fp.endswith((".js", ".ts", ".json", ".html", ".css")):
                    fmt = "prettier"
                elif fp.endswith(".go"):
                    fmt = "gofmt"
                elif fp.endswith(".rs"):
                    fmt = "rustfmt"

            if fmt == "black":
                ps = f"python -m black '{fp}'"
            elif fmt == "prettier":
                ps = f"npx prettier --write '{fp}'"
            elif fmt == "gofmt":
                ps = f"gofmt -w '{fp}'"
            elif fmt == "rustfmt":
                ps = f"rustfmt '{fp}'"
            else:
                return f"Formatlayıcı ({fmt}) çalıştırılamadı."
            return run_powershell(ps)

        elif name == "file_watch":
            p = os.path.expanduser(args.get("path", ""))
            sec = args.get("check_seconds", 2)
            if not os.path.exists(p):
                return f"Hata: Yol bulunamadı ({p})"
            try:
                mtime = os.path.getmtime(p)
                time.sleep(sec)
                new_mtime = os.path.getmtime(p)
                if new_mtime != mtime:
                    return f"Dosya/Klasör değiştirildi: {p}"
                return f"Değişiklik tespit edilmedi ({p})"
            except Exception as e:
                return f"İzleme hatası: {str(e)}"

        elif name == "git_manage":
            action = args.get("action")
            repo_path = os.path.expanduser(args.get("repo_path", "."))
            extra_args = args.get("args")
            branch = args.get("branch")
            message = args.get("message")

            if not os.path.exists(repo_path):
                return f"Hata: Dizin bulunamadı ({repo_path})"

            cmd_parts = ["git"]
            if action == "status":
                cmd_parts.extend(["status", "--short"])
            elif action == "diff":
                cmd_parts.extend(["diff"])
            elif action == "log":
                cmd_parts.extend(["log", "-n", "10", "--oneline"])
            elif action == "add":
                target = extra_args if extra_args else "."
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
                    return "Hata: checkout için branch adı girilmelidir."
                cmd_parts.extend(["checkout", branch])
            elif action == "init":
                cmd_parts.extend(["init"])
            elif action == "custom":
                if not extra_args:
                    return "Hata: custom için args belirtilmelidir."
                cmd_parts.extend(extra_args.split())
            else:
                cmd_parts.extend(["status"])

            res = subprocess.run(cmd_parts, capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=repo_path, timeout=60)
            out = res.stdout.strip() if res.stdout else ""
            err = res.stderr.strip() if res.stderr else ""
            return out if out else (err if err else "Git komutu başarıyla tamamlandı.")

        elif name == "project_analyze":
            rpath = os.path.expanduser(args.get("root_path", "."))
            if not os.path.exists(rpath):
                return f"Hata: Dizin bulunamadı ({rpath})"
            info = {
                "root_path": os.path.abspath(rpath),
                "detected_project_types": [],
                "config_files": [],
                "scripts_or_commands": {},
                "dependencies_summary": []
            }
            files_in_root = os.listdir(rpath)
            for f in files_in_root:
                full_f = os.path.join(rpath, f)
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
            return json.dumps(info, ensure_ascii=False, indent=2)

        elif name == "test_runner":
            rpath = os.path.expanduser(args.get("root_path", "."))
            fw = args.get("framework", "auto")
            tfilter = args.get("test_filter")
            if not os.path.exists(rpath):
                return f"Hata: Dizin bulunamadı ({rpath})"
            
            files = os.listdir(rpath)
            if fw == "auto":
                if "pytest.ini" in files or "requirements.txt" in files or any(f.endswith(".py") for f in files):
                    fw = "pytest"
                elif "package.json" in files:
                    fw = "npm"
                elif any(f.endswith(".csproj") for f in files) or any(f.endswith(".sln") for f in files):
                    fw = "dotnet"
                elif "go.mod" in files:
                    fw = "go"
                elif "Cargo.toml" in files:
                    fw = "cargo"

            if fw == "pytest":
                cmd = ["pytest"]
                if tfilter:
                    cmd.extend(["-k", tfilter])
            elif fw == "npm":
                cmd = ["npm", "test"]
            elif fw == "dotnet":
                cmd = ["dotnet", "test"]
                if tfilter:
                    cmd.extend(["--filter", tfilter])
            elif fw == "go":
                cmd = ["go", "test", "./..."]
            elif fw == "cargo":
                cmd = ["cargo", "test"]
            else:
                return f"Desteklenmeyen test altyapısı: {fw}"

            res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=rpath, timeout=180)
            out = res.stdout.strip() if res.stdout else ""
            err = res.stderr.strip() if res.stderr else ""
            return f"--- TEST ÇIKTISI ({fw}) ---\n{out}\n\n{err}"

        elif name == "lsp_query":
            rpath = os.path.expanduser(args.get("root_path", "."))
            fpath = os.path.expanduser(args.get("file_path", "")) if args.get("file_path") else ""
            action = args.get("action", "diagnostics")
            if action == "diagnostics":
                if fpath.endswith(".py") or any(f.endswith(".py") for f in os.listdir(rpath)):
                    cmd = f"python -m py_compile '{fpath}'" if fpath else f"python -m compileall '{rpath}'"
                    return run_powershell(cmd)
                elif fpath.endswith((".ts", ".js")) or "package.json" in os.listdir(rpath):
                    return run_powershell("npx tsc --noEmit")
                elif any(f.endswith(".csproj") for f in os.listdir(rpath)):
                    return run_powershell("dotnet build /clp:NoSummary /warnaserror")
                else:
                    return "LSP Diagnostics: Sözdizimi hatası bulunamadı."
            return f"LSP ({action}): İşlem tamamlandı."

        elif name == "docker_manage":
            act = args.get("action")
            cname = args.get("container_name")
            iname = args.get("image_name")
            cmd_str = args.get("command")

            cmd_parts = ["docker"]
            if act == "ps":
                cmd_parts.extend(["ps", "-a"])
            elif act == "images":
                cmd_parts.extend(["images"])
            elif act == "run":
                if not iname:
                    return "Hata: run işlemi için image_name gereklidir."
                cmd_parts.extend(["run", "-d"])
                if cname:
                    cmd_parts.extend(["--name", cname])
                cmd_parts.append(iname)
            elif act == "stop":
                if not cname:
                    return "Hata: stop işlemi için container_name gereklidir."
                cmd_parts.extend(["stop", cname])
            elif act == "logs":
                if not cname:
                    return "Hata: logs işlemi için container_name gereklidir."
                cmd_parts.extend(["logs", "--tail", "50", cname])
            elif act == "exec":
                if not cname or not cmd_str:
                    return "Hata: exec işlemi için container_name ve command gereklidir."
                cmd_parts.extend(["exec", cname] + cmd_str.split())
            elif act == "compose_up":
                cmd_parts = ["docker-compose", "up", "-d"]
            elif act == "compose_down":
                cmd_parts = ["docker-compose", "down"]
            else:
                cmd_parts.extend(["ps"])

            res = subprocess.run(cmd_parts, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120)
            out = res.stdout.strip() if res.stdout else ""
            err = res.stderr.strip() if res.stderr else ""
            return out if out else (err if err else "Docker komutu başarıyla çalıştırıldı.")

        elif name == "k8s_manage":
            act = args.get("action", "get")
            res_type = args.get("resource", "pods")
            rname = args.get("name")
            ns = args.get("namespace", "default")
            if act == "get":
                ps = f"kubectl get {res_type} -n {ns} -o wide" if not rname else f"kubectl get {res_type} {rname} -n {ns} -o yaml"
            elif act == "logs":
                ps = f"kubectl logs {rname} -n {ns} --tail=100"
            elif act == "describe":
                ps = f"kubectl describe {res_type} {rname} -n {ns}"
            elif act == "delete":
                ps = f"kubectl delete {res_type} {rname} -n {ns}"
            else:
                ps = f"kubectl get {res_type} -n {ns}"
            return run_powershell(ps)

        elif name == "execute_command":
            cmd = args.get("command", "")
            shell = args.get("shell", "powershell")
            cwd = os.path.expanduser(args.get("cwd")) if args.get("cwd") else None
            if shell == "cmd":
                cmd_args = ["cmd.exe", "/c", cmd]
            elif shell == "bash":
                cmd_args = ["bash", "-c", cmd]
            else:
                cmd_args = ["powershell", "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass", "-Command", f"[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; {cmd}"]
            res = subprocess.run(cmd_args, capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=cwd, timeout=120)
            out = res.stdout.strip() if res.stdout else ""
            err = res.stderr.strip() if res.stderr else ""
            return out if out else (err if err else "Komut başarıyla tamamlandı.")

        elif name == "get_process_list":
            proc_filter = args.get("filter")
            if proc_filter:
                ps = f"Get-Process -Name '{proc_filter}' -ErrorAction SilentlyContinue | Select-Object Id, ProcessName, CPU, WorkingSet64 | Format-Table -AutoSize"
            else:
                ps = "Get-Process | Select-Object Id, ProcessName, CPU, WorkingSet64 -First 40 | Format-Table -AutoSize"
            return run_powershell(ps)

        elif name == "kill_process":
            pid = args.get("pid")
            pname = args.get("name")
            force = "-Force" if args.get("force", True) else ""
            if pid:
                ps = f"Stop-Process -Id {pid} {force}"
            elif pname:
                ps = f"Stop-Process -Name '{pname}' {force}"
            else:
                return "Hata: PID veya süreç adı (name) belirtilmelidir."
            return run_powershell(ps)

        elif name == "manage_service":
            sname = args.get("name")
            action = args.get("action")
            comp = args.get("computer_name")
            username = args.get("username")
            password = args.get("password")

            if action == "start":
                cmd = f"Start-Service -Name '{sname}'"
            elif action == "stop":
                cmd = f"Stop-Service -Name '{sname}'"
            elif action == "restart":
                cmd = f"Restart-Service -Name '{sname}'"
            elif action == "enable":
                cmd = f"Set-Service -Name '{sname}' -StartupType Automatic"
            elif action == "disable":
                cmd = f"Set-Service -Name '{sname}' -StartupType Disabled"
            else:
                cmd = f"Get-Service -Name '{sname}'"

            if comp and comp.lower() not in ["localhost", "127.0.0.1", "."]:
                cred_prefix = make_ps_cred_prefix(username, password)
                cred_arg = " -Credential $cred" if (username and password) else ""
                ps = f"{cred_prefix}Invoke-Command -ComputerName '{comp}'{cred_arg} -ScriptBlock {{ {cmd} }}"
            else:
                ps = cmd
            return run_powershell(ps)

        elif name == "invoke_remote_command":
            comp = args.get("computer_name", "localhost")
            cmd = args.get("command", "")
            username = args.get("username")
            password = args.get("password")

            cred_prefix = make_ps_cred_prefix(username, password)
            cred_arg = " -Credential $cred" if (username and password) else ""
            ps = f"{cred_prefix}Invoke-Command -ComputerName '{comp}'{cred_arg} -ScriptBlock {{ {cmd} }}"
            return run_powershell(ps)

        elif name == "create_pssession":
            comp = args.get("computer_name", "localhost")
            username = args.get("username")
            password = args.get("password")

            cred_prefix = make_ps_cred_prefix(username, password)
            cred_arg = " -Credential $cred" if (username and password) else ""
            ps = f"{cred_prefix}$s = New-PSSession -ComputerName '{comp}'{cred_arg}; Get-PSSession; Remove-PSSession $s"
            return run_powershell(ps)

        elif name == "copy_to_remote":
            comp = args.get("computer_name")
            src = os.path.expanduser(args.get("source", ""))
            dest = args.get("destination", "")
            username = args.get("username")
            password = args.get("password")

            cred_prefix = make_ps_cred_prefix(username, password)
            cred_arg = " -Credential $cred" if (username and password) else ""
            ps = f"{cred_prefix}$s = New-PSSession -ComputerName '{comp}'{cred_arg}; Copy-Item -Path '{src}' -Destination '{dest}' -ToSession $s -Recurse -Force; Remove-PSSession $s"
            return run_powershell(ps)

        elif name == "copy_from_remote":
            comp = args.get("computer_name")
            src = args.get("source", "")
            dest = os.path.expanduser(args.get("destination", ""))
            username = args.get("username")
            password = args.get("password")

            cred_prefix = make_ps_cred_prefix(username, password)
            cred_arg = " -Credential $cred" if (username and password) else ""
            ps = f"{cred_prefix}$s = New-PSSession -ComputerName '{comp}'{cred_arg}; Copy-Item -Path '{src}' -Destination '{dest}' -FromSession $s -Recurse -Force; Remove-PSSession $s"
            return run_powershell(ps)

        elif name == "test_connection":
            comp = args.get("computer_name", "localhost")
            username = args.get("username")
            password = args.get("password")

            if username and password:
                cred_prefix = make_ps_cred_prefix(username, password)
                ps = f"{cred_prefix}Test-WSMan -ComputerName '{comp}' -Credential $cred"
            else:
                ps = f"Test-NetConnection -ComputerName '{comp}' | Select-Object ComputerName, RemoteAddress, PingSucceeded, TcpTestSucceeded | Format-List"
            return run_powershell(ps)

        elif name == "registry_read_write":
            path = args.get("path", "")
            op = args.get("operation")
            vname = args.get("value_name", "")
            val = args.get("value", "")
            hive = args.get("hive", "HKLM")

            if op == "read":
                ps = f"(Get-ItemProperty -Path '{hive}:\\{path}').'{vname}'" if vname else f"Get-ItemProperty -Path '{hive}:\\{path}'"
            elif op == "write":
                ps = f"Set-ItemProperty -Path '{hive}:\\{path}' -Name '{vname}' -Value '{val}' -Force"
            elif op == "delete":
                ps = f"Remove-ItemProperty -Path '{hive}:\\{path}' -Name '{vname}' -Force" if vname else f"Remove-Item -Path '{hive}:\\{path}' -Recurse -Force"
            else:
                ps = f"Get-ChildItem -Path '{hive}:\\{path}'"
            return run_powershell(ps)

        elif name == "wmi_query":
            q = args.get("query", "")
            ns = args.get("namespace", "root/cimv2")
            comp = args.get("computer_name")
            username = args.get("username")
            password = args.get("password")

            if comp and comp.lower() not in ["localhost", "127.0.0.1", "."]:
                cred_prefix = make_ps_cred_prefix(username, password)
                cred_arg = " -Credential $cred" if (username and password) else ""
                ps = f"{cred_prefix}Get-CimInstance -Query \"{q}\" -Namespace '{ns}' -ComputerName '{comp}'{cred_arg} | Format-List"
            else:
                ps = f"Get-CimInstance -Query \"{q}\" -Namespace '{ns}' | Format-List"
            return run_powershell(ps)

        elif name == "event_log_query":
            log = args.get("log_name", "System")
            max_e = args.get("max_events", 50)
            comp = args.get("computer_name")
            comp_arg = f" -ComputerName '{comp}'" if (comp and comp.lower() not in ["localhost", "127.0.0.1", "."]) else ""
            ps = f"Get-EventLog -LogName '{log}' -Newest {max_e}{comp_arg} | Select-Object TimeGenerated, EntryType, Source, EventID, Message | Format-Table -AutoSize"
            return run_powershell(ps)

        elif name == "scheduled_task_manage":
            tname = args.get("task_name")
            act = args.get("action")
            aexec = args.get("action_exec")
            aargs = args.get("action_args", "")

            if act == "run":
                ps = f"Start-ScheduledTask -TaskName '{tname}'"
            elif act == "stop":
                ps = f"Stop-ScheduledTask -TaskName '{tname}'"
            elif act == "enable":
                ps = f"Enable-ScheduledTask -TaskName '{tname}'"
            elif act == "disable":
                ps = f"Disable-ScheduledTask -TaskName '{tname}'"
            elif act == "delete":
                ps = f"Unregister-ScheduledTask -TaskName '{tname}' -Confirm:$false"
            elif act == "create":
                ps = f"$action = New-ScheduledTaskAction -Execute '{aexec}' -Argument '{aargs}'; Register-ScheduledTask -TaskName '{tname}' -Action $action -Force"
            else:
                ps = f"Get-ScheduledTask -TaskName '{tname}'"
            return run_powershell(ps)

        elif name == "http_request":
            url = args.get("url")
            method = args.get("method", "GET").upper()
            headers = args.get("headers", {})
            data = args.get("data")

            req = urllib.request.Request(url, method=method)
            if headers:
                for k, v in headers.items():
                    req.add_header(k, str(v))
            body = data.encode('utf-8') if data else None
            with urllib.request.urlopen(req, data=body, timeout=30) as resp:
                content = resp.read().decode('utf-8', errors='replace')
                return f"HTTP {resp.status}:\n{content[:4000]}"

        elif name == "db_query":
            db_type = args.get("db_type", "sqlite")
            query = args.get("query", "")
            db_path = os.path.expanduser(args.get("db_path_or_conn", ""))
            if db_type == "sqlite":
                import sqlite3
                try:
                    conn = sqlite3.connect(db_path)
                    cursor = conn.cursor()
                    cursor.execute(query)
                    if query.strip().lower().startswith("select") or query.strip().lower().startswith("pragma"):
                        rows = cursor.fetchall()
                        cols = [desc[0] for desc in cursor.description] if cursor.description else []
                        conn.close()
                        return json.dumps({"columns": cols, "rows": rows}, ensure_ascii=False, indent=2)
                    else:
                        conn.commit()
                        conn.close()
                        return "Sorgu başarıyla çalıştırıldı ve kaydedildi."
                except Exception as e:
                    return f"SQLite Hatası: {str(e)}"
            return "Desteklenmeyen veritabanı tipi."

    except Exception as e:
        return f"İşlem sırasında hata oluştu: {str(e)}"
    return "Bilinmeyen araç."

desktop_folder = os.path.join(os.path.expanduser("~"), "Desktop")

messages = [
    {
        "role": "system",
        "content": (
            "Sen bilgisayarda, yazılım projelerinde, veritabanlarında ve uzak sistemlerde tam yetkili, otonom bir AI Sistem Yöneticisi, DevSecOps ve Yazılım Ajanısın.\n\n"
            "Mevcut Tam Otomasyon Araç Setin (31 Adet Tam Yetkili Araç):\n"
            "- Dosya & Kod Düzenleme: write_file, read_file, list_directory, copy_move_delete, search_files, code_edit, patch_apply, symbol_search, code_format, file_watch\n"
            "- Yazılım & Git & LSP: git_manage, project_analyze, test_runner, lsp_query\n"
            "- Konteyner & K8s: docker_manage, k8s_manage\n"
            "- Sistem & Süreç: execute_command, get_process_list, kill_process, manage_service\n"
            "- Uzak Yönetim: invoke_remote_command, create_pssession, copy_to_remote, copy_from_remote, test_connection\n"
            "- Windows İleri Seviye: registry_read_write, wmi_query, event_log_query, scheduled_task_manage\n"
            "- Ağ, REST & DB: http_request, db_query\n\n"
            f"Kullanıcının Masaüstü (Desktop) yolu: '{desktop_folder}'.\n\n"
            "KURALLAR:\n"
            "1. Yerel, kod, git, test, veritabanı veya sistem işlemlerinde araçları derhal çağır ve görevi tamamla.\n"
            "2. Uzak bağlantılarda hedef IP/bilgisayar adı, kullanıcı adı (username) ve şifre (password) eksikse kullanıcıdan nezaketle iste."
        )
    }
]

print("==========================================================")
print("🚀 MÜKEMMEL TAM OTOMASYONLU AI AGENT & KOD/SİSTEM YÖNETİCİSİ")
print("✅ 31 Adet Tam Yetkili Araç (Git, LSP, Test, Docker, K8s, DB, Patch, Format) Aktif!")
print(f"📁 Masaüstü Yolu: {desktop_folder}")
print("🚪 Çıkmak için 'exit' veya 'quit' yazabilirsiniz.")
print("==========================================================\n")

while True:
    try:
        user_prompt = input("\nSiz: ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\nSohbet sonlandırıldı.")
        break

    if not user_prompt:
        continue

    if user_prompt.lower() in ["exit", "quit"]:
        print("Sohbet sonlandırıldı.")
        break

    messages.append({"role": "user", "content": user_prompt})

    while True:
        max_retries = 5
        retry_delay = 2
        success = False
        tool_calls_accumulator = {}
        assistant_response = ""

        for attempt in range(1, max_retries + 1):
            try:
                completion = client.chat.completions.create(
                    model="nvidia/nemotron-3-ultra-550b-a55b",
                    messages=messages,
                    tools=tools,
                    temperature=1,
                    top_p=0.95,
                    max_tokens=8192,
                    extra_body={"chat_template_kwargs": {"enable_thinking": True}, "reasoning_budget": 8192},
                    stream=True
                )

                has_reasoning = False
                has_started_content = False
                tool_calls_accumulator = {}
                assistant_response = ""

                for chunk in completion:
                    if not chunk.choices:
                        continue

                    delta = chunk.choices[0].delta

                    reasoning = getattr(delta, "reasoning_content", None)
                    if reasoning:
                        if not has_reasoning:
                            print("\n[Düşünce Süreci]:\n", end="", flush=True)
                            has_reasoning = True
                        print(reasoning, end="", flush=True)

                    if delta.tool_calls:
                        for tc in delta.tool_calls:
                            idx = tc.index
                            if idx not in tool_calls_accumulator:
                                tool_calls_accumulator[idx] = {
                                    "id": tc.id or "",
                                    "name": tc.function.name if tc.function and tc.function.name else "",
                                    "arguments": tc.function.arguments if tc.function and tc.function.arguments else ""
                                }
                            else:
                                if tc.id:
                                    tool_calls_accumulator[idx]["id"] += tc.id
                                if tc.function:
                                    if tc.function.name:
                                        tool_calls_accumulator[idx]["name"] += tc.function.name
                                    if tc.function.arguments:
                                        tool_calls_accumulator[idx]["arguments"] += tc.function.arguments

                    if delta.content is not None:
                        if not has_started_content:
                            if has_reasoning:
                                print("\n\n[Cevap]:\n", end="", flush=True)
                            else:
                                print("\n[Cevap]:\n", end="", flush=True)
                            has_started_content = True
                        print(delta.content, end="", flush=True)
                        assistant_response += delta.content

                print()
                success = True
                break

            except Exception as e:
                err_msg = str(e)
                if ("ResourceExhausted" in err_msg or "32/32" in err_msg or "429" in err_msg or "limit" in err_msg.lower()) and attempt < max_retries:
                    print(f"\n[Sunucu Yoğun ({attempt}/{max_retries})]: NVIDIA sunucu worker limiti (32/32) dolu. {retry_delay} sn içinde otomatik tekrar deneniyor...")
                    time.sleep(retry_delay)
                    retry_delay += 2
                    continue
                else:
                    print(f"\n[API Uyarısı/Hatası]: {e}")
                    print("NVIDIA API istek limiti veya ağ hatası oluştu.")
                    if messages and messages[-1]["role"] == "user":
                        messages.pop()
                    break

        if not success:
            break

        if tool_calls_accumulator:
            tool_calls_list = []
            for idx in sorted(tool_calls_accumulator.keys()):
                tc_info = tool_calls_accumulator[idx]
                tool_calls_list.append({
                    "id": tc_info["id"],
                    "type": "function",
                    "function": {
                        "name": tc_info["name"],
                        "arguments": tc_info["arguments"]
                    }
                })

            messages.append({
                "role": "assistant",
                "content": assistant_response if assistant_response else None,
                "tool_calls": tool_calls_list
            })

            for tc_info in tool_calls_list:
                func_name = tc_info["function"]["name"]
                try:
                    func_args = json.loads(tc_info["function"]["arguments"])
                except Exception:
                    func_args = {}

                print(f"\n[Araç Çalıştırılıyor: {func_name}] (Parametreler: {func_args})")
                tool_result = execute_tool(func_name, func_args)
                print(f"[Araç Sonucu]: {tool_result}")

                messages.append({
                    "role": "tool",
                    "tool_call_id": tc_info["id"],
                    "content": tool_result
                })

            continue
        else:
            if assistant_response:
                messages.append({"role": "assistant", "content": assistant_response})
            break