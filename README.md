# 🦄 Spirit Animal Generator (AI Server)

This is a **Flask-based AI server** that generates **spirit animal images** using **Stable Diffusion**.  
It runs inside **Docker** with **GPU acceleration** and is exposed to the internet using **Ngrok**, allowing it to be accessed by a **Next.js frontend**.

---

## **📌 Features**
✅ Generates **AI-powered spirit animal images**  
✅ Uses **Stable Diffusion v1.5** for high-quality images  
✅ Runs inside **Docker with NVIDIA GPU support**  
✅ Uses **Ngrok** to expose the API securely  
✅ Includes **rate-limiting** to prevent bot abuse  

---

## **📌 1. Installation Guide**

### **🛠️ Prerequisites**
- **Ubuntu 20.04+ or Debian-based Linux**
- **NVIDIA GPU with CUDA drivers installed**
- **Docker & Docker Compose**
- **Ngrok (for exposing the server)**

### **1️⃣ Install Docker & Docker Compose**
Run the following commands:
```bash
# Install Docker
sudo apt update
sudo apt install -y docker.io docker-compose

# Enable Docker to start on boot
sudo systemctl enable docker
sudo systemctl start docker
```
Check installation:
```bash
docker --version
docker-compose --version
```

### **2️⃣ Install NVIDIA GPU Support for Docker**
If you have an **NVIDIA GPU**, install the required Docker GPU runtime:
Follow guide here: https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html

### **3️⃣ Install Ngrok**
Ngrok is used to expose your local server to the internet.
Follow simple 2-step guide here: 
https://dashboard.ngrok.com/get-started/setup/linux

---

## **📌 2. How to Run the Server**
Once installed, follow these steps:

### **1️⃣ Start the Flask AI Server in Docker**
```bash
docker-compose up --build -d
```
Check that the server is running:
```bash
docker ps
```
If you see `flask-app` running, it’s working!

### **2️⃣ Expose Flask to the Internet Using Ngrok**
Run Ngrok to create a public URL for your Flask server:
```bash
ngrok http 5000
```
Ngrok will generate an HTTPS URL like:
```
Forwarding https://abcd-1234.ngrok-free.app -> http://localhost:5000
```
Copy this URL, as it will be used in the **Next.js frontend**.

### **3️⃣ Test the Server**
You can test your server with:
```bash
curl https://abcd-1234.ngrok-free.app/generate
```
Or use the provided **client_local_test.py** script.

---

## **📌 3. Next.js Integration**
Now, update your **Next.js app** to use the Ngrok URL.

Edit your API route (e.g., `app/api/generate/route.ts`):
```ts
export async function POST(req: Request) {
  const response = await fetch("https://abcd-1234.ngrok-free.app/generate", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });

  if (!response.ok) {
    return Response.json({ error: "Failed to fetch AI response" }, { status: 500 });
  }

  const data = await response.json();
  return Response.json(data);
}
```
---

## **📌 4. Summary**
✅ **Flask AI Server runs inside Docker** with GPU support  
✅ **Exposed using Ngrok** (so Next.js can reach it)  
✅ **Next.js calls Flask via Ngrok** instead of directly  
✅ **Rate-limiting added** to prevent bot abuse  


