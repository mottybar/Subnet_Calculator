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
    #convert cidr to binary mask
    binary = ""
    for i in range(cidr):
        binary += str(1)
    for i in range(32-cidr):
        binary += str(0)
    # Split the binary mask into four octets
    decimal = []
    for i in range(0, len(binary), 8):
        # Convert each octet from binary to decimal
        decimal.append(str(int(binary[i:i+8], 2)))
    # Join the decimal octets with dots to create the dotted-decimal notation
    decimal = ".".join(decimal)
    return decimal


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
    size = 2**((32-cidr) % 8)
    octet = octet_number(cidr)
    ip_octets = ip.split('.')
    #put zero on every octet to the right of the current octet
    for i in range(octet+1, 4):
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
        num_of_hosts, num_of_subnets = calculate_number_of_hosts(cidr, num_of_subnets)

    # 4. Number of subnets
    else:
        num_of_hosts = number_of_hosts_or_subnets
        num_of_subnets, num_of_hosts = calculate_number_of_subnets(cidr, num_of_hosts)

    print("number of hosts:", num_of_hosts)
    print("number of subnets:", num_of_subnets)
    # 5. For (maximum) two first and two last subnets
    # a. Network address
    #network_address(ip_address, cidr)
    # b. Broadcast address
    #broadcast_address(ip_address, cidr)


if __name__ == "__main__":
    main()
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
    # network_address("172.12.12.12", 22)
    # broadcast_address("172.12.12.12", 22)
    #convert_cidr_to_decimal()