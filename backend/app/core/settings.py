
class Settings:
    """
    Configuration settings for the application.
    """
    # Define the default model name for the language model
    # Replace with the Hugging Face model of your choice
    MODEL_NAME = "homebrewltd/Ichigo-llama3.1-s-instruct-v0.4"

    # Other configuration options (optional)
    MAX_RESPONSE_LENGTH = 512
    TEMPERATURE = 0.7
    NUM_RETURN_SEQUENCES = 1


# Create an instance of the settings for use in the app
settings = Settings()
