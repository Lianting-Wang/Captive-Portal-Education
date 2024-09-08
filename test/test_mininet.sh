#!/bin/bash

# Cleanup function to release the Mininet
function cleanup() {
    echo "Interrupt signal received, stopping process..."
    kill $python_pid
    echo "Initial Mininet cleanup..."
    mn -c > /dev/null 2>&1
    echo "Mininet cleanup successful"
    exit 0
}

# Catch SIGINT (Ctrl+C) signal and call the cleanup function
trap cleanup SIGINT

# Function to handle the choice selection
select_mod() {
  echo "Please select the type of test to run:"
  echo "1) Don't test your own DNS/Web server files"
  echo "2) Test your own DNS server file"
  echo "3) Test your own Web server file"
  echo "4) Test both your own DNS and Web server files"
  echo -e "Press Enter to select the first option (mod = 0) or enter your choice [1-4]: "

  read -r choice
  
  case $choice in
    ""|1)
      mod=0
      ;;
    2)
      mod=3
      ;;
    3)
      mod=4
      ;;
    4)
      mod=5
      ;;
    *)
      echo "Invalid choice. Exiting."
      exit 1
      ;;
  esac
}

# Reminder message for using command-line arguments
echo "Reminder: You can also run the script with the desired test directly by using: ./test.sh [1-4]"
echo "For example: ./test.sh 3 to test your own Web server file."

# Check if an option is provided as a command-line argument
if [ -z "$1" ]; then
  # If no argument is provided, prompt for selection
  select_mod
else
  case $1 in
    1)
      mod=0
      ;;
    2)
      mod=3
      ;;
    3)
      mod=4
      ;;
    4)
      mod=5
      ;;
    *)
      echo "Invalid option. Please use a number between 1 and 4."
      exit 1
      ;;
  esac
fi

# Display a "Testing..." message
echo -e "Testing...\nThis may take some time.\n"

# Run the Python script with the chosen mod value and suppress the output, and capture the process ID
python test_mininet.py --mod $mod > /dev/null 2>&1 &
python_pid=$!

# Wait for the Python process to finish or for a signal to be caught
wait $python_pid

# Display the results
echo "Test Results:"
cat mininet_grade.txt | grep -E 'Initial Connectivity Test|Web Connectivity Test|Failed Certification Test|Succeed Certification Test|Second Connectivity Test|Final Connectivity Test|Summary'

# Notify user that the more detailed test results can be found in mininet_grade.txt
echo -e "\nTest completed. You can find the more detailed test results in the mininet_grade.txt file."
