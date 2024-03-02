# run_script.py

# Your Python script code goes here
from zapv2 import ZAPv2
import time


# The URL you want to scan
target_url = 'https://nicklago.com'


# ZAP API key (default is empty, set it if you have configured one)
api_key = 'm18dup4hkpg84pebd4skak6kl1'


# Local ZAP instance
zap = ZAPv2(apikey=api_key)


print(f'Starting to spider {target_url}')
scan_id = zap.spider.scan(target_url)
time.sleep(2)


# Wait for the spider to complete
while int(zap.spider.status(scan_id)) < 100:
   print('Spider progress %: {}'.format(zap.spider.status(scan_id)))
   time.sleep(2)
print('Spider completed')


# Start the active scan
print(f'Starting active scan on {target_url}')
scan_id = zap.ascan.scan(target_url)
while int(zap.ascan.status(scan_id)) < 100:
   print('Scan progress %: {}'.format(zap.ascan.status(scan_id)))
   time.sleep(5)
print('Active Scan completed')


# Retrieve the alerts
alerts = zap.core.alerts(baseurl=target_url)


print('\nVulnerabilities found:')
for i, alert in enumerate(alerts, start=1):
   print(f"{i}. {alert['alert']}")
   print(f"   Risk: {alert['risk']}")
   print(f"   URL: {alert['url']}")
   print(f"   Param: {alert['param']}")
   print(f"   Attack: {alert['attack']}")
   print(f"   Evidence: {alert['evidence']}\n")

