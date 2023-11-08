import src.helpers as hf
import src.getters as gf
#describe transit gateways
def describe_tgws(session):
    """Function to describe the TGW's."""
    hf.print_section_banner('Begin Describe TGWs')
    response = session.describe_transit_gateways()
    tgw_array = response['TransitGateways']
    #iterate through array of TGWs
    for my_arr in tgw_array:
        tgw_state = my_arr['State']
        if tgw_state == 'available':
            tgw_id = my_arr['TransitGatewayId']
            tgw_asn = my_arr['Options']['AmazonSideAsn']
            tgw_def_rt_tbl_assoc = my_arr['Options']['DefaultRouteTableAssociation']
            tgw_def_rt_tbl_prop = my_arr['Options']['DefaultRouteTablePropagation']
            my_tag_info = my_arr['Tags']
            #iterate through the tag info to determine tag name
            tgw_name = "Unset"
            for my_item in my_tag_info:
                key = my_item['Key']
                if key == 'Name':
                    tgw_name = my_item['Value']
            #import statement
            print(f'#terraform import aws_ec2_transit_gateway.{tgw_name} {tgw_id}')
            #tf code
            print(f'''resource "aws_ec2_transit_gateway" "{tgw_name}" {{
  description = "{tgw_name}"              
  amazon_side_asn = {tgw_asn}
  default_route_table_association = "{tgw_def_rt_tbl_assoc}"
  default_route_table_propagation = "{tgw_def_rt_tbl_prop}"
  tags = {{
    Name = "{tgw_name}"
  }}
}}
''')
    hf.print_section_banner('End Describe TGWs')

#describe transit gateway route tables
def describe_rtbs(session):
    """Function to describe the TGW Route Table's."""
    hf.print_section_banner('Begin Describe TGW RTBs')
    response = session.describe_transit_gateway_route_tables()
    rtb_array = response['TransitGatewayRouteTables']
    #iterate through array of VPNs
    for my_arr in rtb_array:
        rtb_state = my_arr['State']
        if rtb_state == 'available':
            rtb_id = my_arr['TransitGatewayRouteTableId']
            rtb_tgw_id = my_arr['TransitGatewayId']
            rtb_tgw_name = gf.get_tgw_name_by_id(session,rtb_tgw_id)
            my_tag_info = my_arr['Tags']
            #iterate through the tag info to determine tag name
            rtb_name = "Unset"
            for my_item in my_tag_info:
                key = my_item['Key']
                if key == 'Name':
                    rtb_name = my_item['Value']
            #import statement
            print(f'#terraform import aws_ec2_transit_gateway_route_table.{rtb_name} {rtb_id}')
            #tf code
            print(f'''resource "aws_ec2_transit_gateway_route_table" "{rtb_name}" {{
  transit_gateway_id  = aws_ec2_transit_gateway.{rtb_tgw_name}.id
  tags = {{
    Name = "{rtb_name}"
  }}
}}
''')
    hf.print_section_banner('End Describe TGW RTBs')