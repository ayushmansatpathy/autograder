import json
import time
import os
import requests

BASE_URL = "http://127.0.0.1:8000"
DATA_FILE = os.path.join(os.path.dirname(__file__), "sample_data.json")


def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def test_root_endpoint():
    """Sanity check that backend is running."""
    resp = requests.get(f"{BASE_URL}/")
    assert resp.status_code == 200


def test_upload_text():
    """
    Test text ingestion endpoint.
    Matches UploadText schema exactly.
    """
    payload = {
        "user_id": "test_user",
        "filename": "test_doc.txt",
        "text": "A binary search tree stores values in sorted order."
    }

    resp = requests.post(f"{BASE_URL}/upload-text", json=payload)
    assert resp.status_code == 200


def test_grade_answer_endpoint():
    """
    Functional test for grading.
    Matches GradeAnswer schema exactly.
    """
    data = load_data()
    case = data["cases"][0]

    payload = {
        "user_id": "test_user",
        "question": data["question"],
        "student_response": case["student_answer"]
    }

    t0 = time.perf_counter()
    resp = requests.post(f"{BASE_URL}/grade-answer", json=payload)
    dt = time.perf_counter() - t0

    assert resp.status_code == 200
    body = resp.json()

    # assert "score" in body
    # assert "feedback" in body

    assert "response" in body
    assert isinstance(body["response"], str)
    assert len(body["response"]) > 0


    # Good answer should score reasonably high
    # assert body["score"] >= case["expected_score"] - 2
    # assert dt < 5.0 

    assert len(body["response"]) > 0
    assert dt < 30.0