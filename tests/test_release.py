import importlib.util
from pathlib import Path
import os
import subprocess
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('release', Path(__file__).resolve().parents[1] / '.github/scripts/release.py')
release = importlib.util.module_from_spec(spec)
spec.loader.exec_module(release)


class ReleaseTests(unittest.TestCase):
    def test_selection(self):
        cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                def git(*args):
                    subprocess.run(['git', *args], check=True, capture_output=True)
                git('init'); git('config', 'user.name', 'Test'); git('config', 'user.email', 'test@example.com')
                Path('VERSION').write_text('0.1.0'); Path('RELEASE').write_text('0.1.0')
                git('add', '.'); git('commit', '-m', 'release')
                tag, sha, create = release.select()
                self.assertEqual(tag, 'v0.1.0'); self.assertTrue(create)
                git('tag', tag)
                self.assertFalse(release.select()[2])
                git('commit', '--allow-empty', '-m', 'docs')
                self.assertFalse(release.select()[2])
                Path('VERSION').write_text('0.2.0')
                with self.assertRaises(ValueError): release.select()
                Path('RELEASE').write_text('0.2.0')
                self.assertTrue(release.select()[2])
                Path('VERSION').write_text('../bad')
                with self.assertRaises(ValueError): release.select()
            finally:
                os.chdir(cwd)
