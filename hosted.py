from langchain.agents import create_react_agent, AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain_core.tools import tool
from langchain.prompts import PromptTemplate
from langchain_openai.chat_models import ChatOpenAI
from langchain_ollama.chat_models import ChatOllama
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from pypdf import PdfReader
import psycopg2

connection_string = "dbname=postgres host=localhost port=4884 user=postgres password=Postgres"
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')


def vectorize(docPath, docName):
    try:
        with psycopg2.connect(connection_string) as con:
            with con.cursor() as cur:

                doc_exists_query = """
                SELECT 1
                FROM item_origin
                WHERE file_name = %s
                """

                cur.execute(doc_exists_query, (docName,))

                row = cur.fetchone()
                if row:
                    print("File already exists")
                    return

                item_insertion = """
                INSERT INTO item_origin(file_name)
                VALUES(%s) RETURNING id
                """

                cur.execute(item_insertion, (docName,))

                row = cur.fetchone()
                if row:
                    id = row[0]
                else:
                    raise Exception('Could not get the id')

                doc = PdfReader(docPath)
                text = ""
                for page in doc.pages:
                    text += page.extract_text()

                splitter = RecursiveCharacterTextSplitter(
                    chunk_size=350,
                    chunk_overlap=50,
                )

                chunks = splitter.split_text(text)

                embedding_insertion = """
                INSERT INTO vectorized_item(content, embedding, origin_id)
                VALUES(%s, %s, %s)
                """

                for chunk in chunks:
                    tensor = model.encode(chunk)
                    cur.execute(embedding_insertion,
                                (chunk, tensor.tolist(), id))

                con.commit()
    except (Exception, psycopg2.DatabaseError) as err:
        if con:
            con.rollback()
        raise RuntimeError(f"Failed to transcribe video: {err}")


vectorize("zigDoc.pdf", "Zig documentation")


@tool
def search_on_vector_db(text) -> str:
    """
    Makes a semantic search using our vector database

    Only use this tool when the makes a question related
    to the Zig programming language or if HE tells you
    to get help from the vector database.
    """
    try:
        with psycopg2.connect(connection_string) as con:
            with con.cursor() as cur:
                embedding = model.encode(text)

                cur.execute("""
                    SELECT id, content
                    FROM vectorized_item
                    ORDER BY embedding <-> %s::vector
                    LIMIT 75
                """, (embedding.tolist(),))

                result = cur.fetchall()
                format_str = "-------\n"
                for row in result:
                    format_str += row[1] + "\n"
                    format_str += "-------\n"

                return format_str
    except (Exception, psycopg2.DatabaseError) as err:
        if con:
            con.rollback()
        raise RuntimeError(f"Failed to transcribe video: {err}")


chat = ChatOpenAI(
    base_url="https://hermes.ai.unturf.com/v1",
    api_key="Not-needed",
    model="adamo1139/Hermes-3-Llama-3.1-8B-FP8-Dynamic"
)

# chat = ChatOllama(model="tinyllama:latest")

prompt = PromptTemplate.from_template("""
Answer the following questions as best you can. You have
access to the following tools:

{tools}

You can also use the chat history to retain information:

{chat_history}

If the question doesn't requieres the use of a tool
then simply try answering based on your knowledge

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action

You may only repeat the Thought/Action/Action Input/Observation
cycle up to 3 times.

If after 3 attempts you are still unsure, tell the user to be
more specific in what he ment by that question.

Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}
""")

memory = ConversationBufferMemory(memory_key="chat_history",
                                  return_messages=True)

tools = [search_on_vector_db]

agent = create_react_agent(chat,
                           tools,
                           prompt=prompt)

executor = AgentExecutor(agent=agent, tools=tools, memory=memory,
                         verbose=True, handle_parsing_errors=True,
                         max_iterations=3)

print("""

Talk to the AI in english, I can't promise it will be as precise
in spanish

""")

while (True):
    user_input = input("\nIn what can I help you?\n > ")
    if (user_input == "!q"):
        break

    executor.invoke({"input": user_input})
