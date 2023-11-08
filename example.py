#!/bin/python3
"""Example script for running boto3 describe scripts to backport existing AWS infrastructure."""
from src.client import BOTOclient
import src.describe_cgws as cgws
import src.describe_vpns as vpns
import src.describe_tgws as tgws
import src.describe_attachments as attach
import src.describe_prefixlists as prefix
def main():
    """Main function for example script."""
    my_type = '' ## ec2 for most
    my_profile = '' ## profile name for the account (usually in ~/.aws/ credentials or config)
    my_region = '' ## region name
    my_account_owner_id = '' ## account id
    client = BOTOclient(my_type, my_profile, my_region)
    my_client = client.get_client()
    cgws.describe(my_client)
    vpns.describe(my_client)
    tgws.describe_tgws(my_client)
    tgws.describe_rtbs(my_client)
    attach.describe_vpn(my_client)
    attach.describe_peer(my_client, my_region)
    attach.describe_accepter(my_client, my_region)
    prefix.describe_lists(my_client, my_account_owner_id)
    prefix.describe_refs(my_client)

if __name__ == "__main__":
    main()
