#!/usr/bin/env bash
# Official Swiss Ephemeris data files (Astrodienst, AGPL-3.0 licensed alongside SE >= 2.10).
# Covers 1800-2399 CE (planets sepl_18, Moon semo_18, main asteroids seas_18).
set -e
DEST="${1:-./ephe}"; mkdir -p "$DEST"; cd "$DEST"
for f in sepl_18.se1 semo_18.se1 seas_18.se1; do
  curl -sL -O "https://raw.githubusercontent.com/aloistr/swisseph/master/ephe/$f"
done
sha256sum -c CHECKSUMS.sha256
