import json
import os
import time
import statistics
import requests

BASE_URL = os.getenv("AUTOGRADER_BASE_URL", "http://127.0.0.1:8000")
DATA_FILE = os.path.join(os.path.dirname(__file__), "sample_data.json")


def main():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Warm-up run (reduces cold-start bias)
    warm_payload = {
        "user_id": data["user_id"],
        "question": data["question"],
        "student_response": data["cases"][0]["student_response"],
    }
    requests.post(f"{BASE_URL}/grade-answer", json=warm_payload, timeout=60)

    latencies = []
    for case in data["cases"]:
        payload = {
            "user_id": data["user_id"],
            "question": data["question"],
            "student_response": case["student_response"],
        }

        t0 = time.perf_counter()
        r = requests.post(f"{BASE_URL}/grade-answer", json=payload, timeout=60)
        dt = time.perf_counter() - t0

        r.raise_for_status()
        latencies.append(dt)
        print(f"{case['name']}: {dt:.2f}s")

    print("\nAverage latency:", statistics.mean(latencies))
    print("Max latency:", max(latencies))


if __name__ == "__main__":
    main()