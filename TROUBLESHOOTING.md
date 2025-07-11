# 🔧 Troubleshooting Guide - Basic Output Issues

## 🚨 Problem: Getting Basic "Welcome" Pages Instead of Comprehensive Applications

If you're getting simple basic outputs like blank pages with just "Welcome" instead of the comprehensive applications the system is designed to create, this guide will help you fix the issue.

## 🔍 Quick Diagnosis

First, run the diagnostic tool to identify the root cause:

```bash
python diagnose_issues.py
```

This will check:
- ✅ Ollama service status
- ✅ Model availability and functionality
- ✅ System resources
- ✅ Python environment
- ✅ Project structure
- ✅ Model response quality

## 🛠️ Quick Fix

For immediate fixes, run the automated repair tool:

```bash
python quick_fix.py
```

This will automatically:
- 🔧 Restart Ollama service
- 📦 Re-pull AI models
- 🐍 Fix Python dependencies
- 🔐 Fix file permissions
- ⚡ Optimize Ollama settings
- 🧪 Test model responses

## 🎯 Root Causes & Solutions

### 1. **AI Model Response Failures**

**Symptoms:**
- Models generate very short responses
- Timeout errors during generation
- Empty or incomplete responses

**Solutions:**
```bash
# Restart Ollama service
pkill ollama
ollama serve &

# Re-pull models with better settings
ollama pull llama2:7b-chat
ollama pull deepseek-coder:33b

# Test model responses
curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama2:7b-chat",
    "prompt": "Create a simple technical specification",
    "options": {"temperature": 0.3, "num_ctx": 2000}
  }'
```

### 2. **Token Limit Issues**

**Symptoms:**
- Generation stops mid-response
- Incomplete file structures
- Timeout errors

**Solutions:**
- Reduced `max_tokens` from 16000 to 8000 in `utils/ollama_client.py`
- Added chunked generation for large prompts
- Implemented multiple retry attempts with different settings

### 3. **Fallback to Basic Templates**

**Symptoms:**
- Only basic Next.js structure created
- Missing comprehensive features
- Simple "Welcome" pages

**Solutions:**
- Enhanced fallback templates with more features
- Multiple parsing strategies for AI responses
- Better error handling and retry logic

### 4. **System Resource Issues**

**Symptoms:**
- Slow generation
- Memory errors
- Process crashes

**Solutions:**
```bash
# Check system resources
free -h
df -h
nvidia-smi  # If using GPU

# Optimize Ollama settings
export OLLAMA_MAX_LOADED_MODELS=2
export OLLAMA_NUM_PARALLEL=4
export OLLAMA_MAX_QUEUE=512
```

### 5. **Model Quality Issues**

**Symptoms:**
- Models not following output format
- Inconsistent responses
- Poor code quality

**Solutions:**
- Improved prompts with explicit format requirements
- Better temperature and parameter settings
- Enhanced parsing strategies

## 🔧 Manual Fixes

### Fix 1: Restart Everything

```bash
# Stop all processes
pkill -f ollama
pkill -f python

# Clear any cached data
rm -rf ~/.ollama/models/*/tmp

# Restart Ollama
ollama serve &

# Wait for service to start
sleep 10

# Test connection
curl http://localhost:11434/api/tags
```

### Fix 2: Reinstall Models

```bash
# Remove existing models
ollama rm llama2:7b-chat
ollama rm deepseek-coder:33b

# Pull fresh models
ollama pull llama2:7b-chat
ollama pull deepseek-coder:33b

# Verify models
ollama list
```

### Fix 3: Update Python Environment

```bash
# Upgrade pip
pip install --upgrade pip

# Reinstall dependencies
pip uninstall -r requirements.txt -y
pip install -r requirements.txt

# Verify installation
python -c "import requests, rich, click; print('Dependencies OK')"
```

### Fix 4: Check Project Structure

```bash
# Verify all files are present
ls -la
ls -la agents/
ls -la prompts/
ls -la utils/

# Check file permissions
chmod +x main.py
chmod +x setup.sh
chmod +x diagnose_issues.py
chmod +x quick_fix.py
```

### Fix 5: Test Individual Components

