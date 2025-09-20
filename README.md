# Subdomain Enumerator

A Python script to enumerate subdomains of a given domain using a wordlist.  
It resolves DNS, checks reachable subdomains over HTTPS, and saves results to a file.

## Features
- Uses a built-in default wordlist or a custom wordlist.
- Multi-threaded for faster scanning.
- Works on Windows, Linux, and macOS.
- Saves results in `found_subdomains.txt`.

## Installation
1. Clone the repository:

git clone https://github.com/surendrakumar2005/subdomain-enumeration.git


2. Navigate to the project folder:

cd subdomain-enumerator


3. Install dependencies:

pip install requests


4. Usage
   
python subdomain_enum.py -H example.com -w wordlist.txt -t 50


-H: Target domain (required)

-w: Optional wordlist file

-t: Number of threads (default: 50)

Default Wordlist

Includes common subdomains such as www, mail, ftp, blog, dev, etc.

Output

Reachable subdomains are saved to found_subdomains.txt.
