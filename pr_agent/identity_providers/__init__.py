from pr_agent.config_loader import get_settings
from pr_agent.identity_providers.default_identity_provider import \
    DefaultIdentityProvider

_IDENTITY_PROVIDERS = {
    'default': DefaultIdentityProvider
}


def get_identity_provider():
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
    identity_provider_id = get_settings().get("CONFIG.IDENTITY_PROVIDER", "default")
    if identity_provider_id not in _IDENTITY_PROVIDERS:
        raise ValueError(f"Unknown identity provider: {identity_provider_id}")
    return _IDENTITY_PROVIDERS[identity_provider_id]()
