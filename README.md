# probethis
finds active domains from list of subdomains with status code, size and title
<img src="https://i.imgur.com/eWze1UC.jpg">

## Usage
### Examples
```
▶ cat domains.txt | probethis.py
▶ probethis.py -f domain-list.txt
▶ assetfinder.py --subs-only example.com | probethis.py
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
### Use threading [default 5]
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
