import dns
import dns.resolver
import dns.rdatatype
import sys
import copy


class DnsContainer:
    def __init__(self, url='', data={}, children=[]):
        self.url = url
        self.data = data
        self.children = children


def search_recursive(url):
    children = copy.deepcopy(get_subdomain(url))
    data = copy.deepcopy(get_data(url))

    # Leaf node of the tree
    if children == []:
        return DnsContainer(url=url, data=data, children=copy.deepcopy(children))
    else:   # Inner node (with a list of children)
        temp_list = list()
        for child in children:
            temp_list.append(copy.deepcopy(search_recursive(child)))
        temp_list.append(DnsContainer(url=url, data=data, children=copy.deepcopy(temp_list)))

        return DnsContainer(url=url, data=data, children=copy.deepcopy(temp_list))


def start_search(url):
    dns_object = search_recursive(url)
    return dns_object


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


def get_data(url):
    data_dict = dict()
    data_dict['a'] = list()
    data_dict['aaaa'] = list()
    data_dict['mx'] = list()
    data_dict['cname'] = list()

    # message_a = dns.resolver.query(url, 'a', raise_on_no_answer=False)
    try:
        message_a = dns.resolver.query(str(url), 'a', raise_on_no_answer=False)

        temp_list = list()

        for entry in message_a:
            temp_list.append(entry)
        data_dict['a'] = temp_list

    except ValueError:
        print(ValueError)

    # message_aaaa = dns.resolver.query(url, 'aaaa', raise_on_no_answer=False)
    try:
        message_aaaa = dns.resolver.query(str(url), 'aaaa', raise_on_no_answer=False)

        temp_list = list()

        for entry in message_aaaa:
            temp_list.append(entry)
        data_dict['aaaa'] = temp_list

    except ValueError:
        print(ValueError)

    # message_mx = dns.resolver.query(url, 'mx', raise_on_no_answer=False)
    try:
        message_mx = dns.resolver.query(str(url), 'mx', raise_on_no_answer=False)

        temp_list = list()

        for entry in message_mx:
            ip_mx_list = list()

            # MX registry attributes -> preference + exchange (url)
            message_mx_a = dns.resolver.query(str(entry.exchange), 'a', raise_on_no_answer=False)

            for ip in message_mx_a:
                ip_mx_list.append(ip)

            temp_list.append([entry, ip_mx_list])

        data_dict['mx'] = temp_list

    except ValueError:
        print(ValueError)

    # message_cname = dns.resolver.query(url, 'cname', raise_on_no_answer=False)
    try:
        message_cname = dns.resolver.query(str(url), 'cname', raise_on_no_answer=False)

        temp_list = list()

        for entry in message_cname:
            temp_list.append(entry)
        data_dict['cname'] = temp_list

    except ValueError:
        print(ValueError)

    return data_dict


def print_dns_object(tree):
    return print_dns_recursive(tree, '')


def print_dns_recursive(tree, tabs):
    url = tree.url if type(tree.url) == str else tree.url.to_text()

    if len(tree.children) == 0:
        print('[+]\t' + tabs + url + ':')
        print('[-]\t\t' + tabs + 'Mail servers:')
        for mail in tree.data['mx']:
            for ip in mail[1]:
                print('[-]\t\t\t' + tabs + str(mail[0].exchange) + ' [' + str(mail[0].preference) + ']: ' + str(ip))

        print('[-]\t\t' + tabs + 'Related IPv4:')
        for ip in tree.data['a']:
            print('[-]\t\t\t' + tabs + str(ip) + ' [' + str(url) + ']')

        print('[-]\t\t' + tabs + 'Related IPv6:')
        for ip in tree.data['aaaa']:
            print('[-]\t\t\t' + tabs + str(ip) + ' [' + str(url) + ']')
        return
    else:
        print('[+]\t' + tabs + url + ':')
        print('[-]\t\t' + tabs + 'Mail servers:')
        for mail in tree.data['mx']:
            for ip in mail[1]:
                print('[-]\t\t\t' + tabs + str(mail[0].exchange) + ' [' + str(mail[0].preference) + ']: ' + str(ip))

        print('[-]\t\t' + tabs + 'Related IPv4:')
        for ip in tree.data['a']:
            print('[-]\t\t\t' + tabs + str(ip) + ' [' + str(url) + ']')

        print('[-]\t\t' + tabs + 'Related IPv6:')
        for ip in tree.data['aaaa']:
            print('[-]\t\t\t' + tabs + str(ip) + ' [' + str(url) + ']')

        for child in tree.children:
            print('[-]')
            print_dns_recursive(child, tabs + '\t\t')
        return


def main(url):
    results = start_search(url)
    print_dns_object(results)


if __name__ == '__main__' and len(sys.argv) == 2:
    print('Start!')
    main(sys.argv[1])

