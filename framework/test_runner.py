import subprocess
from framework.logger import get_logger
from pathlib import Path

logger = get_logger(__name__)


def run_tests():
    logger.info("Starting test run")

    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)

    result = subprocess.run(
        [
            "python",
            "-m",
            "pytest",
            "tests",
            "--html=reports/report.html",
            "--self-contained-html",
        ],
        capture_output=True,
        text=True
    )

    with open(
        "reports/latest_test_run.txt",
        "w",
        encoding="utf-8"
    ) as report:
        report.write("STDOUT\n")
        report.write(result.stdout)

        report.write("\n\nSTDERR\n") #two blank lines between stdout and stderr
        report.write(result.stderr)

    if result.returncode == 0:
        logger.info("All tests passed")
    else:
        logger.error("Tests failed")

    return result.returncode


if __name__ == "__main__":
    run_tests()