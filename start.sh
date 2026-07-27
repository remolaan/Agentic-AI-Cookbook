#!/usr/bin/env bash
set -e

PORT="${1:-8090}"

echo "=== Starting Gradio on port $PORT ==="

# Open firewall
echo "lanpass@123" | sudo -S firewall-cmd --add-port="$PORT"/tcp --permanent
echo "lanpass@123" | sudo -S firewall-cmd --reload

# Start app detached (survives shell exit)
cd "$(dirname "$0")"
setsid .venv/bin/python 01_hello_llm/main_gr.py "$PORT" &>/tmp/gradio.log &

PID=$!
echo "Started PID=$PID"
echo "Open http://124.43.162.57:$PORT"
