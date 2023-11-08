#get name for aws data type
#example usage get_tag_name_by_id(result_array,'CustomerGatewayId',my_cgw_id)
def get_tag_name_by_id(aws_result_array,aws_data_field,id_to_match):
    """Function to get name for aws data type."""
    result_name = "Unset"
    for my_arr in aws_result_array:
        this_id = my_arr[aws_data_field]
        if this_id == id_to_match:
            my_tag_info = my_arr['Tags']
            #iterate through the tag info to determine tag name
            for my_item in my_tag_info:
                key = my_item['Key']
                if key == 'Name':
                    result_name = my_item['Value']
    return result_name


#get cgw name by id
def get_cgw_name_by_id(session, my_cgw_id):
    """Function to get CGW name by ID."""
    response = session.describe_customer_gateways()

    cgw_array = response['CustomerGateways']
    cgw_name = get_tag_name_by_id(cgw_array,'CustomerGatewayId',my_cgw_id)
    return cgw_name

#get tgw name by id
def get_tgw_name_by_id(session, my_tgw_id):
    """Function to get TGW name by ID."""
    response = session.describe_transit_gateways()

    tgw_array = response['TransitGateways']
    tgw_name = get_tag_name_by_id(tgw_array,'TransitGatewayId',my_tgw_id)
    return tgw_name

#get transit gateway route table ids
def get_tgw_rtb_ids(session):
    """Function to get the TGW Route Table ID's"""
    response = session.describe_transit_gateway_route_tables()
    rtb_array = response['TransitGatewayRouteTables']
    #iterate through array of RTBs
    rtb_id_list = []
    for my_arr in rtb_array:
        rtb_state = my_arr['State']
        if rtb_state == 'available':
            rtb_id = my_arr['TransitGatewayRouteTableId']
            rtb_id_list.append(rtb_id)
    return rtb_id_list

#get tgw rtb name by id
def get_tgw_rtb_name_by_id(session,my_tgw_rtb_id):
    """Function to get TGW RTB name by ID."""
    response = session.describe_transit_gateway_route_tables()

    rtb_array = response['TransitGatewayRouteTables']
    rtb_name = get_tag_name_by_id(rtb_array,'TransitGatewayRouteTableId',my_tgw_rtb_id)
    return rtb_name

#get prefix list name by id
def get_pfx_list_name_by_id(session,my_pfx_list_id):
    """Function to get Managed Prefix List name by ID."""
    response = session.describe_managed_prefix_lists(
        Filters=[{'Name': 'prefix-list-id','Values': [my_pfx_list_id,]}]
        )
    #assuming only 1 response here and a valid response, should add some error checking here
    pfx_list_name = response['PrefixLists'][0]['PrefixListName']
    return pfx_list_name

#get vpn name by id
def get_vpn_name_by_id(session,vpn_id):
    """Function to get VPN name by ID."""
    response = session.describe_vpn_connections(
        Filters=[{'Name': 'vpn-connection-id','Values': [vpn_id,]}]
        )
    my_tag_info = response['VpnConnections'][0]['Tags']
    #iterate through the tag info to determine tag name
    vpn_name = "Unset"
    for my_item in my_tag_info:
        key = my_item['Key']
        if key == 'Name':
            vpn_name = my_item['Value']
    return vpn_name