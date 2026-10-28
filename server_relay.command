#!/bin/bash
# Relay: runs job scripts dropped into outputs/server_jobs/ on the GPU server (ssh beauty).
# Each <name>.sh runs once; output goes to <name>.log and <name>.done gets the exit code.
# Close this window to stop the relay.
cd "$(dirname "$0")"
J=outputs/server_jobs; mkdir -p "$J"
echo "relay started $(date); watching $J"
while true; do
  for job in "$J"/*.sh; do
    [ -e "$job" ] || continue
    base="${job%.sh}"; [ -e "$base.started" ] && continue
    date > "$base.started"
    case "$job" in
      *.local.sh) ( bash "$job" > "$base.log" 2>&1; echo $? > "$base.done" ) & ;;   # runs on the Mac (e.g. rsync to the server)
      *)          ( ssh -o BatchMode=yes -o ServerAliveInterval=30 beauty 'bash -s' < "$job" > "$base.log" 2>&1; echo $? > "$base.done" ) & ;;
    esac
    echo "$(date '+%H:%M:%S') started $(basename "$job")"
  done
  sleep 5
done
