## Guide for Setup Captive Portal Project

### Guide for Connect to a Linux Device (Mininet) Using Remote SSH in Visual Studio Code

This tutorial will guide you through the steps to connect to a Mininet virtual device using the Remote - SSH extension in Visual Studio Code (VSCode). This method is recommended for its ease and efficiency, though students are welcome to use alternative methods if preferred.

#### Prerequisites
- Ensure you have Visual Studio Code installed on your computer. If not, download and install it from [the official Visual Studio Code website](https://code.visualstudio.com/).
- Install the Remote - SSH extension in VSCode. You can find it by searching for "Remote - SSH" in the Extensions view (`Ctrl+Shift+X`).

#### Step 1: Determining the IP Address of Your Mininet Device
1. **Start your Mininet VM.** Ensure that the Mininet virtual machine is running.
2. **Access the Mininet command line.** You can do this through your VM interface.
3. **Retrieve the IP Address:**
   - In the Mininet command line, type `ifconfig` and press Enter.
   - Look for the `eth0` section (or the primary network interface). Note down the IP address listed next to `inet addr`. This is the IP address you'll use to connect.

#### Step 2: Configuring VSCode for Remote SSH
1. **Open VSCode.**
2. **Open the Command Palette** by pressing `F1` or `Ctrl+Shift+P`.
3. **Type 'Remote-SSH: Connect to Host...'** and select it.
4. **Enter the SSH Connection Command:**
   - Type `ssh mininet@<IP_ADDRESS>` (replace `<IP_ADDRESS>` with the IP address you noted earlier).
   - Press Enter.

#### Step 3: Adding the SSH Host
1. **Select 'Configure SSH Hosts...'** in the bottom left corner of the screen that pops up after the previous step.
2. **Select the SSH configuration file to update** (typically found at `~/.ssh/config` on your local machine).
3. **Add the following configuration** to the file:
   ```bash
   Host mininet-vm
       HostName <IP_ADDRESS>
       User mininet
   ```
   - Replace `<IP_ADDRESS>` with the actual IP address of your Mininet device.
   - Save and close the file.

#### Step 4: Connecting to the Mininet Device
1. **Open the Command Palette again** (`F1` or `Ctrl+Shift+P`).
2. **Type 'Remote-SSH: Connect to Host...'** again and select it.
3. **Choose 'mininet-vm'** from the list of configured hosts.
4. **Enter the password** when prompted. The default password is `mininet`.

#### Step 5: Working in VSCode
Once connected, you can use VSCode as if you were working locally on the Mininet device. You can open terminals, edit files, and execute commands directly in VSCode.

#### Additional Tips
- **Password Re-entry:** You may need to enter the password multiple times during your session, especially when initiating new terminal sessions within VSCode.
- **Troubleshooting Connections:** If you encounter issues connecting, verify the IP address and SSH configuration. Ensure that the Mininet VM is properly configured to accept SSH connections.

This method provides a seamless way to work with your Mininet device, leveraging the powerful features of VSCode. Feel free to explore other options and tools to enhance your learning and development experience.

### Guide for Set Up Captive Portal Project

#### Step 1: Set Up the Captive Portal Environment

After connecting to your Mininet device via VSCode as described in the previous guide, the next step is to prepare your environment by installing necessary packages and configuring the project setup.

1. **Open the VSCode terminal window.**
   - You can do this by pressing `Ctrl+` (backtick) or navigating through the menu (`View > Terminal`).

2. **Update the system and install required tools:**
   - In the terminal window, run the following command to update the system packages and install essential tools like `curl`:
     ```bash
     sudo apt update; sudo apt install -y curl
     ```
3. **Download and run the setup script:**
   - Next, run the following command to download and execute the setup script from the Captive Portal Education GitHub repository:
     ```bash
     /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Lianting-Wang/Captive-Portal-Education/main/set_up.sh)"
     ```
   This script will set up the environment by installing necessary dependencies and cloning the project repository.

#### Step 2: Replace the Working Directory with Our Project Folder

Our working path for this assignment is `/home/mininet/Captive-Portal`, which you can open using the Open button or the command palette (`Ctrl+Shift+P`) and type `Open Folder`.

- Once you've navigated to the correct working directory, run the `ls` command in terminal window to check that the required project files are present:
   ```bash
   ls
   ```
   You should see files and folders related to the Captive Portal project.

#### Step 3: Running the Initial Test

1. **Run the test script:**
   - To verify that your environment is set up correctly, you will now run the test script provided with the project. In the VSCode terminal, run the following command:
     ```bash
     sudo ./test.sh
     ```
   - The script will prompt you for an option to select a test. You can press `Enter` to select the default option, which checks whether the environment configuration is correct.

2. **Check the results:**
   - Once the tests have completed, you should see a summary of the results. If the environment has been set up correctly, the output will include a message similar to:
     ```
     Summary: 10 / 10 Test Success!
     ```
   - This confirms that everything is configured correctly, and you can now proceed with your work on the project.

#### Additional Notes:
- If you encounter any issues during the setup, verify your connection to the Mininet VM and ensure that all required dependencies have been installed.
- If the test does not pass, review the error messages for troubleshooting or reach out to the teaching assistant for help.

By following these steps, your Captive Portal project environment will be correctly set up and ready for development.