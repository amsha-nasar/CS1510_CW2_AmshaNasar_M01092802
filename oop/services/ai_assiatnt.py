

from openai import OpenAI
from typing import List, Dict


class DomainAssistant:
    """
    Unified AI assistant class that supports:
    Multiple domains (cyber, data_science, IT)
    """

    SYSTEM_PROMPTS = {
        "cyber": """
        You are a cybersecurity expert assistant.
        - Analyze incidents and threats
        - Explain attack vectors
        - Use MITRE ATT&CK terminology
        - Provide actionable mitigation steps.
        """,

        "data_science": """
        You are a helpful data science expert.
        - Analyze datasets
        - Explain ML models
        - Suggest visualizations
        - Provide statistical insights.
        """,

        "it": """
        You are an IT support specialist.
        - Troubleshoot hardware/software issues
        - Diagnose logs
        - Provide step-by-step solutions.
        """
    }

    def __init__(self, api_key: str, domain: str):
        self.client = OpenAI(api_key=api_key)
        self._history: List[Dict[str, str]] = []

        # Load the system prompt for the selected domain
        self.set_domain(domain)

    # ---------------------------------------------------------
    # Domain & System Prompt Handling
    # ---------------------------------------------------------
    def set_domain(self, domain: str):
        """Switch the assistant role context."""
        if domain not in self.SYSTEM_PROMPTS:
            raise ValueError(f"Invalid domain: {domain}")

        self.domain = domain
        self._system_prompt = self.SYSTEM_PROMPTS[domain]

        # Reset history and add new system message
        self.clear_history()

    def set_system_prompt(self, prompt: str):
        """Override system prompt manually."""
        self._system_prompt = prompt
        self.clear_history()

    # ---------------------------------------------------------
    # Messaging
    # ---------------------------------------------------------
    def add_user_message(self, message: str):
        self._history.append({"role": "user", "content": message})

    def add_assistant_message(self, message: str):
        self._history.append({"role": "assistant", "content": message})

    # ---------------------------------------------------------
    # Generate AI Response
    # ---------------------------------------------------------
    def generate_response(self) -> str:
        """
        Sends conversation to OpenAI and returns the assistant reply.
        Includes system prompt automatically.
        """

        messages = [{"role": "system", "content": self._system_prompt}] + self._history

        completion = self.client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=messages
        )

        response = completion.choices[0].message.content
        self.add_assistant_message(response)
        return response

    # ---------------------------------------------------------
    # History Control
    # ---------------------------------------------------------
    def get_history(self, include_system=False):
        """Return user + assistant messages only."""
        if include_system:
            return [{"role": "system", "content": self._system_prompt}] + self._history
        return self._history

    def clear_history(self):
        """Clear conversation except system prompt."""
        self._history.clear()
