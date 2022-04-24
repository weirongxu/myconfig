#!/usr/bin/env bash
local cargo_env_path=$HOME/.cargo/env
if [[ -f $cargo_env_path ]]; then
  try-source "$HOME/.cargo/env"
else
  add-path "$HOME/.cargo/bin"
fi

local src_paths=(
  /usr/local/share/rust/rust_src
)
if exists-cmd rustc; then
  src_paths+=("$(rustc --print sysroot)/lib/rustlib/src/rust/src")
fi
for _path in ${src_paths[@]}; do
  if [[ -d $_path ]]; then
    export RUST_SRC_PATH=$_path
    break
  fi
done
