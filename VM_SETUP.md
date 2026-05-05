## Virtual Machine Setup for Mockup Mommy

### Requirements
- Windows 10/11 VM (Professional edition recommended)
- Minimum 8GB RAM allocated to VM
- At least 50GB disk space
- Virtualization software (VirtualBox, VMware, or Hyper-V)
- Adobe Photoshop CC 2022 or later license

### Setup Steps

1. **Create Windows VM**
   - Download Windows 10/11 ISO from Microsoft
   - Create new VM with recommended specs:
     - 8GB RAM minimum
     - 4 CPU cores minimum
     - 50GB disk space
     - Enable virtualization features
     - Enable network adapter in bridge mode

2. **Install Windows**
   - Install Windows normally in VM
   - Install all Windows updates
   - Enable Remote Desktop (optional but recommended)

3. **Install Required Software**
   - Install Adobe Photoshop CC 2022 or later
   - Install Python 3.9+ and add to PATH
   - Install Git
   - Install Node.js and npm

4. **Configure Photoshop**
   - Launch Photoshop
   - Go to Edit > Preferences > Scripting
   - Enable "Allow Scripts to Write Files and Access Network"
   - Enable "Enable Remote Connections" (if available)
   - Restart Photoshop

5. **Setup Mockup Mommy**
   ```bash
   # Clone repository
   git clone https://github.com/yourusername/mockup-mommy.git
   cd mockup-mommy

   # Setup backend
   cd backend
   python -m venv env
   .\env\Scripts\activate
   pip install -r requirements.txt

   # Setup frontend
   cd ../frontend
   npm install
   ```

6. **Configure Environment**
   - Create `.env` file in backend directory:
   ```env
   PHOTOSHOP_PATH="C:\Program Files\Adobe\Adobe Photoshop 2024\Photoshop.exe"
   TEMPLATE_PATH="scripts/template.psd"
   ```

7. **Test Setup**
   - Start backend server:
   ```bash
   cd backend
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```
   - Start frontend (in new terminal):
   ```bash
   cd frontend
   npm start
   ```
   - Access the application through VM's IP address:
     - Backend: http://<VM_IP>:8000
     - Frontend: http://<VM_IP>:3000

### Network Configuration
- Ensure VM network is in bridge mode
- Configure Windows Firewall to allow ports 8000 and 3000
- Note the VM's IP address for accessing the application

### Troubleshooting
1. **Photoshop Not Found**
   - Verify Photoshop installation path
   - Check if Photoshop is running
   - Ensure script permissions are enabled

2. **Network Issues**
   - Check VM network settings
   - Verify Windows Firewall settings
   - Ensure ports 8000 and 3000 are open

3. **Performance Issues**
   - Check VM resource allocation
   - Monitor CPU and RAM usage
   - Consider increasing VM resources if needed 