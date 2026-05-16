# MCP Chat

MCP Chat is a command-line interface application that enables interactive chat capabilities with AI models through the Anthropic API. The application supports document retrieval, command-based prompts, and extensible tool integrations via the MCP (Model Control Protocol) architecture.

## Prerequisites

- Python 3.9+
- Anthropic API Key

## Setup

### Step 1: Configure the environment variables

1. Create or edit the `.env` file in the project root and verify that the following variables are set correctly:

```
ANTHROPIC_API_KEY=""  # Enter your Anthropic API secret key
```

### Step 2: Install dependencies

#### Option 1: Setup with uv (Recommended)

[uv](https://github.com/astral-sh/uv) is a fast Python package installer and resolver.

1. Install uv, if not already installed:

```bash
pip install uv
```

2. Create and activate a virtual environment:

```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:

```bash
uv pip install -e .
```

4. Run the project

```bash
uv run main.py
```

#### Option 2: Setup without uv

1. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install anthropic python-dotenv prompt-toolkit "mcp[cli]==1.8.0"
```

3. Run the project

```bash
python main.py
```

## Usage

### Basic Interaction

Simply type your message and press Enter to chat with the model.

### Document Retrieval

Use the @ symbol followed by a document ID to include document content in your query:

```
> Tell me about @deposition.md
```

### Commands

Use the / prefix to execute commands defined in the MCP server:

```
> /summarize deposition.md
```

Commands will auto-complete when you press Tab.

## MCP Servers

### `mcp_server.py` (stdio transport)

This server communicates over stdin/stdout. Claude Code manages its process lifecycle automatically.

Run directly (for testing):

```bash
uv run mcp_server.py
```

Add to Claude Code:

```bash
claude mcp add --scope project document-mcp -- uv run --directory /Users/a.namazbekov/Projects/cli_project python mcp_server.py
```

> **Note:** The `--directory` flag ensures `uv` resolves the correct virtual environment and logs are written to the right location, even when the command is run from a different project directory.

### `mcp_server_http.py` (streamable-http transport)

This server runs as a standalone HTTP process on `http://127.0.0.1:8000`.

Start the server:

```bash
uv run mcp_server_http.py
```

Add to Claude Code (server must be running first):

```bash
claude mcp add --transport http --scope project document-mcp-http http://127.0.0.1:8000/mcp
```

Verify both servers are registered:

```bash
claude mcp list
```

## Development

### Adding New Documents

Edit the `mcp_server.py` file to add new documents to the `docs` dictionary.

### Implementing MCP Features

To fully implement the MCP features:

1. Complete the TODOs in `mcp_server.py`
2. Implement the missing functionality in `mcp_client.py`

### Linting and Typing Check

There are no lint or type checks implemented.
