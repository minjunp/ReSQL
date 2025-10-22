"""
Generic example script for generating SQL error reasoning data with any Hugging Face model.

This standalone script demonstrates the ReSQL framework's core concept:
analyzing SQL generation errors and creating reasoning explanations.

Usage:
    python generate_reasoning_data.py

You can modify the MODEL_NAME variable to use any compatible Hugging Face model.
"""

import json
import time
from typing import Dict, List, Optional


def create_error_analysis_prompt(
    question: str,
    evidence: str,
    db_info: str,
    gold_query: str,
    generated_query: str,
    error_message: str
) -> str:
    """
    Create a structured prompt for SQL error analysis.

    Args:
        question: Natural language question
        evidence: Additional context or hints
        db_info: Database schema information
        gold_query: Correct SQL query
        generated_query: Model-generated query that failed
        error_message: Execution error message

    Returns:
        Formatted prompt string for the model
    """
    question_with_evidence = question + (" " + evidence if evidence else "")

    prompt = f"""### Task:
You are given:
- A 'Question' that needs to be answered using SQL.
- A 'Database information' that describes the tables and columns.
- A 'Gold SQL Query' that correctly answers the question.
- A 'Generated SQL query' that was produced by the model but resulted in an execution error.
- The 'Error message' that was returned when executing the generated query.

Your task is to analyze 'why the generated SQL query failed' and provide an explanation of the error.

### Guidelines for Analysis:
1. **Identify the Error Type**
   - Syntax Error: Issues like incorrect SQL syntax or missing keywords.
   - Semantic Error: The query structure is valid but references nonexistent tables/columns.
   - Logical Error: The query does not match the intended question meaning.

2. **Compare Against the Gold Query**
   - Identify key differences between the 'generated query' and 'gold query'.
   - Explain which specific mistakes led to the execution error.

# Question: {question_with_evidence}
# Database information: {db_info}
# Gold SQL Query: {gold_query}
# Generated SQL query: {generated_query}
# Error message: {error_message}

### Response Format (JSON)
```json
{{
    "Analysis": "<Your generated analysis here>",
    "Error Type": "<Syntax Error / Semantic Error / Logical Error>"
}}
```
"""
    return prompt


def load_model_and_tokenizer(model_name: str, use_gpu: bool = True):
    """
    Load any Hugging Face model and tokenizer.

    Args:
        model_name: Hugging Face model identifier (e.g., "Qwen/Qwen2.5-7B-Instruct")
        use_gpu: Whether to use GPU if available

    Returns:
        Tuple of (model, tokenizer)
    """
    try:
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer

        print(f"Loading model: {model_name}")

        # Determine device
        device_map = "auto" if use_gpu and torch.cuda.is_available() else None

        # Load tokenizer
        tokenizer = AutoTokenizer.from_pretrained(model_name)

        # Load model
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.bfloat16 if use_gpu else torch.float32,
            device_map=device_map,
            trust_remote_code=True
        )

        print(f"✓ Model loaded successfully on {'GPU' if use_gpu else 'CPU'}")
        return model, tokenizer

    except ImportError:
        print("Error: transformers or torch not installed.")
        print("Install with: pip install transformers torch")
        return None, None
    except Exception as e:
        print(f"Error loading model: {e}")
        return None, None


