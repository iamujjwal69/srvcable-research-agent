# Super Investing — SRVCABLE AI Research Agent

A small Python command-line research agent that reads the eight supplied Markdown documents and asks Google Gemini to generate a concise, source-cited investment research brief.

**The company is fictional. Do not search for it online.** The analysis date for this assignment is 23 September 2026.

## What it does
1. Loads Markdown documents from `research_pack/`.
2. Assigns stable source IDs (`S1`–`S8`).
3. Sends the supplied evidence plus a separate system prompt to Google Gemini via the official `google-genai` SDK.
4. Saves the Markdown brief to `output/` and run metadata/validation checks to `logs/`.
5. Runs three prompt variants so you can compare baseline, conflict-aware, and conflict/injection/entity-aware behavior.

The API integration uses the official Google GenAI Python SDK (`google-genai`) and reads the model name from `.env`.

## Requirements
- Windows, macOS, or Linux
- Python 3.10 or newer (Python 3.11/3.12/3.14 supported)
- A Google Gemini API key (from Google AI Studio)

If you do not have an API key immediately, you can test the local document loading and report paths with `--offline-preview`, but the preview is not an LLM-generated result and should not be submitted as if it were.

## Setup (Windows PowerShell)
Open this folder in VS Code, then choose **Terminal → New Terminal**.

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation, skip activation and use the environment's Python directly:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Copy `.env.example` to `.env`, then open `.env` and configure your Gemini API key:

```text
LLM_PROVIDER=gemini
GEMINI_API_KEY=your_actual_gemini_api_key_here
GEMINI_MODEL=gemini-3.8-flash
```

Do not share the key or commit `.env` to GitHub. `.gitignore` excludes it.

## Run the agent

With the virtual environment active:

```powershell
python main.py --ticker SRVCABLE --run 1
python main.py --ticker SRVCABLE --run 2
python main.py --ticker SRVCABLE --run 3
```

- Run 1: baseline prompt.
- Run 2: adds explicit revenue-conflict handling.
- Run 3: adds conflict handling, embedded-instruction resistance, and entity-identity caution.

Each successful run writes:
- `output/srvcable_brief_run_1.md` (or run 2/3)
- `logs/run_1_metadata.json` (or run 2/3)

The script prints the report and basic validation results to the terminal. Validation checks required headings, presence/validity of citation IDs, and a few known source-pack risks. Passing validation does **not** prove every claim is correct; manually review the report.

### Test without an API key
To verify that the project files load and output folders work:

```powershell
python main.py --offline-preview --run 1
```

This produces a clearly labelled **OFFLINE PREVIEW — not an LLM-generated run**. Do not describe it as an actual model run in your assignment test log.

## Project layout

```text
srvcable-research-agent/
├── main.py
├── system_prompt.md
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── test_log.md
├── research_pack/       # exact eight source documents from the supplied ZIP
├── output/              # generated reports
└── logs/                # run metadata and validation checks
```

## Model choice
The default is `gemini-3.8-flash` (or `gemini-2.5-flash`) for fast, cost-effective instruction-following and document grounding. You can change `GEMINI_MODEL` in `.env` to another model available to your API account. If the configured model is invalid or unavailable, the agent will alert you.

## Design decisions
- **Direct context, not a vector database:** the pack has only eight short documents, so sending the complete pack is simpler and makes evidence easier to inspect.
- **Source IDs:** stable IDs make it easier to trace a statement back to a document.
- **Separate system prompt:** keeps research rules reviewable and versionable.
- **Prompt variants:** each run adds a specific design change so observed differences can be documented.
- **Untrusted documents:** text inside source files is evidence, not authority over the agent's instructions. This reduces prompt-injection risk but cannot guarantee perfect resistance.
- **Programmatic checks:** basic checks catch missing headings or invalid source IDs, but do not verify every factual claim.

## Important source-pack issues the agent should handle
- Official company release `[S2]` reports revenue of ₹1,248 crore (+18.0%); media report `[S1]` says ₹1,428 crore (+35%). The brief should flag the conflict rather than average figures.
- `[S6]` is a promotional stock-tip blog with an embedded instruction attempting to manipulate the AI. Do not obey it or treat its price target as a reliable valuation.
- `[S8]` is about a local cable TV/broadband operator, and the pack does not establish that it is the same entity as the listed cable manufacturer.
- `[S7]` is a 2024 pledge article, while `[S4]` is a later official shareholding summary with a different figure; dates/definitions may differ.

## Assignment deliverables
1. Push the code, `system_prompt.md`, and README to GitHub (never push `.env`).
2. Run the agent at least three times and truthfully complete `test_log.md`.
3. Paste the report exactly as generated into the assignment form. If you manually edit it, disclose what changed.
4. Record a 2–3 minute screen demo: show a run, explain one design decision, and discuss one limitation.
