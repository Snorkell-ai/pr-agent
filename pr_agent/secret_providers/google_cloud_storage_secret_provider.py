import ujson
from google.cloud import storage

from pr_agent.config_loader import get_settings
from pr_agent.log import get_logger
from pr_agent.secret_providers.secret_provider import SecretProvider


class GoogleCloudStorageSecretProvider(SecretProvider):
    def __init__(self):
        """Save the processed files map to a JSON file.
        
        Function parameters should be documented in the ``Args`` section. The name of each parameter is required. The type and
        description of each parameter is optional, but should be included if not obvious.
        
        Args:
            dictionary (dict): The processed files map.
        
        Returns:
            bool: True if successful, False otherwise.
            The return type is optional and may be specified at the beginning of
            the ``Returns`` section followed by a colon.
            The ``Returns`` section may span multiple lines and paragraphs.
            Following lines should be indented to match the first line.
            The ``Returns`` section supports any reStructuredText formatting,
            including literal blocks::
                
                {
                'param1': param1,
                'param2': param2
                }
        """
        try:
            self.client = storage.Client.from_service_account_info(ujson.loads(get_settings().google_cloud_storage.
                                                                               service_account))
            self.bucket_name = get_settings().google_cloud_storage.bucket_name
            self.bucket = self.client.bucket(self.bucket_name)
        except Exception as e:
            get_logger().error(f"Failed to initialize Google Cloud Storage Secret Provider: {e}")
            raise e

    def get_secret(self, secret_name: str) -> str:
        """Save the processed files map to a JSON file.
        
        Function parameters should be documented in the ``Args`` section. The name of each parameter is required. The type and
        description of each parameter is optional, but should be included if not obvious.
        
        Args:
            dictionary (dict): The processed files map.
        
        Returns:
            bool: True if successful, False otherwise.
            The return type is optional and may be specified at the beginning of
            the ``Returns`` section followed by a colon.
            The ``Returns`` section may span multiple lines and paragraphs.
            Following lines should be indented to match the first line.
            The ``Returns`` section supports any reStructuredText formatting,
            including literal blocks::
                
                {
                'param1': param1,
                'param2': param2
                }
        """
        try:
            blob = self.bucket.blob(secret_name)
            return blob.download_as_string()
        except Exception as e:
            get_logger().warning(f"Failed to get secret {secret_name} from Google Cloud Storage: {e}")
            return ""

    def store_secret(self, secret_name: str, secret_value: str):
        """Save the processed files map to a JSON file.
        
        Function parameters should be documented in the ``Args`` section. The name of each parameter is required. The type and
        description of each parameter is optional, but should be included if not obvious.
        
        Args:
            dictionary (dict): The processed files map.
        
        Returns:
            bool: True if successful, False otherwise.
            The return type is optional and may be specified at the beginning of
            the ``Returns`` section followed by a colon.
            The ``Returns`` section may span multiple lines and paragraphs.
            Following lines should be indented to match the first line.
            The ``Returns`` section supports any reStructuredText formatting,
            including literal blocks::
                
                {
                'param1': param1,
                'param2': param2
                }
        """
        try:
            blob = self.bucket.blob(secret_name)
            blob.upload_from_string(secret_value)
        except Exception as e:
            get_logger().error(f"Failed to store secret {secret_name} in Google Cloud Storage: {e}")
            raise e
