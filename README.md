# DNS Python simple example

This is a small program that given an URL can get info recursively about DNS.

## Index

- Requirements
- Main functions
- Example
- Notes
- Disclaimer

## Requirements

To develop this code and also recommended to run this example it was used:

- Python 3.6.4
- dnspython package 1.16.0

## Main functions

- **start_search(url):**
Given a domain sets up the recursive search over it (search_recursive(url))
- **get_subdomain(url):**
Given a domain return a list of the NS entries found.
- **get_data(url):**
Given a domain return a dictionary containing some register info (key -> name of the register/value -> entries): 
A, AAAA, MX, CNAME.
- **print_dns_object(tree):**
Given a dns_object this function sets up the main recursive function to print the whole tree (print_dns_recursive(tree, 
tabs))
- **main(url)**:
Given a domain it generates a tree and after that prints immediately the result.

## Example

This example is censored but it still shows how to use it and the results.
```bash
C:\Users\----\PycharmProjects\pydnsexample>python main.py ----.com
Start!
----.com
ns51--.we----sa.eu.
ns51--.we----sa.eu.
[+]     ----.com:
[-]             Mail servers:
[-]                     -------com.mail.prot---ion.out--ok.com. [0]: XX4.XX7.XX6.X36
[-]                     -------com.mail.prot---ion.out--ok.com. [0]: XX4.XX7.XX5.X36
[-]             Related IPv4:
[-]                     XX8.XX5.X32.X86 [----.com]
[-]             Related IPv6:
[-]
[+]                     ns51--.we----sa.eu.:
[-]                             Mail servers:
[-]                             Related IPv4:
[-]                                     XX4.XX3.X84.X70 [ns51--.we----sa.eu.]
[-]                             Related IPv6:
[-]
[+]                     ns51--.we----sa.eu.:
[-]                             Mail servers:
[-]                             Related IPv4:
[-]                                     XX8.XX5.X30.X47 [ns51--.we----sa.eu.]
[-]                             Related IPv6:
```

## Notes

- CNAME register is requested but not used in this example.
- There are many more registers which can be useful as SOA or PTR.
- The best way to understand how a protocol,tool or programming language work is trying to use it.

## Disclaimer

This code is just a small example of how to use pydns. The code is free to be used or modified as open source.

Remember: Use this code at your own risk without breaking the law or making a harmful use of it.

If you manage to scan repeatedly a domain, which can be seen as a malicious 
practice, you may be spotted by an IDS or IPS. 

Your IP may be blocked or even you will be found using your public IP and ISP. Do not overuse it over the same domain.