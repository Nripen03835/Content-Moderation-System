def format_output(result, user_text):
    return {
        "input": user_text,
        "moderation_result": {
            "classification": result["classification"],
            "violated_policy": result["violated_policy"],
            "reasoning": result["reasoning"]
        }
    }
