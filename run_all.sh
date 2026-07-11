#!/usr/bin/env bash
# ONE-COMMAND TIER-0 CERTIFICATION - fully package-relative
set -e
cd "$(dirname "$0")"
rm -f reports/tier0_certification.json reports/swetest_raw_outputs.json reports/regression_report.json reports/pytest_results.xml
echo "[1/5] preflight: environment + ephemeris checksum validation"
python3 preflight.py
echo "[2/5] certification calculations: swetest reference + strict-SWIEPH engine + arcsec comparison + KP holdout regression + anti-fitting scan"
python3 certify_tier0.py
echo "[3/5] Brihat categorical regression (comparison fixtures, freshly recomputed)"
python3 compare.py > reports/brihat_regression_console.txt
echo "[4/5] full automated test suite (skips are failures)"
python3 -m pytest tests -q --junitxml=reports/pytest_results.xml
echo "[5/5] final result block + human-readable report (single source of truth)"
python3 finalize_report.py
