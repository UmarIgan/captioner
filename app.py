import gradio as gr
from llama_cpp import Llama
from llama_cpp_agent import LlamaCppAgent, MessagesFormatterType
from llama_cpp_agent.providers import LlamaCppPythonProvider

# Model Configuration
SYSTEM_PROMPT = "You are a helpful, respectful, and honest assistant."
CHAT_TEMPLATE = MessagesFormatterType.LLAMA_3
MODEL_PATH = "Llama-3.2-1B-Instruct-Q4_K_M.gguf"  # Update this to your actual model path
TEMPERATURE = 0.3
MAX_NEW_TOKENS = 1024
CONTEXT_WINDOW = 8000
N_GPU_LAYERS = 0  # Set to 0 for CPU, or -1 for GPU if available
N_BATCH = 1024

def initialize_model():
    """Initialize the Llama model and agent."""
    try:
        llm = Llama(
            model_path=MODEL_PATH, 
            n_gpu_layers=N_GPU_LAYERS, 
            n_batch=N_BATCH, 
            n_ctx=CONTEXT_WINDOW
        )
        provider = LlamaCppPythonProvider(llm)
        settings = provider.get_provider_default_settings()
        settings.temperature = TEMPERATURE
        settings.max_tokens = MAX_NEW_TOKENS
        settings.stream = True

        agent = LlamaCppAgent(
            provider, 
            system_prompt=SYSTEM_PROMPT, 
            predefined_messages_formatter_type=CHAT_TEMPLATE, 
            debug_output=False
        )
        return agent, settings
    except Exception as e:
        raise gr.Error(f"Failed to initialize model: {str(e)}")

def chat_response(message, history):
    """Generate a response from the Llama model."""
    try:
        # Initialize model if not already done
        if not hasattr(chat_response, 'agent'):
            chat_response.agent, chat_response.settings = initialize_model()

        # Accumulate response chunks
        full_response = ""
        for chunk in chat_response.agent.get_chat_response(
            message, 
            llm_sampling_settings=chat_response.settings, 
            returns_streaming_generator=True, 
            print_output=False
        ):
            full_response += chunk
            yield full_response

    except Exception as e:
        yield f"An error occurred: {str(e)}"

def main():
    # Create Gradio interface
    demo = gr.ChatInterface(
        chat_response,
        title="Llama-3.2 1B Chatbot",
        description="Chat with a lightweight Llama-3.2 1B model",
        theme="default"
    )
    
    return demo

if __name__ == "__main__":
    demo = main()
    demo.launch(server_name="0.0.0.0", server_port=7860)
