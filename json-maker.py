import json
import random

def create_jsonl(data, filename, num_lines=30):
    # Example random prompts and responses
    random_examples = [
        [
            ("system", "You are a helpful assistant that provides information based on user queries."),
            ("user", "How do I reverse a list in Python?"),
            ("assistant", "You can use list.reverse() or list[::-1] to reverse a list in Python.")
        ],
        [
            ("system", "You are a helpful assistant that provides information based on user queries."),
            ("user", "What's the capital of France?"),
            ("assistant", "The capital of France is Paris.")
        ],
        [
            ("system", "You are a helpful assistant that provides information based on user queries."),
            ("user", "Who wrote 'To Kill a Mockingbird'?"),
            ("assistant", "Harper Lee wrote 'To Kill a Mockingbird'.")
        ]
    ]

    # Combine provided data with enough random examples to reach num_lines
    all_data = data + [random.choice(random_examples) for _ in range(num_lines - len(data))]

    with open(filename, 'w', encoding='utf-8') as f:
        for conversation in all_data:
            messages = [
                {"role": role, "content": content}
                for role, content in conversation
            ]
            json.dump({"messages": messages}, f, ensure_ascii=False)
            f.write('\n')

# using the function
create_jsonl([
    [
        ("system", "You are a helpful assistant that provides information based on user queries."),
        ("user", "What is the weather like today?"),
        ("assistant", "I don't have access to real-time weather data, but you can check a weather website or app for the latest updates.")
    ]
], "conversations.jsonl", num_lines=30)
