import src.helpers as hf
import src.getters as gf
#describe transit gateway vpn attachments
def describe_vpn(session):
    """Function to describe the TGW VPN Attachments."""
    hf.print_section_banner('Begin Describe TGW VPN Attachments')
    response = session.describe_transit_gateway_attachments()
    tgw_array = response['TransitGatewayAttachments']
    #iterate through array of VPNs
    for my_arr in tgw_array:
        vpn_state = my_arr['State']
        att_type = my_arr['ResourceType']
        if vpn_state == 'available' and att_type == 'vpn':
            vpn_id = my_arr['ResourceId']
            my_tag_info = my_arr['Tags']
            vpn_name = "Unset"
            for my_item in my_tag_info:
                key = my_item['Key']
                if key == 'Name':
                    vpn_name = my_item['Value']
            #if vpn_name is 'unset' then check the vpn itself for name tag
            if vpn_name == 'Unset':
                vpn_name = gf.get_vpn_name_by_id(session,vpn_id)
            #descriptive name for the attachment tag i.e. TGW-Attach-VPN-yyy-zzz
            if 'TGW-Attach-' not in vpn_name:
                vpn_descr_name = 'TGW-Attach-' + vpn_name
            else:
                vpn_descr_name = vpn_name
            '''    
            #convert the VCG VPN attachment name to generic terraform names i.e. VPN-yyy-zzz
            vpn_name = hf.vcg_check(vpn_name)
            #generic name for VPN attachment i.e TGW-Attach-VPN-yyy-zzz
            '''
            if 'TGW-Attach-' not in vpn_name:
                vpn_attach_name = 'TGW-Attach-' + vpn_name
            else:
                vpn_attach_name = vpn_name    
            print(f'#TGW VPN Attachment for {vpn_descr_name}')
            print(f'''data "aws_ec2_transit_gateway_vpn_attachment" "{vpn_attach_name}" {{
  transit_gateway_id = aws_ec2_transit_gateway.TGW-VPN.id
  vpn_connection_id  = aws_vpn_connection.{vpn_name}.id
}}
''')
            print(f'#TGW VPN Attachment name tag for {vpn_descr_name}')
            print(f'''resource "aws_ec2_tag" "{vpn_attach_name}" {{
  resource_id  = data.aws_ec2_transit_gateway_vpn_attachment.{vpn_attach_name}.id
    key = "Name"
    value = "{vpn_descr_name}"
}}
''')
    hf.print_section_banner('End Describe TGW VPN Attachments')

#describe transit gateway peering attachments
def describe_peer(session,my_region):
    """Function to describe the TGW Peering Attachments."""
    hf.print_section_banner('Begin Describe TGW Peering Attachments')
    response = session.describe_transit_gateway_peering_attachments()
    tgw_array = response['TransitGatewayPeeringAttachments']
    #iterate through array of VPNs
    for my_arr in tgw_array:
        attach_state = my_arr['State']
        if attach_state == 'available':
            #we only backport if we are the requester region
            req_region = my_arr['RequesterTgwInfo']['Region']
            if req_region == my_region:
                peer_region = my_arr['AccepterTgwInfo']['Region']
                peer_tgw_id = my_arr['AccepterTgwInfo']['TransitGatewayId']
                my_tgw_id = my_arr['RequesterTgwInfo']['TransitGatewayId']
                my_tgw_name = gf.get_tgw_name_by_id(session,my_tgw_id)
                attach_id = my_arr['TransitGatewayAttachmentId']
                #iterate through the tag info to determine tag name
                my_tag_info = my_arr['Tags']
                peer_name = "Unset"
                for my_item in my_tag_info:
                    key = my_item['Key']
                    if key == 'Name':
                        peer_name = my_item['Value']
                #import statement
                import_data = f'{peer_name} {attach_id}'
                print(f'#terraform import aws_ec2_transit_gateway_peering_attachment.{import_data}')
                #tf code
                print(f'''resource "aws_ec2_transit_gateway_peering_attachment" "{peer_name}" {{
  peer_region  = "{peer_region}"
  transit_gateway_id  = aws_ec2_transit_gateway.{my_tgw_name}.id
  peer_transit_gateway_id = "{peer_tgw_id}"
  tags = {{
    Name = "{peer_name}"
  }}
}}
''')
    hf.print_section_banner('End Describe TGW Peering Attachments')

#describe transit gateway peering attachments accepter
def describe_accepter(session,my_region):
    """Function to describe the TGW Peering Attachment Accepters."""
    hf.print_section_banner('Begin Describe TGW Peering Attachments Accepters')
    response = session.describe_transit_gateway_peering_attachments()
    tgw_array = response['TransitGatewayPeeringAttachments']
    #iterate through array of VPNs
    for my_arr in tgw_array:
        attach_state = my_arr['State']
        if attach_state == 'available':
            #we only backport if we are the accepter region
            req_region = my_arr['RequesterTgwInfo']['Region']
            if req_region != my_region:
                attach_id = my_arr['TransitGatewayAttachmentId']
                #iterate through the tag info to determine tag name
                my_tag_info = my_arr['Tags']
                peer_name = "Unset"
                for my_item in my_tag_info:
                    key = my_item['Key']
                    if key == 'Name':
                        peer_name = my_item['Value']
                #import statement
                import_data = f'{peer_name} {attach_id}'
                print(f'#terraform import aws_ec2_transit_gateway_peering_attachment_accepter.{import_data}')
                #tf code
                print(f'''resource "aws_ec2_transit_gateway_peering_attachment_accepter" "{peer_name}" {{
  transit_gateway_attachment_id = "{attach_id}"
  tags = {{
    Name = "{peer_name}"
    Side = "Accepter"
  }}
}}
''')
    hf.print_section_banner('End Describe TGW Peering Attachments')