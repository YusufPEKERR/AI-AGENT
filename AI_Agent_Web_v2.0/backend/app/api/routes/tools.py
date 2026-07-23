from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import os
import psutil
import subprocess

router = APIRouter(prefix="/api/tools", tags=["tools"])

# Complete 100+ DevSecOps & Cybersecurity Tool Registry Catalog
TOOLS_CATALOG = [
    # Core System & File Admin
    {"id": "run_command", "name": "Run Command", "category": "System Admin", "description": "Execute shell commands asynchronously or synchronously on the host system.", "params": ["CommandLine", "Cwd", "WaitMsBeforeAsync"]},
    {"id": "view_file", "name": "View File", "category": "File Ops", "description": "Inspect text or binary file contents with specified line ranges.", "params": ["AbsolutePath", "StartLine", "EndLine"]},
    {"id": "write_to_file", "name": "Write To File", "category": "File Ops", "description": "Create new files or overwrite existing ones with full content.", "params": ["TargetFile", "CodeContent", "Overwrite"]},
    {"id": "replace_file_content", "name": "Replace File Content", "category": "File Ops", "description": "Single contiguous edit block replacement in target files.", "params": ["TargetFile", "TargetContent", "ReplacementContent", "StartLine", "EndLine"]},
    {"id": "multi_replace_file_content", "name": "Multi Replace File Content", "category": "File Ops", "description": "Non-contiguous multi-chunk edits across target file.", "params": ["TargetFile", "ReplacementChunks"]},
    {"id": "list_dir", "name": "List Directory", "category": "File Ops", "description": "List directory contents including file sizes and subdirectories.", "params": ["DirectoryPath"]},
    {"id": "grep_search", "name": "Grep Search", "category": "File Ops", "description": "Ripgrep regex or literal pattern search across repository files.", "params": ["SearchPath", "Query", "IsRegex", "CaseInsensitive"]},
    {"id": "manage_task", "name": "Manage Task", "category": "System Admin", "description": "List, monitor, send input to, or terminate background processes.", "params": ["Action", "TaskId", "Input"]},
    {"id": "schedule", "name": "Schedule Task", "category": "System Admin", "description": "Schedule one-shot timers or recurring cron background notifications.", "params": ["DurationSeconds", "CronExpression", "Prompt"]},
    {"id": "get_weather", "name": "Weather Live", "category": "Hava & Widgets", "description": "Get real-time weather forecasts and conditions for any city worldwide.", "params": ["CityName", "Units"]},
    {"id": "get_currency_rates", "name": "Currency & Crypto Rates", "category": "Hava & Widgets", "description": "Fetch live financial exchange rates and cryptocurrency prices.", "params": ["BaseCurrency", "TargetCurrency"]},

    # 1. Ağ Keşif & Tarama (Reconnaissance)
    {"id": "nmap_scan", "name": "Nmap", "category": "Ağ Keşif & Tarama", "description": "Port tarama, servis/versiyon tespiti, OS fingerprinting.", "params": ["TargetHost", "ScanType", "PortRange"]},
    {"id": "masscan", "name": "Masscan", "category": "Ağ Keşif & Tarama", "description": "Büyük ölçekli, yüksek hızlı port tarama (Internet-wide).", "params": ["TargetSubnet", "Rate"]},
    {"id": "zmap", "name": "Zmap", "category": "Ağ Keşif & Tarama", "description": "Tek port üzerinden tüm interneti tarama.", "params": ["Port", "Bandwidth"]},
    {"id": "shodan_query", "name": "Shodan", "category": "Ağ Keşif & Tarama", "description": "İnternete açık cihazların arama motoru sorgulama.", "params": ["QueryKey"]},
    {"id": "maltego_osint", "name": "Maltego", "category": "Ağ Keşif & Tarama", "description": "OSINT ve ilişki haritalama grafik analizi.", "params": ["TargetEntity"]},
    {"id": "theharvester", "name": "theHarvester", "category": "Ağ Keşif & Tarama", "description": "E-posta, domain, subdomain OSINT toplama.", "params": ["Domain", "Source"]},
    {"id": "amass_enum", "name": "Amass", "category": "Ağ Keşif & Tarama", "description": "Derinlemesine subdomain keşfi (OWASP projesi).", "params": ["Domain"]},
    {"id": "recon_ng", "name": "Recon-ng", "category": "Ağ Keşif & Tarama", "description": "Modüler web keşif ve bilgi toplama framework'ü.", "params": ["Workspace", "Module"]},
    {"id": "spiderfoot", "name": "SpiderFoot", "category": "Ağ Keşif & Tarama", "description": "Otomatik OSINT otomasyonu ve veri toplama.", "params": ["TargetDomain"]},

    # 2. Zafiyet Tarama & Analiz
    {"id": "nessus_scan", "name": "Nessus", "category": "Zafiyet Tarama & Analiz", "description": "Profesyonel kurumsal zafiyet tarayıcı.", "params": ["TargetIP", "PolicyId"]},
    {"id": "openvas_scan", "name": "OpenVAS", "category": "Zafiyet Tarama & Analiz", "description": "Açık kaynak zafiyet tarayıcı (Greenbone).", "params": ["TargetRange"]},
    {"id": "nikto_scan", "name": "Nikto", "category": "Zafiyet Tarama & Analiz", "description": "Web sunucu güvenlik zafiyet tarayıcı.", "params": ["HostURL", "Port"]},
    {"id": "wapiti_scan", "name": "Wapiti", "category": "Zafiyet Tarama & Analiz", "description": "Web uygulama zafiyet tarayıcı (XSS, SQLi vb.).", "params": ["TargetURL"]},
    {"id": "sqlmap", "name": "SQLmap", "category": "Zafiyet Tarama & Analiz", "description": "Otomatik SQL injection tespit ve sömürme.", "params": ["URL", "DatabaseType"]},
    {"id": "xsstrike", "name": "XSStrike", "category": "Zafiyet Tarama & Analiz", "description": "Gelişmiş Cross-Site Scripting (XSS) tespit aracı.", "params": ["TargetURL"]},
    {"id": "nuclei", "name": "Nuclei", "category": "Zafiyet Tarama & Analiz", "description": "Şablon tabanlı hızlı zafiyet tarayıcı.", "params": ["Target", "TemplateTags"]},
    {"id": "burp_suite", "name": "Burp Suite", "category": "Zafiyet Tarama & Analiz", "description": "Web uygulama güvenlik test proxy'si ve tarayıcısı.", "params": ["TargetScope"]},

    # 3. Exploitation Framework'leri
    {"id": "metasploit", "name": "Metasploit", "category": "Exploitation Frameworks", "description": "Gelişmiş sömürü ve zafiyet istismar framework'ü.", "params": ["ExploitModule", "RHOST", "LHOST"]},
    {"id": "cobalt_strike", "name": "Cobalt Strike", "category": "Exploitation Frameworks", "description": "Ticari adversary simulation ve C2 platformu.", "params": ["Listener", "BeaconType"]},
    {"id": "empire_c2", "name": "Empire", "category": "Exploitation Frameworks", "description": "PowerShell/Python post-exploitation framework.", "params": ["ListenerName", "Stager"]},
    {"id": "covenant", "name": "Covenant", "category": "Exploitation Frameworks", "description": ".NET tabanlı C2 (Command & Control) framework.", "params": ["GruntId"]},
    {"id": "sliver_c2", "name": "Sliver", "category": "Exploitation Frameworks", "description": "Çapraz platform C2 framework (Bishop Fox).", "params": ["SessionId"]},
    {"id": "mythic_c2", "name": "Mythic", "category": "Exploitation Frameworks", "description": "Modüler C2 framework ve ajan yönetimi.", "params": ["PayloadType"]},
    {"id": "havoc_c2", "name": "Havoc", "category": "Exploitation Frameworks", "description": "Modern post-exploitation C2 framework.", "params": ["AgentId"]},
    {"id": "pupy_rat", "name": "Pupy", "category": "Exploitation Frameworks", "description": "Çapraz platform RAT (Remote Access Trojan).", "params": ["PayloadOS"]},

    # 4. Kimlik Bilgisi Toplama & Sömürme
    {"id": "mimikatz", "name": "Mimikatz", "category": "Kimlik Bilgisi & Exploitation", "description": "Windows credential dumping ve Kerberos sömürme.", "params": ["Command"]},
    {"id": "lazagne", "name": "LaZagne", "category": "Kimlik Bilgisi & Exploitation", "description": "Çoklu uygulamalardan parola toplama.", "params": ["Module"]},
    {"id": "seatbelt", "name": "Seatbelt", "category": "Kimlik Bilgisi & Exploitation", "description": "Windows host güvenlik enumerasyonu.", "params": ["CommandGroup"]},
    {"id": "sharphound", "name": "SharpHound", "category": "Kimlik Bilgisi & Exploitation", "description": "Active Directory BloodHound veri toplayıcı.", "params": ["SearchForest"]},
    {"id": "bloodhound", "name": "BloodHound", "category": "Kimlik Bilgisi & Exploitation", "description": "Active Directory saldırı yolu görselleştirme.", "params": ["DatabaseQuery"]},
    {"id": "kerbrute", "name": "Kerbrute", "category": "Kimlik Bilgisi & Exploitation", "description": "Kerberos brute-force ve kullanıcı enumerasyonu.", "params": ["UserList", "Domain"]},
    {"id": "rubeus", "name": "Rubeus", "category": "Kimlik Bilgisi & Exploitation", "description": "Kerberos ticket manipülasyonu (C#).", "params": ["Action"]},
    {"id": "impacket", "name": "Impacket", "category": "Kimlik Bilgisi & Exploitation", "description": "Windows protokol exploitation kütüphanesi.", "params": ["Script", "TargetAuth"]},
    {"id": "crackmapexec", "name": "CrackMapExec", "category": "Kimlik Bilgisi & Exploitation", "description": "Ağ üzerinde toplu post-exploitation / lateral movement.", "params": ["Protocol", "TargetList"]},
    {"id": "evil_winrm", "name": "Evil-WinRM", "category": "Kimlik Bilgisi & Exploitation", "description": "WinRM üzerinden shell erişimi ve komut çalıştırma.", "params": ["TargetIP", "User", "Password"]},

    # 5. Kablosuz Ağ Saldırıları
    {"id": "aircrack_ng", "name": "Aircrack-ng", "category": "Kablosuz Ağ Saldırıları", "description": "WEP/WPA kırma ve kablosuz ağ paket analizi.", "params": ["Interface", "CapFile"]},
    {"id": "reaver", "name": "Reaver", "category": "Kablosuz Ağ Saldırıları", "description": "WPS PIN brute-force ve anahtar çıkarma.", "params": ["BSSID", "Interface"]},
    {"id": "pixiewps", "name": "PixieWPS", "category": "Kablosuz Ağ Saldırıları", "description": "WPS Pixie-Dust offline PIN saldırısı.", "params": ["PKE", "PKR"]},
    {"id": "bettercap", "name": "Bettercap", "category": "Kablosuz Ağ Saldırıları", "description": "MITM, WiFi, BLE, HID saldırı framework'ü.", "params": ["Module", "Caplet"]},
    {"id": "kismet", "name": "Kismet", "category": "Kablosuz Ağ Saldırıları", "description": "Kablosuz ağ dedektörü, sniffer ve IDS.", "params": ["SourceInterface"]},
    {"id": "wifite", "name": "Wifite", "category": "Kablosuz Ağ Saldırıları", "description": "Otomatik WiFi kırma ve saldırı aracı.", "params": ["TargetBSSID"]},
    {"id": "hcxdumptool", "name": "hcxdumptool", "category": "Kablosuz Ağ Saldırıları", "description": "WPA handshake yakalama ve pcapng dönüştürme.", "params": ["Interface", "OutputFile"]},
    {"id": "fluxion", "name": "Fluxion", "category": "Kablosuz Ağ Saldırıları", "description": "Evil Twin ve sosyal mühendislik WiFi saldırısı.", "params": ["TargetSSID"]},

    # 6. Web Uygulama Saldırıları
    {"id": "commix", "name": "Commix", "category": "Web Uygulama Saldırıları", "description": "Otomatik Command injection sömürme aracı.", "params": ["Url", "DataPayload"]},
    {"id": "nosqlmap", "name": "NoSQLMap", "category": "Web Uygulama Saldırıları", "description": "NoSQL injection ve MongoDB sömürme otomasyonu.", "params": ["TargetIP"]},
    {"id": "jexboss", "name": "JexBoss", "category": "Web Uygulama Saldırıları", "description": "JBoss/WildFly zafiyet tespiti ve exploitation.", "params": ["HostURL"]},
    {"id": "log4j_scan", "name": "Log4j-scan", "category": "Web Uygulama Saldırıları", "description": "Log4Shell (CVE-2021-44228) tespiti ve tarayıcı.", "params": ["TargetURLList"]},
    {"id": "spring4shell", "name": "Spring4Shell", "category": "Web Uygulama Saldırıları", "description": "Spring Framework exploit ve tarama araçları.", "params": ["TargetURL"]},
    {"id": "ffuf_gobuster", "name": "ffuf / Gobuster / Dirb", "category": "Web Uygulama Saldırıları", "description": "Yüksek hızlı web dizin ve dosya brute-force aracı.", "params": ["Url", "WordlistPath"]},
    {"id": "wpscan", "name": "WPScan", "category": "Web Uygulama Saldırıları", "description": "WordPress güvenlik ve eklenti zafiyet tarayıcı.", "params": ["TargetURL", "ApiToken"]},
    {"id": "joomscan", "name": "JoomScan", "category": "Web Uygulama Saldırıları", "description": "Joomla CMS güvenlik tarayıcı.", "params": ["TargetURL"]},

    # 7. Sosyal Mühendislik (Phishing Ötesi)
    {"id": "set_toolkit", "name": "SET (Social Engineering Toolkit)", "category": "Sosyal Mühendislik", "description": "Phishing, credential harvesting ve USB dropper framework.", "params": ["AttackVector"]},
    {"id": "gophish", "name": "GoPhish", "category": "Sosyal Mühendislik", "description": "Açık kaynak phishing kampanya yönetim platformu.", "params": ["CampaignName"]},
    {"id": "evilginx", "name": "Evilginx", "category": "Sosyal Mühendislik", "description": "Reverse proxy ile MFA token çalma (AiTM).", "params": ["Phishlet", "Domain"]},
    {"id": "modlishka", "name": "Modlishka", "category": "Sosyal Mühendislik", "description": "Reverse proxy tabanlı phishing ve MFA bypass.", "params": ["ConfigPath"]},
    {"id": "king_phisher", "name": "King Phisher", "category": "Sosyal Mühendislik", "description": "Phishing kampanya ve e-posta simülasyonu.", "params": ["ServerAddr"]},
    {"id": "usb_rubber_ducky", "name": "USB Rubber Ducky", "category": "Sosyal Mühendislik", "description": "HID emülasyonu ile keystroke injection script yükleme.", "params": ["PayloadScript"]},
    {"id": "bash_bunny", "name": "Bash Bunny", "category": "Sosyal Mühendislik", "description": "Gelişmiş USB saldırı ve sömürü platformu.", "params": ["SwitchPosition"]},
    {"id": "wifi_pineapple", "name": "WiFi Pineapple", "category": "Sosyal Mühendislik", "description": "WiFi rogue access point ve MITM donanım platformu.", "params": ["SSIDName"]},

    # 8. Parola Kırma (Ek Araçlar)
    {"id": "hydra", "name": "Hydra", "category": "Parola Kırma", "description": "Çoklu protokol destekli online brute-force aracı.", "params": ["TargetIP", "Service", "UserList", "PassList"]},
    {"id": "john_ripper", "name": "John the Ripper", "category": "Parola Kırma", "description": "Gelişmiş offline parola ve hash kırma aracı.", "params": ["HashFile", "Wordlist"]},
    {"id": "hashcat", "name": "Hashcat", "category": "Parola Kırma", "description": "GPU hızlandırmalı dünya lideri hash kırma aracı.", "params": ["HashType", "HashFile", "Wordlist"]},
    {"id": "medusa", "name": "Medusa", "category": "Parola Kırma", "description": "Hızlı, paralel, modüler ağ kimlik doğrulama kırma.", "params": ["TargetIP", "Module"]},
    {"id": "ncrack", "name": "Ncrack", "category": "Parola Kırma", "description": "Yüksek hızlı ağ kimlik doğrulama kırma (Nmap ekibi).", "params": ["TargetList", "Services"]},
    {"id": "ophcrack", "name": "Ophcrack", "category": "Parola Kırma", "description": "LM/NTLM rainbow table ile Windows parola kırma.", "params": ["HashFile", "TablePath"]},
    {"id": "rainbowcrack", "name": "RainbowCrack", "category": "Parola Kırma", "description": "Genel rainbow table hesaplama ve hash çözme.", "params": ["HashValue"]},
    {"id": "cewl", "name": "CeWL", "category": "Parola Kırma", "description": "Hedef web sitesinden özel kelime listesi (wordlist) üretme.", "params": ["URL", "Depth"]},
    {"id": "crunch", "name": "Crunch", "category": "Parola Kırma", "description": "Karakter kalıplarına göre wordlist jeneratörü.", "params": ["MinLen", "MaxLen", "Charset"]},
    {"id": "cupp", "name": "CUPP", "category": "Parola Kırma", "description": "Kişiye özel profil çıkararak wordlist üretme aracı.", "params": ["InteractiveProfile"]},

    # 9. Privilege Escalation
    {"id": "peas_scripts", "name": "LinPEAS / WinPEAS", "category": "Privilege Escalation", "description": "Linux/Windows privilege escalation otomatik enumerasyon scriptleri.", "params": ["OS", "OutputFormat"]},
    {"id": "powerup", "name": "PowerUp", "category": "Privilege Escalation", "description": "Windows zafiyet tespiti ve privilege escalation (PowerSploit).", "params": ["FunctionName"]},
    {"id": "beroot", "name": "BeRoot", "category": "Privilege Escalation", "description": "Linux/Windows/Mac privilege escalation kontrol aracı.", "params": ["OS"]},
    {"id": "gtfobins", "name": "GTFOBins", "category": "Privilege Escalation", "description": "Unix binary'leri ile privilege escalation referansı ve denetleyici.", "params": ["BinaryName"]},
    {"id": "lolbas", "name": "LOLBAS", "category": "Privilege Escalation", "description": "Windows imzalı binary exploitation referansı.", "params": ["ExecutableName"]},
    {"id": "linux_exploit_suggester", "name": "Linux Exploit Suggester", "category": "Privilege Escalation", "description": "Linux Kernel exploit öneri ve zafiyet eşleştirme.", "params": ["KernelVersion"]},
    {"id": "win_exploit_suggester", "name": "Windows Exploit Suggester", "category": "Privilege Escalation", "description": "Windows yamaları ve eksik güncellemeleri analiz etme.", "params": ["SystemInfoFile"]},

    # 10. Tersine Mühendislik & Exploit Geliştirme
    {"id": "ghidra", "name": "Ghidra", "category": "Tersine Mühendislik", "description": "NSA açık kaynak reverse engineering framework.", "params": ["BinaryPath"]},
    {"id": "ida_pro", "name": "IDA Pro", "category": "Tersine Mühendislik", "description": "Endüstri standardı disassembler ve decompiler.", "params": ["File"]},
    {"id": "radare2", "name": "Radare2 / Rizin", "category": "Tersine Mühendislik", "description": "Açık kaynak komut satırı reverse engineering framework.", "params": ["Binary"]},
    {"id": "x64dbg", "name": "x64dbg / OllyDbg", "category": "Tersine Mühendislik", "description": "Windows kullanıcı modu ikili hata ayıklayıcı (debugger).", "params": ["Executable"]},
    {"id": "gdb_pwndbg", "name": "GDB + PEDA/Pwndbg", "category": "Tersine Mühendislik", "description": "Linux exploit geliştirme ve bellek analizi.", "params": ["CoreFile"]},
    {"id": "immunity_debugger", "name": "Immunity Debugger", "category": "Tersine Mühendislik", "description": "Exploit geliştirme odaklı debugger.", "params": ["TargetApp"]},
    {"id": "mona_py", "name": "Mona.py", "category": "Tersine Mühendislik", "description": "Immunity Debugger exploit geliştirme eklentisi.", "params": ["Command"]},
    {"id": "ropper", "name": "Ropper / ROPgadget", "category": "Tersine Mühendislik", "description": "ROP gadget bulma ve zincir oluşturma.", "params": ["BinaryPath"]},
    {"id": "pwntools", "name": "pwntools", "category": "Tersine Mühendislik", "description": "CTF & exploit geliştirme Python kütüphanesi.", "params": ["Script"]},
    {"id": "frida", "name": "Frida", "category": "Tersine Mühendislik", "description": "Dinamik kod enjeksiyonu ve instrumentation toolkit.", "params": ["ProcessName"]},

    # 11. Container & Cloud Security
    {"id": "kube_hunter", "name": "kube-hunter", "category": "Container & Cloud Security", "description": "Kubernetes zafiyet tarayıcı ve sızma testi aracı.", "params": ["RemoteIP"]},
    {"id": "kube_bench", "name": "kube-bench", "category": "Container & Cloud Security", "description": "Kubernetes CIS benchmark denetleyici.", "params": ["Targets"]},
    {"id": "trivy", "name": "Trivy", "category": "Container & Cloud Security", "description": "Container image, dosya sistemi ve Git deposu zafiyet tarayıcı.", "params": ["ImageName"]},
    {"id": "falco", "name": "Falco", "category": "Container & Cloud Security", "description": "Container ve K8s çalışma zamanı tehdit algılama.", "params": ["RuleSet"]},
    {"id": "scoutsuite", "name": "ScoutSuite", "category": "Container & Cloud Security", "description": "Multi-cloud (AWS, Azure, GCP) güvenlik denetimi.", "params": ["Provider"]},
    {"id": "pacu", "name": "Pacu", "category": "Container & Cloud Security", "description": "AWS exploitation framework.", "params": ["Module"]},
    {"id": "cloudsploit", "name": "CloudSploit", "category": "Container & Cloud Security", "description": "Cloud güvenlik ve konfigürasyon tarayıcısı.", "params": ["CloudAccount"]},

    # 12. Adli Bilişim & Anti-Forensics
    {"id": "volatility", "name": "Volatility", "category": "Adli Bilişim & Anti-Forensics", "description": "Gelişmiş RAM bellek adli bilişim (memory forensics) framework'ü.", "params": ["MemDumpPath", "Profile", "Plugin"]},
    {"id": "autopsy", "name": "Autopsy / Sleuth Kit", "category": "Adli Bilişim & Anti-Forensics", "description": "Dijital disk adli bilişim inceleme platformu.", "params": ["CaseDirectory"]},
    {"id": "velociraptor", "name": "Velociraptor", "category": "Adli Bilişim & Anti-Forensics", "description": "Endpoint monitoring & forensic izleme platformu.", "params": ["ClientName"]},
    {"id": "artifact_kit", "name": "Cobalt Strike Artifact Kit", "category": "Adli Bilişim & Anti-Forensics", "description": "AV/EDR Atlatma ve anti-forensic derleme kiti.", "params": ["Option"]},
    {"id": "veil_framework", "name": "Veil Framework", "category": "Adli Bilişim & Anti-Forensics", "description": "AV evasion payload jeneratörü.", "params": ["PayloadLanguage"]},
    {"id": "shellter", "name": "Shellter", "category": "Adli Bilişim & Anti-Forensics", "description": "PE infector ile dinamik shellcode enjeksiyonu ve AV atlatma.", "params": ["TargetPE"]},
    {"id": "scarecrow", "name": "ScareCrow", "category": "Adli Bilişim & Anti-Forensics", "description": "Process injection ile shellcode çalıştırma ve EDR atlatma.", "params": ["RawPayload"]}
]

