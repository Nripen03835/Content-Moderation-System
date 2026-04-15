# Content Moderation System (LLM-style)

A lightweight content moderation system that uses policy-driven prompting and simulated LLM reasoning to classify and moderate user-generated text.

## Features

- **Policy-Driven Moderation**: Clear, definable policies for content classification
- **Explainable Reasoning**: Every moderation decision includes clear reasoning
- **Structured JSON Output**: Easy-to-parse JSON responses for integration
- **No External Dependencies**: Mock LLM engine (no API keys, no external calls)
- **Extensible Design**: Simple to add new policies and custom rules

## Categories

- **Allowed**: Content that complies with all policies
- **Restricted**: Content with minor policy violations that may need review
- **Disallowed**: Content that violates policies and should be blocked

## Supported Policies

1. **HATE_SPEECH**: Content attacking or demeaning groups based on race, religion, gender, or identity
2. **VIOLENCE**: Content promoting or glorifying physical harm or violence
3. **HARASSMENT**: Abusive, insulting, or threatening language toward individuals
4. **SELF_HARM**: Encouraging or promoting self-harm
5. **SEXUAL_CONTENT**: Explicit sexual or pornographic content

## Project Structure

```
content_moderation_llm/
├── main.py                    # Entry point for interactive moderation
├── moderator/
│   ├── __init__.py           # Package initialization
│   ├── policies.py           # Policy definitions
│   ├── prompt_builder.py     # Policy-driven prompt generation
│   ├── mock_llm.py           # Simulated LLM reasoning engine
│   ├── parser.py             # Output formatting
│   └── moderator.py          # Main moderation pipeline
├── examples/
│   └── test_cases.py         # Example test cases
└── README.md                 # This file
```

## How It Works

1. **Build Prompt**: Creates a structured prompt using defined policies
2. **Simulate LLM Reasoning**: Mock LLM analyzes content against policies
3. **Generate Output**: Returns structured JSON with classification, violated policy, and reasoning

## Usage

### Interactive Mode

```bash
python main.py
```

Then enter text when prompted:
```
Enter text to moderate: I will kill you
```

Output:
```json
{
  "input": "I will kill you",
  "moderation_result": {
    "classification": "Disallowed",
    "violated_policy": "VIOLENCE",
    "reasoning": "The text includes terms associated with physical harm or violence."
  }
}
```

### Programmatic Usage

```python
from moderator.moderator import moderate_text
import json

result = moderate_text("Your text here")
print(json.dumps(result, indent=2))
```

### Run Test Cases

```bash
python examples/test_cases.py
```

## Example Output

### Allowed Content
```json
{
  "input": "I love everyone",
  "moderation_result": {
    "classification": "Allowed",
    "violated_policy": null,
    "reasoning": "The content does not violate any defined policies."
  }
}
```

### Restricted Content
```json
{
  "input": "You are an idiot",
  "moderation_result": {
    "classification": "Restricted",
    "violated_policy": "HARASSMENT",
    "reasoning": "The content contains insulting or abusive language."
  }
}
```

### Disallowed Content
```json
{
  "input": "I will kill you",
  "moderation_result": {
    "classification": "Disallowed",
    "violated_policy": "VIOLENCE",
    "reasoning": "The text includes terms associated with physical harm or violence."
  }
}
```

## Extending the System

### Add a New Policy

1. Update `moderator/policies.py`:
```python
POLICIES = {
    "HATE_SPEECH": "...",
    # ... existing policies ...
    "NEW_POLICY": "Description of the policy",
}
```

2. Add detection logic in `moderator/mock_llm.py`:
```python
elif any(word in text for word in ["trigger_word_1", "trigger_word_2"]):
    violated_policy = "NEW_POLICY"
    classification = "Disallowed"
    reasoning.append("Explanation of why this violates the policy.")
```

## Future Enhancements

- **Real LLM Integration**: Upgrade to use OpenAI API or local models
- **Confidence Scores**: Add confidence metrics to classifications
- **Multi-Language Support**: Add support for Hindi, Gujarati, and other languages
- **FastAPI Service**: Convert to a REST API for production use
- **Database Logging**: Store moderation decisions for auditing
- **Custom Thresholds**: Configurable sensitivity levels for different policies

## Requirements

- Python 3.7+
- No external dependencies required for basic usage

## License

This project is open source and available for educational and commercial use.
