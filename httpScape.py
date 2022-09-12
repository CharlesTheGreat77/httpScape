import requests, os, random, argparse
from threading import Thread

class httpScape:
    def __init__(self):
        self.pList = []
        self.proxies = []
        self.threads = []
        self._COUNTER = 1
        self._MAX_PROXIES = 0
        self._VERBOSE = ''
        
    def scrape(self):
        request = requests.get('https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all').text
        for proxy in request.split():
            self.pList.append({'http':f'http://{proxy}', 'https': f'http://{proxy}'})
    
    def check(self):
        while self._COUNTER < self._MAX_PROXIES:
            proxy = random.choice(self.pList)
            addr = list(proxy.values())
            server = addr[0]
            ip = server.replace('http://', '')
            if ip in self.proxies:
                self.check()
            try:
                response = requests.get('https://google.com/', timeout=5, proxies=proxy)
                if response.status_code == 200:
                    self.proxies.append(ip)
                    self._COUNTER += 1
                    if self._VERBOSE:
                        print(f'[\u2705] {ip}')
                if self._COUNTER >= len(self.pList):
                    break
            except:
                self.check()
                
    def main(self):
        parser = argparse.ArgumentParser(description='HTTP Proxy Scraper/Checker Framework')
        parser.add_argument('-m', '--maximum', help='specify max amount of proxies', type=int, required=False)
        parser.add_argument('-o', '--output', help='specify output file name [default:proxies.txt]', type=str, default='proxies.txt')
        parser.add_argument('-t', '--threads', help='specify amount of threads [default:5]', type=int, default=5)
        parser.add_argument('-v', '--verbose', help='enable verbosity', action='store_true')
        args = parser.parse_args()
        
        self._MAX_PROXIES = args.maximum
        output = args.output
        numThreads = args.threads
        self._VERBOSE = args.verbose
        cwd = os.getcwd()
        
        self.scrape()
        print(f'[*] {len(self.pList)} Proxies found..\n')
        print(f'[*] Checking connectivity of {self._MAX_PROXIES} proxies..')
        for index in range(numThreads):
            t = Thread(target=self.check, daemon=True)
            self.threads.append(t)
            t.start()
        for index, thread in enumerate(self.threads):
            t.join()

        print(f'[*] Saving proxies to {output}')  
        with open(f'{cwd}/{output}', 'w') as file:
            file.write('\n'.join(self.proxies))

scrape = httpScape()
scrape.main()
