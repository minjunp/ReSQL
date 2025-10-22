# ReSQL Repository Structure

Complete overview of the repository organization and contents.

```
ReSQL/
│
├── 📄 README.md                      # Main documentation (START HERE!)
├── 📄 QUICKSTART.md                  # 5-minute getting started guide
├── 📄 CONTRIBUTING.md                # Contribution guidelines
├── 📄 LICENSE                        # MIT License
├── 📄 CITATION.cff                   # Citation information
├── 📄 requirements.txt               # Python dependencies
├── 📄 .gitignore                     # Git ignore rules
│
├── 📁 Analysis/                      # Core reasoning generation code
│   ├── 📄 README.md                  # Module documentation
│   ├── 🐍 Inference_template_qwen_7b.py  # Main generation script
│   └── 📁 resql/                     # Additional utilities (optional)
│
├── 📁 Data/                          # Base BIRD & SPIDER datasets
│   ├── 📄 README.md                  # Dataset documentation
│   ├── 📊 BIRD_Train.json            # BIRD training set (125MB)
│   ├── 📊 BIRD_Dev.json              # BIRD dev set (16MB)
│   ├── 📊 SPIDER_Train.json          # SPIDER training set (56MB)
│   └── 📊 SPIDER_DEV.json            # SPIDER dev set (7.1MB)
│
├── 📁 Result/                        # Pre-generated reasoning datasets
│   ├── 📄 README.md                  # Results documentation
│   │
│   ├── 📁 Qwen2.5-7b/                # Qwen 7B results
│   │   ├── 📊 BIRD_DEV_Qwen2.5-7B-Instruct_Result_Self_Debugging.json
│   │   ├── 📊 SPIDER_DEV_Qwen2.5-7B-Instruct_Result_Self_Debugging.json
│   │   └── 📁 Incorrect_case/        # Categorized errors
│   │
│   ├── 📁 Qwen2.5-3b/                # Qwen 3B results
│   │   ├── 📊 BIRD_DEV_Qwen2.5-3B-Instruct_Result_Self_Debugging.json
│   │   └── 📊 SPIDER_DEV_Qwen2.5-3B-Instruct_Result_Self_Debugging.json
│   │
│   ├── 📁 Qwen2.5-1.5b/              # Qwen 1.5B results
│   │   ├── 📊 BIRD_DEV_Qwen2.5-1.5B-Instruct_Result_Self_Debugging.json
│   │   └── 📊 SPIDER_DEV_Qwen2.5-1.5B-Instruct_Result_Self_Debugging.json
│   │
│   ├── 📁 Llama3.1-8b/               # Llama 3.1 8B results
│   │   ├── 📊 BIRD_DEV_Meta-Llama-3.1-8B-Instruct_Result_Self_Debugging.json
│   │   └── 📊 SPIDER_DEV_Meta-Llama-3.1-8B-Instruct_Result_Self_Debugging.json
│   │
│   ├── 📁 Llama3.2-3b/               # Llama 3.2 3B results
│   │   ├── 📊 BIRD_DEV_Llama-3.2-3B-Instruct_Result_Self_Debugging.json
│   │   └── 📊 SPIDER_DEV_Llama-3.2-3B-Instruct_Result_Self_Debugging.json
│   │
│   ├── 📁 Llama3.2-1b/               # Llama 3.2 1B results
│   │   ├── 📊 BIRD_DEV_Llama-3.2-1B-Instruct_Result_Self_Debugging.json
│   │   └── 📊 SPIDER_DEV_Llama-3.2-1B-Instruct_Result_Self_Debugging.json
│   │
│   ├── 📁 Gemma2-9b/                 # Gemma 9B results
│   │   ├── 📊 BIRD_DEV_gemma-2-9b-it_Result_Self_Debugging.json
│   │   └── 📊 SPIDER_DEV_gemma-2-9b-it_Result_Self_Debugging.json
│   │
│   ├── 📁 Gemma2-2b/                 # Gemma 2B results
│   │   ├── 📊 BIRD_DEV_gemma-2-2b-it_Result_Self_Debugging.json
│   │   └── 📊 SPIDER_DEV_gemma-2-2b-it_Result_Self_Debugging.json
│   │
│   ├── 📁 Mistral-v0.3-7b/           # Mistral 7B results
│   │   ├── 📊 BIRD_DEV_Mistral-7B-Instruct-v0.3_Result_Self_Debugging.json
│   │   └── 📊 SPIDER_DEV_Mistral-7B-Instruct-v0.3_Result_Self_Debugging.json
│   │
│   ├── 📁 Exaone3.5-7.8b/            # EXAONE 7.8B results
│   │   ├── 📊 BIRD_DEV_EXAONE-3.5-7.8B-Instruct_Result.json
│   │   └── 📊 SPIDER_DEV_EXAONE-3.5-7.8B-Instruct_Result.json
│   │
│   └── 📁 GPT_Prev/                  # Previous GPT results (legacy)
│
└── 📁 examples/                      # Usage examples and tutorials
    ├── 📄 README.md                  # Examples documentation
    ├── 🐍 load_and_explore_data.py   # Dataset exploration script
    └── 🐍 generate_reasoning_data.py # Custom generation example
```

## Quick Navigation

### 🚀 Getting Started
1. Read [README.md](README.md) - Overview and setup
2. Check [QUICKSTART.md](QUICKSTART.md) - 5-minute guide
3. Explore [examples/](examples/) - Usage examples

