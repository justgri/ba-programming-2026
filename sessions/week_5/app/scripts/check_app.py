"""Exercise registered pages and lecture widgets without starting a server."""

from pathlib import Path
import os
import sys


APP_ROOT = Path(__file__).resolve().parents[1]
CACHE = APP_ROOT / ".cache"
for name in ("matplotlib", "tmp", "xdg"):
    (CACHE / name).mkdir(parents=True, exist_ok=True)
os.environ["MPLCONFIGDIR"] = str(CACHE / "matplotlib")
os.environ["TMPDIR"] = str(CACHE / "tmp")
os.environ["XDG_CACHE_HOME"] = str(CACHE / "xdg")
os.environ["MPLBACKEND"] = "Agg"
sys.dont_write_bytecode = True
sys.path.insert(0, str(APP_ROOT))

import logging

logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)

from streamlit.testing.v1 import AppTest
import matplotlib.pyplot as plt


def check(at, label):
    """Report Streamlit exceptions and error elements as failures."""
    failures = [str(error.value) for error in at.exception]
    failures.extend(str(error.value) for error in at.error)
    if failures:
        raise AssertionError(f"{label}: {'; '.join(failures)}")
    print(f"PASS: {label}", flush=True)
    plt.close("all")


def run():
    # Run through the real entrypoint: verifies navigation and app-root imports.
    # Exercise both supported launch directories to detect cwd-dependent paths.
    for cwd in (APP_ROOT.parents[2], APP_ROOT):
        os.chdir(cwd)
        at = AppTest.from_file(str(APP_ROOT / "app.py"), default_timeout=90).run()
        check(at, f"entrypoint from {cwd.relative_to(APP_ROOT.parents[2])}")
        for page in sorted((APP_ROOT / "pages").glob("*.py")):
            at.switch_page(f"pages/{page.name}").run()
            check(at, f"{page.name} from {cwd.relative_to(APP_ROOT.parents[2])}")

    at.switch_page("pages/lecture_week_5_data_viz.py").run()
    at.multiselect[0].set_value(["Switzerland"]).run()
    check(at, "visualization: one country without US/China")
    at.multiselect[0].set_value([]).run()
    check(at, "visualization: empty country selection")
    at.multiselect[0].set_value(["United States", "China"]).run()
    check(at, "visualization: restored comparison")
    at.selectbox[0].select("CRRA").run()
    check(at, "visualization: CRRA utility")


if __name__ == "__main__":
    run()
