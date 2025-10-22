# ReSQL Examples

This folder contains example scripts demonstrating how to use the ReSQL framework and datasets.

## Available Examples

### 1. Load and Explore Data (`load_and_explore_data.py`)

Demonstrates how to:
- Load pre-generated reasoning datasets
- Analyze error type distributions
- Compare error rates across difficulty levels
- Extract and display specific error cases
- Compare results across multiple models

**Usage:**
```bash
python examples/load_and_explore_data.py
```

**What it shows:**
- Error distribution (Syntax, Semantic, Logical)
- Error rates by difficulty (simple, moderate, challenging)
- Side-by-side comparison of generated vs. gold queries
- Detailed analysis explanations

**Output example:**
```
============================================================
ERROR DISTRIBUTION
============================================================
Successful queries: 1234
Failed queries: 266

Error types:
  - Semantic Error: 145
  - Logical Error: 89
  - Syntax Error: 32

============================================================
ERROR RATE BY DIFFICULTY
============================================================
Simple: 45/500 (9.0% error rate)
Moderate: 123/600 (20.5% error rate)
Challenging: 98/400 (24.5% error rate)
```

### 2. Generate Reasoning Data (`generate_reasoning_data.py`)

**Standalone, generic script** that works with any Hugging Face model.

Demonstrates how to:
- Load any Hugging Face model (generic approach)
- Create error analysis prompts
- Generate reasoning explanations for SQL errors
- Process datasets with execution errors
- Parse and save results with analysis

**Key Features:**
- ✅ No dependencies on Analysis folder
- ✅ Works with any HF model (Qwen, Llama, Gemma, etc.)
- ✅ Self-contained with all necessary functions
- ✅ Example data included for testing
- ✅ Handles both GPU and CPU inference

**Usage:**
```bash
# Run with default model (Qwen 7B)
python examples/generate_reasoning_data.py

# Or edit the script to use a different model:
# MODEL_NAME = "meta-llama/Llama-3.2-1B-Instruct"
# MODEL_NAME = "google/gemma-2-2b-it"
```

**Quick customization:**
1. Change `MODEL_NAME` variable (line 287)
2. Replace `example_data` with your SQL errors (line 298)
3. Run the script!

**For production use with larger datasets, see:** `Analysis/Inference_template_qwen_7b.py`

## Quick Start

### Prerequisites

Install required packages:
```bash
pip install -r requirements.txt
```

### Running Examples

1. **Explore pre-generated datasets:**
```bash
cd examples
python load_and_explore_data.py
```

2. **Generate custom reasoning data:**
```bash
# Edit generate_reasoning_data.py to set your model and data paths
python generate_reasoning_data.py
```

## Example Outputs

### Error Analysis Example

```json
{
    "question": "What is the average age of students?",
    "sql_query": "SELECT AVG(student_age) FROM students",
    "result": "EXECUTION ERROR: no such column: student_age",
    "Analysis_inference": {
        "Analysis": "The generated query references a column 'student_age' that does not exist in the database schema. According to the database information, the correct column name is 'age', not 'student_age'. This is a common naming error where the model added an unnecessary table name prefix to the column.",
        "Error Type": "Semantic Error"
    }
}
```

## Customization

### Analyzing Different Models

Modify the paths in `load_and_explore_data.py`:

```python
# Compare multiple models
model_results = {
    'Qwen-7B': load_json('Result/Qwen2.5-7b/BIRD_DEV_Qwen2.5-7B-Instruct_Result_Self_Debugging.json'),
    'Llama-8B': load_json('Result/Llama3.1-8b/BIRD_DEV_Meta-Llama-3.1-8B-Instruct_Result_Self_Debugging.json'),
    'Gemma-9B': load_json('Result/Gemma2-9b/BIRD_DEV_gemma-2-9b-it_Result_Self_Debugging.json'),
}
compare_models(model_results)
```

### Custom Error Analysis Prompts

Modify the prompt template in `generate_reasoning_data.py`:

```python
def create_error_analysis_prompt(question, evidence, db_info, gold_query, generated_query, error_message):
    # Customize this function to change the analysis prompt
    prompt = f"""
    Your custom prompt here...
    Question: {question}
    ...
    """
    return prompt
```

## Code Organization

```
examples/
├── README.md                        # This file
├── load_and_explore_data.py        # Dataset exploration example
└── generate_reasoning_data.py      # Reasoning generation example
```

## Common Use Cases

### 1. Finding Specific Error Patterns

```python
from pathlib import Path
import json

def find_foreign_key_errors(data):
    """Find errors related to foreign key constraints."""
    fk_errors = []
    for item in data:
        if 'Analysis_inference' in item:
            analysis = item['Analysis_inference']['Analysis'].lower()
            if 'foreign key' in analysis or 'join' in analysis:
                fk_errors.append(item)
    return fk_errors
```

### 2. Extracting Training Data

```python
def convert_to_training_format(data):
    """Convert to instruction-tuning format."""
    training_data = []
    for item in data:
        if 'Analysis_inference' in item:
            training_data.append({
                'instruction': f"Analyze this SQL error:\n{item['sql_query']}\nError: {item['result']}",
                'input': f"Question: {item['question']}\nDatabase: {item['input'][:200]}...",
                'output': item['Analysis_inference']['Analysis']
            })
    return training_data
```

### 3. Computing Error Statistics

```python
def compute_error_statistics(data):
    """Compute detailed error statistics."""
    stats = {
        'total': len(data),
        'errors': 0,
        'by_type': {},
        'by_difficulty': {},
        'avg_query_length': 0
    }

    query_lengths = []
    for item in data:
        if 'sql_query' in item:
            query_lengths.append(len(item['sql_query']))

        if 'Analysis_inference' in item:
            stats['errors'] += 1
            error_type = item['Analysis_inference']['Error Type']
            stats['by_type'][error_type] = stats['by_type'].get(error_type, 0) + 1

        difficulty = item.get('difficulty', 'unknown')
        if difficulty not in stats['by_difficulty']:
            stats['by_difficulty'][difficulty] = {'total': 0, 'errors': 0}
        stats['by_difficulty'][difficulty]['total'] += 1
        if 'Analysis_inference' in item:
            stats['by_difficulty'][difficulty]['errors'] += 1

    stats['avg_query_length'] = sum(query_lengths) / len(query_lengths) if query_lengths else 0
    return stats
```

## Tips

1. **Memory Management**: When loading large datasets, consider processing in batches
2. **GPU Usage**: For inference, ensure CUDA is properly configured
3. **Error Handling**: The examples include basic error handling; extend as needed
4. **Custom Analysis**: Modify prompts to focus on specific error types

## Getting Help

- Check the main README: `../README.md`
- Review the full inference script: `../Analysis/Inference_template_qwen_7b.py`
- See dataset documentation: `../Data/README.md` and `../Result/README.md`

## Next Steps

After exploring these examples:

1. **Use pre-generated datasets** for your research
2. **Generate reasoning data** for your own models
3. **Fine-tune models** using the reasoning data
4. **Evaluate improvements** on BIRD and SPIDER benchmarks

For questions or issues, please open an issue on GitHub.
