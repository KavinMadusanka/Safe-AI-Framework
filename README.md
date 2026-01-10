# TRUSTED FRAMEWORK FOR VIBE CODING INTEGRATION INTO STABLE SOFTWARE SYSTEMS

## 🎯 Main Research Objective

To design and implement a secure, explainable, and developer-friendly framework that enables the safe integration of AI-generated code into existing stable software systems.

## 🧩 Framework Architecture (High-Level)

The framework consists of four tightly integrated components, each addressing a critical risk in vibe coding:
- Secure Plugin Isolation & Interface Enforcement
- Secure Communication & Authentication Mechanism
- Automated AI & Rule-Based Code Visualization (UML)
- Secure-by-Design AI Code Generator

Together, these components create a real-time, security-aware vibe coding ecosystem.

### 🔐 Secure Plugin Isolation & Interface Enforcement
Secure Plugin Isolation (Docker Sandbox)
- Runs AI-generated plugins inside isolated Docker containers to protect the host system and the uploaded core project.
- Read-only plugin mount: plugin code is mounted as ro so the container cannot modify plugin files.
- Reusable mode: one container per plugin slug
- Controlled exposure: plugin runner exposes only a single service port mapped to a random host port.
- Centralized orchestration: backend manages plugin lifecycle via API endpoints.

Secure Integration into the Core System
- The uploaded “core system” never executes plugin code directly.
- Core system pages call the backend endpoint and receive the plugin output safely.
- Route-to-plugin mapping ensures only the correct plugin appears on its intended page.


### 🔑 Secure Communication & Authentication Mechanism


### 📊 Automated AI & Rule-Based Code Visualization (UML)

- Captures AI-generated code in real time
- Converts code into a Common Intermediate Representation (CIR)
- Generates UML diagrams using:
   AI-based semantic interpretation
   Regex-based deterministic parsing
- Renders UML diagrams using PlantUML
- Enables side-by-side comparison for verification
- Improves developer understanding and explainability

### 🛡️ Secure-by-Design AI Code Generator

- Enhances prompts with secure coding guidelines
- Generates code using AI models (e.g., Gemini)
- Performs real-time static code analysis
- Detects hardcoded secrets and insecure patterns
- Scans dependencies for known vulnerabilities (CVEs)

Automatically replaces insecure code snippets

Outputs validated, security-compliant code
