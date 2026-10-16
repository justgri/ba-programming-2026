# Lecture 5 Streamlit app

Run from the repository root:

```sh
python3 -m pip install -r sessions/week_5/app/requirements.txt
python3 -m streamlit run sessions/week_5/app/app.py
```

All seven page files remain directly under `pages/`. The explicit navigation in
`app.py` registers those files; old registrations for absent student files were
removed. Data paths are derived from each page's `__file__`, so launching from
the repository root or the app directory uses the same bundled data.

## Review and validation — 2026-10-15

- Fixed stale `pages/shared/` registrations and working-directory-dependent paths.
- Added `openpyxl` for the multi-sheet Excel concatenation demonstration.
- Sorted annual CSV inputs and displayed their filenames in the joins example.
- Guarded empty/single-country visualization selections and absent comparison data.
- Fixed the truncated smoking-model call, loaded the bundled semicolon-delimited
  CSV, and converted model predictors to floats for statsmodels.
- The third econometrics tab is unfinished and explicitly marked as a placeholder.
  Week 4's reshaping/summarization/transformation headings also remain outlines.

The reusable check is `scripts/check_app.py`. It uses Streamlit's bundled
`AppTest`, the real entrypoint, every registered page, both launch directories,
and country/utility widget changes. Inputs are the app's Python files and bundled
teaching datasets under `data/`; it does not use external or Vault data.
Dependencies are in `requirements.txt`; validation needs no browser or server.

Run the check from the repository root:

```sh
mkdir -p sessions/week_5/app/checks
PYTHONDONTWRITEBYTECODE=1 python3 sessions/week_5/app/scripts/check_app.py > sessions/week_5/app/checks/smoke-check.log 2>&1
```

Validation logs stay in ignored `checks/`; Matplotlib, XDG and temporary caches
stay in ignored `.cache/` under this app. No generated project artifacts belong
outside the repository.

Validation passed with Python 3.13 and Streamlit 1.54.0: both entrypoint launch
directories, all seven pages from each directory, single/empty/restored country
selections, and CRRA utility (20 checks). No page exceptions or Streamlit error
elements were reported. Streamlit still logs deprecation notices for existing
`use_container_width` calls and automatically converts a mixed-type `year`
column in the Excel demonstration for display; these do not block the lecture.
