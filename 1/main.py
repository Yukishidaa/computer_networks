import subprocess
import re


def get_statistic(domain, packeges=1):
    result = []
    
    info = subprocess.run(["ping", domain, f"-c {packeges}"],
                            capture_output=True,
                            text=True).stdout
    rtt = re.search(r'(\d+\.\d+)/(\d+\.\d+)/(\d+\.\d+)/(\d+\.\d+)', info)
    stat = re.search(r'(\d+)\s+packets? transmitted,\s*(\d+)\s+received,\s*(\d+)%\s+packet loss',
                      info, re.IGNORECASE)
    
    if rtt:
        result.extend(rtt.groups())
    else:
        result.extend(['Error'] * 4)
    
    if stat:
        result.extend(stat.groups())
    else:
        result.extend(['Error'] * 3)
    
    return result

domains = [
    "10.255.255.1",
    "youtube.com",
    "google.com",
    "yandex.ru",
    "github.com",
    "wikipedia.org",
    "mail.ru",
    "cloudflare.com",
    "vk.com",
    "apple.com",
    "mail.ru.com",
    "stackoverflow.com",
]

with open('result.csv', 'w') as file:
    file.write('domain,min,avg,max,mdev,packets transmitted,received,packet loss%\n')
    for domain in domains:
        file.write(','.join([domain] + get_statistic(domain, 2)) + '\n')
