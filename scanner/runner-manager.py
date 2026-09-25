"""LaunchAgent supervisor. Credentials stay in the host keychain, outside jobs."""
import json
import os
from pathlib import Path
import subprocess
import time
import uuid

BASE = Path(__file__).resolve().parent
ENV = {**os.environ, 'PATH': '/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin'}


def run(args, **kwargs):
    return subprocess.run(args, env=ENV, **kwargs)


while True:
    try:
        if run(['docker', 'info'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode:
            time.sleep(15); continue
        run(['docker', 'start', 'gen1mod-review'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        reply = run(['gh', 'api', '--method', 'POST', 'repos/bryanthaboi/gen1recomp-mod-index/actions/runners/registration-token'],
                    capture_output=True, check=True)
        token = json.loads(reply.stdout)['token']
        name = 'mod-scan-' + uuid.uuid4().hex[:10]
        # No home mount, socket, write credentials, or persistent job workspace.
        run(['docker', 'run', '--rm', '--init', '-i', '--name', name, '--cpus', '2', '--memory', '3g', '--pids-limit', '256',
             '--cap-drop', 'ALL', '--security-opt', 'no-new-privileges',
             '-e', f'RUNNER_NAME={name}', '-e', 'REFERENCE_IMAGES=/references',
             '-v', str(BASE / 'references') + ':/references:ro',
             '-v', str(BASE / 'state' / 'cache') + ':/scan-cache:ro', 'gen1mod-runner:local'],
            input=(token + '\n').encode(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        # Remove a registration if the container stopped before processing its one job.
        listing = run(['gh', 'api', 'repos/bryanthaboi/gen1recomp-mod-index/actions/runners'], capture_output=True, check=True)
        for runner in json.loads(listing.stdout).get('runners', []):
            if runner['name'] == name and not runner['busy']:
                run(['gh', 'api', '--method', 'DELETE', f"repos/bryanthaboi/gen1recomp-mod-index/actions/runners/{runner['id']}"],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        # Never log subprocess output, arguments, tokens, or host paths.
        print('Runner unavailable; retrying in 15 seconds', flush=True)
    time.sleep(15)
