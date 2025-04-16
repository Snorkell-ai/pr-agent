import json
import os

from pr_agent.algo.utils import get_settings, github_action_output


class TestGitHubOutput:
    def test_github_action_output_enabled(self, monkeypatch, tmp_path):
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
        get_settings().set('GITHUB_ACTION_CONFIG.ENABLE_OUTPUT', True)
        monkeypatch.setenv('GITHUB_OUTPUT', str(tmp_path / 'output'))
        output_data = {'key1': {'value1': 1, 'value2': 2}}
        key_name = 'key1'

        github_action_output(output_data, key_name)

        with open(str(tmp_path / 'output'), 'r') as f:
            env_value = f.read()

        actual_key = env_value.split('=')[0]
        actual_data = json.loads(env_value.split('=')[1])

        assert actual_key == key_name
        assert actual_data == output_data[key_name]

    def test_github_action_output_disabled(self, monkeypatch, tmp_path):
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
        get_settings().set('GITHUB_ACTION_CONFIG.ENABLE_OUTPUT', False)
        monkeypatch.setenv('GITHUB_OUTPUT', str(tmp_path / 'output'))
        output_data = {'key1': {'value1': 1, 'value2': 2}}
        key_name = 'key1'

        github_action_output(output_data, key_name)

        assert not os.path.exists(str(tmp_path / 'output'))

    def test_github_action_output_notset(self, monkeypatch, tmp_path):
        # not set config
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
        monkeypatch.setenv('GITHUB_OUTPUT', str(tmp_path / 'output'))
        output_data = {'key1': {'value1': 1, 'value2': 2}}
        key_name = 'key1'

        github_action_output(output_data, key_name)

        assert not os.path.exists(str(tmp_path / 'output'))

    def test_github_action_output_error_case(self, monkeypatch, tmp_path):
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
        monkeypatch.setenv('GITHUB_OUTPUT', str(tmp_path / 'output'))
        output_data = None # invalid data
        key_name = 'key1'

        github_action_output(output_data, key_name)

        assert not os.path.exists(str(tmp_path / 'output'))
