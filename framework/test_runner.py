import subprocess
from framework.logger import get_logger

logger = get_logger(__name__)

def run_tests():
    logger.info("Starting test run")

    result = subprocess.run(
        [
            "pytest",
            "tests",
            "--html=reports/report.html"
        ],
        capture_output=True,
        text=True
    )

    with open(
        "reports/latest_test_run.txt",
        "w"
    ) as report:
        report.write(result.stdout)

    if result.returncode == 0:
        logger.info("All tests passed")
    else:
        logger.error("Tests failed")

    return result.returncode


if __name__ == "__main__":
    run_tests()