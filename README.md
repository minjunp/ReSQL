# ReSQL: Self-Improving Text-to-SQL Generation via Retrieval-augmented Error Reasoning

[![Dataset](https://img.shields.io/badge/Dataset-Available-green)](#datasets)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Official implementation of **ReSQL: Self-Improving Text-to-SQL Generation via Retrieval-augmented Error Reasoning**, submitted to LREC 2026.

## Overview

ReSQL is a novel framework for improving Text-to-SQL generation through retrieval-augmented error reasoning. The framework generates high-quality reasoning datasets by analyzing SQL execution errors and their root causes, enabling models to learn from their mistakes and improve performance.

### Key Features

- **Error Analysis Framework**: Systematic analysis of SQL generation errors (Syntax, Semantic, and Logical errors)
- **Multi-Model Support**: Compatible with various LLMs (Qwen, Llama, Gemma, Mistral, EXAONE)
- **Ready-to-Use Datasets**: Pre-generated reasoning datasets for BIRD and SPIDER benchmarks
- **Easy Integration**: Simple API for generating reasoning data from your own Text-to-SQL outputs

## Table of Contents

- [Installation](#installation)
- [Datasets](#datasets)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Repository Structure](#repository-structure)
- [Citation](#citation)
- [License](#license)

## Installation

### Requirements

- Python 3.8+
- CUDA-compatible GPU (recommended)
- Hugging Face account with access token

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ReSQL.git
cd ReSQL
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure your Hugging Face token:
```python
# In Analysis/Inference_template_qwen_7b.py, line 12
login(token='your_huggingface_token_here')
```

## Datasets

### Available Datasets

We provide pre-generated reasoning datasets for multiple LLMs on BIRD and SPIDER benchmarks:

| Model | Size | BIRD Results | SPIDER Results |
|-------|------|--------------|----------------|
| **Qwen2.5-7B** | 7B | [Download](generated_outputs/Qwen2.5-7b/) | [Download](generated_outputs/Qwen2.5-7b/) |
| **Qwen2.5-3B** | 3B | [Download](generated_outputs/Qwen2.5-3b/) | [Download](generated_outputs/Qwen2.5-3b/) |
| **Qwen2.5-1.5B** | 1.5B | [Download](generated_outputs/Qwen2.5-1.5b/) | [Download](generated_outputs/Qwen2.5-1.5b/) |
| **Llama-3.1-8B** | 8B | [Download](generated_outputs/Llama3.1-8b/) | [Download](generated_outputs/Llama3.1-8b/) |
| **Llama-3.2-3B** | 3B | [Download](generated_outputs/Llama3.2-3b/) | [Download](generated_outputs/Llama3.2-3b/) |
| **Llama-3.2-1B** | 1B | [Download](generated_outputs/Llama3.2-1b/) | [Download](generated_outputs/Llama3.2-1b/) |
| **Gemma-2-9B** | 9B | [Download](generated_outputs/Gemma2-9b/) | [Download](generated_outputs/Gemma2-9b/) |
| **Gemma-2-2B** | 2B | [Download](generated_outputs/Gemma2-2b/) | [Download](generated_outputs/Gemma2-2b/) |
| **Mistral-7B-v0.3** | 7B | [Download](generated_outputs/Mistral-v0.3-7b/) | [Download](generated_outputs/Mistral-v0.3-7b/) |
| **EXAONE-3.5-7.8B** | 7.8B | [Download](generated_outputs/Exaone3.5-7.8b/) | [Download](generated_outputs/Exaone3.5-7.8b/) |

### Dataset Format

Each dataset contains JSON files with the following structure:

```json
{
    "question_id": 0,
    "db_id": "database_name",
    "question": "Natural language question",
    "evidence": "Additional context or hints",
    "difficulty": "simple|moderate|challenging",
    "input": "Database schema with sample rows",
    "output": "Gold SQL query",
    "sql_query": "Generated SQL query",
    "result": "Execution result or error message",
    "Analysis_inference": {
        "Analysis": "Detailed error analysis",
        "Error Type": "Syntax Error|Semantic Error|Logical Error"
    }
}
```

### Base Datasets

The `rawdata/` folder contains preprocessed versions of:
- **BIRD** (BIg Bench for LaRge-scale Database Grounded Text-to-SQL Evaluation)
  - `BIRD_Train.json` (125MB)
  - `BIRD_Dev.json` (16MB)
- **SPIDER** (Yale Semantic Parsing and Text-to-SQL Challenge)
  - `SPIDER_Train.json` (56MB)
  - `SPIDER_DEV.json` (7.1MB)

## Quick Start

### Generate Reasoning Data

```python
# Set your model and GPU
model = "Qwen/Qwen2.5-7B-Instruct"
model_name = "Qwen2.5-7B-Instruct"
os.environ['CUDA_VISIBLE_DEVICES'] = '0'

# Run the inference script
python Analysis/Inference_template_qwen_7b.py
```

The script will:
1. Load the specified model
2. Process BIRD and SPIDER datasets
3. Analyze execution errors
4. Generate reasoning explanations
5. Save results to `generated_outputs/{model_name}/`

## Usage

### Using Pre-generated Datasets

```python
import json

# Load a pre-generated reasoning dataset
with open('generated_outputs/Qwen2.5-7b/BIRD_DEV_Qwen2.5-7B-Instruct_Result_Self_Debugging.json', 'r') as f:
    data = json.load(f)

# Access error analysis
for item in data:
    if 'Analysis_inference' in item:
        print(f"Question: {item['question']}")
        print(f"Error Type: {item['Analysis_inference']['Error Type']}")
        print(f"Analysis: {item['Analysis_inference']['Analysis']}")
```

### Generating Custom Reasoning Data

1. **Modify the model configuration** in `Analysis/Inference_template_qwen_7b.py`:

```python
# Line 218-219
model = "your-model-name"
model_name = "your-model-identifier"
```

2. **Adjust GPU settings**:

```python
# Line 245
os.environ['CUDA_VISIBLE_DEVICES'] = '0'  # Your GPU ID
```

3. **Run the script**:

```bash
python Analysis/Inference_template_qwen_7b.py
```

### Error Analysis Prompt

The framework uses a structured prompt to analyze SQL errors:

```python
prompt = f"""
### Task:
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

# Question: {question}
# Database information: {db_info}
# Gold SQL Query: {gold_query}
# Generated SQL query: {generated_query}
# Error message: {execution_result}

### Response Format (JSON)
```json
{{
    "Analysis": "<Your generated analysis here>",
    "Error Type": "<Syntax Error / Semantic Error / Logical Error>"
}}
```
"""
```

## Repository Structure

```
ReSQL/
├── Analysis/
│   ├── Inference_template_qwen_7b.py    # Main reasoning generation script
│   └── resql/                            # Additional utilities (if any)
├── rawdata/
│   ├── BIRD_Train.json                   # BIRD training set (125MB)
│   ├── BIRD_Dev.json                     # BIRD development set (16MB)
│   ├── SPIDER_Train.json                 # SPIDER training set (56MB)
│   └── SPIDER_DEV.json                   # SPIDER development set (7.1MB)
├── generated_outputs/
│   ├── Qwen2.5-7b/                       # Results for Qwen2.5-7B
│   ├── Qwen2.5-3b/                       # Results for Qwen2.5-3B
│   ├── Qwen2.5-1.5b/                     # Results for Qwen2.5-1.5B
│   ├── Llama3.1-8b/                      # Results for Llama-3.1-8B
│   ├── Llama3.2-3b/                      # Results for Llama-3.2-3B
│   ├── Llama3.2-1b/                      # Results for Llama-3.2-1B
│   ├── Gemma2-9b/                        # Results for Gemma-2-9B
│   ├── Gemma2-2b/                        # Results for Gemma-2-2B
│   ├── Mistral-v0.3-7b/                  # Results for Mistral-7B-v0.3
│   └── Exaone3.5-7.8b/                   # Results for EXAONE-3.5-7.8B
├── requirements.txt                       # Python dependencies
├── LICENSE                                # MIT License
└── README.md                              # This file
```

### Result Folder Structure

Each model's result folder contains:
- `BIRD_DEV_{model}_Result_Self_Debugging.json` - BIRD dev set with reasoning analysis
- `SPIDER_DEV_{model}_Result_Self_Debugging.json` - SPIDER dev set with reasoning analysis
- `Incorrect_case/` - Categorized incorrect cases by difficulty and debugging iteration (for some models)

## Supported Models

The framework supports the following model families:

### Qwen Models
- Qwen/Qwen2.5-7B-Instruct
- Qwen/Qwen2.5-3B-Instruct
- Qwen/Qwen2.5-1.5B-Instruct

### Llama Models
- meta-llama/Meta-Llama-3.1-8B-Instruct
- meta-llama/Llama-3.2-3B-Instruct
- meta-llama/Llama-3.2-1B-Instruct

### Gemma Models
- google/gemma-2-9b-it
- google/gemma-2-2b-it

### Other Models
- mistralai/Mistral-7B-Instruct-v0.3
- LGAI-EXAONE/EXAONE-3.5-7.8B-Instruct

## Error Type Categories

ReSQL categorizes SQL generation errors into three main types:

1. **Syntax Error**: Incorrect SQL syntax, missing keywords, or malformed queries
2. **Semantic Error**: Valid SQL structure but references non-existent tables, columns, or incorrect data types
3. **Logical Error**: Syntactically and semantically correct but doesn't match the question's intent

## Performance Tips

- **GPU Memory**: For 7B+ models, we recommend GPUs with at least 16GB VRAM
- **Batch Processing**: The script processes datasets incrementally and saves progress
- **Resume Capability**: If interrupted, the script will resume from the last saved checkpoint

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- BIRD Dataset: [https://bird-bench.github.io/](https://bird-bench.github.io/)
- SPIDER Dataset: [https://yale-lily.github.io/spider](https://yale-lily.github.io/spider)
- Built with Hugging Face Transformers

---

**Note**: This repository is associated with our LREC 2026 submission. Pre-generated datasets are ready for immediate use in your Text-to-SQL research.
