#conversion method for bool to string -
#aws returns bool for true false but tf requires this as a string
def bool_to_string(aws_bool):
    """Function to convert bool to string value."""
    if aws_bool:
        return "true"
    return "false"


def print_section_banner(text):
    """Function to print section banner."""
    print(f'############################### {text} ############################### ')



#string manipulator for VeloCloud VPN Imports
def vcg_check(vpn_name):
    """Internal function for naming VPN."""
    if 'VCG' in vpn_name and 'PRIMARY' in vpn_name:
        return 'VPN-VELOCLOUD-PRIMARY'
    if 'VCG' in vpn_name and 'BACKUP' in vpn_name:
        return 'VPN-VELOCLOUD-BACKUP'
    return vpn_name