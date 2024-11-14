import os
import uuid
import psycopg
from psycopg import Error
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
from langchain_postgres import PostgresChatMessageHistory

load_dotenv()

# PostgreSQL connection details
DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")

# Establish a synchronous connection to the database
# (or use psycopg.AsyncConnection for async)
# Connect to PostgreSQL
try:
    sync_connection = psycopg.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
except (Exception, Error) as e:
    print("Error connecting to PostgreSQL:", e)
    exit()

print("PostgresSQL server information")
cursor = sync_connection.cursor()
cursor.execute("SELECT version();")
record = cursor.fetchone()
print("You are connected to - ", record, "\n")

# Create the table schema (only needs to be done once)
table_name = "chat_history"
PostgresChatMessageHistory.create_tables(sync_connection, table_name)

# This could be a username or a unique ID
# session_id = str(uuid.uuid4())
session_id = "user_session_new"

# Initialize the chat history manager
chat_history = PostgresChatMessageHistory(
    table_name,
    session_id,
    sync_connection=sync_connection
)

# Add messages to the chat history

# Initialize Chat Model
model = ChatOpenAI()

print("Start chatting with the AI. Type 'exit' to quit.")


while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break

    # Add the user message to the chat history
    chat_history.add_user_message(user_input)

    ai_response = model.invoke(user_input)
    print(f"AI: {ai_response.content}")

    # Add the AI message to the chat history
    chat_history.add_ai_message(ai_response.content)