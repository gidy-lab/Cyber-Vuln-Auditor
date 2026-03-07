import os
import subprocess
from google import genai
from dotenv import load_dotenv

# 1. Initialize environment and client
load_dotenv()
# The client automatically picks up the 'GEMINI_API_KEY' from your .env file
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def get_ai_analysis(scan_output):
    """
    Attempts to use Gemini 3 Flash Preview. 
    If the preview has expired or renamed, it falls back to the stable Gemini 2.5 Flash.
    """
    # Priority order of models to try
    models_to_try = ["gemini-3-flash-preview", "gemini-2.5-flash"]
    
    for model_name in models_to_try:
        try:
            print(f"[*] Consulting {model_name} for expert analysis...")
            response = client.models.generate_content(
                model=model_name,
                contents=f"You are a professional cybersecurity auditor. Analyze the following Nmap scan results and provide a detailed vulnerability report with remediation steps:\n\n{scan_output}"
            )
            return response.text
        except Exception as e:
            # If it's a 404, we silently try the next model
            if "404" in str(e):
                print(f"[!] {model_name} not found, trying fallback...")
                continue
            else:
                return f"An unexpected error occurred: {str(e)}"
    
    return "Error: No compatible models were found. Check your API version."

def main():
    print("--- Auditor Tool v4.1.0 ---")
    target = input("Enter target IP (e.g., 192.168.56.101): ")
    
    if not target:
        print("Error: Target IP is required.")
        return

    try:
        print(f"[*] Scanning {target} using Nmap...")
        # Running a service version scan (-sV)
        result = subprocess.check_output(f"nmap -sV {target}", shell=True).decode()
        
        # Get analysis from Gemini
        analysis = get_ai_analysis(result)
        
        # Save results to a Markdown file
        filename = f"audit_report_{target.replace('.', '_')}.md"
        with open(filename, "w") as f:
            f.write(f"# Security Audit Report for {target}\n\n")
            f.write(analysis)
        
        print(f"\n[+] Audit Complete! Report saved to: {filename}")
        
    except subprocess.CalledProcessError:
        print("[!] Error: Nmap failed. Ensure Nmap is installed and you have permission to scan.")
    except Exception as e:
        print(f"[!] An error occurred: {e}")

if __name__ == "__main__":
    main()