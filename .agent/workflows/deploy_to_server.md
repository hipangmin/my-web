---
description: Deploy the website to a Linux server using Git
---

# Deployment Workflow

This workflow assumes you have a Linux server (Ubuntu/CentOS) with a web server (Nginx or Apache) installed.

## Prerequisites
- SSH access to your server
- `git` installed on the server
- Web server (Nginx/Apache) installed and running

## Steps

1. **Connect to your server**
   Open your terminal (or PowerShell) and SSH into your server:
   ```bash
   ssh user@your_server_ip
   ```

2. **Navigate to the web root**
   Usually `/var/www/html` or `/usr/share/nginx/html`.
   ```bash
   cd /var/www/html
   ```

3. **Clone the repository (First time only)**
   If the directory is empty:
   ```bash
   sudo git clone https://github.com/hipangmin/my-web.git .
   ```
   *Note: The `.` at the end clones into the current directory.*

4. **Pull latest changes (Updates)**
   If you already cloned it:
   ```bash
   sudo git pull origin main
   ```

5. **Set Permissions**
   Ensure the web server user (usually `www-data` or `nginx`) owns the files:
   ```bash
   sudo chown -R www-data:www-data /var/www/html
   sudo chmod -R 755 /var/www/html
   ```

6. **Verify**
   Visit your server's IP or domain in the browser.
