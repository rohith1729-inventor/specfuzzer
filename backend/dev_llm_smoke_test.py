"""Quick manual check for the remote LLM gateway."""
from __future__ import annotations

from backend.llm_client import generate_for_specfuzzer


def main() -> None:
    prompt = (
        "Given the API endpoint GET /users/{id}, respond ONLY with JSON containing a "
        "list named 'tests'. Each item must include 'name' and 'description' fields "
        "describing adversarial scenarios."
    )
    output = generate_for_specfuzzer(prompt, max_tokens=256, temperature=0.4)
    print(output)


if __name__ == "__main__":
    main()
