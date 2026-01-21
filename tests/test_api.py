from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_upload_resume_endpoint():
    with open("tests/sample_resume.pdf", "rb") as f:
        response = client.post(
            "/upload_resume/",
            files={"file": ("resume.pdf", f, "application/pdf")},
            data={"role": "Machine Learning Engineer"}
        )

    assert response.status_code == 200
    data = response.json()

    assert "role" in data
    assert "skill_questions" in data
    assert "project_questions" in data

    assert isinstance(data["project_questions"], list)
    assert len(data["project_questions"]) > 0
