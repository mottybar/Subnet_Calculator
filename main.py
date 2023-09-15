import re


def valid_ip_address():
    """
    get an ip address from the user and validate pattern
    :return: valid ip address
    :rtype: string
    """
    ip_address = input("enter an IP address: ")
    while not re.fullmatch(r"((25[0-5]|2[0-4][0-9]|[0-1]?[0-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|[0-1]?[0-9]?[0-9])",
                           ip_address):
        ip_address = input("IP address is not valid, please enter again: ")
    return ip_address
    # regex: ((25[0-5]|2[0-4][0-9]|[0-1]?[0-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|[0-1]?[0-9]?[0-9])


def valid_cidr():
    """
    get a CIDR from the user and validate integer
    :return: valid CIDR
    :rtype: int
    """
    cidr = input("please enter valid CIDR: ")
    while not cidr.isdigit() or not 0 <= int(cidr) <= 32:
        cidr = input("please enter valid CIDR: ")
    return int(cidr)


def valid_host_or_subnet():
    """
    get string from the user and validate only "hosts" or "subnets"
    :return: valid input
    :rtype: string
    """
    # use list
    hosts_or_subnets = input("please enter 'hosts' or 'subnets': ")
    while hosts_or_subnets != "hosts" and hosts_or_subnets != "subnets":
        hosts_or_subnets = input("please enter 'hosts' or 'subnets': ")
    return hosts_or_subnets


def valid_number_of_hosts_or_subnets(cidr):
    """
    get a number of hosts or subnets from the user and validate integer (according to valid_host_or_subnet function)
    :return: valid number
    :rtype: int
    """
    # todo check if number of hosts or subnets is too big
    number = input("please enter the number of hosts or subnets: ")
    while not number.isdigit():
        number = input("please enter the number of hosts or subnets: ")

    return int(number)


def convert_cidr_to_decimal(cidr):
    """
    get CIDR and convert to decimal form for example 255.255.255.224
    :return: valid decimal cidr
    :rtype: string
    """
    # todo: check if need validation
    cidr_to_decimal_mapping = {1: "128.0.0.0", 2: "192.0.0.0", 3: "224.0.0.0", 4: "240.0.0.0", 5: "248.0.0.0",
                               6: "252.0.0.0", 7: "254.0.0.0", 8: "255.0.0.0", 9: "255.128.0.0", 10: "255.192.0.0",
                               11: "255.224.0.0", 12: "255.240.0.0", 13: "255.248.0.0", 14: "255.252.0.0",
                               15: "255.254.0.0", 16: "255.255.0.0", 17: "255.255.128.0", 18: "255.255.192.0",
                               19: "255.255.224.0", 20: "255.255.240.0", 21: "255.255.248.0", 22: "255.255.252.0",
                               23: "255.255.254.0", 24: "255.255.255.0", 25: "255.255.255.128", 26: "255.255.255.192",
                               27: "255.255.255.224", 28: "255.255.255.240", 29: "255.255.255.248",
                               30: "255.255.255.252", 31: "255.255.255.254", 32: "255.255.255.255"}
    decimal_cidr = cidr_to_decimal_mapping.get(cidr, "invalid key")
    return decimal_cidr


def calculate_number_of_hosts(cidr, number_of_subnets):
    """
    calculate the number of hosts
    number_of_hosts=2**(32-CIDR)
    number_of_host > user hosts
    :return: int
    :rtype:
    """
    # 1. from number_of_subnets infer how many bits we need for the subnets
    bits_for_subnets = 0
    num_of_bits = 0
    subnet_num_found = False
    while num_of_bits <= 32 - cidr and not subnet_num_found:
        if 2 ** num_of_bits >= number_of_subnets:
            bits_for_subnets = num_of_bits
            subnet_num_found = True
        num_of_bits += 1

    # 2. calculate the number of hosts
    hosts = 2 ** (32 - cidr - bits_for_subnets) - 2
    subnets = 2 ** bits_for_subnets
    return hosts, subnets


def calculate_number_of_subnets(cidr, number_of_hosts):
    """
    calculate the number of subnets
    32-cidr-hosts=subnets
    :return:
    :rtype:
    """
    # 1. from number_of_hosts infer how many bits we need for the hosts
    bits_for_hosts = 0
    num_of_bits = 0
    host_num_found = False
    while num_of_bits <= 32 - cidr and host_num_found is False:
        if 2 ** num_of_bits >= number_of_hosts:
            bits_for_hosts = num_of_bits
            host_num_found = True
        num_of_bits += 1

    # 2. calculate the number of subnets
    subnets = 2 ** (32 - cidr - bits_for_hosts)
    hosts = 2 ** bits_for_hosts
    return subnets, hosts


