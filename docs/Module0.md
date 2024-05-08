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
Once connected, you can use VSCode as if you were working locally on the Mininet device. You can open terminals, edit files, and execute commands directly in VSCode. Our working path for this assignment is `/home/mininet/Captive-Portal-Education-main`, which you can open using the Open button or the command palette (`Ctrl+Shift+P`) and type `Open Folder`.

#### Additional Tips
- **Password Re-entry:** You may need to enter the password multiple times during your session, especially when initiating new terminal sessions within VSCode.
- **Troubleshooting Connections:** If you encounter issues connecting, verify the IP address and SSH configuration. Ensure that the Mininet VM is properly configured to accept SSH connections.

This method provides a seamless way to work with your Mininet device, leveraging the powerful features of VSCode. Feel free to explore other options and tools to enhance your learning and development experience.
