# json-dotenv

Read and transform `.env` files from the command line, with JSON output for scripts.
Select several keys, set or remove several values, and pipe the result into other tools.
The input file is unchanged unless explicitly selected as the output.

## Install

Requires Python 3.10 or newer, on Unix-like systems.

```sh
pip install json-dotenv
```

To install this checkout (including changes not yet published on PyPI):

```sh
pip install .
```

## Examples

Given `.env`:

```dotenv
APP_NAME='My app'
PORT=8080
TEMPLATE=${APP_NAME}
```

```sh
json-dotenv list -f .env
# {"APP_NAME": "My app", "PORT": "8080", "TEMPLATE": "${APP_NAME}"}

json-dotenv get -f .env -k APP_NAME -k PORT
json-dotenv keys -f .env
json-dotenv set -f .env -k PORT -v 9090 -k MODE -v production
json-dotenv unset -f .env -k TEMPLATE

# Read stdin and write a new dotenv file.
cat .env | json-dotenv set -f - -k PORT -v 9090 --format env -o result.env

# Start with no input file.
json-dotenv set -f '' -k APP_NAME -v 'My app' --format env

# Explicitly replace the original, after a successful conversion.
json-dotenv set -f .env -k PORT -v 9090 --format env -o .env
```

JSON output is a dictionary, except `keys`, which returns an array. Values remain
strings; a bare key without `=` becomes JSON `null`, while `KEY=` becomes `""`.
JSON is an output format; JSON input is not supported.

## Multiline values and interpolation

Use standard quoted dotenv values for multiline content:

```dotenv
CONFIG="first line
second line"
```

`${VARIABLE}` expressions are literal by default, both in input files and in
values passed to `set`. Add `--allow-envvar` to expand them. Shell arguments must
also be single-quoted to prevent expansion by your shell:

```sh
json-dotenv set -f '' -k TEMPLATE -v '${HOME}'
json-dotenv set -f '' -k TEMPLATE -v '${HOME}' --allow-envvar
```

With interpolation enabled, file values follow python-dotenv's expansion rules.
New values are expanded in argument order, using the parsed file and earlier
assignments ahead of process environment variables. Undefined references become
empty strings unless they provide a supported default.

## Output and errors

- `--format json` is the default; `--format env` generates dotenv syntax.
- `-q always` quotes all assigned dotenv values; `-q auto` quotes when needed.
- `-q never` rejects values that need quoting, rather than silently corrupting them.
- `--force` ignores missing keys for `get` and `unset`; it does not bypass syntax errors.
- Malformed input, invalid key names and mismatched key/value counts fail before output.
- `-o FILE` replaces the file atomically using a temporary file in the same directory.
  Existing Unix ownership and permission bits are preserved; new files use mode `0600`.
  Symbolic-link destinations are rejected. ACLs and extended attributes are not preserved.
- Output is dotenv data, not an executable shell script. Do not `source` untrusted output.

Exit codes: `0` success, `2` command-line syntax error, `4` invalid data or missing
key, `5` file I/O failure, `6` unexpected error, `255` interruption.
Run `json-dotenv --help` for all options. The legacy `-c COMMAND` form remains accepted.
Existing `JSON_DOTENV_*` options remain available: `COMMAND`, `FILE`, `OUTPUT`,
`QUOTE`, `ALLOW_ENVVAR`, and `LOGFILE`.

## Migration from 0.0.29

Version 0.1.0 requires Python 3.10+. It uses standard dotenv parsing: comments
are ignored, single quotes are handled correctly, and multiline values must be
quoted. Legacy unquoted continuation lines must be converted to quoted values.
`set` now preserves `${...}` unless interpolation is explicitly enabled.
Formatting and comments are not preserved when generating a new dotenv file.
Duplicate keys use the last value. Names must match `[A-Za-z_][A-Za-z0-9_]*`.

## Development and automatic tags

```sh
python -m pip install -r requirements.txt build
python -m unittest discover -s tests -v
python -m build
```

CI tests Python 3.10–3.14 and builds the source distribution and wheel.
To release, update `VERSION`, `RELEASE`, `setup.yml`, `bin/json-dotenv`'s
`__version__`, and `CHANGELOG` together, then merge into `master`.
After successful tests, GitHub Actions creates `vX.Y.Z` at that commit.
Existing ancestor tags are left untouched, so documentation-only commits do not
move releases. A conflicting tag fails the workflow. Manual workflow execution
on `master` can retry tag creation. Only the built-in GitHub token is required.

### Automatic PyPI publication

After the tests and tag creation, the same workflow builds the tagged code,
checks the distributions, and uploads them to PyPI in a separate job using
Trusted Publishing (OIDC). No stored PyPI API token is needed. Ordinary commits
on an already released version do not republish it. Existing PyPI files are
skipped on retries; they cannot be overwritten.

One-time setup: in the PyPI project's **Manage → Publishing** page, add a GitHub
publisher with these exact values:

| Field | Value |
| --- | --- |
| Owner | `decryptus` |
| Repository | `json-dotenv` |
| Workflow filename | `ci.yml` |
| Environment | `pypi` |

To publish the existing `v0.1.0` tag or retry a release, open **Actions → Tests,
version tag and PyPI → Run workflow**, select `master` and enter the tag. The
selected tag must belong to master's history and match its version files. With
no tag input, a manual run follows the normal automatic version selection.

The publication job needs the PyPI publisher configured before it can succeed.
GitHub release notes are not created. Publication occurs in the same workflow
as tagging, so it does not depend on a bot-created tag triggering another run.

Licensed under GPL-3.0-or-later.
