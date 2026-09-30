#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: bash install.sh TARGET_DIRECTORY [--force]

Install the survey-only Codex agent, project config, and skill into an existing
project. Refuses to overwrite any destination unless --force is supplied.
Restart Codex in that project after installation.
EOF
}

if [[ $# -lt 1 || $# -gt 2 || "$1" == "--help" || "$1" == "-h" ]]; then
  usage
  [[ $# -eq 1 && ( "$1" == "--help" || "$1" == "-h" ) ]] && exit 0
  exit 2
fi

target="$1"
force=0
if [[ $# -eq 2 ]]; then
  [[ "$2" == "--force" ]] || { usage >&2; exit 2; }
  force=1
fi
[[ -d "$target" ]] || { echo "target directory does not exist: $target" >&2; exit 1; }

source_root="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
target="$(cd "$target" && pwd)"

dest_config="$target/.codex/config.toml"
dest_agent="$target/.codex/agents/survey.toml"
dest_skill="$target/.agents/skills/reasflow-survey"
dest_manifest="$target/.reasflow-survey/manifest.txt"

for destination in "$dest_config" "$dest_agent" "$dest_skill"; do
  if [[ -e "$destination" || -L "$destination" ]]; then
    if [[ "$force" -ne 1 ]]; then
      echo "existing target: $destination" >&2
      echo "Nothing was installed. Use --force only when replacing these targets is intended." >&2
      exit 1
    fi
  fi
done

mkdir -p "$target/.codex/agents" "$target/.agents/skills" "$target/.reasflow-survey"
if [[ "$force" -eq 1 ]]; then
  rm -f "$dest_config" "$dest_agent"
  rm -rf "$dest_skill"
fi
cp "$source_root/codex-config.toml" "$dest_config"
cp "$source_root/agents/survey.toml" "$dest_agent"
cp -R "$source_root/skills/reasflow-survey" "$dest_skill"
cat > "$dest_manifest" <<EOF
SOURCE $source_root
FILE $dest_config
FILE $dest_agent
DIR $dest_skill
EOF

echo "Installed reasflow-survey into $target"
echo "Restart Codex in that project to load the new config, agent, and skill."
