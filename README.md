# An AI-powered autograder
A RAG-powered autograder for CS520

## 1. Requirements

### 1.1 Overview

This project delivers an AI-assisted auto-grading system for written/short-answer assignments submitted through Gradescope.  
It uses a Retrieval-Augmented Generation (RAG) pipeline by grounding an LLM in course-specific materials (rubrics, keys, slides, readings) to produce consistent rubric-based scores and explainable feedback at scale.

#### Objectives
- Cut turnaround time for grading while preserving instructor control and academic integrity.  
- Improve consistency across graders and sections via rubric enforcement and calibration.  
- Provide actionable, evidence-linked feedback to students to support learning.  
- Surface analytics (rubric reliability, grade distributions, concept gaps) for instructors and departments.

#### Intended Audience & Stakeholders
- Primary: Instructors, TAs/graders, students  
- Secondary: Course coordinators, department admins, academic integrity/compliance (FERPA), IT/security

#### Why It Matters
Grading written work is time-intensive and inconsistent across graders.  
Grounding an LLM with course materials enables faster, more consistent, and explainable grading with human-in-the-loop oversight — improving efficiency and decision-making without sacrificing quality.

---

### 1.2 Features

1. **Retrieval-Augmented Generation (RAG) Pipeline**  
   Automatically retrieves the most relevant course documents (rubrics, solutions, slides, readings) to ground LLM evaluations, ensuring that scores and comments align with instructor-defined criteria.

2. **Rubric-Based Evaluation and Feedback**  
   Maps model outputs directly to rubric items, producing structured grading explanations (e.g., criterion met/not met + evidence). Supports instructor-approved rubrics for transparency and consistency.

3. **Explainable Feedback Generation**  
   Generates concise, rubric-linked feedback for students, citing the specific parts of their submission and corresponding reference material that justify each score.

4. **Multi-Course and Section Support**  
   Handles multiple courses, sections, and grader roles with role-based access control, enabling department-wide scaling while maintaining data separation and FERPA compliance.

---

### 1.3 Functional Requirements (Use Cases)

1. **Instructor Authentication**  
   - Description: Instructor logs in using university or Gradescope credentials. A secure access token is stored locally.  
   - Success Case: Instructor gains access to dashboard.  
   - Failure Case: Invalid credentials or expired session.

2. **Course and Assignment Retrieval**  
   - Description: Instructor selects a course, and the system retrieves all assignments and submissions via Gradescope API.  
   - Success Case: Assignments load successfully.  
   - Failure Case: API returns incomplete or failed response.

3. **Rubric Configuration**  
   - Description: Instructor defines or imports grading rubrics (criteria, weights, comments).  
   - Success Case: Rubric validated and stored.  
   - Failure Case: Formatting or data errors during import.

4. **Submission Upload and Preprocessing**  
   - Description: System fetches each student submission, converts it to text, and uploads to secure storage (AWS S3).  
   - Success Case: Submissions uploaded successfully.  
   - Failure Case: Upload fails due to network or permission issues.

5. **Contextual Grading with RAG Pipeline**  
   - Description: AI model (LangChain + LLaMA + Pinecone) grades each submission using the rubric and relevant course materials.  
   - Success Case: AI produces contextually relevant score and feedback.  
   - Failure Case: Model inference fails or produces incomplete output.

6. **Instructor Review and Adjustment**  
   - Description: Instructor reviews AI-suggested scores and feedback in the Chrome extension, then modifies or approves them.  
   - Success Case: Instructor finalizes all grades.  
   - Failure Case: UI synchronization or save errors.

7. **Automated Grade Submission**  
   - Description: Finalized grades and feedback are submitted back to Gradescope via API.  
   - Success Case: Grades successfully appear on Gradescope.  
   - Failure Case: API rate limit or timeout errors.

8. **Analytics and Performance Tracking**  
   - Description: System logs grading metrics (time, overrides, consistency) and visualizes analytics in a dashboard.  
   - Success Case: Analytics display accurately.  
   - Failure Case: Logging or visualization module errors.

---

### 1.4 Non-Functional Requirements

1. **Performance (Speed Under Load)**  
   - The system should support approximately 500 concurrent graders without lag.  
   - A “Preview Grade” should appear within 5 seconds, even during peak load.

2. **Security (Protecting Data)**  
   - All traffic must be encrypted (TLS 1.3).  
   - Stored files and grades must be encrypted (AES-256).  
   - Passwords must be securely hashed and never stored in plain text.

3. **Access and Accountability**  
   - Users sign in through university single sign-on (SSO).  
   - Roles such as Instructor, TA, and Viewer determine visibility and permissions.  
   - Every grading action (rubric used, score change, release) is logged for traceability.

4. **Usability and Accessibility**  
   - Fully compatible with screen readers and keyboard-only navigation.  
   - The interface should include clear labels, high contrast, and quick grading workflows (under 1 minute per submission).

5. **Reliability and Recovery**  
   - Uptime must be at least 99.5% during semesters.  
   - Automatic hourly backups with restoration possible within 4 hours.  
   - Re-sending grades should not duplicate submissions.

---

### 1.5 Challenges and Risks

1. **Model Hallucinations / Misalignment**  
   - Risk: AI may produce unsupported claims or assign grades inconsistent with the rubric.  
   - Mitigation: Enforce strict RAG grounding, rubric-first prompts, apply confidence thresholds, and enable human review for flagged cases.

2. **Bias and Fairness**  
   - Risk: Systematic score discrepancies between sections or due to phrasing variations.  
   - Mitigation: Use attribute masking, conduct periodic fairness audits, track inter-grader agreement, and refine rubrics accordingly.

3. **Scalability During Deadlines**  
   - Risk: Grading spikes may overload system capacity near submission deadlines.  
   - Mitigation: Implement autoscaling workers, batch grading, and pre-warming servers before high-demand periods.

4. **Academic Integrity and Prompt Attacks**  
   - Risk: Students could insert adversarial content designed to manipulate the model.  
   - Mitigation: Apply content sanitization, prompt injection detection, and human escalation procedures.

5. **Privacy and Compliance**  
   - Risk: Mishandling or over-retention of student data could violate FERPA or institutional policy.  
   - Mitigation: Enforce FERPA-aligned data handling, retention limits, and auditable deletions.

6. **Cost Overruns**  
   - Risk: Excessive model usage may cause budget overruns.  
   - Mitigation: Apply token limits, caching, context summarization, budget alerts, and tiered model selection.

