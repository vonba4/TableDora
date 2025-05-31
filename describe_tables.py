import configparser
import pandas as pd
from sqlalchemy import create_engine
from openai import OpenAI

# Read database configuration
config = configparser.ConfigParser()
config.read('db_config.ini')
db_params = config['database']

# Build SQLAlchemy connection string
conn_str = (
    f"postgresql+psycopg2://{db_params['user']}:{db_params['password']}@"
    f"{db_params['host']}:{db_params['port']}/{db_params['database']}"
)
engine = create_engine(conn_str)

# Get table names
query = """
SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';
"""
tables = pd.read_sql(query, engine)

# Display tables and let user select one
table_list = tables['table_name'].tolist()
print('Tables in the database:')
for idx, tbl in enumerate(table_list, 1):
    print(f"{idx}. {tbl}")

choice = input(f"\nSelect a table to describe (1-{len(table_list)}): ")
try:
    selected_idx = int(choice) - 1
    if not (0 <= selected_idx < len(table_list)):
        raise ValueError
    selected_table = table_list[selected_idx]
except (ValueError, IndexError):
    print("Invalid selection. Exiting.")
    exit(1)

# Load selected table into a DataFrame
df = pd.read_sql(f'SELECT * FROM "{selected_table}"', engine)
print(f"\nLoaded table: {selected_table}")
print(df.head())

# Describe the DataFrame with custom stats
print(f"\nRow count for {selected_table}: {len(df)}")

print(f"\nCount of empty or NULL values per column:")
null_counts = df.isnull().sum()
empty_counts = (df == '').sum() if not df.empty else pd.Series(dtype=int)
for col in df.columns:
    total_empty = null_counts.get(col, 0) + empty_counts.get(col, 0)
    print(f"  {col}: {total_empty}")

print(f"\nTop 10 repeated values per column:")
for col in df.columns:
    print(f"\nColumn: {col}")
    value_counts = df[col].value_counts(dropna=False).head(10)
    print(value_counts)

def get_openai_api_key():
    config = configparser.ConfigParser()
    config.read('openai_config.ini')
    return config['openai']['api_key']

# Initialize OpenAI client after getting the API key
def send_to_chatgpt(prompt, content):
    api_key = get_openai_api_key()
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(model="gpt-4o",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": content}
        ])
    return response.choices[0].message.content

# Compose summary output for the selected table
table_summary = []
table_summary.append(f"Row count: {len(df)}")
table_summary.append("Count of empty or NULL values per column:")
for col in df.columns:
    total_empty = null_counts.get(col, 0) + empty_counts.get(col, 0)
    table_summary.append(f"  {col}: {total_empty}")
table_summary.append("Top 10 repeated values per column:")
for col in df.columns:
    value_counts = df[col].value_counts(dropna=False).head(10)
    table_summary.append(f"\nColumn: {col}")
    table_summary.append(str(value_counts))
summary_text = '\n'.join(table_summary)

# Send summary to ChatGPT for classification and description
chatgpt_prompt = (
    "You are a data analyst. Given the following summary statistics of a database table, classify the type of data and provide a brief description of what this table might represent."
)
chatgpt_response = send_to_chatgpt(chatgpt_prompt, summary_text)
print("\nChatGPT classification and description:")
print(chatgpt_response)
