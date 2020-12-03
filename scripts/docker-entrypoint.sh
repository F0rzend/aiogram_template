#!/bin/sh

set -e

if [ -n "${RUN_MIGRATIONS}" ]; then
  aerich upgrade
fi

exec python -O -m app