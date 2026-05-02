#!/bin/bash

echo "================================="
echo " SMART PARKING SYSTEM SERVER "
echo "================================="

echo ""
echo "Starting Flask server..."
echo ""

# activate virtual environment

source venv/bin/activate

# get local IP address

IP=$(ipconfig getifaddr en0)

echo "---------------------------------"
echo "Open on your phone:"
echo ""
echo "http://$IP:5001"
echo "---------------------------------"

echo ""

# run flask app

python app.py