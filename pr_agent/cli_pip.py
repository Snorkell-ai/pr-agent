from pr_agent import cli
from pr_agent.config_loader import get_settings


def main():
    # Fill in the following values
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
    provider = "github"  # GitHub provider
    user_token = "..."  # GitHub user token
    openai_key = "..."  # OpenAI key
    pr_url = "..."  # PR URL, for example 'https://github.com/Codium-ai/pr-agent/pull/809'
    command = "/review"  # Command to run (e.g. '/review', '/describe', '/ask="What is the purpose of this PR?"')

    # Setting the configurations
    get_settings().set("CONFIG.git_provider", provider)
    get_settings().set("openai.key", openai_key)
    get_settings().set("github.user_token", user_token)

    # Run the command. Feedback will appear in GitHub PR comments
    cli.run_command(pr_url, command)


if __name__ == '__main__':
    main()