def octet_number(cidr):
    if 25 <= cidr <= 32:
        return 3
    elif 17 <= cidr <= 24:
        return 2
    elif 9 <= cidr <= 16:
        return 1
    elif 0 <= cidr <= 8:
        return 0
    return None


def network_address(ip, cidr):
    size = 2**((32-cidr) % 8)
    octet = octet_number(cidr)
    ip_octets = ip.split('.')
    ip_octets[octet] = str(0)
    print("first network:", ip_octets)
    ip_octets[octet] = str(size)
    print("second network", ip_octets)
    ip_octets[octet] = str(256 - size)
    print("last network", ip_octets)
    ip_octets[octet] = str(256 - (size * 2))
    print("one before last network", ip_octets)



def broadcast_address(cidr):
    pass

# def two_first_and_two_last_subnets(ip, cidr):
#     #calculate network address by put zero in the host portion
#     #calculate next network address using number of hosts
#     network_address = []
#     size = 2**((32 - cidr) % 8)
#     ip_octets = ip.split('.')
#     print(ip_octets)
#     subnet_mask = convert_cidr_to_decimal(cidr)
#     subnet_octets = subnet_mask.split('.')
#     for i in range(4):
#         network_address.append(int(ip_octets[i]) & int(subnet_octets[i]))
#     print(network_address)
#     if 25 <= cidr <= 32:
#         #first network
#         ip_octets[3] = 0
#         print("first network:", ip_octets)
#         #first network broadcast
#         ip_octets[3] = size - 1
#         print("first_network_broadcast:", ip_octets)
#         #second network
#         ip_octets[3] = size
#         print("second network:", ip_octets)
#         #second network broadcast
#         ip_octets[3] = (size * 2) - 1
#         print("second network broadcast:", ip_octets)
#         #one before last network
#         ip_octets[3] = 256 - (size * 2)
#         print("one before last network:", ip_octets)
#         #one_before_last_network_broadcast
#         ip_octets[3] = 256 - size - 1
#         print("one before last network broadcast", ip_octets)
#         #last network
#         ip_octets[3] = 256 - size
#         print("last network:", ip_octets)
#         #last_network_broadcast
#         ip_octets[3] = 255
#         print("last network broadcast", ip_octets)
#
#     elif 17 <= cidr <= 24:
#         #first network
#         ip_octets[2] = 0
#         ip_octets[3] = 0
#         print("first network:", ip_octets)
#         #first network broadcast
#         ip_octets[2] = size - 1
#         ip_octets[3] = 255
#         print("first_network_broadcast:", ip_octets)
#         #second network
#         ip_octets[2] = size
#         ip_octets[3] = 0
#         print("second network:", ip_octets)
#         #second network broadcast
#         ip_octets[2] = (size * 2) - 1
#         ip_octets[3] = 255
#         print("second network broadcast:", ip_octets)
#         #one before last network
#         ip_octets[2] = 256 - (size * 2)
#         ip_octets[3] = 0
#         print("one before last network:", ip_octets)
#         #one_before_last_network_broadcast
#         ip_octets[2] = 256 - size - 1
#         ip_octets[3] = 255
#         print("one before last network broadcast", ip_octets)
#         #last network
#         ip_octets[2] = 256 - size
#         ip_octets[3] = 0
#         print("last network:", ip_octets)
#         #last_network_broadcast
#         ip_octets[2] = 255
#         ip_octets[3] = 255
#         print("last network broadcast", ip_octets)
#
#     elif 9 <= cidr <= 16:
#         #first network
#         ip_octets[1] = 0
#         ip_octets[2] = 0
#         ip_octets[3] = 0
#         print("first network:", ip_octets)
#         #first network broadcast
#         ip_octets[1] = size - 1
#         ip_octets[2] = 255
#         ip_octets[3] = 255
#         print("first_network_broadcast:", ip_octets)
#         #second network
#         ip_octets[1] = size
#         ip_octets[2] = 0
#         ip_octets[3] = 0
#         print("second network:", ip_octets)
#         #second network broadcast
#         ip_octets[1] = (size * 2) - 1
#         ip_octets[2] = 255
#         ip_octets[3] = 255
#         print("second network broadcast:", ip_octets)
#         #one before last network
#         ip_octets[1] = 256 - (size * 2)
#         ip_octets[2] = 0
#         ip_octets[3] = 0
#         print("one before last network:", ip_octets)
#         #one_before_last_network_broadcast
#         ip_octets[1] = 256 - size - 1
#         ip_octets[2] = 255
#         ip_octets[3] = 255
#         print("one before last network broadcast", ip_octets)
#         #last network
#         ip_octets[1] = 256 - size
#         ip_octets[2] = 0
#         ip_octets[3] = 0
#         print("last network:", ip_octets)
#         #last_network_broadcast
#         ip_octets[1] = 255
#         ip_octets[2] = 255
#         ip_octets[3] = 255
#         print("last network broadcast", ip_octets)
#
#     elif 0 <= cidr <= 8:
#         # first network
#         ip_octets[0] = 0
#         ip_octets[1] = 0
#         ip_octets[2] = 0
#         ip_octets[3] = 0
#         print("first network:", ip_octets)
#         # first network broadcast
#         ip_octets[0] = size - 1
#         ip_octets[1] = 255
#         ip_octets[2] = 255
#         ip_octets[3] = 255
#         print("first_network_broadcast:", ip_octets)
#         # second network
#         ip_octets[0] = size
#         ip_octets[1] = 0
#         ip_octets[2] = 0
#         ip_octets[3] = 0
#         print("second network:", ip_octets)
#         # second network broadcast
#         ip_octets[0] = (size * 2) - 1
#         ip_octets[1] = 255
#         ip_octets[2] = 255
#         ip_octets[3] = 255
#         print("second network broadcast:", ip_octets)
#         # one before last network
#         ip_octets[0] = 256 - (size * 2)
#         ip_octets[1] = 0
#         ip_octets[2] = 0
#         ip_octets[3] = 0
#         print("one before last network:", ip_octets)
#         # one_before_last_network_broadcast
#         ip_octets[0] = 256 - size - 1
#         ip_octets[1] = 255
#         ip_octets[2] = 255
#         ip_octets[3] = 255
#         print("one before last network broadcast", ip_octets)
#         # last network
#         ip_octets[0] = 256 - size
#         ip_octets[1] = 0
#         ip_octets[2] = 0
#         ip_octets[3] = 0
#         print("last network:", ip_octets)
#         # last_network_broadcast
#         ip_octets[0] = 255
#         ip_octets[1] = 255
#         ip_octets[2] = 255
#         ip_octets[3] = 255
#         print("last network broadcast", ip_octets)


