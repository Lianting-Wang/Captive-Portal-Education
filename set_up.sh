#!/bin/bash

# Update package lists and install curl and unzip if they are not installed
sudo apt update
sudo apt install -y curl unzip

# Create and navigate to the target directory
mkdir -p ~/Captive-Portal
cd ~/Captive-Portal || exit

# Download and unzip the archive
curl -L -o Captive-Portal.zip https://github.com/Lianting-Wang/Captive-Portal-Education/archive/refs/heads/main.zip
unzip -o Captive-Portal.zip
rm Captive-Portal.zip

# Move the extracted files to the current directory
# Get the name of the extracted directory (assuming the zip contains only one top-level directory)
extracted_dir=$(find . -mindepth 1 -maxdepth 1 -type d)

# Move files including hidden files to the current directory and forcefully remove the temporary directory
if [ -d "$extracted_dir" ]; then
  # Move regular files and directories
  mv "$extracted_dir"/* "$extracted_dir"/.* . 2>/dev/null
  
  # Remove the directory and its contents
  rm -rf "$extracted_dir"
fi

# Add executable permissions to all .sh files
find . -type f -name "*.sh" -exec chmod +x {} \;