def generate_analysis(
    prompt: str,
    model,
    tokenizer,
    max_new_tokens: int = 512,
    temperature: float = 0.0
) -> str:
    """
    Generate error analysis using the model.

    Args:
        prompt: The analysis prompt
        model: Loaded language model
        tokenizer: Model tokenizer
        max_new_tokens: Maximum tokens to generate
        temperature: Sampling temperature (0.0 for deterministic)

    Returns:
        Generated analysis text
    """
    try:
        import torch

        # Format as chat messages (works for most instruction-tuned models)
        messages = [
            {"role": "system", "content": "You are a knowledgeable assistant to analyze SQL queries."},
            {"role": "user", "content": prompt}
        ]

        # Try to apply chat template (if model supports it)
        try:
            formatted_prompt = tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True
            )
        except:
            # Fallback: use the prompt directly
            formatted_prompt = prompt

        # Tokenize
        inputs = tokenizer(formatted_prompt, return_tensors="pt")

        # Move to same device as model
        if hasattr(model, 'device'):
            inputs = {k: v.to(model.device) for k, v in inputs.items()}

        # Generate
        print("Generating analysis...")
        start_time = time.time()

        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=temperature > 0.0,
                temperature=temperature if temperature > 0.0 else 1.0,
                eos_token_id=tokenizer.eos_token_id,
                pad_token_id=tokenizer.pad_token_id if tokenizer.pad_token_id else tokenizer.eos_token_id
            )

        end_time = time.time()

        # Decode only the generated part (exclude input)
        generated_ids = outputs[0][inputs['input_ids'].shape[1]:]
        response = tokenizer.decode(generated_ids, skip_special_tokens=True)

        print(f"✓ Generated in {end_time - start_time:.2f} seconds")
        return response.strip()

    except Exception as e:
        print(f"Error during generation: {e}")
        return f"Error: {str(e)}"


def process_error_sample(
    sample: Dict,
    model,
    tokenizer,
    max_new_tokens: int = 512
) -> Dict:
    """
    Process a single SQL error sample to generate reasoning.

    Args:
        sample: Dictionary with question, queries, error, etc.
        model: Loaded language model
        tokenizer: Model tokenizer
        max_new_tokens: Maximum tokens for generation

    Returns:
        Updated sample with analysis
    """
    # Skip if no execution error
    if 'EXECUTION ERROR' not in sample.get('result', ''):
        print(f"  ⊙ No error in sample {sample.get('question_id', '?')}, skipping")
        return sample

    print(f"\n{'='*60}")
    print(f"Processing sample {sample.get('question_id', '?')}")
    print(f"Question: {sample['question'][:80]}...")

    # Extract information
    question = sample.get('question', '')
    evidence = sample.get('evidence', '')
    db_info = sample.get('input', '')
    gold_query = sample.get('output', sample.get('query', ''))
    generated_query = sample.get('sql_query', '')
    error_message = sample.get('result', '')

    # Create prompt
    prompt = create_error_analysis_prompt(
        question, evidence, db_info, gold_query, generated_query, error_message
    )

    # Generate analysis
    if model is not None:
        analysis_text = generate_analysis(prompt, model, tokenizer, max_new_tokens)

        # Try to parse JSON from response
        try:
            # Look for JSON in the response
            if '```json' in analysis_text:
                json_start = analysis_text.find('```json') + 7
                json_end = analysis_text.find('```', json_start)
                json_str = analysis_text[json_start:json_end].strip()
            elif '{' in analysis_text and '}' in analysis_text:
                json_start = analysis_text.find('{')
                json_end = analysis_text.rfind('}') + 1
                json_str = analysis_text[json_start:json_end]
            else:
                json_str = analysis_text

            analysis_json = json.loads(json_str)
            sample['Analysis_inference'] = analysis_json
            print(f"✓ Error Type: {analysis_json.get('Error Type', 'Unknown')}")
        except:
            # If JSON parsing fails, store as text
            sample['Analysis_inference'] = {
                "Analysis": analysis_text,
                "Error Type": "Unknown"
            }
            print("⚠ Could not parse JSON, storing as text")
    else:
        # Mock analysis if model not available
        sample['Analysis_inference'] = {
            "Analysis": "Mock analysis - model not loaded",
            "Error Type": "Unknown"
        }
        print("⚠ Using mock analysis (model not available)")

    return sample


