def valid_IP_Address():
    """
    get an ip address from the user and validate pattern
    :return: valid ip address
    :rtype: string
    """
    pass

def valid_CIDR():
    """
    get a CIDR from the user and validate integer
    :return: valid CIDR
    :rtype: int
    """
    pass

def valid_host_or_subnet():
    """
    get string from the user and validate only "host" or "subnet"
    :return: valid string
    :rtype: string
    """
    pass

def valid_number_of_hosts_or_subnets():
    """
    get a number of hosts or subnets from the user and validate integer (according to valid_host_or_subnet function)
    :return: valid number
    :rtype: int
    """
    pass


def main():

    IP_Address = valid_IP_Address()


    CIDR = valid_CIDR()

    hosts_or_subnets = valid_host_or_subnet()

    number = valid_number_of_hosts_or_subnets(hosts_or_subnets)


    #Output:
    # 1. Subnet mask (in mask decimal format)
    CIDR_to_decimal(CIDR)
    # 2. Subnet in CIDR
    CIDR
    # 3. Number of hosts
    Number_of_hosts()
    # 4. Number of subnets
    Number_of_subnets()

    # 5. For (maximum) two first and two last subnets
        # a. Network address
        # b. Broadcast address


if __name__ == "__main__":
    main()
