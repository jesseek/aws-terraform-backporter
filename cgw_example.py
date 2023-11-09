#!/bin/python3
"""Example script for running boto3 describe scripts to backport existing AWS infrastructure."""
from src.client import BOTOclient
import src.describe_cgws as cgws

def main():
    """Main function for example script."""
    my_type = 'ec2' ## ec2 for most
    my_profile = '' ## profile name for the account (usually in ~/.aws/ credentials or config)
    my_region = '' ## region name
    client = BOTOclient(my_type, my_profile, my_region)
    my_client = client.get_client()
    cgws.describe(my_client)

if __name__ == "__main__":
    main()