### 📊 Using Datasets
1. [Data/README.md](Data/README.md) - Base datasets (BIRD/SPIDER)
2. [Result/README.md](Result/README.md) - Pre-generated reasoning data
3. Browse [Result/](Result/) - 10 model folders with results

### 🔧 Generating Data
1. [Analysis/README.md](Analysis/README.md) - Code documentation
2. [Analysis/Inference_template_qwen_7b.py](Analysis/Inference_template_qwen_7b.py) - Main script
3. [examples/generate_reasoning_data.py](examples/generate_reasoning_data.py) - Simple example

### 🤝 Contributing
1. [CONTRIBUTING.md](CONTRIBUTING.md) - How to contribute
2. [LICENSE](LICENSE) - MIT License
3. [CITATION.cff](CITATION.cff) - How to cite

## File Sizes

### Data Folder (~204MB total)
- BIRD_Train.json: 125MB
- BIRD_Dev.json: 16MB
- SPIDER_Train.json: 56MB
- SPIDER_DEV.json: 7.1MB

### Result Folder (~350MB total)
Each model folder contains:
- BIRD dev results: ~20-30MB
- SPIDER dev results: ~10-15MB
- Incorrect_case subfolder: varies

### Code
- Analysis script: 12KB
- Example scripts: ~10KB total
- Documentation: ~100KB total

## Key Components

### 1. Main Generation Script
**File:** `Analysis/Inference_template_qwen_7b.py`

**Purpose:** Generate error reasoning data

**Key Functions:**
- `qwen_initialize_model()` - Initialize Qwen models
- `qwen_generate_result()` - Generate with Qwen
- `exaone_initialize_model()` - Initialize EXAONE
- `initialize_model()` - Initialize standard models
- `read_json()` / `save_list_as_json()` - I/O utilities

### 2. Pre-generated Datasets
**Location:** `Result/{model_name}/`

**Format:** JSON with SQL queries, errors, and analysis

**Content:**
- Original question and database info
- Generated SQL query
- Execution result/error
- Error analysis and classification

### 3. Example Scripts
**Location:** `examples/`

**Scripts:**
- `load_and_explore_data.py` - Analysis and exploration
- `generate_reasoning_data.py` - Custom generation

### 4. Documentation
**Files:**
- `README.md` - Main documentation
- `QUICKSTART.md` - Quick start guide
- `{folder}/README.md` - Folder-specific docs

## Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Input: Base Datasets (Data/)                            │
│    - BIRD_Train.json, BIRD_Dev.json                         │
│    - SPIDER_Train.json, SPIDER_DEV.json                     │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Process: Generation Script (Analysis/)                  │
│    - Load model (Qwen/Llama/Gemma/etc.)                    │
│    - Generate SQL queries                                   │
│    - Execute and detect errors                             │
│    - Generate reasoning analysis                           │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Output: Reasoning Datasets (Result/)                    │
│    - SQL queries with execution results                    │
│    - Error analysis and classification                     │
│    - Self-debugging iterations (up to 3)                   │
└─────────────────────────────────────────────────────────────┘
```

## Usage Patterns

### Pattern 1: Use Pre-generated Data
```
User → Result/{model}/ → Load JSON → Use in Research
```

### Pattern 2: Generate Custom Data
```
User → Analysis/Inference_template_qwen_7b.py → Configure → Run → Result/
```

### Pattern 3: Explore and Analyze
```
User → examples/load_and_explore_data.py → Analysis → Insights
```

## Documentation Hierarchy

```
README.md (Main entry point)
├── QUICKSTART.md (Fast start)
├── Data/README.md (Base datasets)
├── Result/README.md (Pre-generated data)
├── Analysis/README.md (Code docs)
├── examples/README.md (Usage examples)
└── CONTRIBUTING.md (Developer guide)
```

## Typical Workflows

### Research Workflow
1. Clone repository
2. Navigate to `Result/{model}/`
3. Load pre-generated reasoning data
4. Use in experiments
5. Cite in paper

### Development Workflow
1. Clone repository
2. Install requirements
3. Configure model in Analysis script
4. Run generation
5. Verify results
6. Use custom data

### Exploration Workflow
1. Clone repository
2. Run `examples/load_and_explore_data.py`
3. Analyze error patterns
4. Generate insights
5. Create visualizations

## Important Files for Reviewers

### Core Implementation
- `Analysis/Inference_template_qwen_7b.py` - Main algorithm
- `examples/generate_reasoning_data.py` - Simplified version

### Datasets
- `Result/{any model}/` - Pre-generated reasoning data
- `Data/` - Base BIRD/SPIDER datasets

### Documentation
- `README.md` - Project overview
- `Result/README.md` - Dataset format and usage
- `Analysis/README.md` - Implementation details

## Version Control

### Tracked Files
- ✅ Source code (.py)
- ✅ Documentation (.md)
- ✅ Configuration (requirements.txt)
- ✅ Datasets (.json) - Currently tracked

### Ignored Files (.gitignore)
- ❌ Python cache (__pycache__)
- ❌ Virtual environments (venv/)
- ❌ IDE files (.vscode/, .idea/)
- ❌ Model checkpoints (.pt, .bin)
- ❌ Logs (*.log)

## Repository Statistics

- **Total Files:** ~200+ (including all datasets)
- **Total Size:** ~550MB
- **Languages:** Python, Markdown
- **Models Supported:** 10
- **Datasets:** 2 (BIRD, SPIDER)
- **Examples:** ~40,000+ reasoning samples

---

**Navigation Tips:**
- Start with README.md for overview
- Use QUICKSTART.md for immediate usage
- Check folder READMEs for specific details
- Run examples/ scripts to understand usage
