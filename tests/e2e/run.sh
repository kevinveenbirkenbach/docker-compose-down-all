#!/bin/sh
set -eu

fail() {
    echo "FAIL: $1" >&2
    exit 1
}

DOCODOL="$(command -v docodol)" || fail "docodol is not on PATH after install"
echo "ok: docodol installed at ${DOCODOL}"

case "${DOCODOL}" in
    /usr/local/bin/*) ;;
    *) fail "docodol resolved to ${DOCODOL}, outside the install prefix" ;;
esac
echo "ok: resolved from the installed package, not the source tree"

docodol --help | grep -q "docker compose down" || fail "--help does not describe the tool"
echo "ok: --help"

mkdir -p /tmp/stacks/alpha /tmp/stacks/beta

output="$(docodol /tmp/stacks --dry-run)"
echo "${output}" | grep -q "DRY RUN: docker compose down" || fail "dry-run marker missing"
echo "${output}" | grep -q "/tmp/stacks/alpha" || fail "alpha was not visited"
echo "${output}" | grep -q "/tmp/stacks/beta" || fail "beta was not visited"
echo "ok: --dry-run visits every first-level subdirectory"

set +e
docodol /nonexistent >/dev/null 2>&1
status=$?
set -e
[ "${status}" -eq 1 ] || fail "missing base directory exited ${status}, expected 1"
echo "ok: missing base directory exits 1"

set +e
output="$(docodol /tmp/stacks 2>&1)"
status=$?
set -e
[ "${status}" -eq 0 ] || fail "a failing compose down changed the exit code to ${status}"
echo "${output}" | grep -q "failed in /tmp/stacks/alpha" || fail "compose failure was not reported"
echo "ok: real docker CLI fails without a daemon, is reported, exit code stays 0"

set +e
output="$(env PATH=/nonexistent-bin "${DOCODOL}" /tmp/stacks 2>&1)"
status=$?
set -e
[ "${status}" -eq 127 ] || fail "missing docker exited ${status}, expected 127"
echo "${output}" | grep -q "required command 'docker' is not installed" || fail "missing docker message wrong"
if echo "${output}" | grep -q "Traceback"; then
    fail "missing docker produced a traceback"
fi
echo "ok: missing docker exits 127 with a clean message"

echo "ALL E2E CHECKS PASSED"
