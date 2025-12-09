# 部署指南 & Nginx 说明

## 为什么使用 Nginx
- **高性能**：单线程、事件驱动，能够在低资源占用下处理成千上万的并发请求。
- **静态文件服务器**：非常适合本项目这种纯 HTML/CSS/JS 的站点，直接把文件返回给浏览器。
- **反向代理 & 负载均衡**：如果以后需要后端服务（PHP、Node、Python），Nginx 可以把请求转发到后端。
- **安全 & 访问控制**：可以限制对 `.git`、隐藏文件的访问，加入 HTTPS、HTTP/2 等安全特性。
- **缓存、压缩、限速**：提升页面加载速度，降低带宽消耗。

## 部署步骤（适用于 CentOS 7 / 8）

### 1. 登录服务器并安装 Nginx
```bash
ssh root@<YOUR_SERVER_IP>
# 安装 EPEL（如果还没有)
yum install -y epel-release
# 安装 Nginx
yum install -y nginx
# 启动并设为开机自启
systemctl start nginx
systemctl enable nginx
```

### 2. 创建站点目录并拉取代码
```bash
# 创建站点根目录（保持与本地结构一致)
mkdir -p /var/www/pangminybm.com/test
cd /var/www/pangminybm.com/test

# 克隆最新代码（如果已经存在仓库则直接 pull)
git clone https://github.com/hipangmin/my-web.git
# 进入项目目录
cd my-web
# 确保本地是最新提交
git fetch origin
git reset --hard origin/main
```

### 3. 配置 Nginx 虚拟主机（Server Block）
编辑 `/etc/nginx/conf.d/pangminybm.conf`（若已存在可直接修改）：
```nginx
server {
    listen 80;
    server_name pangminybm.com <YOUR_IP>;

    # 网站根目录指向实际的 HTML 文件所在路径
    root /var/www/pangminybm.com/test/pangminybm.com;
    index index.html;

    # 防止访问隐藏文件（.git、.env 等）
    location ~ /\. {
        deny all;
    }

    # 允许跨域（如果前端需要）
    add_header Access-Control-Allow-Origin "*";

    # 错误页面（可选）
    error_page 404 /404.html;
}
```
保存后检查语法：
```bash
nginx -t   # 应显示 "syntax is ok" 与 "test is successful"
```
若无错误，重新加载配置：
```bash
systemctl reload nginx
```

### 4. 设置文件权限
```bash
# 让 Nginx 进程能够读取文件（假设 Nginx 运行用户为 nginx）
chown -R nginx:nginx /var/www/pangminybm.com
chmod -R 755 /var/www/pangminybm.com
```
如果 Nginx 运行用户是 `root`，可省略此步骤。

### 5. 验证部署
在浏览器打开：
```
http://<YOUR_IP>/services/ships-registration/index.html
```
- **轮播** 应正常显示所有国旗图片。
- 打开 **开发者工具 (F12)** → **Console**，确认没有 JavaScript 错误。
- 若出现 404，检查 Nginx 错误日志 `/var/log/nginx/error.log` 与访问日志 `/var/log/nginx/access.log`。

### 6. 常见问题 & 小技巧
| 问题 | 解决方案 |
|------|----------|
| 页面 404 | 确认 `root` 指向的是 `.../pangminybm.com`（含 `index.html` 的目录）。 |
| CSS/JS 未加载 | 检查 `elementorFrontendConfig.urls` 是否已全部改为相对路径 `../../`。 |
| 权限错误 | 确认文件/目录所有者为 Nginx 运行用户，或使用 `chmod 755`。 |
| 需要 HTTPS | 安装 `certbot`（Let’s Encrypt）并在 Nginx 中添加 `listen 443 ssl;` 配置。 |
| 将来需要后端 | 在同一 `server` 块中添加 `location /api/ { proxy_pass http://127.0.0.1:3000; }`，Nginx 将充当反向代理。 |

---
**完成以上步骤后，你的站点已经正式上线，轮播功能也已恢复正常。祝部署顺利 🚀**
