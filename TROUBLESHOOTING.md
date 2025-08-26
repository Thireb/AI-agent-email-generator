# Troubleshooting Guide

## Common Issues and Solutions

### 1. OpenAI API Key Error

**Error:** `litellm.AuthenticationError: OpenAIException - The api_key client option must be set`

**Cause:** CrewAI is trying to use OpenAI instead of Ollama due to configuration conflicts.

**Solutions:**

1. **Check Environment Variables:**
   ```bash
   python check_env.py
   ```

2. **Unset OpenAI Environment Variables:**
   ```bash
   unset OPENAI_API_KEY
   unset OPENAI_API_BASE
   unset LITELLM_API_KEY
   ```

3. **Restart Terminal Session:**
   After unsetting variables, restart your terminal or run:
   ```bash
   source ~/.bashrc  # or ~/.zshrc for zsh
   ```

### 2. Ollama Connection Issues

**Error:** `Cannot connect to Ollama`

**Solutions:**

1. **Start Ollama Service:**
   ```bash
   ollama serve
   ```

2. **Check Ollama Status:**
   ```bash
   ollama list
   ```

3. **Test Connection:**
   ```bash
   python test_ollama_connection.py
   ```

### 3. Model Not Available

**Error:** `deepseek-r1:1.5b model not found`

**Solutions:**

1. **Pull the Required Model:**
   ```bash
   ollama pull deepseek-r1:1.5b
   ```

2. **Use Alternative Model:**
   Edit `config/ollama_config.py` and change the default model:
   ```python
   def get_ollama_llm(model_name: str = "gemma3:1b"):  # Change this line
   ```

3. **Check Available Models:**
   ```bash
   ollama list
   ```

### 3.1. Model Format Error

**Error:** `LLM Provider NOT provided. Pass in the LLM provider you are trying to call. You passed model=deepseek-r1:1.5b`

**Cause:** CrewAI expects Ollama models to be prefixed with `ollama/` when using the LangChain integration.

**Solutions:**

1. **Use Correct Model Format:**
   ```python
   # ❌ Wrong format
   model="deepseek-r1:1.5b"
   
   # ✅ Correct format
   model="ollama/deepseek-r1:1.5b"
   ```

2. **Update Configuration Files:**
   - `jd_agent.py`
   - `config/ollama_config.py`
   - `test_ollama_connection.py`

3. **Verify Model Names:**
   ```python
   AVAILABLE_MODELS = [
       "ollama/deepseek-r1:1.5b",
       "ollama/gemma3:1b",
       "ollama/llama3.2:3b"
   ]
   ```

### 4. CrewAI Configuration Issues

**Error:** `Failed to create agents` or `Failed to create crew`

**Solutions:**

1. **Verify Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Check CrewAI Version:**
   ```bash
   pip show crewai
   ```

3. **Test Basic Setup:**
   ```bash
   python -c "from crewai import Agent; print('CrewAI import successful')"
   ```

### 5. Permission Issues

**Error:** `Permission denied` or `Access denied`

**Solutions:**

1. **Check File Permissions:**
   ```bash
   ls -la *.py
   chmod +x *.py  # Make scripts executable
   ```

2. **Check Ollama Permissions:**
   ```bash
   sudo systemctl status ollama
   ```

## Testing Your Setup

### Step 1: Environment Check
```bash
python check_env.py
```

### Step 2: Ollama Connection Test
```bash
python test_ollama_connection.py
```

### Step 3: Full Agent Test
```bash
python run_agent.py --test
```

### Step 4: Run Main Agent
```bash
python run_agent.py
```

## Environment Variables to Check

### Potentially Problematic Variables:
- `OPENAI_API_KEY` - Should be unset for Ollama usage
- `OPENAI_API_BASE` - Should be unset for Ollama usage
- `LITELLM_API_KEY` - Should be unset for Ollama usage
- `CREWAI_LLM` - Should not be set to OpenAI

### Helpful Variables:
- `OLLAMA_HOST` - Can be set to custom Ollama host
- `OLLAMA_ORIGINS` - For CORS configuration if needed

## Getting Help

If you're still experiencing issues:

1. **Check the logs:** Look for specific error messages
2. **Verify Ollama:** Ensure Ollama is running and accessible
3. **Test step by step:** Use the test scripts to isolate the problem
4. **Check versions:** Ensure all packages are compatible

## Common Commands

```bash
# Start Ollama
ollama serve

# Check models
ollama list

# Pull model
ollama pull deepseek-r1:1.5b

# Test connection
curl http://localhost:11434/api/tags

# Check environment
python check_env.py

# Test setup
python test_ollama_connection.py

# Run with tests
python run_agent.py --test
```
