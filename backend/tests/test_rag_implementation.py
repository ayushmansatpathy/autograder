import json
import os
import time
import requests

BASE_URL = os.getenv("AUTOGRADER_BASE_URL", "http://127.0.0.1:8000")
DATA_FILE = os.path.join(os.path.dirname(__file__), "sample_data.json")


def load_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def test_upload_then_grade_uses_rubric_context():
    """
    System/integration test: upload rubric text into Pinecone namespace,
    then grade an answer and verify the LLM output appears rubric-grounded.
    """
    data = load_data()

    # 1) Upload rubric text
    upload_payload = {
        "user_id": data["user_id"],
        "filename": data["filename"],
        "text": data["rubric_text"],
    }
    r1 = requests.post(f"{BASE_URL}/upload-text", json=upload_payload, timeout=30)
    assert r1.status_code == 200, r1.text

    # small pause to reduce flakiness if index/upsert is async-ish
    time.sleep(0.5)

    # 2) Grade
    case = data["cases"][0]
    grade_payload = {
        "user_id": data["user_id"],
        "question": data["question"],
        "student_response": case["student_response"],
    }
    r2 = requests.post(f"{BASE_URL}/grade-answer", json=grade_payload, timeout=60)
    assert r2.status_code == 200, r2.text
    body = r2.json()

    text = body.get("response", "").lower()
    assert len(text) > 0

    # Weak-but-useful check: response mentions key rubric concepts
    expected_any = [s.lower() for s in case["expected_contains_any"]]
    assert any(tok in text for tok in expected_any), (
        "Response doesn't appear grounded in expected rubric concepts.\n"
        f"Response was: {body.get('response','')}"
    )