```bash
# Test Ollama client
python -c "
from utils.ollama_client import OllamaClient
client = OllamaClient()
print('Ollama client:', client.is_model_available('llama2:7b-chat'))
"

# Test planner agent
python -c "
from agents.planner import PlannerAgent
from utils.ollama_client import OllamaClient
client = OllamaClient()
planner = PlannerAgent(client)
print('Planner agent loaded successfully')
"

# Test builder agent
python -c "
from agents.builder import BuilderAgent
from utils.ollama_client import OllamaClient
client = OllamaClient()
builder = BuilderAgent(client)
print('Builder agent loaded successfully')
"
```

## 🧪 Testing Your Fix

After applying fixes, test the system:

```bash
# Run diagnostic again
python diagnose_issues.py

# Test with sample project
python main.py --spec-file data/sample_project_spec.json

# Check generated output
ls -la output/
cd output/*/
npm install
npm run dev
```

## 📊 Expected vs Actual Output

### ✅ **Expected Output (Working System):**
```
output/your-project/
├── app/
│   ├── layout.tsx          # Complete layout with navigation
│   ├── page.tsx           # Rich homepage with features
│   ├── dashboard/         # Dashboard pages
│   ├── auth/             # Authentication pages
│   └── api/              # API routes
├── components/
│   ├── ui/               # Reusable UI components
│   ├── forms/            # Form components
│   └── layout/           # Layout components
├── lib/
│   ├── db.ts            # Database configuration
│   ├── auth.ts          # Authentication setup
│   └── utils.ts         # Utility functions
├── prisma/
│   └── schema.prisma    # Database schema
├── docs/                # Documentation
├── package.json         # Complete dependencies
└── README.md           # Comprehensive documentation
```

### ❌ **Actual Output (Broken System):**
```
output/your-project/
├── app/
│   ├── layout.tsx          # Basic layout
│   ├── page.tsx           # Simple "Welcome" page
│   └── globals.css        # Basic styles
├── package.json           # Minimal dependencies
└── README.md             # Basic documentation
```

## 🚀 Advanced Troubleshooting

### GPU Issues (if using GPU acceleration)

```bash
# Check GPU status
nvidia-smi

# Set GPU memory limits
export PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512

# Use CPU-only if GPU issues persist
export CUDA_VISIBLE_DEVICES=""
```

### Network Issues

```bash
# Check internet connection
ping google.com

# Test Ollama registry access
curl -I https://ollama.ai

# Use proxy if needed
export HTTP_PROXY=http://your-proxy:port
export HTTPS_PROXY=http://your-proxy:port
```

### Memory Issues

```bash
# Check available memory
free -h

# Increase swap if needed
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# Monitor memory usage
htop
```

## 📞 Getting Help

If you're still experiencing issues:

1. **Run the diagnostic tool** and share the output
2. **Check the logs** for specific error messages
3. **Verify your system meets requirements**:
   - RAM: 8GB+ (16GB+ recommended)
   - Storage: 20GB+ free space
   - Python: 3.8+
   - Node.js: 18+ (for generated apps)

4. **Common Error Messages:**
   - `Connection refused`: Ollama not running
   - `Model not found`: Models not downloaded
   - `Timeout`: Increase timeout settings
   - `Out of memory`: Reduce model context or add RAM

## 🎯 Success Checklist

After applying fixes, verify:

- [ ] `python diagnose_issues.py` shows no issues
- [ ] Models generate responses > 100 characters
- [ ] Generated projects have > 10 files
- [ ] Projects include authentication, database, and API routes
- [ ] Projects can be built and run with `npm run dev`

## 💡 Pro Tips

1. **Use RunPod** for consistent GPU performance
2. **Monitor system resources** during generation
3. **Start with simple projects** to test the system
4. **Keep models updated** with `ollama pull`
5. **Use the enhanced fallback** if AI generation fails

## 🔄 Recovery Steps

If everything fails:

```bash
# Complete reset
rm -rf output/
rm -rf data/
pkill -f ollama
ollama serve &
sleep 10
ollama pull llama2:7b-chat
ollama pull deepseek-coder:33b
python quick_fix.py
python main.py
```

This should resolve the basic output issue and get you comprehensive, production-ready applications! 