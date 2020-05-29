# probethis
finds active domains from list of subdomains with status code, size and title
<img src="https://i.imgur.com/lIKlyiz.jpg">

## Usage
### Examples
```
▶ cat domains.txt | probethis.py
▶ probethis.py -f domain-list.txt
▶ assetfinder --subs-only example.com | probethis.py
```
### Input file
list of subdomains as input from file
```
probethis.py -f domains.txt
```
### Output the results
```
cat domains.txt | probethis.py -o valid.txt
```
### Output urls with only specified status codes 
```
cat domains.txt | probethis.py -s 200,403 -o valid.txt
```
### Scan for custom / predefined ports
```
cat domains.txt | probethis.py -p 81,8000
cat domains.txt | probethis.py -p small
```
### Change threads [default 5]
```
cat domains.txt | probethis.py -t 15
```
### Timeout
```
cat domains.txt | probethis.py --timeout=15
```
### Prefer HTTPS
```
cat domains.txt | probethis.py --https
```
