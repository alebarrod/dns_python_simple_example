import dns
import dns.resolver
import dns.rdatatype
import sys
import copy


# This objects represents a DNS domain as a node which can have sons (children).
class DnsContainer:
    def __init__(self, url='', data={}, children=[]):
        self.url = url  # domain (str or NS registry)
        self.data = data  # dictionary (key -> tipe of registry (A, AAAA, MX...)
        self.children = children  # list of DnsContainer (sons of the DnsConteiner node).


# Recursive main function which construct the tree structure. Given a domain keeps creating nodes until a domain has no
# NS registries (childs).
# Input (url (str or NS registry response) - Output (DnsContainer: Root node of the tree).
def search_recursive(url):
    children = copy.deepcopy(get_subdomain(url))
    data = copy.deepcopy(get_data(url))

    # Leaf node of the tree -> has no children
    if children == []:
        return DnsContainer(url=url, data=data, children=copy.deepcopy(children))
    else:   # Inner node (with a list of children)
        temp_list = list()
        for child in children:
            temp_list.append(copy.deepcopy(search_recursive(child)))
        temp_list.append(DnsContainer(url=url, data=data, children=copy.deepcopy(temp_list)))

        return DnsContainer(url=url, data=data, children=copy.deepcopy(temp_list))


# setup of search_recursive().
# Input (domain (str)) - Output (DnsContainer class father. root node).
def start_search(url):
    dns_object = search_recursive(url)
    return dns_object


# Input (domain (str) - Output (list of NS registry entries sons of the given domain).
def get_subdomain(url):
    temp_list = list()

    # message_ns = dns.resolver.query(url, 'ns', raise_on_no_answer=False)
    try:
        print(url)
        message_ns = dns.resolver.query(str(url), dns.rdatatype.NS, raise_on_no_answer=False)

        for entry in message_ns:
            temp_list.append(entry)

    except ValueError:
        print(ValueError)

    return temp_list


# MX value pair is a list of the IPs related to the mail server.
# Input (domain (str)) - Output (dictionary with registries 'a','aaaa','mx','cname' as key and entries as values).
def get_data(url):
    data_dict = dict()
    data_dict['a'] = list()
    data_dict['aaaa'] = list()
    data_dict['mx'] = list()
    data_dict['cname'] = list()

    # Get A registry from domain
    try:
        message_a = dns.resolver.query(str(url), 'a', raise_on_no_answer=False)

        temp_list = list()

        for entry in message_a:
            temp_list.append(entry)
        data_dict['a'] = temp_list

    except ValueError:
        print(ValueError)

    # Get AAAA registry from domain
    try:
        message_aaaa = dns.resolver.query(str(url), 'aaaa', raise_on_no_answer=False)

        temp_list = list()

        for entry in message_aaaa:
            temp_list.append(entry)
        data_dict['aaaa'] = temp_list

    except ValueError:
        print(ValueError)

    # Get MX (mail) registry from domain
    try:
        message_mx = dns.resolver.query(str(url), 'mx', raise_on_no_answer=False)

        temp_list = list()

        for entry in message_mx:
            ip_mx_list = list()

            # MX registry attributes -> preference + exchange (url)
            message_mx_a = dns.resolver.query(str(entry.exchange), 'a', raise_on_no_answer=False)

            for ip in message_mx_a:
                ip_mx_list.append(ip)  # Only save every IP for each mail server

            temp_list.append([entry, ip_mx_list])

        data_dict['mx'] = temp_list

    except ValueError:
        print(ValueError)

    # Get CNAME registry from domain
    try:
        message_cname = dns.resolver.query(str(url), 'cname', raise_on_no_answer=False)

        temp_list = list()

        for entry in message_cname:
            temp_list.append(entry)
        data_dict['cname'] = temp_list

    except ValueError:
        print(ValueError)

    return data_dict


# Setup print_dns_recursive.
# Input (DnsContainer node (root node) - Output (None)
def print_dns_object(tree):
    print_dns_recursive(tree, '')


# Given a node this function prints the node and its sons recursively until finding a leaf node.
# Input (DnsContainer and tabs (str) which store tabulations in each iteration) - Output (None)
def print_dns_recursive(tree, tabs):
    url = tree.url if type(tree.url) == str else tree.url.to_text()

    if len(tree.children) == 0:  # If the DnsContainer has not sons (it is a leaf node)...
        print('[+]\t' + tabs + url + ':')

        # Prints MX registries
        print('[-]\t\t' + tabs + 'Mail servers:')
        for mail in tree.data['mx']:
            for ip in mail[1]:
                print('[-]\t\t\t' + tabs + str(mail[0].exchange) + ' [' + str(mail[0].preference) + ']: ' + str(ip))

        # Prints A registries
        print('[-]\t\t' + tabs + 'Related IPv4:')
        for ip in tree.data['a']:
            print('[-]\t\t\t' + tabs + str(ip) + ' [' + str(url) + ']')

        # Prints AAAA registries
        print('[-]\t\t' + tabs + 'Related IPv6:')
        for ip in tree.data['aaaa']:
            print('[-]\t\t\t' + tabs + str(ip) + ' [' + str(url) + ']')
        return
    else:
        print('[+]\t' + tabs + url + ':')

        # Prints MX registries
        print('[-]\t\t' + tabs + 'Mail servers:')
        for mail in tree.data['mx']:
            for ip in mail[1]:
                print('[-]\t\t\t' + tabs + str(mail[0].exchange) + ' [' + str(mail[0].preference) + ']: ' + str(ip))

        # Prints A registries
        print('[-]\t\t' + tabs + 'Related IPv4:')
        for ip in tree.data['a']:
            print('[-]\t\t\t' + tabs + str(ip) + ' [' + str(url) + ']')

        # Prints AAAA registries
        print('[-]\t\t' + tabs + 'Related IPv6:')
        for ip in tree.data['aaaa']:
            print('[-]\t\t\t' + tabs + str(ip) + ' [' + str(url) + ']')

        # for each child repeat this process (until finding leaf nodes)
        for child in tree.children:
            print('[-]')
            print_dns_recursive(child, tabs + '\t\t')
        return


# Creates a tree given a domain (results) and prints it.
# Input (url which is a domain (str)) - Output (None)
def main(url):
    results = start_search(url)
    print_dns_object(results)


if __name__ == '__main__' and len(sys.argv) == 2:
    print('Start!')
    main(sys.argv[1])

