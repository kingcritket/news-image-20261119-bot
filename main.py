"""news-image-20261119 entry: copy the bundled image to the output directory.

Standard library only, no network. Deterministic: the output bytes are
exactly the bytes of entry.png shipped beside this script. The image was
built by build_entry.py from three AI-generated scene photos (assets/)
with all text drawn by PIL in Liberation Sans.
"""

import os
import shutil
import sys


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    if not os.path.isfile(source):
        print("entry.png not found beside main.py", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(source, os.path.join(out_dir, "entry.png"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
