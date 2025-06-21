#!/bin/bash

echo "🔍 Validating Terminal & Python Unicode Support..."

# 1. Terminal locale check
echo "➤ Checking locale..."
locale | grep -q 'UTF-8' || {
  echo "❌ Locale is not UTF-8. Fixing temporarily..."
  export LANG="en_US.UTF-8"
  export LC_ALL="en_US.UTF-8"
  echo '✅ Applied temporary fix: LANG & LC_ALL set to en_US.UTF-8'
  echo '💡 To make permanent, run:'
  echo 'echo \'export LANG="en_US.UTF-8"\' >> ~/.zprofile && echo \'export LC_ALL="en_US.UTF-8"\' >> ~/.zprofile'
}

# 2. Python unicode print test
echo "➤ Testing Python Unicode..."
if ! command -v python3 >/dev/null 2>&1; then
  echo "❌ Python 3 not found. Installing with Homebrew..."
  brew install python
fi

PYTHON_OUTPUT=$(python3 -c 'print("🧿 Unicode test passed ✅")' 2>&1)
if echo "$PYTHON_OUTPUT" | grep -q "Unicode test passed"; then
  echo "$PYTHON_OUTPUT"
else
  echo "❌ Python Unicode print failed. Applying fix..."
  export PYTHONIOENCODING="utf-8"
  echo 'export PYTHONIOENCODING="utf-8"' >> ~/.zprofile
  source ~/.zprofile
fi

# 3. Font check suggestion
echo "➤ Verifying terminal font..."
echo -e "🔤 Symbol test: \xF0\x9F\x94\x91 \xF0\x9F\x94\x93 \xF0\x9F\x94\x90 \xF0\x9F\x94\x92"
echo "💡 If any icons are boxes or garbled:"
echo "   Open Terminal → Settings → Profiles → Text"
echo "   Set font to: MesloLGS NF, Fira Code, or Hack"
echo "   Or install via:"
echo "   brew tap homebrew/cask-fonts && brew install --cask font-meslo-lg-nerd-font"

# Final verdict
echo "✅ Unicode environment validation complete."
