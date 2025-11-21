

#!/bin/bash

# Load API keys from env.yaml
if [ ! -f "env.yaml" ]; then
    echo "Error: env.yaml not found!"
    exit 1
fi

# Parse YAML and export environment variables
export OPENAI_API_KEY=$(grep "OPENAI_API_KEY:" env.yaml | sed 's/.*: *"\(.*\)"/\1/')
export ANTHROPIC_API_KEY=$(grep "ANTHROPIC_API_KEY:" env.yaml | sed 's/.*: *"\(.*\)"/\1/')
export GEMINI_API_KEY=$(grep "GEMINI_API_KEY:" env.yaml | sed 's/.*: *"\(.*\)"/\1/')

echo "Loaded API keys from env.yaml"

# Uncomment the script you want to run:

# OpenAI
python generate_openai.py

# Claude
# python generate_claude.py

# Gemini
# python generate_gemini.py

