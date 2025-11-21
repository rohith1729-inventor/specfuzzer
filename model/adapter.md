# SpecFuzzer LoRA Adapter

1. Upload your fine-tuned adapter to Hugging Face (e.g., `bhavanagoud111/SpecFuzzer`) or mount the weights locally.
2. Set the following environment variables before starting the backend:

```bash
export BASE_MODEL_ID="meta-llama/Llama-2-7b-hf"
export ADAPTER_MODEL_ID="bhavanagoud111/SpecFuzzer"
# or point directly to a local folder
export ADAPTER_MODEL_PATH="/models/specfuzzer-lora"
export HF_TOKEN="hf_xxx"  # if the repo is private
```

3. When the adapter is not available, the backend automatically attempts to use the OpenAI fallback. Provide your key and preferred model:

```bash
export OPENAI_API_KEY="sk-..."
export OPENAI_MODEL="gpt-4.1-mini"  # or gpt-o-mini
```

4. The FastAPI server always enforces:

> If I cannot upload the fine-tuned adapter, automatically use OpenAI API key for reasoning.
