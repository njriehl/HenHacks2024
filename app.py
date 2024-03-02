from flask import Flask, render_template, request, redirect, url_for
from zapv2 import ZAPv2
import time

app = Flask(__name__)

# The ZAP API key (default is empty, set it if you have configured one)
api_key = 'm18dup4hkpg84pebd4skak6kl1'

# Local ZAP instance
zap = ZAPv2(apikey=api_key)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    target_url = request.form['url']
    if not target_url.startswith('http'):
        target_url = 'http://' + target_url

    print(f'Starting to spider {target_url}')
    scan_id = zap.spider.scan(target_url)
    time.sleep(2)

    # Wait for the spider to complete
    while int(zap.spider.status(scan_id)) < 100:
        print(f'Spider progress %: {zap.spider.status(scan_id)}')
        time.sleep(2)
    print('Spider completed')

    # Start the active scan
    print(f'Starting active scan on {target_url}')
    scan_id = zap.ascan.scan(target_url)
    while int(zap.ascan.status(scan_id)) < 100:
        print(f'Scan progress %: {zap.ascan.status(scan_id)}')
        time.sleep(5)
    print('Active Scan completed')

    # Retrieve the alerts
    alerts = zap.core.alerts(baseurl=target_url)

    return render_template('results.html', alerts=alerts, target_url=target_url)

if __name__ == '__main__':
    app.run(debug=True)
