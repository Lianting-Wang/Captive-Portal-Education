#!/bin/bash

# Function to copy source files to the destination directory
function copy_files() {
    local source_file="$1"
    local tcp_source_file="$2"
    local destination_directory="$3"

    echo "Copying $source_file to $destination_directory"
    cp "$source_file" "$destination_directory"

    echo "Copying $tcp_source_file to $destination_directory"
    cp "$tcp_source_file" "$destination_directory"
}

# Cleanup function to stop the POX process when interrupted
function cleanup() {
    echo "Interrupt signal received, stopping POX process..."
    sudo pkill -f pox.py  # Stop POX process
    echo "POX process stopped."
    exit 0
}

# Catch SIGINT (Ctrl+C) signal and call cleanup
trap cleanup SIGINT

# Handle command-line argument to select the source files
pox_source_file='/home/mininet/Captive-Portal/start_code/switch.py'
pox_tcp_source_file='/home/mininet/Captive-Portal/start_code/tcp_client.py'
SCRIPT_COMMAND=switch
if [ "$1" == "answer" ]; then
    pox_source_file='/home/mininet/Captive-Portal/pox_answer/condition_switch_answer.pyc'
    pox_tcp_source_file='/home/mininet/Captive-Portal/pox_answer/tcp_client_answer.pyc'
    SCRIPT_COMMAND=condition_switch_answer
fi

destination_directory='/home/mininet/pox/ext'

# Call the function to copy files
copy_files "$pox_source_file" "$pox_tcp_source_file" "$destination_directory"

# Run the POX command
echo "Running POX: sudo /home/mininet/pox/pox.py $SCRIPT_COMMAND"
sudo /home/mininet/pox/pox.py "$SCRIPT_COMMAND"

# Keep the script running and waiting for interruptions
wait
