import src.helpers as hf
import src.getters as gf
#describe prefix lists
def describe_lists(session, owner_id):
    """Function to describe Managed Prefix Lists."""
    hf.print_section_banner('Begin Describe Prefix Lists')
    #using network account as filter for owner id
    response = session.describe_managed_prefix_lists(
                    Filters=[{'Name': 'owner-id','Values': [owner_id,]}]
                )
    tgw_array = response['PrefixLists']
    #iterate through array of VPNs
    for my_arr in tgw_array:
        pfx_list_id = my_arr['PrefixListId']
        pfx_list_name = my_arr['PrefixListName']
        pfx_list_addr_fam = my_arr['AddressFamily']
        pfx_list_max_entry = my_arr['MaxEntries']
        #import statement
        print(f'#terraform import aws_ec2_managed_prefix_list.{pfx_list_name} {pfx_list_id}')
        #tf code
        print(f'''resource "aws_ec2_managed_prefix_list" "{pfx_list_name}" {{
  name           = "{pfx_list_name}"
  address_family = "{pfx_list_addr_fam}"
  max_entries    = {pfx_list_max_entry} ''')
        response2 = session.get_managed_prefix_list_entries(PrefixListId=pfx_list_id)

        entry_arr = response2['Entries']
        for my_arr2 in entry_arr:
            cidr = my_arr2['Cidr']
            #print(cidr)
            print(f'  entry {{cidr = "{cidr}"}} ')
        #print tfclosing brackets
        print('}')

    hf.print_section_banner('End Describe Prefix Lists')

#describe tgw prefix list references
#get_transit_gateway_prefix_list_references(TransitGatewayRouteTableId=tgw_rtb_id)
def describe_refs(session):
    """Function to describe TGW Prefix List References."""
    hf.print_section_banner('Begin Describe TGW Prefix List References')
    tgw_rtb_ids = gf.get_tgw_rtb_ids(session)
    for rtb in tgw_rtb_ids:
        response = session.get_transit_gateway_prefix_list_references(
            TransitGatewayRouteTableId=rtb
            )
        ref_array = response['TransitGatewayPrefixListReferences']
        #iterate through array of VPNs
        for my_arr in ref_array:
            blackhole = hf.bool_to_string(my_arr['Blackhole'])
            pfx_list_id = my_arr['PrefixListId']
            pfx_list_name = gf.get_pfx_list_name_by_id(session,pfx_list_id)
            tgw_rtb_id = my_arr['TransitGatewayRouteTableId']
            tgw_rtb_name = gf.get_tgw_rtb_name_by_id(session,tgw_rtb_id)
            tgw_attach_id = my_arr['TransitGatewayAttachment']['TransitGatewayAttachmentId']
            #concat tgw_rtb_id _ pfx_list_id to get tf import id
            pfx_list_import_id = tgw_rtb_id + '_' + pfx_list_id
            pfx_list_import_name = tgw_rtb_name + '_' + pfx_list_name
            #import statement
            import_data = f'{pfx_list_import_name} {pfx_list_import_id}'
            print(f'#terraform import aws_ec2_transit_gateway_prefix_list_reference.{import_data}')
            #tf code
            print(f'''resource "aws_ec2_transit_gateway_prefix_list_reference" "{pfx_list_import_name}" {{
    blackhole = {blackhole}
    prefix_list_id  = aws_ec2_managed_prefix_list.{pfx_list_name}.id
    transit_gateway_route_table_id = aws_ec2_transit_gateway_route_table.{tgw_rtb_name}.id
    transit_gateway_attachment_id  = "{tgw_attach_id}"
    }}
    ''')
    hf.print_section_banner('End Describe TGW Prefix List References')