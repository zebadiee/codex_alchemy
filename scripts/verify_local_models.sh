#!/bin/bash

# scripts/verify_local_models.sh
#
# This script checks the health of the local AI model server (Ollama)
# and verifies that the required models from the Continue configuration
# are installed and available.

# --- Configuration ---
OLLAMA_HOST="http://localhost:11434"
CONFIG_FILE=".continue/config.json"
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# --- Helper Functions ---
function print_status() {
    echo -e "▶ $1"
}

function print_success() {
    echo -e "${GREEN}✔ $1${NC}"
}

function print_error() {
    echo -e "${RED}✖ $1${NC}"
}

function print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# --- Pre-flight Checks ---
print_status "Checking for dependencies..."
if ! command -v curl &> /dev/null; then
    print_error "Dependency 'curl' not found. Please install it."
    exit 1
fi
if ! command -v jq &> /dev/null; then
    print_error "Dependency 'jq' not found. Please install it."
    exit 1
fi
print_success "All dependencies are installed."

# --- Main Logic ---

# 1. Check if config file exists
if [ ! -f "$CONFIG_FILE" ]; then
    print_error "Configuration file not found at '$CONFIG_FILE'"
    exit 1
fi

# 2. Check Ollama Server Status
print_status "Checking Ollama server status at $OLLAMA_HOST..."
if ! curl -s --fail "${OLLAMA_HOST}" > /dev/null; then
    print_error "Ollama server is not reachable at $OLLAMA_HOST."
    print_warning "Please ensure Ollama is running. You can start it with 'ollama serve'."
    exit 1
fi
print_success "Ollama server is running."

# 3. Get Required Local Models from Config
print_status "Parsing required local models from '$CONFIG_FILE'..."
# This query finds any model where the apiBase contains 'localhost' or '127.0.0.1'
REQUIRED_MODELS=$(jq -r '.models[] | select(.apiBase and (.apiBase | test("localhost|127.0.0.1"))) | .model' "$CONFIG_FILE")

if [ -z "$REQUIRED_MODELS" ]; then
    print_warning "No local models found in the configuration file."
    exit 0
fi

echo "Required models:"
echo "$REQUIRED_MODELS"
echo ""

# 4. Get Installed Models from Ollama
print_status "Fetching installed models from Ollama..."
INSTALLED_MODELS_JSON=$(curl -s "${OLLAMA_HOST}/api/tags")
if [ $? -ne 0 ]; then
    print_error "Failed to fetch installed models from Ollama."
    exit 1
fi
INSTALLED_MODELS=$(echo "$INSTALLED_MODELS_JSON" | jq -r '.models[].name')
print_success "Successfully fetched installed models."

# 5. Compare and Report Status
print_status "Verifying model availability..."
ALL_FOUND=true
for model in $REQUIRED_MODELS; do
    # Ollama models often have a version tag like ':latest'. The config might not.
    # We'll check if the model name is a substring of any installed model.
    # E.g., 'qwen2.5-3b-instruct' should match 'qwen2.5-3b-instruct:latest'
    if echo "$INSTALLED_MODELS" | grep -q "^${model}"; then
        print_success "Model '$model' is installed."
    else
        print_error "Model '$model' is NOT installed."
        ALL_FOUND=false
    fi
done

echo ""

# --- Final Status ---
if [ "$ALL_FOUND" = true ]; then
    print_success "All required local models are installed and ready!"
    exit 0
else
    print_error "Some required local models are missing."
    print_warning "Please install the missing models using 'ollama pull <model_name>'."
    exit 1
fi
