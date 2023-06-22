import requests
import threading
from queue import Queue
import argparse

class ProxyScraper:
    def __init__(self, max_valid_proxies):
        self.pList = []
        self.max_valid_proxies = max_valid_proxies
        self.valid_proxies = []
        self.proxy_lock = threading.Lock()
        self.exit_event = threading.Event()

    def scrape(self):
        request = requests.get('https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all').text
        for proxy in request.split():
            self.pList.append({'http': f'http://{proxy}', 'https': f'http://{proxy}'})

    def validate_proxy(self, proxy):
        try:
            response = requests.get('https://google.com', proxies=proxy, timeout=3)
            if response.status_code == 200:
                with self.proxy_lock:
                    self.valid_proxies.append(proxy)
                    if len(self.valid_proxies) >= self.max_valid_proxies:
                        self.exit_event.set()
                print(f"Valid proxy: {proxy['http']}")
        except (requests.RequestException, ValueError):
            pass

    def queue_proxies(self, thready):
        num_threads = thready  # Number of threads for validation
        proxy_queue = Queue()

        for proxy in self.pList:
            proxy_queue.put(proxy)

        def worker():
            while not proxy_queue.empty() and not self.exit_event.is_set():
                proxy = proxy_queue.get()
                self.validate_proxy(proxy)
                proxy_queue.task_done()

        threads = []
        for _ in range(num_threads):
            t = threading.Thread(target=worker)
            t.start()
            threads.append(t)

        while not proxy_queue.empty() and not self.exit_event.is_set():
            self.exit_event.wait(timeout=1)

        self.exit_event.set()
        for t in threads:
            t.join()

    def get_valid_proxies(self):
        return self.valid_proxies[:self.max_valid_proxies]

def main():
        parser = argparse.ArgumentParser(description='Proxy Scraper')
        parser.add_argument('--outfile', '-o', help='Output file name')
        parser.add_argument('--max-valid', '-m', type=int, default=10, help='Maximum number of valid proxies')
        parser.add_argument('--threads', '-t', type=int, default=5, help='number of threads')
        args = parser.parse_args()
        thready = args.threads

        proxy_scraper = ProxyScraper(args.max_valid)
        proxy_scraper.scrape()
        proxy_scraper.queue_proxies(thready)
        valid_proxies = proxy_scraper.get_valid_proxies()

        if args.outfile:
            with open(args.outfile, 'w') as f:
                for proxy in valid_proxies:
                    proxy = proxy['http']
                    proxy = proxy.replace('http://','')
                    f.write(f"{proxy}\n")

main()