def main():
    """
    Main function demonstrating ReSQL reasoning data generation.
    """
    print("="*60)
    print("ReSQL: Generic Reasoning Data Generation")
    print("="*60)

    # ==================== CONFIGURATION ====================
    # Change these variables to use different models or settings

    MODEL_NAME = "Qwen/Qwen2.5-7B-Instruct"  # Change to any HF model
    USE_GPU = True  # Set to False for CPU-only inference
    MAX_NEW_TOKENS = 512

    # For testing, you can use smaller models:
    # MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"
    # MODEL_NAME = "meta-llama/Llama-3.2-1B-Instruct"
    # MODEL_NAME = "google/gemma-2-2b-it"

    # ==================== EXAMPLE DATA ====================
    # This is sample data - replace with your own SQL error data
    example_data = [
        {
            "question_id": 1,
            "question": "What is the total number of students?",
            "evidence": "",
            "difficulty": "simple",
            "input": "Name: students\nInfo: id INTEGER, name TEXT, age INTEGER\nRows: [(1, 'Alice', 20), (2, 'Bob', 21), (3, 'Charlie', 22)]",
            "output": "SELECT COUNT(*) FROM students",
            "sql_query": "SELECT SUM(id) FROM students",
            "result": "EXECUTION ERROR: Result mismatch - expected count, got sum"
        },
        {
            "question_id": 2,
            "question": "List all students older than 20",
            "evidence": "",
            "difficulty": "simple",
            "input": "Name: students\nInfo: id INTEGER, name TEXT, age INTEGER\nRows: [(1, 'Alice', 20), (2, 'Bob', 21), (3, 'Charlie', 22)]",
            "output": "SELECT name FROM students WHERE age > 20",
            "sql_query": "SELECT name FROM students WHERE student_age > 20",
            "result": "EXECUTION ERROR: no such column: student_age"
        }
    ]

    print(f"\nConfiguration:")
    print(f"  Model: {MODEL_NAME}")
    print(f"  Device: {'GPU' if USE_GPU else 'CPU'}")
    print(f"  Max tokens: {MAX_NEW_TOKENS}")
    print(f"  Examples: {len(example_data)}")

    # ==================== LOAD MODEL ====================
    print(f"\n{'='*60}")
    model, tokenizer = load_model_and_tokenizer(MODEL_NAME, USE_GPU)

    if model is None:
        print("\n⚠ Model loading failed. Running in demo mode with mock outputs.")
        print("To use actual models, ensure transformers and torch are installed:")
        print("  pip install transformers torch")

    # ==================== PROCESS DATA ====================
    print(f"\n{'='*60}")
    print("Processing SQL error samples...")
    print(f"{'='*60}")

    results = []
    for i, sample in enumerate(example_data, 1):
        print(f"\n[{i}/{len(example_data)}]")
        processed_sample = process_error_sample(
            sample,
            model,
            tokenizer,
            MAX_NEW_TOKENS
        )
        results.append(processed_sample)

    # ==================== SAVE RESULTS ====================
    output_file = "reasoning_output.json"
    print(f"\n{'='*60}")
    print(f"Saving results to {output_file}")
    print(f"{'='*60}")

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"✓ Saved {len(results)} examples")

    # ==================== DISPLAY RESULTS ====================
    print(f"\n{'='*60}")
    print("SAMPLE OUTPUT")
    print(f"{'='*60}")

    for i, result in enumerate(results[:2], 1):  # Show first 2
        print(f"\nExample {i}:")
        print(f"Question: {result['question']}")
        print(f"Generated Query: {result['sql_query']}")
        print(f"Error: {result['result']}")
        if 'Analysis_inference' in result:
            print(f"Error Type: {result['Analysis_inference'].get('Error Type', 'Unknown')}")
            print(f"Analysis: {result['Analysis_inference'].get('Analysis', 'N/A')[:200]}...")

    # ==================== SUMMARY ====================
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"Total samples processed: {len(results)}")
    print(f"Output file: {output_file}")
    print(f"\nTo process your own data:")
    print(f"1. Replace 'example_data' with your SQL error dataset")
    print(f"2. Change MODEL_NAME to your preferred model")
    print(f"3. Run: python generate_reasoning_data.py")
    print(f"\nFor production use with larger datasets, see:")
    print(f"  ../Analysis/Inference_template_qwen_7b.py")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
