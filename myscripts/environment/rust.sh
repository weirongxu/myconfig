#!/usr/bin/env bash
try-source "$HOME/.cargo/env"
RUST_BIN=$HOME/.cargo/bin
if ! has-path "$RUST_BIN"; then
  add-path "$HOME/.cargo/bin"
fi
