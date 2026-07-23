export interface ToolItem {
  id: string;
  name: string;
  category: 'Dosya & Kod' | 'Yazılım & Git' | 'Konteyner & K8s' | 'Sistem & Süreç' | 'Uzak Yönetim' | 'Windows İleri' | 'Ağ & DB';
  description: string;
  parameters: { name: string; type: string; required: boolean; description: string }[];
  example: string;
}

export const TOOLS_LIST: ToolItem[] = [
  // Dosya & Kod (10)
  {
    id: 'write_file',
    name: 'write_file',
    category: 'Dosya & Kod',
    description: 'Belirtilen yola içerik yazar veya atomik olarak yeni dosya oluşturur.',
    parameters: [
      { name: 'path', type: 'string', required: true, description: 'Yazılacak dosyanın tam yolu' },
      { name: 'content', type: 'string', required: true, description: 'Dosya içeriği' }
    ],
    example: 'write_file(path="src/main.py", content="print(\'Hello World\')")'
  },
  {
    id: 'read_file',
    name: 'read_file',
    category: 'Dosya & Kod',
    description: 'Belirtilen dosyanın içeriğini veya belirli satır aralığını okur.',
    parameters: [
      { name: 'path', type: 'string', required: true, description: 'Okunacak dosyanın yolu' },
      { name: 'start_line', type: 'number', required: false, description: 'Başlangıç satırı' },
      { name: 'end_line', type: 'number', required: false, description: 'Bitiş satırı' }
    ],
    example: 'read_file(path="README.md", start_line=1, end_line=50)'
  },
  {
    id: 'list_directory',
    name: 'list_directory',
    category: 'Dosya & Kod',
    description: 'Dizin içeriğini listeler, dosya ve klasör boyutlarını gösterir.',
    parameters: [
      { name: 'path', type: 'string', required: true, description: 'Listelenecek dizin yolu' }
    ],
    example: 'list_directory(path="./src")'
  },
  {
    id: 'copy_move_delete',
    name: 'copy_move_delete',
    category: 'Dosya & Kod',
    description: 'Dosya veya klasörleri kopyalar, taşır ya da siler.',
    parameters: [
      { name: 'action', type: 'string', required: true, description: 'copy | move | delete' },
      { name: 'src', type: 'string', required: true, description: 'Kaynak yol' },
      { name: 'dest', type: 'string', required: false, description: 'Hedef yol (silme hariç)' }
    ],
    example: 'copy_move_delete(action="copy", src="./main.py", dest="./backup/main.py")'
  },
  {
    id: 'search_files',
    name: 'search_files',
    category: 'Dosya & Kod',
    description: 'Regex veya metin araması ile proje dosyaları içinde arama yapar.',
    parameters: [
      { name: 'query', type: 'string', required: true, description: 'Aranacak kelime veya regex' },
      { name: 'path', type: 'string', required: false, description: 'Aranacak kök dizin' }
    ],
    example: 'search_files(query="FastAPI", path="./src")'
  },
  {
    id: 'code_edit',
    name: 'code_edit',
    category: 'Dosya & Kod',
    description: 'Dosyadaki belirli kod bloklarını güvenli biçimde günceller.',
    parameters: [
      { name: 'path', type: 'string', required: true, description: 'Düzenlenecek dosya yolu' },
      { name: 'target_text', type: 'string', required: true, description: 'Değiştirilecek eski blok' },
      { name: 'replacement_text', type: 'string', required: true, description: 'Yeni kod bloğu' }
    ],
    example: 'code_edit(path="config.py", target_text="DEBUG=False", replacement_text="DEBUG=True")'
  },
  {
    id: 'patch_apply',
    name: 'patch_apply',
    category: 'Dosya & Kod',
    description: 'Standard diff/patch formatındaki değişiklikleri dosyaya uygular.',
    parameters: [
      { name: 'patch_content', type: 'string', required: true, description: 'Unified diff formatında yamalama içeriği' }
    ],
    example: 'patch_apply(patch_content="--- a/file.py\n+++ b/file.py...")'
  },
  {
    id: 'symbol_search',
    name: 'symbol_search',
    category: 'Dosya & Kod',
    description: 'Kod tabanında sınıf, fonksiyon veya değişken tanımlarını bulur.',
    parameters: [
      { name: 'symbol_name', type: 'string', required: true, description: 'Aranacak sembol adı' }
    ],
    example: 'symbol_search(symbol_name="AgentLoop")'
  },
  {
    id: 'code_format',
    name: 'code_format',
    category: 'Dosya & Kod',
    description: 'Ruff, Black, Prettier veya Gofmt kullanarak kodu otomatik biçimlendirir.',
    parameters: [
      { name: 'path', type: 'string', required: true, description: 'Biçimlendirilecek dosya veya dizin' }
    ],
    example: 'code_format(path="src/ai_agent/core/llm_client.py")'
  },
  {
    id: 'file_watch',
    name: 'file_watch',
    category: 'Dosya & Kod',
    description: 'Dosya sistemindeki değişiklikleri canlı olarak dinler.',
    parameters: [
      { name: 'path', type: 'string', required: true, description: 'Dinlenecek dizin yolu' }
    ],
    example: 'file_watch(path="./src")'
  },

  // Yazılım & Git (4)
  {
    id: 'git_manage',
    name: 'git_manage',
    category: 'Yazılım & Git',
    description: 'Git versiyon kontrolü işlemlerini yönetir (status, commit, branch, push, pull).',
    parameters: [
      { name: 'command', type: 'string', required: true, description: 'status | commit | branch | push | checkout' },
      { name: 'args', type: 'string', required: false, description: 'Komut argümanları' }
    ],
    example: 'git_manage(command="status")'
  },
  {
    id: 'project_analyze',
    name: 'project_analyze',
    category: 'Yazılım & Git',
    description: 'Proje yapısını, bağımlılık haritasını ve mimari sağlığı analiz eder.',
    parameters: [
      { name: 'root_dir', type: 'string', required: true, description: 'Proje kök dizini' }
    ],
    example: 'project_analyze(root_dir=".")'
  },
  {
    id: 'test_runner',
    name: 'test_runner',
    category: 'Yazılım & Git',
    description: 'Pytest, Jest, Go test vb. test suite\'lerini çalıştırır ve raporlar.',
    parameters: [
      { name: 'framework', type: 'string', required: true, description: 'pytest | jest | unittest' },
      { name: 'target', type: 'string', required: false, description: 'Çalıştırılacak test yolu' }
    ],
    example: 'test_runner(framework="pytest", target="tests/unit")'
  },
  {
    id: 'lsp_query',
    name: 'lsp_query',
    category: 'Yazılım & Git',
    description: 'Language Server Protocol ile linter hatalarını ve tip uyarılarını sorgular.',
    parameters: [
      { name: 'file_path', type: 'string', required: true, description: 'Analiz edilecek dosya' }
    ],
    example: 'lsp_query(file_path="src/main.py")'
  },

  // Konteyner & K8s (2)
  {
    id: 'docker_manage',
    name: 'docker_manage',
    category: 'Konteyner & K8s',
    description: 'Docker konteynerlerini, imajlarını ve docker-compose servislerini yönetir.',
    parameters: [
      { name: 'subcommand', type: 'string', required: true, description: 'ps | logs | build | up | stop' },
      { name: 'container_id', type: 'string', required: false, description: 'Konteyner ID veya adı' }
    ],
    example: 'docker_manage(subcommand="ps")'
  },
  {
    id: 'k8s_manage',
    name: 'k8s_manage',
    category: 'Konteyner & K8s',
    description: 'Kubernetes pod, deployment ve servislerini kubectl arayüzü ile denetler.',
    parameters: [
      { name: 'resource', type: 'string', required: true, description: 'pods | services | deployments' },
      { name: 'namespace', type: 'string', required: false, description: 'Kubernetes namespace' }
    ],
    example: 'k8s_manage(resource="pods", namespace="default")'
  },

  // Sistem & Süreç (4)
  {
    id: 'execute_command',
    name: 'execute_command',
    category: 'Sistem & Süreç',
    description: 'Güvenlik sınırı içinde yetkili Shell / PowerShell komutlarını çalıştırır.',
    parameters: [
      { name: 'command', type: 'string', required: true, description: 'Çalıştırılacak komut' }
    ],
    example: 'execute_command(command="dir")'
  },
  {
    id: 'get_process_list',
    name: 'get_process_list',
    category: 'Sistem & Süreç',
    description: 'Çalışan aktif süreçleri (PID, CPU, RAM kullanımı) listeler.',
    parameters: [
      { name: 'filter_name', type: 'string', required: false, description: 'Süreç adı filtresi' }
    ],
    example: 'get_process_list(filter_name="python")'
  },
  {
    id: 'kill_process',
    name: 'kill_process',
    category: 'Sistem & Süreç',
    description: 'PID veya süreç adıyla belirtilen süreci sonlandırır.',
    parameters: [
      { name: 'pid', type: 'number', required: true, description: 'Sonlandırılacak süreç PID\'si' }
    ],
    example: 'kill_process(pid=1234)'
  },
  {
    id: 'manage_service',
    name: 'manage_service',
    category: 'Sistem & Süreç',
    description: 'Windows Servislerini veya systemd daemon\'larını yönetir (status, start, stop).',
    parameters: [
      { name: 'service_name', type: 'string', required: true, description: 'Servis adı' },
      { name: 'action', type: 'string', required: true, description: 'status | start | stop | restart' }
    ],
    example: 'manage_service(service_name="wuauserv", action="status")'
  },

  // Uzak Yönetim (5)
  {
    id: 'invoke_remote_command',
    name: 'invoke_remote_command',
    category: 'Uzak Yönetim',
    description: 'WinRM veya SSH protokolü ile uzak sunucuda komut çalıştırır.',
    parameters: [
      { name: 'target_host', type: 'string', required: true, description: 'Hedef sunucu IP veya hostname' },
      { name: 'command', type: 'string', required: true, description: 'Uzakta çalışacak komut' }
    ],
    example: 'invoke_remote_command(target_host="192.168.1.50", command="hostname")'
  },
  {
    id: 'create_pssession',
    name: 'create_pssession',
    category: 'Uzak Yönetim',
    description: 'Uzak Windows sunucusu ile kalıcı PSSession oturumu açar.',
    parameters: [
      { name: 'computer_name', type: 'string', required: true, description: 'Hedef bilgisayar adı' }
    ],
    example: 'create_pssession(computer_name="SRV-DEV-01")'
  },
  {
    id: 'copy_to_remote',
    name: 'copy_to_remote',
    category: 'Uzak Yönetim',
    description: 'Yerel dosyaları uzak sunucuya transfer eder (WinRM/SCP).',
    parameters: [
      { name: 'local_path', type: 'string', required: true, description: 'Yerel dosya yolu' },
      { name: 'remote_path', type: 'string', required: true, description: 'Uzak dosya yolu' }
    ],
    example: 'copy_to_remote(local_path="./app.zip", remote_path="C:\\deploy\\app.zip")'
  },
  {
    id: 'copy_from_remote',
    name: 'copy_from_remote',
    category: 'Uzak Yönetim',
    description: 'Uzak sunucudan yerel ortama dosya indirir.',
    parameters: [
      { name: 'remote_path', type: 'string', required: true, description: 'Uzak dosya yolu' },
      { name: 'local_path', type: 'string', required: true, description: 'Yerel hedef yolu' }
    ],
    example: 'copy_from_remote(remote_path="C:\\logs\\app.log", local_path="./logs/remote.log")'
  },
  {
    id: 'test_connection',
    name: 'test_connection',
    category: 'Uzak Yönetim',
    description: 'Uzak sunucu ping, WinRM ve SSH port bağlantı durumunu test eder.',
    parameters: [
      { name: 'host', type: 'string', required: true, description: 'Test edilecek IP veya domain' }
    ],
    example: 'test_connection(host="10.0.0.1")'
  },

  // Windows İleri (4)
  {
    id: 'registry_read_write',
    name: 'registry_read_write',
    category: 'Windows İleri',
    description: 'Windows Kayıt Defteri (Registry) anahtarlarını okur veya yazar.',
    parameters: [
      { name: 'operation', type: 'string', required: true, description: 'read | write' },
      { name: 'key_path', type: 'string', required: true, description: 'Registry yolu' },
      { name: 'value_name', type: 'string', required: false, description: 'Değer adı' }
    ],
    example: 'registry_read_write(operation="read", key_path="HKLM:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion")'
  },
  {
    id: 'wmi_query',
    name: 'wmi_query',
    category: 'Windows İleri',
    description: 'Windows Management Instrumentation (WMI / CIM) sorguları çalıştırır.',
    parameters: [
      { name: 'wmi_class', type: 'string', required: true, description: 'Win32_OperatingSystem | Win32_LogicalDisk vb.' }
    ],
    example: 'wmi_query(wmi_class="Win32_Processor")'
  },
  {
    id: 'event_log_query',
    name: 'event_log_query',
    category: 'Windows İleri',
    description: 'Windows Olay Günlüklerini (System, Application, Security) filtreleyerek sorgular.',
    parameters: [
      { name: 'log_name', type: 'string', required: true, description: 'System | Application | Security' },
      { name: 'entry_type', type: 'string', required: false, description: 'Error | Warning | Information' }
    ],
    example: 'event_log_query(log_name="System", entry_type="Error")'
  },
  {
    id: 'scheduled_task_manage',
    name: 'scheduled_task_manage',
    category: 'Windows İleri',
    description: 'Windows Görev Zamanlayıcısı (Task Scheduler) görevlerini denetler.',
    parameters: [
      { name: 'task_name', type: 'string', required: true, description: 'Görev adı' },
      { name: 'action', type: 'string', required: true, description: 'list | run | stop | enable' }
    ],
    example: 'scheduled_task_manage(task_name="BackupTask", action="run")'
  },

  // Ağ & DB (2)
  {
    id: 'http_request',
    name: 'http_request',
    category: 'Ağ & DB',
    description: 'REST API endpoint\'lerine GET, POST, PUT, DELETE HTTP istekleri gönderir.',
    parameters: [
      { name: 'method', type: 'string', required: true, description: 'GET | POST | PUT | DELETE' },
      { name: 'url', type: 'string', required: true, description: 'Hedef URL' },
      { name: 'payload', type: 'string', required: false, description: 'JSON gövde içeriği' }
    ],
    example: 'http_request(method="GET", url="https://api.github.com/zen")'
  },
  {
    id: 'db_query',
    name: 'db_query',
    category: 'Ağ & DB',
    description: 'SQLite veritabanlarında SQL sorguları (SELECT, INSERT, UPDATE) çalıştırır.',
    parameters: [
      { name: 'db_path', type: 'string', required: true, description: 'Veritabanı dosya yolu' },
      { name: 'query', type: 'string', required: true, description: 'SQL ifadesi' }
    ],
    example: 'db_query(db_path="./app_data.db", query="SELECT * FROM sessions LIMIT 10")'
  }
];
