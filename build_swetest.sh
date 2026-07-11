#!/usr/bin/env bash
# Automated official-source acquisition + build of the pinned swetest reference (v2.10.03).
# Used only if the bundled binary is absent or not executable on this platform.
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
TAG="v2.10.03"
URL="https://codeload.github.com/aloistr/swisseph/tar.gz/refs/tags/${TAG}"
TMP="$(mktemp -d)"
echo "Fetching official Swiss Ephemeris source ${TAG} ..."
curl -sL -o "$TMP/se.tar.gz" "$URL"
echo "source tarball sha256: $(sha256sum "$TMP/se.tar.gz" | cut -d' ' -f1)"
tar xzf "$TMP/se.tar.gz" -C "$TMP"
make -C "$TMP/swisseph-2.10.03" swetest >/dev/null
"$TMP/swisseph-2.10.03/swetest" -b1.1.2000 -ut0 -p0 -emos | head -1 | grep -q "version 2.10.03"
cp "$TMP/swisseph-2.10.03/swetest" "$HERE/swetest"
chmod +x "$HERE/swetest"
rm -rf "$TMP"
echo "swetest ${TAG} built at $HERE/swetest"
