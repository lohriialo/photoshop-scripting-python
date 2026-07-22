# Contributing

Thanks for improving **photoshop-scripting-python**.

## Ways to contribute

- New sample scripts under `sample_scripts/windows/` or `sample_scripts/mac_scripting/`
- Production recipes under `recipes/`
- Toolkit features under `tools/photoshop_toolkit/`
- Docs fixes and clearer onboarding
- Bug reports with Photoshop version + OS + backend (`comtypes` / `win32com` / appscript)

## Development setup

```bash
git clone https://github.com/lohriialo/photoshop-scripting-python.git
cd photoshop-scripting-python
pip install -e ".[dev]"
# platform extras as needed:
pip install -e ".[windows]"   # or ".[macos]" / ".[gui]"
```

## Guidelines

1. **No machine-specific paths** — use `photoshop_scripting.paths.sample_path` / `ensure_sample` or `pathlib` relative to the file.
2. **Prefer named constants** from `photoshop_scripting.constants` over magic integers.
3. **Use `get_app()`** instead of bare `GetActiveObject` so failures are understandable.
4. **Do not commit** large binary assets unless a sample truly needs them; prefer documenting downloads.
5. Keep samples focused and commented; recipes should expose `--help` via `argparse`.
6. Project code is **MIT**; do not add Adobe-owned binaries you are not allowed to redistribute.

### Sample header

```python
# my_sample.py
__author__ = "Your Name"
__version__ = "1.0"
"""
Short description.

Requirements: Photoshop running on Windows; pip install -e ".[windows]"
"""
```

## Pull requests

1. Fork and create a branch.
2. Make a focused change.
3. Open a PR with: what, why, Photoshop version tested (if applicable).
4. Ensure `python -m compileall photoshop_scripting tools recipes` succeeds.

CI runs syntax checks and path lint (no `C:\Git\...` hardcodes). Full COM tests are optional and skip without Photoshop.

## Code of conduct

Be respectful. Assume good intent. No harassment or spam.
