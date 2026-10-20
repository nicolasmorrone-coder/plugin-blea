#!/bin/bash
set -Eeuo pipefail
BASE_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
PROGRESS_FILE=${1:-/tmp/dependancy_blea_in_progress}
VENV_DIR="$BASE_DIR/python_venv"
trap 'echo "BLEA dependency installation failed at line $LINENO" >&2' ERR
printf '0\n' >"$PROGRESS_FILE"
apt-get update
apt-get install -y python3 python3-dev python3-venv build-essential libglib2.0-dev \
    bluez rfkill python3-bluez python3-requests python3-serial python3-pyudev \
    python3-pil python3-numpy python3-cryptography
printf '40\n' >"$PROGRESS_FILE"
python3 -m venv --system-site-packages "$VENV_DIR"
"$VENV_DIR/bin/python3" -m pip install 'bluepy==1.3.0' pycryptodome
printf '85\n' >"$PROGRESS_FILE"
"$VENV_DIR/bin/python3" -c 'import bluepy.btle, bluetooth, requests, serial, pyudev, PIL, numpy, cryptography; from Crypto.Cipher import AES'
chown -R "$(stat -c '%u:%g' "$BASE_DIR/..")" "$VENV_DIR"
printf '100\n' >"$PROGRESS_FILE"
rm -f -- "$PROGRESS_FILE"
echo 'BLEA dependencies installed in an isolated Python environment'
