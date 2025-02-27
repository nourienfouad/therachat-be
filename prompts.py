from langchain.prompts import PromptTemplate

greeting = (
    "Hello! I’m here to help you find the best mental health chatbot for your needs. "
    "I'll ask you some questions to understand your preferences. If at any point you wish to stop, type 'done'."
)

conversation_prompt_template = """
You are a professional mental health technology advisor with extensive knowledge of AI-driven mental health chatbots.
Your goal is to gather all necessary details from the user to provide a tailored recommendation.
Below is the conversation so far:

{conversation_history}

If you need more details from the user, ask a clarifying question.
When you are ready to deliver your final recommendation, please start your message with "Final Recommendation:".
Also, make sure to highlight any recommended app(s) by enclosing them in "#"`the_recommand`"#".
Now, please provide your next message as the agent.
"""

conversation_prompt = PromptTemplate(
    template=conversation_prompt_template, input_variables=["conversation_history"]
)

def build_history_string(history):
    """Construct a text string from the conversation history."""
    history_str = ""
    for item in history:
        role = "Agent" if item["role"] == "agent" else "User"
        history_str += f"{role}: {item['message']}\n"
    return history_str
