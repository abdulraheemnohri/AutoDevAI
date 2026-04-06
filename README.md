# AutoDevAI – Self-Expanding AI Development Assistant

**Tagline**: “AutoDevAI: Autonomous AI-powered GitHub Dev Assistant with Self-Learning and Public API Discovery”

## Project Goal

Build an autonomous AI-powered GitHub development assistant that can run inside GitHub workflows and help developers with coding tasks using multiple free public AI APIs. AutoDevAI is designed to be production-ready, GitHub-integrated, and self-expanding.

The system is designed to self-expand its capabilities over time by discovering new APIs and tools.

## Key Features

1.  **AI Code Assistant**: Provides capabilities like code review, bug detection, code explanation, refactoring suggestions, documentation generation, and commit summaries. Supports commands like `/ai review`, `/ai fix`, `/ai explain`, `/ai summarize`, `/ai optimize`, and `/ai document`.
2.  **Multi-Provider AI Engine**: Supports multiple AI providers simultaneously with an intelligent router that tracks response speed, success rate, and API availability.
3.  **Automatic API Discovery Engine**: Includes a crawler that discovers free public AI APIs from various sources like GitHub repositories, HuggingFace, developer blogs, and API directories.
4.  **Endpoint Extraction & Validation**: Detects API endpoints using patterns and validates them before storage.
5.  **API Database**: Maintains a local SQLite database of discovered APIs, ranked by reliability.
6.  **Multi Search Engine Hub**: Supports multiple search engines (DuckDuckGo, Brave Search, SearX, Mojeek, Bing) with rotation and result combination for discovery.
7.  **Browser Automation Agent**: Utilizes a headless browser crawler (Playwright) to open websites, scrape documentation, extract API examples, and analyze GitHub repositories.
8.  **Code Analysis Engine**: Analyzes repository code using AST parsing, regex detection, and AI reasoning to detect bugs, security issues, and bad coding practices.
9.  **Knowledge Engine**: Builds a knowledge base from GitHub repositories (READMEs, documentation, code examples, comments) to enhance AI responses.
10. **Self-Expanding Capability Loop**: Runs a continuous improvement loop to discover, validate, store, rank, and use the best resources.

## Project Folder Structure

```
AutoDevAI/
├── .github/
│   └── workflows/
│       └── ai-assistant.yml
├── action/
│   ├── action.yml
│   ├── Dockerfile
│   └── entrypoint.py
├── backend/
│   ├── main.py
│   ├── config.py
│   └── scheduler.py
├── ai_engine/
│   ├── router.py
│   ├── provider_manager.py
│   ├── prompt_builder.py
│   └── response_parser.py
├── providers/
│   ├── groq_provider.py
│   ├── openrouter_provider.py
│   ├── huggingface_provider.py
│   ├── deepinfra_provider.py
│   └── local_llm_provider.py
├── api_discovery/
│   ├── api_searcher.py
│   ├── endpoint_extractor.py
│   ├── api_validator.py
│   └── api_ranker.py
├── browser_agent/
│   ├── crawler.py
│   ├── page_parser.py
│   └── docs_scanner.py
├── search_engines/
│   ├── duckduckgo.py
│   ├── brave.py
│   ├── searx.py
│   └── bing.py
├── code_analysis/
│   ├── analyzer.py
│   ├── ast_parser.py
│   └── security_scanner.py
├── github_bot/
│   ├── webhook_handler.py
│   ├── command_parser.py
│   ├── pr_reviewer.py
│   └── issue_handler.py
├── knowledge_engine/
│   ├── repo_reader.py
│   ├── doc_extractor.py
│   └── summarizer.py
├── database/
│   ├── api_store.py
│   ├── knowledge_store.py
│   └── db_init.py
├── utils/
│   ├── logger.py
│   ├── http_client.py
│   └── cache.py
├── tests/
├── requirements.txt
└── README.md
```

## Technology Stack

*   **Backend**: Python (FastAPI)
*   **Automation**: Playwright, BeautifulSoup
*   **AI Integration**: REST APIs, OpenAI compatible endpoints
*   **Database**: SQLite + SQLAlchemy
*   **Execution**: Docker, GitHub Actions

## Getting Started

### Prerequisites

*   Python 3.10+
*   Docker (for GitHub Action)
*   `playwright install` (after `pip install playwright`)

### Local Setup

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/AbdulRaheem/AutoDevAI.git
    cd AutoDevAI
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    playwright install
    ```

3.  **Set up environment variables**:
    Create a `.env` file in the root directory with your API keys (optional, but recommended for better performance and access to more providers):
    ```
    GITHUB_TOKEN=your_github_token
    GROQ_API_KEY=your_groq_api_key
    OPENROUTER_API_KEY=your_openrouter_api_key
    HF_TOKEN=your_huggingface_token
    DEEPINFRA_API_KEY=your_deepinfra_api_key
    DATABASE_PATH=database/apis.db
    LOG_LEVEL=INFO
    ```

4.  **Run the assistant locally**:
    ```bash
    python action/entrypoint.py
    ```

### GitHub Actions Setup

1.  **Push your repository to GitHub**.
2.  **Add necessary secrets** to your GitHub repository settings (`Settings > Secrets and variables > Actions > New repository secret`). At a minimum, `GITHUB_TOKEN` is required. Add API keys for AI providers if you wish to use them.
3.  The `ai-assistant.yml` workflow will automatically trigger on `issue_comment`, `pull_request`, and `push` events.

## Usage

Once deployed as a GitHub Action, the assistant will respond to `/ai` commands in issue comments or pull request comments. Examples:

*   `/ai review this code`
*   `/ai explain this function`
*   `/ai fix the bug in this file`
*   `/ai summarize this PR`
*   `/ai optimize this function`
*   `/ai document this module`

## Automation Schedule

*   **API Discovery**: Every 6 hours
*   **Endpoint Validation**: Every 24 hours
*   **API Rotation**: Every request

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the Apache License 2.0.
