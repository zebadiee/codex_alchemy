import argparse
import subprocess

def ignite(args):
    print(f"\n🔥 Spiral Codex Hyperdrive Activated 🔥")
    print(f"▶ Mode:        {args.mode}")
    print(f"▶ Invocation:  {args.invoke}")
    print(f"▶ Ritual Pack: {args.ritual_pack}")
    print(f"▶ Mantra:      {args.mantra}")
    print(f"▶ Entropy Sync:{'✔️' if args.entropy_sync else '❌'}")
    print(f"▶ Signature:   {args.signature}")
    print("\n🚀 Spiral Codex is now live.\n")

def deploy(args):
    print("\n🚀 Codex Deployment Initiated")
    print(f"🧱 Mode: {args.mode}")
    print(f"🔧 Components: {args.components}")
    print(f"📡 Entropy Sources: {args.entropy_sources}")
    subprocess.run(["zsh", "./deploy.sh"])

parser = argparse.ArgumentParser(prog='spiral codex')
subparsers = parser.add_subparsers(dest='subcommand', required=True)

ignite_parser = subparsers.add_parser('ignite')
ignite_parser.add_argument('--mode', required=True)
ignite_parser.add_argument('--invoke', required=True)
ignite_parser.add_argument('--ritual-pack', required=True)
ignite_parser.add_argument('--mantra', required=True)
ignite_parser.add_argument('--entropy-sync', action='store_true')
ignite_parser.add_argument('--signature', required=True)
ignite_parser.set_defaults(func=ignite)

deploy_parser = subparsers.add_parser('deploy')
deploy_parser.add_argument('--mode', required=True)
deploy_parser.add_argument('--components', required=True)
deploy_parser.add_argument('--entropy-sources', required=True)
deploy_parser.set_defaults(func=deploy)

args = parser.parse_args()
args.func(args)
