# json-dotenv

## Coding style and validation

- Keep fixed routes, schemas, enum choices, limits and patterns in named constants. In Python use `UPPER_CASE` for module constants and `_UPPER_CASE` for private ones.
- Centralize each identifier grammar, compile fixed regexes once and validate the entire identifier. Preserve existing selector semantics.
- Write technical error messages in English and expose stable machine-readable error codes. Keep localized user-facing text in the presentation layer.

## Configuration file format

- Prefer YAML (`.yaml` / `.yml`) over JSON for project configuration files: it is
  easier to read, supports comments and produces clearer diffs.
- JSON remains acceptable when a tool or ecosystem requires it or does not support
  YAML (for example `package.json`, `tsconfig.json`, `composer.json`). Converting
  existing JSON files is not required.
- When a tool accepts both formats, use YAML for new configuration.
- In YAML, quote ambiguous scalars (`"yes"`, `"no"`, `"on"`, `"off"`, versions such
  as `"1.10"`) to avoid implicit type conversion.

## Commit authorship

Write every commit as `decryptus <decryptus@users.noreply.github.com>`, as both author and committer (run `git config user.name decryptus` and `git config user.email decryptus@users.noreply.github.com` before committing, including when rebasing). Do not add `Co-Authored-By` lines, session links or any mention of an assistant or tool in commit messages. Do not rewrite history already published on the default branch to fix older commits.
