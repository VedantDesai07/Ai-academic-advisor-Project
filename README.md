# AI Academic Advisor

A command-line AI agent that answers academic planning questions using **Anthropic Claude** via **LangChain**. The agent can search the web and look up Wikipedia to supplement its responses, and saves all output to a timestamped text file.

> **Note:** This project is tailored toward questions about the UW Computer Science / WLU BBA Double Degree program, though it can answer general academic questions as well.

---

## Project Structure

```
Ai-academic-advisor-Project/
├── main.py          # Entry point — sets up the LangChain agent and handles user input
├── tools.py         # Defines the three tools available to the agent
├── requirements     # Python package dependencies
└── apikey.env       # Environment file for your Anthropic API key (not committed)
```

---

## How It Works

The app initializes a LangChain agent backed by **Claude** (via `langchain-anthropic`). The agent has access to three tools defined in `tools.py`:

- **`search`** — runs a DuckDuckGo web search via `DuckDuckGoSearchRun`
- **`wiki_tool`** — queries Wikipedia using `WikipediaQueryRun` (returns top 1 result, capped at 100 characters of content per result)
- **`save_text_to_file`** — appends the response to `research_output.txt` with a timestamp

When the user enters a question at the command line, the agent decides which tools to call, gathers information, and returns a structured answer. The response is also saved to `research_output.txt`.

---

## Setup

**1. Clone the repository**

```bash
git clone https://github.com/VedantDesai07/Ai-academic-advisor-Project.git
cd Ai-academic-advisor-Project
```

**2. Install dependencies**

```bash
pip install -r requirements
```

**3. Add your Anthropic API key**

Create (or edit) `apikey.env` in the project root:

```
ANTHROPIC_API_KEY=your_api_key_here
```


**4. Run the app**

```bash
python main.py
```

---

## Dependencies

| Package | Purpose |
|---|---|
| `langchain` | Agent framework |
| `langchain-anthropic` | Claude LLM integration |
| `langchain-community` | DuckDuckGo and Wikipedia tool wrappers |
| `langchain-openai` | Included in requirements (not actively used) |
| `wikipedia` | Wikipedia API access |
| `duckduckgo-search` | Web search |
| `pydantic` | Structured output validation |
| `python-dotenv` | Loads API key from `apikey.env` |

---

## Output

Responses are appended to **`research_output.txt`** in the following format:

```
--- Research Output ---
Timestamp: 2025-01-01 12:00:00

<agent response here>
```

---
