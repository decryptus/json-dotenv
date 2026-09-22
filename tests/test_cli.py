import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from dotenv import dotenv_values

ROOT = Path(__file__).resolve().parents[1]


class CLITests(unittest.TestCase):
    def call(self, *args, data='', ok=True):
        env = {k: v for k, v in os.environ.items() if not k.startswith('JSON_DOTENV_')}
        env.update(JSON_DOTENV_LOGFILE='/nonexistent/review.log', TEST_LITERAL='expanded')
        r = subprocess.run([sys.executable, str(ROOT / 'bin/json-dotenv'), *args],
                           input=data, text=True, capture_output=True, env=env)
        self.assertEqual(r.returncode == 0, ok, r.stderr)
        if not ok:
            self.assertNotIn('Traceback', r.stderr)
        return r.stdout

    def test_standard_syntax(self):
        data = "# heading\nA=one # comment\n# another\nB='hello world'\nexport C=three\nEMPTY=\nBARE\n"
        self.assertEqual(json.loads(self.call('list', '-f', '-', data=data)),
                         dict(A='one', B='hello world', C='three', EMPTY='', BARE=None))

    def test_roundtrip(self):
        for value in ['say "hello"', "it's fine", 'a\\b', 'line\nnext\tend', '${TEST_LITERAL}', 'é😀', '', 'a # b']:
            for quote in ['always', 'auto']:
                with self.subTest(value=value, quote=quote):
                    text = self.call('set', '-f', '', '-k', 'A', '-v', value, '--format', 'env', '-q', quote)
                    self.assertEqual(dotenv_values(stream=io.StringIO(text), interpolate=False)['A'], value)
                    self.assertEqual(json.loads(self.call('list', '-f', '-', data=text))['A'], value)

    def test_interpolation(self):
        for args, data in [(('list', '-f', '-'), 'A=${TEST_LITERAL}\n'),
                           (('set', '-f', '', '-k', 'A', '-v', '${TEST_LITERAL}'), '')]:
            self.assertEqual(json.loads(self.call(*args, data=data))['A'], '${TEST_LITERAL}')
            self.assertEqual(json.loads(self.call(*args, '--allow-envvar', data=data))['A'], 'expanded')

    def test_validation(self):
        for args in [('set', '-k', 'A', '-k', 'B', '-v', '1'),
                     ('set', '-k', 'A', '-v', '1', '-v', '2'),
                     ('set', '-k', 'A=B', '-v', '1'), ('get',),
                     ('set', '-k', 'A', '-v', 'a b', '--format', 'env', '-q', 'never')]:
            self.call(*args, '-f', '', ok=False)
        self.call('list', '-f', '-', data='A="unterminated\n', ok=False)

    def test_get_unset_keys(self):
        data = 'A=one\nB=two\n'
        self.assertEqual(json.loads(self.call('get', '-f', '-', '-k', 'B', data=data)), {'B': 'two'})
        self.assertEqual(json.loads(self.call('unset', '-f', '-', '-k', 'B', data=data)), {'A': 'one'})
        self.assertEqual(json.loads(self.call('keys', '-f', '-', data=data)), ['A', 'B'])
        self.call('get', '-f', '-', '-k', 'C', data=data, ok=False)
        self.assertEqual(json.loads(self.call('get', '-f', '-', '-k', 'C', '--force', data=data)), {})

    def test_example(self):
        result = json.loads(self.call('list', '-f', str(ROOT / 'foo.env')))
        self.assertEqual(len(result), 5)
        self.assertIn("${vars['base_url_https']}", result['MONIT_DOCKER_CONFIG'])

    def test_output_permissions_and_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'config.env'
            path.write_text('A=one\n'); path.chmod(0o640)
            self.call('set', '-f', str(path), '-k', 'A', '-v', 'two', '--format', 'env', '-o', str(path))
            self.assertEqual(path.stat().st_mode & 0o777, 0o640)
            before = path.read_text()
            self.call('set', '-f', str(path), '-k', 'A=B', '-v', 'bad', '-o', str(path), ok=False)
            self.assertEqual(path.read_text(), before)
            link = Path(tmp) / 'link'; link.symlink_to(path)
            self.call('list', '-f', str(path), '-o', str(link), ok=False)
            new = Path(tmp) / 'new'
            self.call('list', '-f', str(path), '-o', str(new))
            self.assertEqual(new.stat().st_mode & 0o777, 0o600)
            self.assertEqual(sorted(p.name for p in Path(tmp).iterdir()), ['config.env', 'link', 'new'])
