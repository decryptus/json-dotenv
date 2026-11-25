# json-dotenv

## Coding style and validation

- Keep fixed routes, schemas, enum choices, limits and patterns in named constants. In Python use `UPPER_CASE` for module constants and `_UPPER_CASE` for private ones.
- Centralize each identifier grammar, compile fixed regexes once and validate the entire identifier. Preserve existing selector semantics.
- Write technical error messages in English and expose stable machine-readable error codes. Keep localized user-facing text in the presentation layer.

## Shared component placement

- Before adding a dependency, implementing a local component or preparing a
  release, inspect the current capabilities of DWho, HTTPdis and Sonicprobe and
  reuse applicable functionality.
- For a new generic capability, assess whether it belongs in one of these shared
  libraries and record the placement decision in the contribution. Keep
  product-specific business rules in this repository.
- When a shared-library change is needed, validate it in its own repository
  against its contracts, supported versions and existing consumers. Then update
  this project's dependency and verify the integration before delivery. Follow
  each repository's release procedures and existing authorization scope.

## Test discovery and execution

- Verify the actual runner and every discovery root before adding or changing
  tests. A green command does not prove that all test declarations were loaded.
  Do not put standalone pytest functions into a suite run only by unittest.
- Check that every test declaration is actually collected by the declared runner,
  with the same interpreter/environment as the tests, before relying on a green
  run.
- Reject empty suites, import/collection errors, duplicate definitions and
  declarations omitted by the runner. Keep test helpers out of the `test*`
  namespace. Explain intentional skips and separate integration prerequisites;
  never hide failures with `continue-on-error` or `|| true`.
- Run the normal test command after the collection check. Report
  collected/executed/skipped counts and investigate unexpected changes;
  collection alone is not a passing test run.
- Check test paths, naming patterns, selection filters and CI commands together.
  A new test directory or non-Python test harness needs an explicit CI entry.
- Preserve supported interpreter matrices. Changing runners requires an explicit
  decision and collection parity.

## Separate user and contributor documentation

- Maintain two distinct entry points and tables of contents: user documentation
  for installation, configuration, operation, public APIs and troubleshooting;
  contributor documentation for architecture, internals, tests, benchmarks,
  release engineering and development plans.
- Keep README and package descriptions focused on users. Link to the contributor
  guide instead of embedding maintainer procedures. Library API examples belong
  in the user guide when they are needed to integrate the library.
- Keep registry publishing, CI setup, repository secrets and maintainer account
  configuration out of user guides, website manuals and package descriptions.
  Never include credential values or private infrastructure evidence in either guide.
- Put implementation reviews and acceptance records under the contributor
  navigation. Preserve user-facing compatibility limits, migration instructions,
  security requirements and failure semantics in the user documentation.
- Apply this separation to generated documentation and FR/EN website content.
  Update source content and generators together; do not patch only generated HTML.
- Before delivery, inspect both entry points, check links and build documentation
  with warnings treated as errors where supported. Review README/package text and
  the deployed manual for accidental maintainer content. Preserve private-project
  visibility and existing review/publication approval requirements.

## Complete delivery and release synchronization

- Treat every delivery as a consistency check across the roadmap, PyPI packages,
  Docker Hub images and registry descriptions, repository/user/contributor
  documentation, demos, and existing product websites. Update every affected
  surface; a merged PR alone does not establish a completed delivery.
- Reconcile roadmap items with actual implementation and verified delivery.
  Distinguish planned, implemented, validated and published/deployed work; keep
  remaining limits and next steps explicit. Do not leave completed releases
  listed as pending or mark unverified work complete.
- For a release, publish the validated packages and images through the existing
  release gates, verify their versions/artifacts in the registries, and align
  installation commands, Compose examples, release notes and supported versions.
  Never overwrite an immutable published version to update its contents.
- Update affected documentation in every maintained language, including README,
  guides, examples, screenshots and diagrams. Keep user and contributor material
  separate and regenerate derived assets from the accepted source.
- Update existing demos and websites when affected, including source/image pins,
  visible versions, shared captures and release metadata. Validate the deployed
  result, links and relevant desktop/mobile flows; preserve private/public
  boundaries, credentials, data and the existing approval scope.
- Inspect applicability on every change. A documentation-only change does not
  require an artificial package/image release; a project without a registry,
  demo or website does not require inventing one. Record why a surface is
  unchanged, not applicable, blocked or explicitly deferred.
- Complete the authorized delivery work before reporting success. In the final
  handoff, distinguish merged code from registry publication and deployment,
  report checks performed, and list any required surface still not updated with
  its concrete blocker. Never imply that a planned publication already happened.

## Deliverable and deployment contents

- Every deliverable and deployment ships only what the product needs to install,
  run and meet its legal obligations. This covers source tarballs and sdists,
  wheels, Docker images, Debian packages, GitHub release assets, browser
  extensions, mobile packages (APK/AAB/IPA), Claude skills and plugins, ChatGPT
  apps and instructions, and published websites.
- Never ship repository or maintainer material: `AGENTS.md`, `CLAUDE.md` and
  other agent instructions, roadmaps, contribution guides, reviews and acceptance
  records, CI configuration (`.github/`), tests and fixtures, development
  scripts, Dockerfiles and build tooling, editor/VCS files, local configuration,
  secrets or credentials.
- Keep what is required: runtime code and assets, the default configuration and
  examples the product loads or documents for installation, `LICENSE` and
  required notices, and the README or metadata a registry needs to describe the
  package. Ship user documentation only in deliverables meant to carry it.
- Select contents with explicit allow-lists: a `.dockerignore` starting with `*`,
  a `MANIFEST.in` without broad `graft`, explicit package data, a dedicated build
  directory for sites and plugins, and `export-ignore` in `.gitattributes` for
  GitHub source archives. Never publish a repository root or `COPY . .` into a
  final image.
- Before each release or deployment, list the actual artifact contents (sdist and
  wheel listings, image filesystem, archive listing, deployed URLs) and remove
  any non-essential file before publishing. Report this check in the handoff.

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
