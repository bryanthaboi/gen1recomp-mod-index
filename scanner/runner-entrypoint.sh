#!/bin/bash
set -euo pipefail
# Only a short-lived registration token enters this disposable container.
read -r registration_token
./config.sh --unattended --ephemeral --url https://github.com/bryanthaboi/gen1recomp-mod-index \
  --token "$registration_token" --name "${RUNNER_NAME}" --labels mod-scan --work /workspace
unset registration_token
exec ./run.sh
