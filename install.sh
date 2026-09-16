#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)

if [ "$#" -gt 1 ]; then
  printf '%s\n' "Usage: $0 [codex-root]" >&2
  exit 2
fi

if [ "$#" -eq 1 ]; then
  codex_root=$1
elif [ -n "${CODEX_HOME:-}" ]; then
  codex_root=$CODEX_HOME
else
  codex_root=$HOME/.codex
fi

pet_dir=$codex_root/pets/sanhao-tu
mkdir -p "$pet_dir"
cp "$script_dir/pet.json" "$pet_dir/pet.json"
cp "$script_dir/spritesheet.webp" "$pet_dir/spritesheet.webp"

printf '%s\n' "三好兔已经安装到：$pet_dir"
printf '%s\n' "重新启动 Codex，或在宠物选择器中重新选择三好兔。"
