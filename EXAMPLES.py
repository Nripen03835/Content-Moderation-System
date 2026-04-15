"""
GROQ LLM Integration - Practical Examples
This file shows how to use the content moderation system with Groq API
"""

# Example 1: Basic Usage
print("=" * 60)
print("EXAMPLE 1: Basic Usage")
print("=" * 60)

from moderator.moderator import moderate_text
import json

# Moderate text
result = moderate_text("Hello, how are you today?")
print(json.dumps(result, indent=2))


# Example 2: Batch Processing
print("\n" + "=" * 60)
print("EXAMPLE 2: Batch Processing Multiple Texts")
print("=" * 60)

text_samples = [
    "This is a great product, I love it!",
    "I really hate the current update",
    "Violence is never the solution",
]

for text in text_samples:
    result = moderate_text(text)
    classification = result['moderation_result']['classification']
    policy = result['moderation_result']['violated_policy']
    print(f"\n📝 Input: {text}")
    print(f"🏷️  Classification: {classification}")
    print(f"⚖️  Policy Violated: {policy}")


# Example 3: Checking Specific Policy Violations
print("\n" + "=" * 60)
print("EXAMPLE 3: Analyze Policy Violations")
print("=" * 60)

texts_to_check = [
    ("That's brilliant sarcasm", "HARASSMENT"),
    ("I will attack you", "VIOLENCE"),
    ("All members of that group are criminals", "HATE_SPEECH"),
]

violated_count = 0
allowed_count = 0

for text, policy in texts_to_check:
    result = moderate_text(text)
    classification = result['moderation_result']['classification']
    
    if result['moderation_result']['violated_policy'] == policy:
        print(f"✅ Correctly detected {policy}")
        violated_count += 1
    else:
        print(f"❌ Did not detect {policy}")
        allowed_count += 1
    
    print(f"   Text: {text}")
    print(f"   Classification: {classification}\n")


# Example 4: Get Detailed Reasoning
print("\n" + "=" * 60)
print("EXAMPLE 4: Detailed LLM Reasoning")
print("=" * 60)

sensitive_text = "That presentation was terrible and I hate the design"
result = moderate_text(sensitive_text)

print(f"Text: {sensitive_text}\n")
print(f"Classification: {result['moderation_result']['classification']}")
print(f"Violated Policy: {result['moderation_result']['violated_policy']}")
print(f"\nReasoning from Groq LLM:")
print(f"{result['moderation_result']['reasoning']}")


# Example 5: Integration with Error Handling
print("\n" + "=" * 60)
print("EXAMPLE 5: Error Handling in Integration")
print("=" * 60)

try:
    # This could be from user input, database, API, etc.
    user_input = "This is user-generated content"
    
    result = moderate_text(user_input)
    
    if result['moderation_result']['classification'] == 'Disallowed':
        print(f"⚠️  Content blocked: {user_input}")
        print(f"   Reason: {result['moderation_result']['violated_policy']}")
    
    elif result['moderation_result']['classification'] == 'Restricted':
        print(f"⚠️  Content flagged for review: {user_input}")
        print(f"   Reason: {result['moderation_result']['reasoning']}")
    
    else:
        print(f"✅ Content approved: {user_input}")

except Exception as e:
    print(f"❌ Error during moderation: {str(e)}")


# Example 6: Creating a Moderation Dashboard Feed
print("\n" + "=" * 60)
print("EXAMPLE 6: Moderation Dashboard Summary")
print("=" * 60)

test_feed = [
    "Great product! Highly recommend",
    "I hate this update so much",
    "The new feature is not working",
    "Check out this amazing feature",
    "This is unacceptable and offensive",
]

stats = {
    "total": len(test_feed),
    "allowed": 0,
    "restricted": 0,
    "disallowed": 0,
    "policies_violated": {}
}

print("\nProcessing content feed...\n")

for i, text in enumerate(test_feed, 1):
    result = moderate_text(text)
    classification = result['moderation_result']['classification']
    policy = result['moderation_result']['violated_policy']
    
    # Update stats
    stats[classification.lower()] += 1
    
    if policy:
        stats["policies_violated"][policy] = stats["policies_violated"].get(policy, 0) + 1
    
    # Show item
    status_symbol = "✅" if classification == "Allowed" else "⚠️ " if classification == "Restricted" else "❌"
    print(f"{i}. {status_symbol} [{classification}] {text[:50]}...")

print("\n" + "-" * 60)
print("DASHBOARD SUMMARY")
print("-" * 60)
print(f"Total items processed: {stats['total']}")
print(f"✅ Allowed: {stats['allowed']}")
print(f"⚠️  Restricted: {stats['restricted']}")
print(f"❌ Disallowed: {stats['disallowed']}")
if stats["policies_violated"]:
    print(f"\nPolicies Violated:")
    for policy, count in stats["policies_violated"].items():
        print(f"  • {policy}: {count}")


# Example 7: Real-time Content Filter
print("\n" + "=" * 60)
print("EXAMPLE 7: Real-time Content Filter")
print("=" * 60)
print("\nSimulating real-time user comment filtering...\n")

user_comments = [
    ("user123", "Awesome article!"),
    ("user456", "This is garbage, I hate everything"),
    ("user789", "Great discussion!"),
]

for username, comment in user_comments:
    result = moderate_text(comment)
    classification = result['moderation_result']['classification']
    
    if classification == 'Disallowed':
        print(f"🚫 [{username}] COMMENT BLOCKED")
        print(f"   Content: {comment}")
        print(f"   Reason: {result['moderation_result']['violated_policy']}\n")
    
    elif classification == 'Restricted':
        print(f"⚠️  [{username}] COMMENT FLAGGED FOR REVIEW")
        print(f"   Content: {comment}\n")
    
    else:
        print(f"✅ [{username}] COMMENT APPROVED")
        print(f"   Content: {comment}\n")


print("=" * 60)
print("Examples completed! Groq LLM is properly integrated.")
print("=" * 60)

# Note: These examples use the actual Groq API
# Responses are real LLM analysis from Groq's mixtral-8x7b-32768 model
