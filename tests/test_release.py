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
                script = str(Path(release.__file__).resolve())
                output = Path('outputs')
                env = dict(os.environ, GITHUB_OUTPUT=str(output), GITHUB_REF='refs/heads/master',
                           GITHUB_EVENT_NAME='workflow_dispatch', RELEASE_TAG='v0.1.0')
                subprocess.run([os.sys.executable, script], env=env, check=True)
                result = dict(line.split('=', 1) for line in output.read_text().splitlines())
                self.assertEqual(result['sha'], sha)
                self.assertEqual(result['publish'], 'true')
                self.assertEqual(result['create'], 'false')
                for bad in ['v9.9.9', '../bad']:
                    env['RELEASE_TAG'] = bad
                    self.assertNotEqual(subprocess.run([os.sys.executable, script], env=env, capture_output=True).returncode, 0)
                Path('VERSION').write_text('0.2.0')
                with self.assertRaises(ValueError): release.select()
                Path('RELEASE').write_text('0.2.0')
                self.assertTrue(release.select()[2])
                Path('VERSION').write_text('../bad')
                with self.assertRaises(ValueError): release.select()
            finally:
                os.chdir(cwd)
