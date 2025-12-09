import { useMemo, useState } from "react";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

export default function Home() {
  const [userId, setUserId] = useState("demo-user");
  const [question, setQuestion] = useState(
    "What are the 3 pillars of Object Oriented Programming?"
  );
  const [rubricText, setRubricText] = useState(
    "Paste your rubric text here. The backend will embed it for retrieval."
  );
  const [studentAnswer, setStudentAnswer] = useState(
    "Type or paste the student's answer here."
  );
  const [gradePreview, setGradePreview] = useState("");
  const [isUploading, setIsUploading] = useState(false);
  const [isGrading, setIsGrading] = useState(false);
  const [toast, setToast] = useState(null);
  const [error, setError] = useState("");
  const [showDialog, setShowDialog] = useState(false);

  const endpointCopy = useMemo(() => API_BASE_URL.replace(/\/$/, ""), []);

  const showToast = (message, tone = "neutral") => {
    setToast({ message, tone });
    setTimeout(() => setToast(null), 3600);
  };

  const handleUploadRubric = async () => {
    setIsUploading(true);
    setError("");
    try {
      const response = await fetch(`${endpointCopy}/upload-text`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          user_id: userId,
          text: rubricText
        })
      });

      if (!response.ok) {
        throw new Error("Upload failed. Check the backend server status.");
      }

      const result = await response.json();
      showToast(result.message || "Rubric uploaded successfully.", "success");
    } catch (err) {
      setError(err.message);
    } finally {
      setIsUploading(false);
    }
  };

  const handleGrade = async () => {
    setIsGrading(true);
    setError("");
    try {
      const response = await fetch(`${endpointCopy}/grade-answer`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          user_id: userId,
          question,
          student_response: studentAnswer
        })
      });

      if (!response.ok) {
        throw new Error("Grading failed. Confirm the rubric is uploaded.");
      }

      const result = await response.json();
      setGradePreview(result.response || "No response returned from model.");
      setShowDialog(true);
      showToast("LLM grading complete.", "success");
    } catch (err) {
      setError(err.message);
    } finally {
      setIsGrading(false);
    }
  };

  return (
    <div className="page">
      <div className="backdrop">
        <div className="orb orb-one" />
        <div className="orb orb-two" />
      </div>

      <main className="shell">
        <header className="hero">
          <div>
            <p className="tag">RAG-powered grading</p>
            <h1>
              AutoGrader<span className="accent">.ai</span>
            </h1>
            <p className="lede">
              Load your rubric, drop in a student answer, and preview the AI
              grade with full rubric grounding.
            </p>
          </div>
        </header>

        <section className="grid">
          <div className="panel">
            <div className="panel-head">
              <p className="eyebrow">Rubric</p>
              <button
                className="ghost"
                onClick={handleUploadRubric}
                disabled={isUploading}
              >
                {isUploading ? "Uploading…" : "Embed rubric"}
              </button>
            </div>
            <textarea
              value={rubricText}
              onChange={(e) => setRubricText(e.target.value)}
              placeholder="Paste rubric text or outcomes here"
            />
          </div>

          <div className="panel">
            <div className="panel-head">
              <p className="eyebrow">Prompt &amp; Identity</p>
            </div>
            <label className="field">
              <span>User / course id</span>
              <input
                value={userId}
                onChange={(e) => setUserId(e.target.value)}
                placeholder="user-id to namespace the vectors"
              />
            </label>
            <label className="field">
              <span>Question prompt</span>
              <input
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                placeholder="What are the three pillars of OOP?"
              />
            </label>
          </div>
        </section>

        <section className="panel">
          <div className="panel-head">
            <p className="eyebrow">Student answer</p>
            <button
              className="primary"
              onClick={handleGrade}
              disabled={isGrading}
            >
              {isGrading ? "Grading…" : "Grade with AutoGrader.ai"}
            </button>
          </div>
          <textarea
            value={studentAnswer}
            onChange={(e) => setStudentAnswer(e.target.value)}
            placeholder="Paste the student's answer here"
            rows={5}
          />
        </section>

        {(error || toast) && (
          <div className="status">
            {error && <p className="error">⚠️ {error}</p>}
            {toast && <p className={`toast ${toast.tone}`}>{toast.message}</p>}
          </div>
        )}
      </main>

      {showDialog && (
        <div className="dialog">
          <div className="dialog-card">
            <div className="dialog-head">
              <div>
                <p className="eyebrow">Preview</p>
                <h3>Model response</h3>
              </div>
              <button className="ghost" onClick={() => setShowDialog(false)}>
                Close
              </button>
            </div>
            <pre className="output" aria-live="polite">
              {gradePreview}
            </pre>
          </div>
        </div>
      )}
    </div>
  );
}
