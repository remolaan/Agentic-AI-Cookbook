# 39 — Generator + Verifier

One agent **generates** content, another **verifies** it. If verification fails, the generator tries again with feedback. This creates a quality loop.

```mermaid
flowchart TD
    G["✍️ Generator"] --> V["🔍 Verifier"]
    V -->|"✅ Pass"| O["Output"]
    V -->|"❌ Fail + feedback"| G
    style G fill:#e3f2fd,color:#000000
    style V fill:#fff3e0,stroke:#e65100,color:#000000
```

## What you'll build

- Generator agent that creates content
- Verifier agent that scores output (pass/fail)
- Conditional edge that loops back on failure
- Max retry limit to prevent infinite loops
