import json
import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_response(prompt):
    """
    Call Groq API to generate LLM-based moderation response.
    
    Args:
        prompt: The formatted prompt for the LLM (contains user text and policies)
    
    Returns:
        A dictionary with classification, violated_policy, and reasoning
    """
    try:
        # Call Groq API with the system prompt
        message = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # Using Groq's available model
            max_tokens=1024,  # Increased for better reasoning
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
        # Extract the response text
        response_text = message.choices[0].message.content
        
        # Try to parse JSON from the response
        try:
            # Extract JSON from the response (in case there's extra text)
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start != -1 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                result = json.loads(json_str)
                
                # Ensure all required fields are present
                classification = result.get("classification", "Allowed")
                violated_policy = result.get("violated_policy")
                reasoning = result.get("reasoning", "")
                
                # If policy is missing but classification indicates violation, extract from reasoning
                if not violated_policy and classification in ["Restricted", "Disallowed"]:
                    violated_policy = _extract_policy_from_text(reasoning)
                
                # For allowed content, still extract any relevant policy context from reasoning
                if not violated_policy and classification == "Allowed":
                    # Check if reasoning mentions specific policies for context
                    context_policy = _extract_policy_context(reasoning)
                    if context_policy:
                        reasoning = f"Content is allowed as written. Context: {reasoning}"
                
                return {
                    "classification": classification,
                    "violated_policy": violated_policy,
                    "reasoning": reasoning,
                    "reasoning_steps": result.get("reasoning_steps", [reasoning])
                }
        except (json.JSONDecodeError, ValueError) as e:
            pass  # Fall through to manual parsing
        except Exception as e:
            pass  # Fall through to manual parsing
        
        # Fallback: parse response text manually but preserve full reasoning
        classification = _extract_classification(response_text)
        violated_policy = _extract_policy_from_text(response_text)
        
        return {
            "classification": classification,
            "violated_policy": violated_policy,
            "reasoning": response_text,
            "reasoning_steps": [response_text]
        }
    
    except Exception as e:
        # Fallback to default response if API fails
        print(f"Error calling Groq API: {str(e)}")
        return {
            "classification": "Allowed",
            "violated_policy": None,
            "reasoning": f"Error occurred during moderation: {str(e)}",
            "reasoning_steps": [f"Error occurred during moderation: {str(e)}"]
        }


def _extract_classification(text):
    """Extract classification from response text."""
    text_lower = text.lower()
    if "disallowed" in text_lower:
        return "Disallowed"
    elif "restricted" in text_lower:
        return "Restricted"
    return "Allowed"


def _extract_policy_from_text(text):
    """
    Extract violated policy name from response text.
    Searches for policy keywords in the text.
    """
    policies = ["HATE_SPEECH", "VIOLENCE", "HARASSMENT", "SELF_HARM", "SEXUAL_CONTENT"]
    text_lower = text.lower()
    
    for policy in policies:
        if policy.lower() in text_lower:
            return policy
    
    return None


def _extract_policy_context(text):
    """
    Extract policy context from reasoning even if no violation.
    Useful for explaining why content is allowed despite sensitive keywords.
    """
    policies = ["HATE_SPEECH", "VIOLENCE", "HARASSMENT", "SELF_HARM", "SEXUAL_CONTENT"]
    text_lower = text.lower()
    
    mentioned_policies = []
    for policy in policies:
        if policy.lower() in text_lower:
            mentioned_policies.append(policy)
    
    return mentioned_policies if mentioned_policies else None


# Keep the legacy helper functions for reference
def _is_quoting_or_reporting(text):
    """Check if text is reporting/quoting (movie, said, etc.) rather than direct threat."""
    reporting_indicators = [
        "said", "told", "said,", "movie", "film", "character", "villain", "actor",
        "play", "scene", "dialogue", "line", "quote", "he said", "she said",
        "the character", "during the"
    ]
    return any(indicator in text for indicator in reporting_indicators)


def _contains_figurative_language(text):
    """Detect figurative language like 'destroy' a presentation, not physical harm."""
    figurative_patterns = {
        "destroy": ["presentation", "argument", "plan", "game", "test", "meeting", "project"],
        "kill": ["presentation", "performance", "app", "it", "that", "this", "the"],
        "crush": ["it", "exam", "test", "goal", "game", "competition"],
        "bomb": ["test", "interview", "presentation", "performance"],
        "slap": []  # Could be figurative but needs more context
    }
    
    for harmful_word, objects in figurative_patterns.items():
        if harmful_word in text:
            if not objects:  # Words that usually need qualifier
                return False
            if any(obj in text for obj in objects):
                return True
    return False


def _is_object_target(text):
    """Check if insult targets an object/app rather than a person/group."""
    object_targets = ["app", "software", "system", "website", "program", "tool", "feature", "update"]
    return any(target in text for target in object_targets)


def _is_group_targeted(text):
    """Detect if attack targets a group or community."""
    group_indicators = [
        "all people", "all of them", "those communities", "from that",
        "the type of people", "anyone who"
    ]
    # More careful detection for "that community" and "people like that"
    # These are concerning but not always hate speech
    if "people like that" in text and "stupid" in text:
        return True
    if "that community" in text and "stupid" in text:
        return True
    return any(indicator in text for indicator in group_indicators)


def _has_conditional_intent(text):
    """Detect conditional/hypothetical violence (if, would, could)."""
    conditional_markers = ["if i had", "if i could", "would", "could", "someone should"]
    return any(marker in text for marker in conditional_markers)


def _is_passive_aggressive(text):
    """Detect sarcasm and passive-aggressive tone."""
    passive_indicators = ["right,", "yeah right", "oh great", "brilliant", "genius",
                          "not.", "eye-roll", "great idea", "oh sure"]
    return any(indicator in text for indicator in passive_indicators)


def _is_distress_signal(text):
    """Detect emotional distress without explicit self-harm intent."""
    distress_markers = ["giving up", "feel like giving up", "want to disappear", 
                        "cannot continue", "can't take it anymore"]
    return any(marker in text for marker in distress_markers)


def _has_hostile_intent(text):
    """Detect hostile or malicious intent toward a person."""
    hostile_markers = ["deserves to fail", "should die", "should suffer"]
    return any(marker in text for marker in hostile_markers)


def _is_implicit_threat(text):
    """Detect implicit/veiled threats."""
    implicit_threats = ["teach him a lesson", "should teach", "teach a lesson"]
    return any(threat in text for threat in implicit_threats)


def _contains_direct_threat(text):
    """Check for direct, immediate threats."""
    direct_threats = ["i will kill", "i am going to kill", "i will attack", "i will hurt",
                      "i will slap", "if i had a chance, i would"]
    return any(threat in text for threat in direct_threats)


# Legacy helper functions (kept for reference but no longer used)
# The new Groq API version is used instead via the generate_response function above



