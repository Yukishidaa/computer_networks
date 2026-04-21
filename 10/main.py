import subprocess
import csv
import socket
import os

sites = ["google.com", "github.com", "archlinux.org", "nsu.ru"]
filename = "report.csv"

def get_data():
    results = []
    
    for site in sites:
        print(f"Работу с {site}...")
        
        try:
            ip = socket.gethostbyname(site)
        except:
            ip = "unknown"
            
        if ip != "unknown":
            try:
                output = subprocess.check_output(["traceroute", "-I", "-n", "-m", "20", ip], text=True)
                
                lines = output.split('\n')
                for line in lines:
                    if line.startswith("traceroute") or not line.strip():
                        continue
                    
                    parts = line.split()
                    hop_n = parts[0]
                    hop_ip = parts[1]
                    
                    if len(parts) >= 3 and parts[2] != "*":
                        ms = parts[2]
                    else:
                        ms = "timeout"
                        
                    results.append([site, ip, hop_n, hop_ip, ms])
            except Exception as e:
                print(f"Error with {site}: {e}")
        else:
            results.append([site, "N/A", "N/A", "DNS Error", "N/A"])
            
    return results

def save_to_csv(data):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Site", "IP", "Hop", "Router", "Time"])
        
        for row in data:
            writer.writerow(row)

if __name__ == "__main__":
    final_data = get_data()
    save_to_csv(final_data)
    print("All done")