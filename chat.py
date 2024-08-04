from src.app.chat.chat import Chat

chat = Chat()

while True:
    query = input(">")
    print(f"<{chat.process_query(query)}")
