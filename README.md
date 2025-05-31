# TableDora

TableDora is a Python tool for exploring and summarizing PostgreSQL database tables, with AI-powered classification and description using either OpenAI or Anthropic LLMs.

## Features
- Connects to a PostgreSQL database using a config file.
- Lists all tables and lets you select one to analyze.
- Loads the selected table into a pandas DataFrame.
- Displays row count, count of empty/NULL values per column, and top 10 repeated values per column.
- Sends a summary of the table to an LLM (OpenAI or Anthropic) for classification and description.
- Model and provider are selectable via the config file.

## Setup
1. **Clone the repository and create a virtual environment:**
   ```zsh
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. **Install dependencies:**
   ```zsh
   pip install -r requirements.txt
   # Or manually:
   pip install pandas sqlalchemy openai anthropic psycopg2-binary
   ```
3. **Configure database and LLM settings:**
   - Edit `db_config.ini` with your PostgreSQL connection details.
   - Edit `openai_config.ini` for LLM API keys and model selection. Example:
     ```ini
     [openai]
     api_key = <your-openai-key>
     model = gpt-3.5-turbo

     [anthropic]
     use = true  # Set to true to use Anthropic, false for OpenAI
     api_key = <your-anthropic-key>
     model = claude-3-opus-20240229
     ```

## Usage
1. **Run the script:**
   ```zsh
   python describe_tables.py
   ```
2. **Follow the prompts:**
   - Select a table to analyze.
   - View the summary statistics and the LLM's classification/description.

## Notes
- `.ini` config files are excluded from git by default for security.
- Supports both OpenAI and Anthropic APIs; select provider and model in `openai_config.ini`.
- Requires a working internet connection for LLM features.

---
For more details, see `.github/copilot-instructions.md`.
