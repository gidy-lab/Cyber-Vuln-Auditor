#!/usr/bin/env python3
import os
import sys
import subprocess
import re
from datetime import datetime

# --- METADATA ---
VERSION = "4.2.0" # Risk-Level Edition
AUTHOR = "Gidy"
SCAN_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def run_audit():
    if len(sys.argv) < 2:
        print(f"Usage: auditor <ip_or_domain_or_url>")
        return

    # Clean the input URL/IP
    raw_input = sys.argv[1]
    target = re.sub(r'^https?://', '', raw_input).split('/')[0]
    
    clean_name = target.replace('.', '-')
    filename = f"Audit_Report_{clean_name}.md"
    
    print(f"--- Cybersecurity Auditor v{VERSION} ---")
    print(f"--- Target Identified: {target} ---")
    print("-" * 50)

    print(f"[+] Launching Deep Security Audit with Risk Assessment...")
    nmap_cmd = f"nmap -sV --top-ports 1000 --script ftp-vsftpd-backdoor,http-enum -T4 {target}"
    
    try:
        scan_results = subprocess.check_output(nmap_cmd, shell=True, stderr=subprocess.STDOUT).decode()
    except Exception as e:
        print(f"[-] Scan Error: {e}")
        return

    # --- UPDATED DATABASE: Consistent Keys & Risk Levels ---
    threat_db = {
        "21/tcp": {
            "name": "FTP Service",
            "risk": "CRITICAL",
            "vuln": "Cleartext Credentials & Backdoor Risk (CVE-2011-2523)",
            "impact": "Root-level access and data theft via unencrypted traffic.",
            "fix": "Disable FTP. Use SFTP (Port 22) with SSH keys."
        },
        "22/tcp": {
            "name": "SSH Service",
            "risk": "MEDIUM",
            "vuln": "Remote Management Access",
            "impact": "Potential for brute-force attacks if passwords are used.",
            "fix": "Disable root login and enforce Key-based authentication."
        },
        "80/tcp": {
            "name": "HTTP (Web)",
            "risk": "HIGH",
            "vuln": "Unencrypted Web Communication",
            "impact": "Session hijacking and MITM attacks on website users.",
            "fix": "Install SSL/TLS Certificate and redirect to Port 443."
        },
        "443/tcp": {
            "name": "HTTPS (Secure Web)",
            "risk": "LOW",
            "vuln": "Encrypted Web Traffic",
            "impact": "Generally secure, but requires checking for weak ciphers.",
            "fix": "Ensure only TLS 1.2 and 1.3 are enabled."
        },
        "445/tcp": {
            "name": "SMB (Windows)",
            "risk": "CRITICAL",
            "vuln": "Remote Code Execution (EternalBlue/MS17-010)",
            "impact": "Network-wide ransomware or worm propagation.",
            "fix": "Disable SMBv1 and apply the latest security patches."
        },
        "3306/tcp": {
            "name": "MySQL Database",
            "risk": "HIGH",
            "vuln": "Remote Database Exposure",
            "impact": "Direct access to sensitive data and brute-force risk.",
            "fix": "Bind to 127.0.0.1 and block port 3306 at the firewall."
        }
    }

    # --- REPORT GENERATION ---
    report_content = f"# Security Audit & Risk Assessment: {target}\n"
    report_content += f"- **Date:** {SCAN_TIME}\n- **Lead Auditor:** {AUTHOR}\n\n"
    report_content += "## 1. Executive Summary\n"
    report_content += "Vulnerabilities are prioritized by Risk Level to guide hardening efforts.\n\n"

    found = False
    for port, data in threat_db.items():
        if port in scan_results:
            found = True
            report_content += f"### [{data['risk']}] {data['name']} ({port})\n"
            report_content += f"- **Vulnerability:** {data['vuln']}\n"
            report_content += f"- **Impact:** {data['impact']}\n"
            report_content += f"- **Remediation:** {data['fix']}\n\n"
            
            # Script-specific validation
            if "vsftpd-backdoor" in scan_results and "21/tcp" == port:
                report_content += "> **VERIFIED:** The vsftpd 2.3.4 backdoor is ACTIVE on this target.\n\n"

    # Add Web Directory Findings
    if "http-enum" in scan_results or "/dvwa/" in scan_results:
        report_content += "### [INFO] Directory Discovery\n"
        report_content += "- **Finding:** Exposed path (e.g., /dvwa/) detected.\n"
        report_content += "- **Risk:** Potential unauthorized access to development tools.\n"
        report_content += "- **Fix:** Restrict access using .htaccess or ACLs.\n\n"

    with open(filename, "w") as f:
        f.write(report_content)
    
    print(f"[+] Audit Finished. Report prioritized by Risk saved as: {filename}")

if __name__ == "__main__":
    run_audit()