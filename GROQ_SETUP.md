# Groq LLM Integration Setup Guide

## Overview
This project now uses the **Groq API** for LLM-based content moderation instead of the mock implementation. The Groq API provides fast, efficient access to large language models for analyzing and moderating user content.

## Installation

### 1. Install Required Dependencies
```bash
pip install -r requirements.txt
```

This installs:
- **groq**: Official Groq API client library
- **python-dotenv**: For secure environment variable management

### 2. Configure API Key
The API key is already configured in the `.env` file located in the project root:
```
GROQ_API_KEY=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
```

**IMPORTANT**: 
- ⚠️ **NEVER commit the `.env` file to version control** - it contains sensitive credentials
- The `.gitignore` file already includes `.env` to prevent accidental commits
- In production, use environment variables or a secure secrets manager

### 3. Run the Application
```bash
python main.py
```

Then enter text to moderate when prompted.

## How It Works

### Architecture
1. **Prompt Builder** (`moderator/prompt_builder.py`): Creates a detailed prompt with moderation policies
2. **Groq LLM** (`moderator/mock_llm.py`): Sends the prompt to Groq API and receives analysis
3. **Parser** (`moderator/parser.py`): Formats the LLM output into structured JSON
4. **Moderator** (`moderator/moderator.py`): Orchestrates the moderation pipeline

### Moderation Policies
The system checks for violations in these categories:
- **HATE_SPEECH**: Content attacking groups based on race, religion, gender, or identity
- **VIOLENCE**: Content promoting or glorifying physical harm
- **HARASSMENT**: Abusive or threatening language toward individuals
- **SELF_HARM**: Encouraging or promoting self-harm
- **SEXUAL_CONTENT**: Explicit or pornographic content

### Classification Levels
- **Allowed**: Content complies with all policies
- **Restricted**: Content is concerning but may be allowed with warnings
- **Disallowed**: Content violates policies and should be blocked

## API Details

### Groq Model
- **Model**: `mixtral-8x7b-32768`
- **Max Tokens**: 512
- **Provider**: Groq API

### Response Format
The LLM returns a JSON response with:
```json
{
  "classification": "Allowed|Restricted|Disallowed",
  "violated_policy": "POLICY_NAME or null",
  "reasoning": "Explanation of the decision"
}
```

## Error Handling
If the Groq API is unavailable, the system gracefully falls back to:
- Returning an error message in the reasoning field
- Defaulting to "Allowed" classification
- Maintaining the application's operation

## Testing

### Test with Allowed Content
```bash
echo "Hello, how are you?" | python main.py
```

### Test with Restricted Content
```bash
echo "I hate all people from that community" | python main.py
```

### Test with Violence Keywords
```bash
echo "I will hurt you" | python main.py
```

## Troubleshooting

### ModuleNotFoundError: groq
**Solution**: Run `pip install -r requirements.txt` to install dependencies

### API Key Not Found
**Solution**: Ensure the `.env` file exists in the project root with `GROQ_API_KEY=...`

### API Rate Limiting
The Groq API may rate limit requests. If you see errors:
- Wait a moment before retrying
- Consider increasing token limits
- Contact Groq support for higher limits

### Connection Errors
- Check your internet connection
- Verify the API key is valid
- Ensure Groq's servers are operational

## Security Best Practices

1. **Never hardcode API keys** in source files
2. **Use environment variables** via `.env` file
3. **Keep `.env` out of version control** - it's in `.gitignore`
4. **Rotate API keys regularly** in production
5. **Use IAM roles** in cloud deployments (AWS, GCP, Azure)
6. **Monitor API usage** for unauthorized access

## Next Steps

1. ✅ Install dependencies: `pip install -r requirements.txt`
2. ✅ Configure API key in `.env` (already done)
3. ✅ Test the application: `python main.py`
4. 🔜 Deploy to production with secure secrets management
5. 🔜 Set up monitoring and logging
6. 🔜 Implement rate limiting for the API

## Support

For issues with:
- **Groq API**: https://console.groq.com/
- **Python dependencies**: Check `requirements.txt`
- **Content moderation logic**: See `moderator/policies.py`
