#!/usr/bin/env python3

import requests
import argparse
import sys
import os
import re
import time
import threading
from colors import *

psmall = ["81", "591", "2082", "2087", "2095", "2096", "3000", "8000", "8001", "8008", "8080", "8083", "8443", "8834", "8888"]
plarge = ["81", "300", "591", "593", "832", "981", "1010", "1311", "2082", "2087", "2095", "2096", "2480", "3000", "3128", "3333", "4243", "4567", "4711", "4712", "4993", "5000", "5104", "5108", "5800", "6543", "7000", "7396", "7474", "8000", "8001", "8008", "8014", "8042", "8069", "8080", "8081", "8088", "8090", "8091", "8118", "8123", "8172", "8222", "8243", "8280", "8281", "8333", "8443", "8500", "8834", "8880", "8888", "8983", "9000", "9043", "9060", "9080", "9090", "9091", "9200", "9443", "9800", "9981", "12443", "16080", "18091", "18092", "20720", "28017"]
domains = []
outputbuffer = []
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}

def print_line(r, url, status_codes):
    try:
        size = "{}B".format(len(r.text))
        status = r.status_code
        # set redirect value to location header if status code is 3xx else ''
        redirect_value = lgreen+"-> {}".format(r.headers['location']) if str(status)[0] == "3" else ''
        title = re.findall(r'<title>(.*?)</title>', r.text)
        title = '' if title == [] else title[0][:40]
        # Use dark yellow for 404
        scolor = lyellow if r.status_code == 404 else statuscolors[int(str(status)[0])]
        if not status_codes:
            # if custom status codes are not provided output all urls
            outputbuffer.append(url)
        else:
            # output only links with provided status codes
            if status in status_codes:
                outputbuffer.append(url)
        # if status is 3xx then display location header value instead of title
        title = title if redirect_value == '' else redirect_value
        print("{:<42}".format(url),scolor,"[{}]".format(status),cyan,"{:<9}".format(size),end,white,"{:<30}".format(title),end)
    except Exception as e:
        pass

def remove_proto(url):
    # remove http and https from input to avoid confusion
    if url.startswith('https://'):
        url = url[8:]
    elif url.startswith('http://'):
        url = url[7:]
    return url

def work(timeout, ports, is_https, status_codes):
    while domains != []:
        try:
            domain = domains.pop()
            domain = remove_proto(domain)
            # if prefer https is selected
            if is_https:
                url = "https://{}".format(domain)
                try:
                    r = requests.get(url, timeout=timeout, allow_redirects=False, headers=headers)
                # if https fails try http
                except requests.exceptions.SSLError:
                    url = "http://{}".format(domain)
                    r = requests.get(url, timeout=timeout, allow_redirects=False, headers=headers)
                    print_line(r, url, status_codes)
            else:
                # do both http and https
                url = "http://{}".format(domain)
                r = requests.get(url, timeout=timeout, allow_redirects=False, headers=headers)
                print_line(r, url, status_codes)
                url = "https://{}".format(domain)
                r = requests.get(url, timeout=timeout, allow_redirects=False, headers=headers)
                print_line(r, url, status_codes)
            if ports:
                # scan for ports if specified
                for port in ports:
                    url = "http://{}:{}".format(domain,port)
                    r = requests.get(url, timeout=timeout, allow_redirects=False, headers=headers)
                    print_line(r, url, status_codes)
        except Exception as e:
            pass

def main():
    print(white,'''
               /    _/_ /       
   _   __  __ /___  /  /_  o _  
  /_)_/ (_(_)/_)</_<__/ /_<_/_)_
 /              ''',end,'''@github/shobhit99''',white,'''
'              
    ''',end)
    usage = '''
    Example:

    probethis.py -f domains.txt -t 5 -o output.txt
    probethis.py -f domains.txt -p [ 81,8080,3000 | small | large]
    cat domains.txt | probethis.py -s 200,403,401 -o filtered.txt
	'''
    parser = argparse.ArgumentParser(description="Find working domains!", epilog=usage, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-f", help="File with domain list", type=str, action="store")
    parser.add_argument("-t", help="No of threads", type=int, default=5, action="store")
    parser.add_argument("-o", help="Output file name, Saves all status codes by default unless codes specified using -s", type=str, action="store")
    parser.add_argument("-s", help="Output urls with only specified status codes seperated by comma", type=str, action="store")
    parser.add_argument("-p", help="[ Custom Ports seperated by comma | small | large ] small and large uses predefined list of ports", type=str, action="store")
    parser.add_argument("--https", help="Prefer HTTPS over http", action="store_true")
    parser.add_argument("--timeout", help="Timeout for requests", type=int, default=5, action="store")
    args = parser.parse_args()
    file = args.f
    threadcount = args.t
    outputfile = args.o
    ports = args.p
    status_codes = args.s
    is_https = args.https
    timeout = args.timeout
    if ports:
        ports = ports.split(",")
    if status_codes:
        if not outputfile:
            sys.exit("Please provide output file name with -o")
        else:
            status_codes = status_codes.split(",")
            status_codes = [int(i) for i in status_codes] 
    # if pipe input
    if not file:
        for d in sys.stdin:
            domains.append(d.rstrip('\n'))
    # if input file
    else:
        data = open(file, "r").read()
        domains.extend(data.split('\n'))
    
    if ports:
        if ports[0] == "small": 
            ports = psmall
        elif ports[0] == "large":
            ports = plarge

    sys.stdout.write(lgreen)
    print("Domains laoded : ", len(domains), white)
    print("{:<42}".format('Domain'), " Status  Size       Title / Redirect",end)
    # thread lists
    tlist = []
    for i in range(threadcount):
        t = threading.Thread(target=work, args=(timeout, ports, is_https, status_codes))
        t.start()
        tlist.append(t)

    try:
        # keep main thread running
        while True:
            time.sleep(2)
            if domains == []:
                for t in tlist:
                    # if any thread is active
                    if t.is_alive():
                        continue
                # all threads are complete
                break
        if outputfile:
            # write ouput to file if provided
            with open(outputfile, "w") as f:
                f.write("\n".join(d for d in outputbuffer))
            sys.stdout.write(end)

    except KeyboardInterrupt:
        print("Aborted by User")
        if outputfile:
            # write ouput to file if provided
            with open(outputfile, "w") as f:
                f.write("\n".join(d for d in outputbuffer))
        os.kill(os.getpid(), 9)
        sys.stdout.write(end)

if __name__ == '__main__':
    main()
