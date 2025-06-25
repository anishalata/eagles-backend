# TODO: move to chroma_utils.py if supporting other sports

from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatOpenAI
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.text_splitter import CharacterTextSplitter
from dotenv import load_dotenv


# Load environment variables (like your OpenAI API key)
load_dotenv()

# This stores the conversation memory (user + bot turns)
chat_history = []

def query_bot(message: str) -> str:
    # 1. Load the Chroma vector store from disk
    vectordb = Chroma(
        persist_directory="chroma_db",  # where your embedded data is
        embedding_function=OpenAIEmbeddings()
    )

    # 2. Turn the vector store into a retriever (gets relevant chunks)
    retriever = vectordb.as_retriever(search_kwargs={"k": 4})

    # 3. Load the LLM (GPT-4o in this case)
    llm = ChatOpenAI(model="gpt-4o", temperature=0)

    # 4. Build the full conversational chain (retriever + LLM + memory)
    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever
    )

    # 5. Run the chatbot on the user's message with memory
    result = chain.run({
        "question": message,
        "chat_history": chat_history
    })

    # 6. Save this turn into the chat history
    chat_history.append((message, result))

    # 7. Return GPT's answer
    return result

def format_game_into_text(game: dict) -> str:
    lines = []

    lines.append(f"On {game.get('date')}, the Eagles played {game.get('event')}.")
    lines.append(f"The final score was {game.get('score')}.")

    if "quarters" in game:
        for quarter, summary in game["quarters"].items():
            lines.append(f"In {quarter}, {summary}")

    if "top_players" in game:
        for player in game["top_players"]:
            line = f"{player.get('name')} had {player.get('yards')} yards"
            if player.get("touchdowns"):
                line += f" and {player['touchdowns']} touchdowns"
            line += "."
            lines.append(line)

    return "\n".join(lines)


def store_game_in_chroma(game: dict):
    # 1. Convert game dict to readable text
    formatted_text = format_game_into_text(game)
    print(f"📝 Formatted text being stored: {formatted_text}")

    # 2. Split into chunks for vector storage
    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_text(formatted_text)
    print(f"📦 Number of chunks created: {len(chunks)}")

    # 3. Add chunks to Chroma vector DB
    vectordb = Chroma(
        persist_directory="chroma_db",
        embedding_function=OpenAIEmbeddings()
    )

    vectordb.add_texts(chunks)
    vectordb.persist()

    print("✅ Game stored in ChromaDB")


if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        response = query_bot(user_input)
        print("Bot:", response)
