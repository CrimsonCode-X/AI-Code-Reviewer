#!/bin/bash
echo "Starting public tunnel to localhost:5000..."
echo "Your secure link will appear below (look for the pinggy-free.link URL):"
ssh -o StrictHostKeyChecking=no -p 443 -R80:localhost:5000 a.pinggy.io
