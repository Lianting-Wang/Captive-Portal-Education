#!/bin/bash

# Read the IP and port from config.ini for TCP server
function get_port_info() {
    TCP_SERVER_PORT=$(grep "TCP_server_port" config.ini | cut -d'=' -f2 | tr -d ' ')
}

# Function to copy source files to the destination directory for POX
function copy_files() {
    local source_file="$1"
    local tcp_source_file="$2"
    local destination_directory="$3"

    echo "Copying $source_file to $destination_directory"
    cp "$source_file" "$destination_directory"

    echo "Copying $tcp_source_file to $destination_directory"
    cp "$tcp_source_file" "$destination_directory"
}

function initialization() {
    get_port_info
    sudo pkill -f pox.py > /dev/null 2>&1  # Stop POX process
    sudo fuser -k "$TCP_SERVER_PORT/tcp" > /dev/null 2>&1  # Kill processes using the TCP port
}

initialization

# Cleanup function to stop all processes when interrupted
function cleanup() {
    echo "Interrupt signal received, stopping processes..."
    initialization
    sleep 1  # Ensure there is enough time to kill the process
    sudo kill $python_mn_pid > /dev/null 2>&1  # Stop the test Python process
    echo "Mininet cleanup..."
    sudo mn -c > /dev/null 2>&1
    echo "All processes have been stopped, and Mininet cleanup is successful."
    exit 0
}

# Catch SIGINT (Ctrl+C) signal and call cleanup function
trap cleanup SIGINT

# Function to handle module selection
select_mod() {
  echo "Please select the modules to be tested:"
  echo "1) Test TCP server"
  echo "2) Test POX"
  echo "3) Test DNS server"
  echo "4) Test Web server"
  echo -e "You can select multiple options by entering their numbers separated by spaces (e.g., '1 2 4').\nPress Enter to skip and check the test environment only."

  read -r selected_modules

  # Reset test flags
  test_tcp=false
  test_pox=false
  mod=0  # Default mod value (don't test DNS or Web server)

  # Process selected options
  if [ -n "$selected_modules" ]; then
    for option in $selected_modules; do
      case $option in
        1)
          test_tcp=true
          ;;
        2)
          test_pox=true
          ;;
        3)
          mod=$((mod+3))  # Enable DNS server testing
          ;;
        4)
          mod=$((mod+4))  # Enable Web server testing
          ;;
        *)
          echo "Invalid option: $option. Ignoring."
          ;;
      esac
    done
  fi

  if [ "$mod" -gt 5 ]; then
    mod=5
  fi
}

# Reminder message for using command-line arguments
echo "Reminder: You can also run the test script with the desired test directly by using: sudo ./test.sh [options]"
echo "For example: 'sudo ./test.sh 1 3' to test TCP and DNS servers."

# Check if options are provided as a command-line argument
if [ -z "$2" ]; then
  # If no argument is provided, prompt for selection
  select_mod
else
  # Use provided argument
  selected_modules="$2"
  select_mod
fi

# --- Start the TCP server if selected ---
SCRIPT_PATH="/home/mininet/Captive-Portal/answer/tcp_server.pyc"
POX_TCP_SOURCE_FILE='/home/mininet/Captive-Portal/pox_answer/tcp_client_answer.pyc'
if [ "$test_tcp" = true ]; then
  SCRIPT_PATH="/home/mininet/Captive-Portal/start_code/tcp_server.py"
  POX_TCP_SOURCE_FILE='/home/mininet/Captive-Portal/start_code/tcp_client.py'
fi
echo "Running TCP server Python script: $SCRIPT_PATH"
python "$SCRIPT_PATH" &

sleep 1  # Ensure there is enough time to start the process

# --- Start POX process if selected ---
POX_SOURCE_FILE='/home/mininet/Captive-Portal/pox_answer/condition_switch_answer.pyc'
SCRIPT_COMMAND=condition_switch_answer
if [ "$test_pox" = true ]; then
  POX_SOURCE_FILE='/home/mininet/Captive-Portal/start_code/switch.py'
  SCRIPT_COMMAND=switch
fi
DESTINATION_DIRECTORY='/home/mininet/pox/ext'

# Call the function to copy files
copy_files "$POX_SOURCE_FILE" "$POX_TCP_SOURCE_FILE" "$DESTINATION_DIRECTORY"

# Run the POX command
echo "Running POX: sudo /home/mininet/pox/pox.py $SCRIPT_COMMAND"
sudo /home/mininet/pox/pox.py "$SCRIPT_COMMAND" &

sleep 5  # Ensure there is enough time to start the process

# --- Display a "Testing..." message ---
echo -e "\nTesting...\nThis may take some time.\n"

# Run the test Python script with the chosen mod value and suppress the output, and capture the process ID
python /home/mininet/Captive-Portal/test_mininet.py --mod $mod &
python_mn_pid=$!

# Wait for the Python test process to finish
wait $python_mn_pid

# Display the results
echo "Test Results:"
cat /home/mininet/Captive-Portal/mininet_grade.txt | grep -E 'Initial Connectivity Test|Web Connectivity Test|Failed Certification Test|Succeed Certification Test|Second Connectivity Test|Final Connectivity Test|Summary'

# Notify user that more detailed test results can be found in mininet_grade.txt
echo -e "\nTest completed. You can find the more detailed test results in the mininet_grade.txt file."

# Call cleanup after the test is done
cleanup
