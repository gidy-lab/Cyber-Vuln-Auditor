import os
import sys

# Version and Metadata
VERSION = "1.1.0"
AUTHOR = "Gidy"
LOCATION = os.getcwd()

print(f"--- Cybersecurity Auditor v{VERSION} ---")
print(f"--- Author: {AUTHOR} ---")
print(f"--- Current Scan Directory: {LOCATION} ---")
print("-" * 40)

# Your existing audit code goes here...
import subprocess
import datetime

def run_audit(target):
    print(f"[*] Starting Security Audit for: {target}")
    
    # Run Nmap Service Detection
    print("[*] Scanning for services... (Please wait)")
    # -sV detects versions, -T4 is for speed
    cmd = f"nmap -sV -T4 {target}"
    result = subprocess.check_output(cmd, shell=True).decode()
    
    # Create the Report File
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    report_name = f"Audit_Report_{timestamp}.md"
    
    with open(report_name, "w") as report:
        report.write(f"# Security Audit Report\n")
        report.write(f"**Target IP:** {target}\n")
        report.write(f"**Date:** {datetime.datetime.now()}\n\n")
        report.write(f"## 1. Raw Scan Results\n```\n{result}\n```\n")
        
        # Logic to find the specific backdoor
        report.write(f"## 2. Critical Findings\n")
        if "vsftpd 2.3.4" in result:
            report.write("### [CRITICAL] vsFTPd 2.3.4 Backdoor Detected\n")
            report.write("- **Vulnerability:** CVE-2011-2523\n")
            report.write("- **Impact:** Allows remote root access to the system.\n")
            report.write("- **Remediation:** Remove this version and install a patched FTP service.\n")
        else:
            report.write("No critical known backdoors detected in this scan.\n")
            
    print(f"[+] Audit Complete! Report saved as: {report_name}")

if __name__ == "__main__":
    target_ip = input("Enter Target IP (Metasploitable): ")
    run_audit(target_ip)