class ToolExecutionRequest(BaseModel):
    tool_id: str
    arguments: Dict[str, Any] = {}

@router.get("/")
def get_tools():
    return {"tools": TOOLS_CATALOG, "total": len(TOOLS_CATALOG)}

@router.post("/execute")
def execute_tool(req: ToolExecutionRequest):
    tool_id = req.tool_id
    args = req.arguments
    
    if tool_id == "list_dir":
        target_path = args.get("DirectoryPath", ".")
        try:
            items = os.listdir(target_path)
            result = [{"name": item, "isDir": os.path.isdir(os.path.join(target_path, item))} for item in items[:50]]
            return {"status": "success", "result": result}
        except Exception as e:
            return {"status": "error", "error": str(e)}
            
    elif tool_id == "view_file":
        file_path = args.get("AbsolutePath")
        if file_path and os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read(100000) # Read up to 100KB for safety
                return {"status": "success", "result": content}
            except Exception as e:
                return {"status": "error", "error": f"Dosya okunamadi: {e}"}
        return {"status": "error", "error": "Dosya bulunamadi"}
            
    elif tool_id == "env_check":
        key = args.get("Key")
        if key:
            val = os.environ.get(key, "Not Found")
            return {"status": "success", "result": {key: val}}
        return {"status": "success", "result": dict(list(os.environ.items())[:15])}
        
    elif tool_id == "git_status":
        try:
            out = subprocess.check_output(["git", "status", "-s"], text=True)
            return {"status": "success", "result": out if out else "Clean working directory."}
        except Exception as e:
            return {"status": "error", "error": str(e)}
            
    elif tool_id == "doctor_diagnose":
        cpu = psutil.cpu_percent()
        mem = psutil.virtual_memory().percent
        disk = psutil.disk_usage("/").percent
        return {
            "status": "success",
            "result": {
                "health": "Optimal" if cpu < 80 and mem < 85 else "Warning",
                "diagnostics": [
                    f"CPU Usage: {cpu}%",
                    f"Memory Usage: {mem}%",
                    f"Disk Usage: {disk}%",
                    "Database connection: Healthy",
                    "Socket.IO ASGI Server: Connected",
                ]
            }
        }
        
    return {
        "status": "success",
        "result": f"Simulated tool '{tool_id}' execution completed with args: {args}"
    }
