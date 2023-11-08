import src.helpers as hf
import src.getters as gf
#describe vpns
def describe(session):
    """Function to describe the VPN's."""
    hf.print_section_banner('Begin Describe VPNs')
    response = session.describe_vpn_connections()
    vpn_array = response['VpnConnections']
    #iterate through array of VPNs
    for my_arr in vpn_array:
        vpn_state = my_arr['State']
        if vpn_state == 'available':
            vpn_id = my_arr['VpnConnectionId']
            vpn_cgw_id = my_arr['CustomerGatewayId']
            vpn_cgw_name = gf.get_cgw_name_by_id(session,vpn_cgw_id)
            vpn_tgw_id = my_arr['TransitGatewayId']
            vpn_tgw_name = gf.get_tgw_name_by_id(session,vpn_tgw_id)
            my_tag_info = my_arr['Tags']
            #iterate through the tag info to determine tag name
            vpn_name = "Unset"
            for my_item in my_tag_info:
                key = my_item['Key']
                if key == 'Name':
                    vpn_name = my_item['Value']
            #import statement
            print(f'#terraform import aws_vpn_connection.{vpn_name} {vpn_id}')
            #tf code
            print(f'''resource "aws_vpn_connection" "{vpn_name}" {{
  customer_gateway_id = aws_customer_gateway.{vpn_cgw_name}.id
  transit_gateway_id  = aws_ec2_transit_gateway.{vpn_tgw_name}.id

  type       = "ipsec.1"

  tags = {{
    Name = "{vpn_name}"
  }}
}}
''')
    hf.print_section_banner('End Describe VPNs')