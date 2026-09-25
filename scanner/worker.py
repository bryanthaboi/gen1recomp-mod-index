import json
from pathlib import Path
import resource
import sys
from engine import Engine

if __name__ == '__main__':
    resource.setrlimit(resource.RLIMIT_AS, (1536 * 1024 * 1024,) * 2)
    resource.setrlimit(resource.RLIMIT_CPU, (610, 615))
    result = Engine().scan(Path(sys.argv[1]).read_bytes())
    Path(sys.argv[2]).write_text(json.dumps(result))
