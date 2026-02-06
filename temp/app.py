import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage, AssistantMessage
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError

endpoint = "https://models.github.ai/inference"
model = "deepseek/DeepSeek-V3-0324"

# Check if token is set
token = os.environ.get("GITHUB_TOKEN")
if not token:
    print("ERROR: GITHUB_TOKEN environment variable is not set!")
    print("Please set it with: $env:GITHUB_TOKEN='your_token_here'")
    exit(1)

print(f"Using token: {token[:10]}...{token[-4:]}")

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(token),
)

# Initialize conversation with system message
messages = [SystemMessage("You are a helpful assistant.")]

print("=" * 50)
print("Welcome to the Interactive Chatbot!")
print("Type 'quit' or 'exit' to end the conversation.")
print("=" * 50)
print()

while True:
    # Get user input
    user_input = input("You: ").strip()
    
    # Check for exit commands
    if user_input.lower() in ['quit', 'exit', 'bye', 'q']:
        print("\nGoodbye! Thanks for chatting!")
        break
    
    # Skip empty inputs
    if not user_input:
        continue
    
    # Add user message to conversation history
    messages.append(UserMessage(user_input))
    
    try:
        # Get response from the model
        response = client.complete(
            messages=messages,
            temperature=1.0,
            top_p=1.0,
            max_tokens=1000,
            model="gpt-4o-mini"
        )
        
        # Extract assistant's reply
        assistant_reply = response.choices[0].message.content
        
        # Add assistant's reply to conversation history
        messages.append(AssistantMessage(assistant_reply))
        
        # Display the response
        print(f"\nAssistant: {assistant_reply}\n")
        
    except HttpResponseError as e:
        print(f"\nAPI Error: {e.status_code} - {e.message}")
        print(f"Details: {e.response.text() if hasattr(e.response, 'text') else 'No details'}\n")
        messages.pop()
    except Exception as e:
        print(f"\nError: {type(e).__name__}: {e}\n")
        # Remove the last user message if there was an error
        messages.pop()
