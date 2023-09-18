import re


def class_to_cidr(ip):
    ip_octet = ip.split('.')
    first_octet = int(ip_octet[0])
    if 0 <= first_octet <= 127:  # class A
        class_cidr = 8
    elif 128 <= first_octet <= 191:  # class B
        class_cidr = 16
    elif 192 <= first_octet <= 223:  # class C
        class_cidr = 24
    else:
        return "invalid first octet"
    return class_cidr


def valid_ip_address():
    """
    get an ip address from the user and validate pattern
    :return: valid ip address
    :rtype: string
    """
    ip_address = input("enter an IP address: ")
    while not re.fullmatch(r"(22[0-3]|2[0-1][0-9]|[0-1]?[0-9]?[0-9])(\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9]?[0-9])){3}",
                           ip_address):
        ip_address = input("IP address is not valid, please enter again: ")
    return ip_address

    # regex for all valid ip addresses 0.0.0.0 - 255.255.255.255: ((25[0-5]|2[0-4][0-9]|[0-1]?[0-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|[0-1]?[0-9]?[0-9])
    # regex for classes a,b,c ip addresses 0.0.0.0 - 223.255.255.255: (22[0-3]|2[0-1][0-9]|[0-1]?[0-9]?[0-9])(\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9]?[0-9])){3}

def valid_cidr(ip):
    """
    get a CIDR from the user and validate integer
    :return: valid CIDR
    :rtype: int
    """
    cidr = input("please enter valid CIDR: ")
    # if the cidr is empty call to function which return the cidr by the class
    if cidr.strip() == "":
        cidr = class_to_cidr(ip)
    else:
        while not cidr.isdigit() or not 1 <= int(cidr) <= 32:
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
    bits_for_hosts_or_subnets = 32 - cidr
    number_of_hosts_or_subnets = 2 ** bits_for_hosts_or_subnets
    # print(number_of_hosts_or_subnets)
    number = input("please enter the number of hosts or subnets: ")
    while not number.isdigit() or int(number) > number_of_hosts_or_subnets:
        number = input("invalid number of hosts or subnets: ")
    return int(number)


def convert_cidr_to_decimal(cidr):
    """
    get CIDR and convert to decimal form for example 255.255.255.224
    :return: valid decimal cidr
    :rtype: string
    """
    # convert cidr to binary mask
    binary = ""
    for i in range(cidr):
        binary += str(1)
    for i in range(32 - cidr):
        binary += str(0)
    # Split the binary mask into four octets
    decimal = []
    for i in range(0, len(binary), 8):
        # Convert each octet from binary to decimal
        decimal.append(str(int(binary[i:i + 8], 2)))
    # Join the decimal octets with dots to create the dotted-decimal notation
    decimal = ".".join(decimal)
    return decimal


def calculate_number_of_hosts(cidr, number_of_subnets):
    """
    calculate the number of hosts
    number_of_hosts=2**(32-CIDR)
    number_of_host > user hosts
    :return: hosts, subnets
    :rtype: int, int
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

    # 2. calculate the number of hosts and subnets
    hosts = 2 ** (32 - cidr - bits_for_subnets) - 2
    subnets = 2 ** bits_for_subnets
    return hosts, subnets


def calculate_number_of_subnets(cidr, number_of_hosts):
    """
    calculate the number of subnets
    32-cidr-hosts=subnets
    :return:subnets, hosts
    :rtype: int, int
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

    # 2. calculate the number of subnets and hosts
    subnets = 2 ** (32 - cidr - bits_for_hosts)
    hosts = 2 ** bits_for_hosts - 2
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
    size = 2 ** ((32 - cidr) % 8)
    octet = octet_number(cidr)
    ip_octets = ip.split('.')
    # put zero on every octet to the right of the current octet
    for i in range(octet + 1, 4):
        ip_octets[i] = str(0)
    ip_octets[octet] = str(0)
    print("first network:", ".".join(ip_octets))
    ip_octets[octet] = str(size)
    print("second network:", ".".join(ip_octets))
    ip_octets[octet] = str(256 - (size * 2))
    print("one before last network:", ".".join(ip_octets))
    ip_octets[octet] = str(256 - size)
    print("last network:", ".".join(ip_octets))


def broadcast_address(ip, cidr):
    size = 2 ** ((32 - cidr) % 8)
    octet = octet_number(cidr)
    ip_octets = ip.split('.')
    # put 255 on every octet to the right of the current octet
    for i in range(octet + 1, 4):
        ip_octets[i] = str(255)
    ip_octets[octet] = str(size - 1)
    print("first broadcast:", ".".join(ip_octets))
    ip_octets[octet] = str((size * 2) - 1)
    print("second broadcast:", ".".join(ip_octets))
    ip_octets[octet] = str(255 - size)
    print("one before last broadcast:", ".".join(ip_octets))
    ip_octets[octet] = str(255)
    print("last broadcast:", ".".join(ip_octets))


def main():
    # Input:
    ip_address = valid_ip_address()

    cidr = valid_cidr(ip_address)

    hosts_or_subnets = valid_host_or_subnet()

    number_of_hosts_or_subnets = valid_number_of_hosts_or_subnets(cidr)

    # Output:
    # 1. Subnet mask (in mask decimal format)
    decimal_cidr = convert_cidr_to_decimal(cidr)

    print("subnet mask :", decimal_cidr)
    # 2. Subnet in cidr
    print("cidr is", cidr)

    # 3. Number of hosts
    if hosts_or_subnets == "subnets":
        num_of_subnets = number_of_hosts_or_subnets
        num_of_hosts, num_of_subnets = calculate_number_of_hosts(cidr, num_of_subnets)

    # 4. Number of subnets
    else:
        num_of_hosts = number_of_hosts_or_subnets
        num_of_subnets, num_of_hosts = calculate_number_of_subnets(cidr, num_of_hosts)

    print("number of hosts:", num_of_hosts)
    print("number of subnets:", num_of_subnets)
    print("=====================================================================")
    # 5. For (maximum) two first and two last subnets
    # a. Network address
    network_address(ip_address, cidr)
    # b. Broadcast address
    print("=====================================================================")
    broadcast_address(ip_address, cidr)


if __name__ == "__main__":
    main()
    # valid_number_of_hosts_or_subnets(22)
    # IP_Address = valid_IP_Address()
    # print(IP_Address)
    # cidr = valid_cidr()
    # print(cidr)
    # valid_host_or_subnet()
    # valid_number_of_hosts_or_subnets()
    # decimal = CIDR_to_decimal()
    # print(decimal)
    # result = calculate_number_of_subnets(16, 32)
    # print(result)
    # result = calculate_number_of_subnets(24, 2000)
    # print(result)
    # network_address("172.12.12.12", 22)
    # broadcast_address("172.12.12.12", 22)
    # convert_cidr_to_decimal()

