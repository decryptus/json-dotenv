"""Select a version tag without modifying Git refs."""
import os
from pathlib import Path
import re
import subprocess


def git(*args):
    return subprocess.check_output(['git', *args], text=True).strip()


def select():
    version = Path('VERSION').read_text().strip()
    if not re.fullmatch(r'(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)', version):
        raise ValueError('VERSION must be X.Y.Z')
    if Path('RELEASE').read_text().strip() != version:
        raise ValueError('VERSION and RELEASE differ')
    tag = 'v' + version
    head = git('rev-parse', 'HEAD')
    ref = 'refs/tags/' + tag
    exists = subprocess.run(['git', 'show-ref', '--verify', '--quiet', ref]).returncode == 0
    if exists:
        tagged = git('rev-parse', ref + '^{commit}')
        subprocess.run(['git', 'merge-base', '--is-ancestor', tagged, head], check=True)
    return tag, head, not exists


if __name__ == '__main__':
    requested = os.environ.get('RELEASE_TAG', '')
    if requested:
        if os.environ.get('GITHUB_EVENT_NAME') != 'workflow_dispatch' or os.environ.get('GITHUB_REF') != 'refs/heads/master':
            raise ValueError('Manual publication must run from master')
        if not re.fullmatch(r'v(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)', requested):
            raise ValueError('Expected vX.Y.Z')
        sha = git('rev-parse', '--verify', 'refs/tags/' + requested + '^{commit}')
        subprocess.run(['git', 'merge-base', '--is-ancestor', sha, 'HEAD'], check=True)
        if git('show', sha + ':VERSION') != requested[1:] or git('show', sha + ':RELEASE') != requested[1:]:
            raise ValueError('Tag and version files differ')
        tag, create, publish = requested, False, True
    else:
        tag, sha, create = select()
        publish = create or git('rev-parse', 'refs/tags/' + tag + '^{commit}') == sha
    with open(os.environ['GITHUB_OUTPUT'], 'a') as output:
        output.write(f'tag={tag}\nsha={sha}\ncreate={str(create).lower()}\npublish={str(publish).lower()}\n')
