from chatterbot import chatterbot



if __name__ == "__main__":
    # Create a new chat bot named Charlie
    chatbot = chatterbot("Charlie")

    # Get a response to the input "How are you?"
    response = chatbot.get_response("How are you?")

    print(response)
    print(response)