L.A.P.H. — Local Autonomous Programming Helper

🧠 What L.A.P.H. Actually Is (Full Corporate Jargon Mode):
A locally-hosted, multi-agent, self-reflexive autonomous programming framework capable of continuous code generation, execution, validation, and correction through iterative feedback cycles, leveraging decentralized LLM orchestration, dynamic error-driven model routing, and fully offline compute workflows.

🍼 What That Means in Human Words:
A lil AI homie who writes code, runs it, sees if it exploded, learns from the explosion, and tries again.
(Linux-only for now — because Arch btw.)

🚀 Vision
L.A.P.H. is designed as a fully offline, privacy-preserving, developer-grade AI agent that:
1. Writes code
2. Runs code
3. Reads the errors
4. Fixes itself
5. …and keeps iterating until the output is clean.
Think of it as your local junior developer intern that never complains, never sleeps, and runs entirely on your machine. No API keys. No cloud. No telemetry. Just vibes and compute.

🎯 Project Roadmap
Phase 1 — Core Autonomy (MVP):
 Generate → run → capture error → fix → repeat
Local LLM loop via Ollama/Qwen3
Basic sandboxing
Minimal project memory (state.txt and error logs)
Status: In development (started 17 Nov 2025)

Phase 2 — Vision Feedback Loop:
Screenshot-based error analysis
GUI inspection using a tiny local vision model
Model learns from both text errors and visual glitches
Self-correction for tkinter/PyQt/pygame apps

Phase 3 — Multi-Model Pipeline + Agentic Skills:
“Thinker model” (e.g., Qwen3-14B)
“Coder model” (e.g., smaller 3B/4B model)
“Vision model” (ViT/TinyLLaVA)
Dynamic routing based on task complexity
Auto-install missing libraries
Auto-optimize its own parameters
Generates a persistent activity log via a super-tiny 1B summarizer

⚡ Quickstart:
Install deps:
pip install -r requirements.txt

Pull the default model (recommended):
ollama pull qwen3:14b

ollama pull qwen3:4b

ollama pull llava-llama3:8b

ollama pull qwen2.5-coder:7b-instruct

Configure your model endpoint in:
core/llm_interface.py

Run the agent:
python3 core/main.py

📅 Date Started: 17 November 2025
