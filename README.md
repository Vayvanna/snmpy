```markdown
# 🐳 SNMPy Setup Guide (Branch: `prod-siege`)

This guide walks you through installing Docker, configuring proxy access
(critical in enterprise environments), setting up environment variables,
and deploying the SNMPy app using Docker Compose.

---

## ✅ 1. Install Docker & Docker Compose

```bash
sudo apt update
sudo apt install -y docker.io docker-compose
```

---

## 👤 2. Enable Docker for Non-root Usage

Add your user to the `docker` group:

```bash
sudo usermod -aG docker $USER
newgrp docker  # Or log out and log back in
```

---

## 🌐 3. Configure System-wide Proxy Access

> ⚠️ **Important:** If you're behind a corporate proxy, configure system-wide environment variables to allow internet access for Docker, Git, etc.

Edit `/etc/environment`:

```bash
sudo nano /etc/environment
```

Append the following (modify IP and port if needed):

```env
PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin"
http_proxy="http://10.10.200.200:8080"
https_proxy="http://10.10.200.200:8080"
no_proxy="localhost,127.0.0.1,localdomain,10.1.10.150"
```

Apply changes:

```bash
source /etc/environment
```

---

## 📁 4. (Optional) Create a Project Directory

```bash
mkdir -p ~/snmpy
cd ~/snmpy
```

---

## 📥 5. Clone the Repository (Branch: `prod-siege`)

```bash
git clone --branch prod-siege https://github.com/Vayvanna/snmpy.git
cd snmpy
```

> 📝 At the time of writing, the latest commit is `44718f`.

(Optional) Checkout a specific commit:

```bash
git checkout 44718f
```

---

## 🔐 6. Create a `.env` File for Configuration

Create a `.env` file in the root of the repo:

```bash
nano .env
```

Paste the following (update secrets if necessary):
You need to create a TELEGRAM bot and get its token
and you need the TELEGRAM profile id on the account 
you expect to receive the notifications on.
also create a username, password and a secretkey
```env
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
TELEGRAM_CHAT_ID2=
LOGIN_USERNAME=
LOGIN_PASSWORD=
SECRET_KEY=
FLASK_APP=run.py
FLASK_ENV=development
```

---

## 🐳 7. Build and Start Docker Compose

```bash
docker compose up --build
```

---

## 🔁 8. Restart Docker Compose

```bash
docker compose restart
```

---

## 🧼 9. Remove Docker Containers & Clean Volumes

To fully reset your containers and PostgreSQL volume:

```bash
docker compose down
docker volume rm snmpy_pgdata
docker compose up --build
```

---

## ✅ Done

Your SNMPy stack should now be running and accessible locally. Check the logs or use `docker ps` to verify container status.
```

