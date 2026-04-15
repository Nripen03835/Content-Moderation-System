from moderator.policies import POLICIES


def build_prompt(user_text):
    policy_text = "\n".join([f"{k}: {v}" for k, v in POLICIES.items()])

    prompt = f"""
You are a content moderation system. Analyze content carefully considering context, tone, and intent.

Policies to Check:
{policy_text}

Analysis Guidelines:
1. Check for policy violations
2. Consider context:
   - Is it figurative language? (destroy = do well, kill = excel, etc.)
   - Is it in entertainment context? (movie quotes, games, sports)
   - Is it sarcasm or joking?
   - Is it directed at a person, group, or object?
3. Classify into:
   - Allowed (no violations, explain why if context matters)
   - Restricted (concerning but arguable)
   - Disallowed (clear violation)
4. Always identify the SPECIFIC POLICY if there's any concern, even for "Allowed" content

Return output in JSON format:
{{
  "classification": "...",
  "violated_policy": "POLICY_NAME or null",
  "reasoning": "Detailed explanation of analysis and why content is allowed/restricted/disallowed"
}}

User Content:
\"\"\"{user_text}\"\"\"
"""
    return prompt
