#!/usr/bin/env bash
set -euo pipefail
root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
units="$HOME/.config/systemd/user"
mkdir -p "$units"
for name in biblical-graphite-wallpaper-rotation.service biblical-graphite-wallpaper-rotation.timer; do
  install -m 644 "$root/rotation/$name" "$units/$name"
done
omarchy hook install theme-set "$root/rotation/50-biblical-graphite-rotation"
systemctl --user daemon-reload
systemctl --user enable biblical-graphite-wallpaper-rotation.timer
bash "$root/rotation/50-biblical-graphite-rotation"
