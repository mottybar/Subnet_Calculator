import re


def valid_IP_Address():
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

def valid_CIDR():
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
    #use list
    hosts_or_subnets = input("please enter 'hosts' or 'subnets': ")
    while hosts_or_subnets != "hosts" and hosts_or_subnets != "subnets":
        hosts_or_subnets = input("please enter 'hosts' or 'subnets': ")
    return hosts_or_subnets

def valid_number_of_hosts_or_subnets():
    """
    get a number of hosts or subnets from the user and validate integer (according to valid_host_or_subnet function)
    :return: valid number
    :rtype: int
    """
    number = input("please enter the number of hosts or subnets")
    while not number.isdigit():
        number = input("please enter the number of hosts or subnets")
    return int(number)


def CIDR_to_decimal():
    """
    get CIDR and convert to decimal form for example 255.255.255.224
    :return: valid decimal cidr
    :rtype: string
    """
    cidr_to_decimal = {1: "128.0.0.0", 2: "192.0.0.0", 3: "224.0.0.0", 4: "240.0.0.0", 5: "248.0.0.0",
                       6: "252.0.0.0", 7: "254.0.0.0", 8: "255.0.0.0", 9: "255.128.0.0", 10: "255.192.0.0",
                       11: "255.224.0.0", 12: "255.240.0.0", 13: "255.248.0.0", 14: "255.252.0.0",
                       15: "255.254.0.0", 16: "255.255.0.0", 17: "255.255.128.0", 18: "255.255.192.0",
                       19: "255.255.224.0", 20: "255.255.240.0", 21: "255.255.248.0", 22: "255.255.252.0",
                       23: "255.255.254.0", 24: "255.255.255.0", 25: "255.255.255.128", 26: "255.255.255.192",
                       27: "255.255.255.224", 28: "255.255.255.240", 29: "255.255.255.248",
                       30: "255.255.255.252", 31: "255.255.255.254", 32: "255.255.255.255"}
    CIDR = valid_CIDR()
    decimal_cidr = cidr_to_decimal.get(CIDR, "invalid key")
    return decimal_cidr


def Number_of_hosts(CIDR, number_of_subnets):
    """
    calculate the number of hosts
    number_of_hosts=2**(32-CIDR)
    number_of_host > user hosts
    :return: int
    :rtype:
    """
    #1. from number_of_subnets infer how many bits we need for the subnets
    new_cidr = 0
    num_of_bits = 0
    flag = False
    while num_of_bits <= 32-CIDR and flag is False:
        if 2**num_of_bits >= number_of_subnets:
            new_cidr = CIDR + num_of_bits
            flag = True
        num_of_bits += 1


    #2. calculate the number of hosts
    hosts = 2**(32-new_cidr)-2
    return hosts

def Number_of_subnets(CIDR, number_of_hosts):
    """
    calculate the number of subnets
    32-cidr-hosts=subnet
    :return:
    :rtype:
    """
    # 1. from number_of_hosts infer how many bits we need for the hosts
    bits_for_hosts = 0
    num_of_bits = 0
    flag = False
    while num_of_bits <= 32-CIDR and flag is False:
        if 2**num_of_bits >= number_of_hosts:
            bits_for_hosts = num_of_bits
            flag = True
        num_of_bits += 1

#2. calculate the number of subnets
    subnets = 2**(32-CIDR-bits_for_hosts)
    return subnets


def main():


    IP_Address = valid_IP_Address()

    CIDR = valid_CIDR()

    hosts_or_subnets = valid_host_or_subnet()

    number_of_hosts_or_subnets = valid_number_of_hosts_or_subnets()

    # Output:
    # 1. Subnet mask (in mask decimal format)
    CIDR_to_decimal(CIDR)
    # 2. Subnet in CIDR
    print(CIDR)
    # 3. Number of hosts
    if hosts_or_subnets == "subnets":
        num_of_subnets = number_of_hosts_or_subnets
        num_of_hosts = Number_of_hosts(IP_Address,CIDR,num_of_subnets)

    # 4. Number of subnets
    else:
        num_of_hosts = number_of_hosts_or_subnets
        num_of_subnets = Number_of_subnets(IP_Address,CIDR,num_of_hosts)


    # 5. For (maximum) two first and two last subnets
    # a. Network address
    # b. Broadcast address


if __name__ == "__main__":
    #IP_Address = valid_IP_Address()
    #print(IP_Address)
    # cidr = valid_CIDR()
    # print(cidr)
    #valid_host_or_subnet()
    #valid_number_of_hosts_or_subnets()
    #decimal = CIDR_to_decimal()
    #print(decimal)
    result = Number_of_subnets(16, 32)
    print(result)