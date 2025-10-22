# ReSQL Quick Start Guide

Get started with ReSQL in 5 minutes!

## Option 1: Use Pre-generated Datasets (Fastest)

Perfect for researchers who want to use the reasoning data immediately.

```python
import json

# Load pre-generated reasoning dataset
with open('Result/Qwen2.5-7b/BIRD_DEV_Qwen2.5-7B-Instruct_Result_Self_Debugging.json', 'r') as f:
    data = json.load(f)

# Access error analysis
for item in data[:5]:  # First 5 examples
    if 'Analysis_inference' in item:
        print(f"Question: {item['question']}")
        print(f"Error: {item['Analysis_inference']['Error Type']}")
        print(f"Analysis: {item['Analysis_inference']['Analysis']}\n")
```

**Available datasets:**
- 10 different models (Qwen, Llama, Gemma, Mistral, EXAONE)
- BIRD and SPIDER benchmarks
- Ready to download from `Result/` folder

## Option 2: Generate Your Own Reasoning Data

For researchers who want to create reasoning data for custom models.

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Configure Hugging Face

Get your token from https://huggingface.co/settings/tokens

```python
# In Analysis/Inference_template_qwen_7b.py, line 12
login(token='your_token_here')
```

### Step 3: Select Your Model

```python
# In Analysis/Inference_template_qwen_7b.py, lines 218-219
model = "Qwen/Qwen2.5-7B-Instruct"  # Change to your model
model_name = "Qwen2.5-7B-Instruct"
```

### Step 4: Set GPU

```python
# Line 245
os.environ['CUDA_VISIBLE_DEVICES'] = '0'  # Your GPU ID
```

### Step 5: Run!

```bash
python Analysis/Inference_template_qwen_7b.py
```

Results will be saved to `Result/{model_name}/`

## Option 3: Explore with Examples

Try the example scripts to understand the framework.

```bash
# Explore pre-generated datasets
python examples/load_and_explore_data.py

# See how to generate reasoning data
python examples/generate_reasoning_data.py
```

## What's in the Box?

### 📁 Data/ - Base Datasets
- BIRD_Train.json (125MB)
- BIRD_Dev.json (16MB)
- SPIDER_Train.json (56MB)
- SPIDER_DEV.json (7.1MB)

### 📁 Result/ - Pre-generated Reasoning
- 10 model folders with analysis results
- Both BIRD and SPIDER benchmarks
- ~1500+ BIRD examples, ~1000+ SPIDER examples per model

### 📁 Analysis/ - Generation Code
- `Inference_template_qwen_7b.py` - Main script
- Multi-model support
- Automatic error detection

### 📁 examples/ - Usage Examples
- `load_and_explore_data.py` - Dataset exploration
- `generate_reasoning_data.py` - Custom generation

## Common Use Cases

### Use Case 1: Train on Error Reasoning

```python
import json

# Load reasoning data
with open('Result/Qwen2.5-7b/BIRD_DEV_Qwen2.5-7B-Instruct_Result_Self_Debugging.json', 'r') as f:
    data = json.load(f)

# Convert to training format
training_data = []
for item in data:
    if 'Analysis_inference' in item:
        training_data.append({
            'input': f"Analyze this SQL error:\nQuestion: {item['question']}\nQuery: {item['sql_query']}\nError: {item['result']}",
            'output': item['Analysis_inference']['Analysis']
        })

# Save for fine-tuning
with open('training_data.json', 'w') as f:
    json.dump(training_data, f, indent=2)
```

### Use Case 2: Error Pattern Analysis

```python
from collections import Counter

# Analyze error distributions
error_types = Counter()
for item in data:
    if 'Analysis_inference' in item:
        error_types[item['Analysis_inference']['Error Type']] += 1

print("Error Distribution:")
for error_type, count in error_types.most_common():
    print(f"  {error_type}: {count}")
```

### Use Case 3: Retrieval-Augmented Generation

```python
# Build error corpus for retrieval
error_corpus = []
for item in data:
    if 'Analysis_inference' in item:
        error_corpus.append({
            'query': item['sql_query'],
            'error': item['result'],
            'analysis': item['Analysis_inference']['Analysis'],
            'error_type': item['Analysis_inference']['Error Type']
        })

# Use for RAG when encountering similar errors
```

## System Requirements

### Minimum
- Python 3.8+
- 8GB RAM
- CPU-only (for loading/exploring data)

### Recommended (for generation)
- Python 3.9+
- 16GB+ RAM
- NVIDIA GPU with 16GB+ VRAM
- CUDA 11.8+

## GPU Memory Guide

| Model Size | GPU | Memory |
|-----------|-----|---------|
| 1-2B | RTX 3060 | 8GB |
| 3-7B | RTX 3090 | 24GB |
| 7-9B | A100 | 40GB |

## Next Steps

1. **Read the full README**: `README.md`
2. **Check dataset docs**: `Data/README.md` and `Result/README.md`
3. **Try examples**: `examples/README.md`
4. **Generate reasoning**: `Analysis/README.md`

## Getting Help

- 📖 Full documentation: See README.md
- 🐛 Issues: Open on GitHub
- 💡 Examples: Check `examples/` folder
- 📧 Contact: [your-email@example.com]

## Quick Links

- [Main README](README.md) - Full documentation
- [Dataset Documentation](Data/README.md) - Data format and usage
- [Results Documentation](Result/README.md) - Pre-generated datasets
- [Examples](examples/README.md) - Usage examples
- [Analysis Module](Analysis/README.md) - Generation code

---

**Ready in 5 minutes. Research-grade quality. Open source.**

🎯 Start with pre-generated datasets → 📊 Analyze results → 🚀 Generate your own → 📝 Publish
