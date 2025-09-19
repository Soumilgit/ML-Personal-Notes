## **NVIDIA Jetson Nano – Quick Notes**
<img width="1900" height="1460" alt="image" src="https://github.com/user-attachments/assets/8fc5efef-93be-46f6-afb9-6a7268bb19da" />

### **1. Overview**
- **Jetson Nano** is a small, powerful single-board computer by NVIDIA for edge AI applications.
- **CPU:** Quad-core ARM Cortex-A57
- **GPU:** 128-core Maxwell
- **RAM:** 4 GB LPDDR4
- **OS:** Ubuntu-based (JetPack SDK)

### **2. Key Features**
- Runs modern AI frameworks (TensorFlow, PyTorch, Caffe, etc.)
- Supports computer vision, robotics, and Edge AI projects.
- Multiple I/O: GPIO, I2C, I2S, SPI, UART, CSI camera, HDMI, 4x USB 3.0

### **3. Setup Guide**
#### **A. Hardware Requirements**
- Jetson Nano board (with or without onboard eMMC, check version)
- microSD card (16GB+ UHS-1 recommended) – for non-eMMC model
- Power source: 5V/2A (micro-USB) or 5V/4A (DC barrel jack)
- Peripherals: monitor (HDMI/DP), mouse, keyboard
<img width="905" height="408" alt="image" src="https://github.com/user-attachments/assets/df247ea6-f8ff-4ae7-ba16-4a70c31fa537" />

#### **B. Software Installation**
1. **Download JetPack/Image:**
   - Download from NVIDIA's official site.
   - Use 'balenaEtcher' to write image to the SD card.
2. **Insert SD card & Power on**
3. **First boot setup:**
   - Connect keyboard, mouse, and display.
   - Complete Ubuntu setup (user, region, Wi-Fi if needed).
4. **Update & Upgrade:**
   ```bash
   sudo apt update && sudo apt upgrade
   ```

### **4. Basic Commands**
- **Pinout:** See with `gpio readall` (after installing Jetson.GPIO).
- **Enable I2C/SPI:** Use `sudo /opt/nvidia/jetson-io/jetson-io.py`
- **Check NVIDIA driver version:**
  ```bash
  cat /proc/driver/nvidia/version
  ```
- **Access camera (CSI):**
  ```bash
  gst-launch-1.0 nvarguscamerasrc ! nvoverlaysink
  ```

### **5. Installing Libraries**
- **Python GPIO:**
  ```bash
  sudo pip3 install Jetson.GPIO
  ```
- **OpenCV:**
  ```bash
  sudo apt install python3-opencv
  ```
- **TensorFlow/PyTorch:**
  - For Jetson, use NVIDIA’s recommended wheel files.

### **6. Deep Learning On Jetson**
- Pre-installed CUDA toolkit, cuDNN, TensorRT.
- Optimize models with TensorRT.
- Deploy using Jupyter Notebook or via SSH.

### **7. Useful Tips**
- Always use proper power supply (many issues resolve with sufficient current).
- Passive or active heatsink/cooling advised for long AI tasks.
- Use `jtop` or `tegrastats` for monitoring system usage.

### **8. Resources**
- [Official Jetson Nano Developer Guide]
- [NVIDIA GitHub: JetsonHacksNano]
- [NVIDIA Forums: Jetson Nano]

***

**Sample Project Structure**
```markdown
project/
│
├── data/
├── src/
│   └── main.py
├── models/
├── README.md
└── requirements.txt
```

***
