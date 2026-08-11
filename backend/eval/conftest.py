import os
import json
from eval_tracker import tracker
from datetime import datetime


def pytest_sessionfinish(session, exitstatus):
    """
    This Pytest hook runs automatically at the end of the entire test session.
    It calculates the averages from the tracker and saves them as a JSON file.
    """
    report = {}

    for metric_name, scores in tracker.scores.items():
        print(scores)
        if scores:
            average = sum(scores) / len(scores)
            report[f"average_{metric_name}"] = round(average, 5)
        else:
            report[f"average_{metric_name}"] = None

    report_dir = "test_reports"
    os.makedirs(report_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_path = os.path.join(report_dir, f"eval_{timestamp}.json")
    with open(report_path, "w") as json_file:
        json.dump(report, json_file, indent=4)

    print(f"\n\n[SUCCESS] Evaluation summary saved to {report_path}")
