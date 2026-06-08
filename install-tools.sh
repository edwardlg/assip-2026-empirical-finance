#!/usr/bin/env bash
# One-shot installer for: jq, fd, fzf, tree, unzip, gh, go, rust, aws, gcloud
# Safe to re-run: idempotent for PATH edits; apt/installers no-op if already up to date.

set -euo pipefail

log() { printf "\n\033[1;36m=== %s ===\033[0m\n" "$*"; }

log "Stage 1/6: apt essentials (jq, fd, fzf, tree, unzip)"
sudo apt-get update
sudo apt-get install -y jq fd-find fzf tree unzip wget ca-certificates
mkdir -p "$HOME/.local/bin"
ln -sf "$(command -v fdfind)" "$HOME/.local/bin/fd"

log "Stage 2/6: GitHub CLI (gh)"
sudo mkdir -p -m 755 /etc/apt/keyrings
wget -qO- https://cli.github.com/packages/githubcli-archive-keyring.gpg \
  | sudo tee /etc/apt/keyrings/githubcli-archive-keyring.gpg > /dev/null
sudo chmod go+r /etc/apt/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" \
  | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt-get update
sudo apt-get install -y gh

log "Stage 3/6: Go (1.23.4)"
curl -fsSL https://go.dev/dl/go1.23.4.linux-amd64.tar.gz -o /tmp/go.tgz
sudo rm -rf /usr/local/go
sudo tar -C /usr/local -xzf /tmp/go.tgz
rm /tmp/go.tgz

log "Stage 4/6: Rust (rustup, default toolchain)"
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --no-modify-path

log "Stage 5/6: AWS CLI v2"
curl -fsSL https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip -o /tmp/awscliv2.zip
unzip -q /tmp/awscliv2.zip -d /tmp
if command -v aws >/dev/null 2>&1; then
  sudo /tmp/aws/install --update
else
  sudo /tmp/aws/install
fi
rm -rf /tmp/aws /tmp/awscliv2.zip

log "Stage 6/6: Google Cloud SDK (gcloud)"
CLOUDSDK_CORE_DISABLE_PROMPTS=1 curl -fsSL https://sdk.cloud.google.com | bash > /tmp/gcloud-install.log 2>&1 || {
  echo "gcloud install failed — see /tmp/gcloud-install.log"; tail -30 /tmp/gcloud-install.log; exit 1;
}

log "Updating ~/.bashrc PATH entries (idempotent)"
add_line() {
  local line="$1"
  grep -qxF "$line" "$HOME/.bashrc" 2>/dev/null || echo "$line" >> "$HOME/.bashrc"
}
add_line 'export PATH="$PATH:/usr/local/go/bin"'
add_line 'export PATH="$HOME/.local/bin:$PATH"'
add_line '[ -f "$HOME/.cargo/env" ] && . "$HOME/.cargo/env"'
add_line '[ -f "$HOME/google-cloud-sdk/path.bash.inc" ] && . "$HOME/google-cloud-sdk/path.bash.inc"'
add_line '[ -f "$HOME/google-cloud-sdk/completion.bash.inc" ] && . "$HOME/google-cloud-sdk/completion.bash.inc"'

log "ALL DONE — open a new shell (or run: source ~/.bashrc) to pick up new PATH"
echo "Then verify with: jq --version; fd --version; fzf --version; gh --version; go version; cargo --version; aws --version; gcloud --version"
