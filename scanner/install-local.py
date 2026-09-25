"""Install the review container and disposable runner supervisor on macOS.

Provide secrets beforehand in the private installation directory, never argv.
"""
import os
from pathlib import Path
import plistlib
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
BASE = Path.home() / 'Library/Application Support/gen1mod-review'
BASE.mkdir(parents=True, exist_ok=True)
os.chmod(BASE, 0o700)
for name in ['state/cache', 'logs', 'secrets']:
    (BASE / name).mkdir(parents=True, exist_ok=True)
if not (BASE / 'references').exists():
    raise SystemExit('Install the reference images in the private references directory first')
for name in ['github-token', 'pushcut-url']:
    if not (BASE / 'secrets' / name).exists():
        raise SystemExit('Missing local credential file: ' + name)
    os.chmod(BASE / 'secrets' / name, 0o600)

def run(args, **kwargs): return subprocess.run(args, check=True, **kwargs)

run(['docker', 'build', '-q', '-t', 'gen1mod-review:local', '-f', str(ROOT / 'Dockerfile'), str(ROOT.parent)])
run(['docker', 'build', '-q', '-t', 'gen1mod-runner:local', '-f', str(ROOT / 'Dockerfile.runner'), str(ROOT.parent)])
shutil.copy2(ROOT / 'runner-manager.py', BASE / 'runner-manager.py')
subprocess.run(['docker', 'rm', '-f', 'gen1mod-review'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
run(['docker', 'volume', 'create', 'gen1mod-review-db'], stdout=subprocess.DEVNULL)
# Keep SQLite locks on the Linux filesystem; macOS shared folders are for backups/cache.
run(['docker', 'run', '--rm', '--user', 'root', '-v', 'gen1mod-review-db:/database',
     '-v', str(BASE / 'state') + ':/previous:ro', 'gen1mod-review:local', 'sh', '-c',
     f'if [ ! -f /database/review.sqlite3 ] && [ -f /previous/review.sqlite3 ]; then cp /previous/review.sqlite3 /database/review.sqlite3; fi; chown -R {os.getuid()}:{os.getgid()} /database'])
run(['docker', 'run', '-d', '--name', 'gen1mod-review', '--restart', 'unless-stopped', '--init',
     '--user', f'{os.getuid()}:{os.getgid()}', '--cpus', '2', '--memory', '3g', '--pids-limit', '128',
     '--cap-drop', 'ALL', '--security-opt', 'no-new-privileges', '--read-only', '--tmpfs', '/tmp:size=1024m',
     '-p', '127.0.0.1:8849:8849', '-e', 'TZ=America/New_York', '-e', 'PYTHONDONTWRITEBYTECODE=1',
     '-e', 'REVIEW_DATABASE=/database/review.sqlite3', '-v', 'gen1mod-review-db:/database',
     '-e', 'GH_TOKEN_FILE=/run/secrets/github-token', '-e', 'PUSHCUT_WEBHOOK_URL_FILE=/run/secrets/pushcut-url',
     '-e', 'PUBLISH_QUARANTINE=1', '-v', str(BASE / 'state') + ':/state',
     '-v', str(BASE / 'references') + ':/references:ro', '-v', str(BASE / 'secrets') + ':/run/secrets:ro', 'gen1mod-review:local'])
label = 'org.gen1recomp.mod-review'
plist = Path.home() / 'Library/LaunchAgents' / (label + '.plist')
plist.parent.mkdir(parents=True, exist_ok=True)
plist.write_bytes(plistlib.dumps({'Label': label, 'ProgramArguments': [sys.executable, str(BASE / 'runner-manager.py')],
    'RunAtLoad': True, 'KeepAlive': True, 'ThrottleInterval': 15,
    'StandardOutPath': str(BASE / 'logs/supervisor.log'), 'StandardErrorPath': str(BASE / 'logs/supervisor-error.log')}))
# Existing supervisors pick up the rebuilt image for their next disposable runner.
# Restarting launchd here can kill an active job and leave its GitHub run stuck.
loaded = subprocess.run(['launchctl', 'print', f'gui/{os.getuid()}/{label}'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
if loaded.returncode:
    run(['launchctl', 'bootstrap', f'gui/{os.getuid()}', str(plist)])
print('Installed review service at http://localhost:8849 and disposable GitHub runner supervisor')
