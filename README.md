# httpScape
Simple multithreaded HTTP Proxy Scraper/Checker

```
     \_______/
 `.,-'\_____/`-.,'
  /`..'\ _ /`.,'\
 /  /`.,' `.,'\  \
/__/__/     \__\__\__
\  \  \     /  /  /
 \  \,'`._,'`./  /
  \,'`./___\,'`./
 ,'`-./_____\,-'`. [ HTTPSCAPE ]
     /       \
```
# Usage
```
$ python3 httpScape.py --help
usage: httpScrape.py [-h] [-m MAXIMUM]
                     [-o OUTPUT]
                     [-t THREADS] [-v]
HTTP Proxy Scraper/Checker Framework
options:
  -h, --help           show this help
                       message and exit
  -m MAXIMUM, --maximum MAXIMUM
                       specify max amount
                       of proxies
  -o OUTPUT, --output OUTPUT
                       specify output file
                       name [default:proxie
                       s.txt]
  -t THREADS, --threads THREADS
                       specify amount of
                       threads [default:5]
```

# Prerequisites
```
python3
```

# Install
```
git clone https://github.com/CharlesTheGreat77/httpScape
cd httpScape
python3 venv <virtual_environment_name>
source <virtual_environment_name>/bin/activate
pip3 install -r requirements.txt
```
