#!/bin/python3
"""boto3 client connector."""
import boto3

#set up session to aws
class BOTOclient:
    """Class for boto3 client connector."""
    def __init__(self, boto_type, profile_name, region):
        """Initiate client session."""
        self.name = profile_name
        self.region = region
        self.type = boto_type
        self.session = boto3.Session(profile_name=self.name)
        self.client = self.session.client(self.type,region_name=self.region)
    def get_client(self):
        """Get client session."""
        return self.client
