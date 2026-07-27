# 48 — Code Review Agent

An agent that **reviews code** — checks for bugs, style issues, and security problems — then produces a **structured report**.

```mermaid
flowchart TD
    C["📄 Code input"] --> A["🤖 Code Reviewer"]
    A -->|"check_style"| S["🔍 Style Checker"]
    A -->|"check_security"| SEC["🔒 Security Scan"]
    A -->|"analyze_logic"| L["🧠 Logic Analyzer"]
    S --> A
    SEC --> A
    L --> A
    A --> R["📊 Structured Report"]
    style A fill:#e3f2fd,stroke:#1565c0
    style R fill:#e8f5e9,stroke:#2e7d32
```

## What you'll build

- Tools for style checking, security scanning, and logic analysis
- Agent that calls tools and collects results
- `with_structured_output` for a typed review report
- Condition: if critical issues found, mark as FAIL
