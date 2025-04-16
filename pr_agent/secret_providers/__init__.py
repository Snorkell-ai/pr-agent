from pr_agent.config_loader import get_settings


def get_secret_provider():
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
    if not get_settings().get("CONFIG.SECRET_PROVIDER"):
        return None

    provider_id = get_settings().config.secret_provider
    if provider_id == 'google_cloud_storage':
        try:
            from pr_agent.secret_providers.google_cloud_storage_secret_provider import \
                GoogleCloudStorageSecretProvider
            return GoogleCloudStorageSecretProvider()
        except Exception as e:
            raise ValueError(f"Failed to initialize google_cloud_storage secret provider {provider_id}") from e
    else:
        raise ValueError("Unknown SECRET_PROVIDER")
