import argparse
from agent.rituals.compress_and_teach import compress_and_teach

parser = argparse.ArgumentParser(description="Compress and patternize text for symbolic training.")
parser.add_argument("text", type=str, help="Text to compress and patternize")
parser.add_argument("--label", type=str, default="manual-teach", help="Optional training label")
args = parser.parse_args()

result = compress_and_teach(args.text, label=args.label)

print("\n📚 Training Result:")
print(result)

