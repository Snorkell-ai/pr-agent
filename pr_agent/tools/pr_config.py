from dynaconf import Dynaconf

from pr_agent.config_loader import get_settings
from pr_agent.git_providers import get_git_provider
from pr_agent.log import get_logger


class PRConfig:
    """
    The PRConfig class is responsible for listing all configuration options available for the user.
    """
    def __init__(self, pr_url: str, args=None, ai_handler=None):
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
        self.git_provider = get_git_provider()(pr_url)

    async def run(self):
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
        get_logger().info('Getting configuration settings...')
        get_logger().info('Preparing configs...')
        pr_comment = self._prepare_pr_configs()
        if get_settings().config.publish_output:
            get_logger().info('Pushing configs...')
            self.git_provider.publish_comment(pr_comment)
            self.git_provider.remove_initial_comment()
        return ""

    def _prepare_pr_configs(self) -> str:
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
        conf_file = get_settings().find_file("configuration.toml")
        conf_settings = Dynaconf(settings_files=[conf_file])
        configuration_headers = [header.lower() for header in conf_settings.keys()]
        relevant_configs = {
            header: configs for header, configs in get_settings().to_dict().items()
            if (header.lower().startswith("pr_") or header.lower().startswith("config")) and header.lower() in configuration_headers
        }

        skip_keys = ['ai_disclaimer', 'ai_disclaimer_title', 'ANALYTICS_FOLDER', 'secret_provider', "skip_keys", "app_id", "redirect",
                     'trial_prefix_message', 'no_eligible_message', 'identity_provider', 'ALLOWED_REPOS',
                     'APP_NAME', 'PERSONAL_ACCESS_TOKEN', 'shared_secret', 'key', 'AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'user_token',
                     'private_key', 'private_key_id', 'client_id', 'client_secret', 'token', 'bearer_token', 'jira_api_token','webhook_secret']
        partial_skip_keys = ['key', 'secret', 'token', 'private']
        extra_skip_keys = get_settings().config.get('config.skip_keys', [])
        if extra_skip_keys:
            skip_keys.extend(extra_skip_keys)
        skip_keys_lower = [key.lower() for key in skip_keys]


        markdown_text = "<details> <summary><strong>🛠️ PR-Agent Configurations:</strong></summary> \n\n"
        markdown_text += f"\n\n```yaml\n\n"
        for header, configs in relevant_configs.items():
            if configs:
                markdown_text += "\n\n"
                markdown_text += f"==================== {header} ===================="
            for key, value in configs.items():
                if key.lower() in skip_keys_lower:
                    continue
                if any(skip_key in key.lower() for skip_key in partial_skip_keys):
                    continue
                markdown_text += f"\n{header.lower()}.{key.lower()} = {repr(value) if isinstance(value, str) else value}"
                markdown_text += "  "
        markdown_text += "\n```"
        markdown_text += "\n</details>\n"
        get_logger().info(f"Possible Configurations outputted to PR comment", artifact=markdown_text)
        return markdown_text
