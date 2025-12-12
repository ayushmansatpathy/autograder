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

## 1.3 System Architecture

### Backend Overview (FastAPI + RAG Pipeline)

The backend powers the complete Retrieval-Augmented Grading workflow. It is responsible for ingesting PDFs, extracting text, splitting documents into meaningful chunks, generating embeddings, storing them in a vector database, retrieving relevant rubric material, and finally grading student answers with an LLM.

The system extracts text from uploaded PDF files using a PDF processing library and converts them into plain text suitable for downstream retrieval. These documents are then broken into overlapping semantic chunks to preserve context and ensure high-quality retrieval. Each chunk is embedded using a sentence transformer model and stored in Pinecone along with metadata such as the source filename, chunk index, and raw text. The embedding and vector storage logic is fully modularized so that document ingestion can be extended to additional formats in the future.

For retrieval, the backend takes an instructor query or a student answer, embeds it, and searches Pinecone to surface the most relevant rubric or reference material. The system supports per-user or per-course namespaces, ensuring clean data boundaries for FERPA compliance and multi-course usage.

The backend then performs grading using an LLM through a structured prompt template. The prompt enforces rubric alignment, partial credit, conciseness, and consistency. The model is instructed to follow the rubric exactly and avoid hallucination if information is missing. This ensures that grading remains transparent, explainable, and reproducible, while giving instructors confidence in the reliability of the system.

### Frontend Overview (Next.js Interface)

The frontend provides a simple, intuitive interface for graders and instructors. Its primary purpose is to enable fast, repeatable grading while exposing only the controls that matter: the question, the student’s response, and the rubric.

Users can upload reference materials, which the backend automatically processes and stores. The main grading page allows graders to enter the question text, paste the student’s answer, and supply rubric information. When submitted, the frontend sends these inputs to the backend and displays a finalized score along with a concise explanation produced by the LLM. The explanation is grounded in the rubric to ensure traceability and instructional value.

Although lightweight by design, the frontend architecture supports future extensions such as batch grading workflows, instructor dashboards, grading analytics, or cross-course administration tools. Its minimal structure keeps the user experience fast and focused while still allowing significant room for platform growth.