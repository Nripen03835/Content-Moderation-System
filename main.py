from moderator.moderator import moderate_text
import json


if __name__ == "__main__":
    user_input = input("Enter text to moderate: ")

    result = moderate_text(user_input)

    print("\nModeration Result:")
    print(json.dumps(result, indent=2))
