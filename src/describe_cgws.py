import src.helpers as hf
#describe customer gateways
def describe(session):
    """Function to describe the CGW's."""
    hf.print_section_banner('Begin Describe CGWs')
    response = session.describe_customer_gateways()
    cgw_array = response['CustomerGateways']
    #iterate through array of TGWs
    for my_arr in cgw_array:
        cgw_state = my_arr['State']
        if cgw_state == 'available':
            cgw_asn = my_arr['BgpAsn']
            cgw_ip = my_arr['IpAddress']
            cgw_id = my_arr['CustomerGatewayId']
            my_tag_info = my_arr['Tags']
            #iterate through the tag info to determine tag name
            cgw_name = "Unset"
            for my_item in my_tag_info:
                key = my_item['Key']
                if key == 'Name':
                    cgw_name = my_item['Value']
            #import statement
            print(f'#terraform import aws_customer_gateway.{cgw_name} {cgw_id}')
            #tf code
            print(f'''resource "aws_customer_gateway" "{cgw_name}" {{
  bgp_asn    = {cgw_asn}
  ip_address = "{cgw_ip}"
  type       = "ipsec.1"

  tags = {{
    Name = "{cgw_name}"
  }}
}}
''')
    hf.print_section_banner('End Describe CGWs')