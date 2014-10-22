import subprocess
import time

while True:
    subprocess.call('scrapy crawl VK', shell=True)
    time.sleep(55)