def main():
    ip_address = valid_ip_address()

    cidr = valid_cidr()

    hosts_or_subnets = valid_host_or_subnet()

    number_of_hosts_or_subnets = valid_number_of_hosts_or_subnets(cidr)

    # Output:
    # 1. Subnet mask (in mask decimal format)
    decimal_cidr = convert_cidr_to_decimal(cidr)
    print("decimal cidr is:", decimal_cidr)
    # 2. Subnet in cidr
    print("cidr is", cidr)
    # 3. Number of hosts
    if hosts_or_subnets == "subnets":
        num_of_subnets = number_of_hosts_or_subnets
        num_of_hosts = calculate_number_of_hosts(cidr, num_of_subnets)

    # 4. Number of subnets
    else:
        num_of_hosts = number_of_hosts_or_subnets
        num_of_subnets, num_of_hosts = calculate_number_of_subnets(cidr, num_of_hosts)

    print("number of hosts:", num_of_hosts)
    print("number of subnets:", num_of_subnets)
    # 5. For (maximum) two first and two last subnets
    # a. Network address
    # b. Broadcast address


if __name__ == "__main__":
    # main()
    # IP_Address = valid_IP_Address()
    # print(IP_Address)
    # cidr = valid_CIDR()
    # print(cidr)
    # valid_host_or_subnet()
    # valid_number_of_hosts_or_subnets()
    # decimal = CIDR_to_decimal()
    # print(decimal)
    # result = calculate_number_of_subnets(16, 32)
    # print(result)
    # result = calculate_number_of_subnets(24, 2000)
    # print(result)
    network_address("172.12.12.12", 27)