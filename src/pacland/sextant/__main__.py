"""CLI: ``python -m pacland.sextant "<question>"`` -> simulate -> classify -> certificate."""
import json
import sys

from .engine import run


def main(argv=None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if not args:
        print('usage: python -m pacland.sextant "<question>"', file=sys.stderr)
        return 2
    result = run(" ".join(args))
    print(json.dumps(result, indent=2))
    return 1 if result.get("verdict") == "UNKNOWN" else 0


if __name__ == "__main__":
    sys.exit(main())
