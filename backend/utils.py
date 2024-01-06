import json

def extract_json(text) -> str:
    counter = 0
    json_start = None
    json_end = None

    for i, char in enumerate(text):
        if char == '{':
            counter += 1
            if json_start is None:
                json_start = i
        elif char == '}':
            counter -= 1
            if counter == 0 and json_start is not None:
                json_end = i + 1
                break

    if json_start is not None and json_end is not None:
        try:
            return text[json_start:json_end]
        except json.JSONDecodeError as e:
            return f"Error parsing JSON: {e}"
    else:
        return "No JSON found"
