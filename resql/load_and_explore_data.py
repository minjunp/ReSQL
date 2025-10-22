"""
Example script demonstrating how to load and explore ReSQL datasets.

This script shows:
1. Loading pre-generated reasoning datasets
2. Analyzing error types and distributions
3. Comparing generated vs. gold queries
4. Extracting specific error cases
"""

import json
from collections import Counter
from pathlib import Path


def load_json(file_path):
    """Load JSON data from file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def analyze_error_distribution(data):
    """Analyze distribution of error types in the dataset."""
    error_types = Counter()
    successful_queries = 0

    for item in data:
        if 'Analysis_inference' in item:
            error_type = item['Analysis_inference'].get('Error Type', 'Unknown')
            error_types[error_type] += 1
        else:
            successful_queries += 1

    print("\n" + "="*60)
    print("ERROR DISTRIBUTION")
    print("="*60)
    print(f"Successful queries: {successful_queries}")
    print(f"Failed queries: {sum(error_types.values())}")
    print("\nError types:")
    for error_type, count in error_types.most_common():
        print(f"  - {error_type}: {count}")

    return error_types, successful_queries


def analyze_by_difficulty(data):
    """Analyze errors by question difficulty."""
    difficulty_errors = {}

    for item in data:
        difficulty = item.get('difficulty', 'unknown')
        if difficulty not in difficulty_errors:
            difficulty_errors[difficulty] = {'total': 0, 'errors': 0}

        difficulty_errors[difficulty]['total'] += 1
        if 'Analysis_inference' in item:
            difficulty_errors[difficulty]['errors'] += 1

    print("\n" + "="*60)
    print("ERROR RATE BY DIFFICULTY")
    print("="*60)
    for difficulty in ['simple', 'moderate', 'challenging']:
        if difficulty in difficulty_errors:
            stats = difficulty_errors[difficulty]
            error_rate = (stats['errors'] / stats['total'] * 100) if stats['total'] > 0 else 0
            print(f"{difficulty.capitalize()}: {stats['errors']}/{stats['total']} ({error_rate:.1f}% error rate)")


def show_error_examples(data, error_type, num_examples=3):
    """Display example queries with specific error type."""
    examples = [
        item for item in data
        if item.get('Analysis_inference', {}).get('Error Type') == error_type
    ]

    print("\n" + "="*60)
    print(f"EXAMPLES OF {error_type.upper()}")
    print("="*60)

    for i, example in enumerate(examples[:num_examples], 1):
        print(f"\nExample {i}:")
        print(f"Question: {example['question']}")
        print(f"\nGold Query:\n{example['output']}")
        print(f"\nGenerated Query:\n{example['sql_query']}")
        print(f"\nError:\n{example['result']}")
        print(f"\nAnalysis:\n{example['Analysis_inference']['Analysis']}")
        print("-" * 60)


def compare_models(model_results):
    """Compare error rates across different models."""
    print("\n" + "="*60)
    print("MODEL COMPARISON")
    print("="*60)

    comparison = {}
    for model_name, data in model_results.items():
        total = len(data)
        errors = sum(1 for item in data if 'Analysis_inference' in item)
        error_rate = (errors / total * 100) if total > 0 else 0
        comparison[model_name] = {
            'total': total,
            'errors': errors,
            'error_rate': error_rate
        }

    # Sort by error rate
    for model_name in sorted(comparison.keys(), key=lambda x: comparison[x]['error_rate']):
        stats = comparison[model_name]
        print(f"{model_name}: {stats['errors']}/{stats['total']} ({stats['error_rate']:.1f}% errors)")


def main():
    """Main function to demonstrate dataset exploration."""

    # Example: Load Qwen 7B results on BIRD dev set
    print("Loading ReSQL reasoning dataset...")

    # Adjust this path to your actual data location
    data_path = Path(__file__).parent.parent / "Result" / "Qwen2.5-7b"
    bird_file = data_path / "BIRD_DEV_Qwen2.5-7B-Instruct_Result_Self_Debugging.json"

    if not bird_file.exists():
        print(f"Error: Dataset not found at {bird_file}")
        print("Please adjust the path in the script to point to your data.")
        return

    data = load_json(bird_file)
    print(f"Loaded {len(data)} examples from BIRD dev set")

    # Analyze error distribution
    error_types, successful = analyze_error_distribution(data)

    # Analyze by difficulty
    analyze_by_difficulty(data)

    # Show examples of each error type
    for error_type in ['Syntax Error', 'Semantic Error', 'Logical Error']:
        if error_type in [et for et, _ in error_types.most_common()]:
            show_error_examples(data, error_type, num_examples=2)

    # Example: Compare multiple models (if available)
    print("\n" + "="*60)
    print("MULTI-MODEL COMPARISON EXAMPLE")
    print("="*60)
    print("To compare models, load multiple result files:")
    print("""
model_results = {
    'Qwen-7B': load_json('Result/Qwen2.5-7b/BIRD_DEV_...json'),
    'Llama-8B': load_json('Result/Llama3.1-8b/BIRD_DEV_...json'),
    'Gemma-9B': load_json('Result/Gemma2-9b/BIRD_DEV_...json'),
}
compare_models(model_results)
    """)


if __name__ == "__main__":
    main()
