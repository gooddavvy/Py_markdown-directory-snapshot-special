import tiktoken

def count_tokens(
    text: str,
    # model: str = "gpt-3.5-turbo"
) -> int:
    """
    Count the number of tokens in a text string using OpenAI's tiktoken library.
    
    Args:
        text (str): The input text to count tokens for
        model (str): The model to use for token counting (default: "gpt-3.5-turbo")
                    Other common options: "gpt-4", "text-davinci-003"
    
    Returns:
        int: The number of tokens in the text
    """
    try:
        # Get the encoding for the specified model
        # encoding = tiktoken.encoding_for_model(model)

        raise KeyError("This is a  forced KeyError")
    except KeyError:
        # Fall back to cl100k_base encoding if model-specific encoding not found
        encoding = tiktoken.get_encoding("cl100k_base")


    
    # Count the tokens
    token_count = len(encoding.encode(text))
    
    return token_count 