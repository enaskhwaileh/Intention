"""Offline configuration tests using synthetic credentials only."""

import contextlib
import io
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import MagicMock, patch

from intention_grounding.cli import main
from intention_grounding.groq_config import groq_api_key, groq_model_id
from intention_grounding.grounder import GroqGrounderProvider
from intention_grounding.interpreter.providers import GroqProvider, list_available_models
from intention_grounding.provider_errors import MissingGroqCredentialError, MissingGroqModelError


class GroqConfigurationTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.env_path = Path(self.directory.name) / 'intention_grounding' / '.env'
        self.env_path.parent.mkdir()
        env_patch = patch('intention_grounding.groq_config.ENV_PATH', self.env_path)
        env_patch.start()
        self.addCleanup(env_patch.stop)

    def test_path_is_independent_of_working_directory(self):
        self.env_path.write_text('GROQ_API_KEY=synthetic-key\nGROQ_MODEL_ID=synthetic-model\n')
        original = Path.cwd()
        self.addCleanup(os.chdir, original)
        with patch.dict(os.environ, {}, clear=True):
            for directory in (Path(self.directory.name), self.env_path.parent, Path(tempfile.gettempdir())):
                os.chdir(directory)
                self.assertEqual('synthetic-key', groq_api_key())
                self.assertEqual('synthetic-model', groq_model_id())
                self.assertEqual('synthetic-model', GroqProvider().model)
                self.assertEqual('synthetic-model', GroqGrounderProvider().model)

    def test_exported_values_precede_env_and_mocked_model_listing(self):
        self.env_path.write_text('GROQ_API_KEY=file-only-key\nGROQ_MODEL_ID=file-model\n')
        factory = MagicMock()
        factory.return_value.__enter__.return_value.models.list.return_value.data = []
        with patch.dict(os.environ, {'GROQ_API_KEY': 'exported-key', 'GROQ_MODEL_ID': 'exported-model'}, clear=True):
            self.assertEqual('exported-key', groq_api_key())
            self.assertEqual('exported-model', groq_model_id())
            self.assertEqual('override-model', groq_model_id('override-model'))
            self.assertEqual([], list_available_models(client_factory=factory))
        factory.assert_called_once_with(api_key='exported-key', timeout=30.0, max_retries=0)

    def test_missing_and_empty_values_are_sanitized(self):
        for content in ('', 'GROQ_API_KEY=\nGROQ_MODEL_ID=\n'):
            with self.subTest(content=bool(content)):
                self.env_path.write_text(content)
                with patch.dict(os.environ, {}, clear=True):
                    with self.assertRaisesRegex(MissingGroqCredentialError, 'GROQ_API_KEY is missing or empty'):
                        groq_api_key()
                    with self.assertRaisesRegex(MissingGroqModelError, 'GROQ_MODEL_ID is missing or empty'):
                        groq_model_id()

    def test_env_credential_absent_from_output_and_artifacts(self):
        secret = 'synthetic-artifact-secret'
        self.env_path.write_text(f'GROQ_API_KEY={secret}\nGROQ_MODEL_ID=synthetic-model\n')

        class FailingProvider:
            metadata = {'provider': 'mock', 'model': 'synthetic-model'}

            def invoke(self, *_):
                raise RuntimeError('Authorization: Bearer ' + secret)

        output = Path(self.directory.name) / 'runs'
        stream = io.StringIO()
        with patch.dict(os.environ, {}, clear=True), \
             patch('intention_grounding.cli.GroqProvider', return_value=FailingProvider()), \
             patch('intention_grounding.cli.GroqGrounderProvider', return_value=FailingProvider()), \
             contextlib.redirect_stdout(stream):
            self.assertEqual(2, main(['--mode', 'groq', '--input', 'Compare income.', '--output', str(output)]))
        self.assertNotIn(secret, stream.getvalue())
        for artifact in next(output.iterdir()).iterdir():
            self.assertNotIn(secret, artifact.read_text())


if __name__ == '__main__':
    unittest.main()
