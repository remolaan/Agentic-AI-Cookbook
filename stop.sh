#!/usr/bin/env bash
set -e

PORT="${1:-8090}"

echo "=== Stopping Gradio on port $PORT ==="

# Kill all python processes running main_gr.py
PIDS=$(pgrep -f "main_gr.py" 2>/dev/null || true)
if [ -n "$PIDS" ]; then
    echo "Killing PIDs: $PIDS"
    kill -9 $PIDS 2>/dev/null || true
    echo "Gradio stopped."
else
    echo "No Gradio process found."
fi

# Close firewall port
echo "lanpass@123" | sudo -S firewall-cmd --remove-port="$PORT"/tcp --permanent
echo "lanpass@123" | sudo -S firewall-cmd --reload
echo "Port $PORT closed."

# Verify
sleep 1
if ss -tlnp 2>/dev/null | grep -q ":$PORT "; then
    echo "WARNING: Port $PORT is still in use!"
else
    echo "Port $PORT is free."
fi
