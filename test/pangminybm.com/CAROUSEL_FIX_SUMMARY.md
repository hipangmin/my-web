# 项目轮播修复总结

## 1️⃣ 背景
- 项目是从 **WordPress** 站点迁移到静态 HTML。\
- 页面使用 **Elementor** 生成的代码，其中包含大量 **绝对 URL**（如 `https://pangminybm.com/...`）和 **srcset**、**sizes** 属性。
- 这些绝对路径在本地 `file://` 或服务器 IP 访问时会导致 **404**、**JS 错误**，从而使轮播（Swiper/Elementor nested‑carousel）无法正常工作。

## 2️⃣ 关键问题
| 序号 | 问题描述 | 影响 |
|------|----------|------|
| 1 | 绝对 URL（`https://pangminybm.com/...`）在本地访问失效 | 图片、JS、CSS 加载 404 |
| 2 | `srcset` 中的多分辨率图片引用了不存在的文件 | 浏览器尝试加载不存在的资源，产生错误 |
| 3 | 缺失的 **Elementor** JavaScript bundle（`nested-carousel`, `nav-menu` 等） | 轮播初始化脚本缺失，控制台报 `Uncaught ReferenceError` |
| 4 | 部署后代码未同步到服务器 | 本地调试成功但线上仍旧报错 |

## 3️⃣ 解决思路
1. **统一使用相对路径**：将所有 `https://pangminybm.com/` 替换为 `../../`（相对根目录），并在 **Elementor 配置对象 `elementorFrontendConfig.urls`** 中同样替换。
2. **移除 `srcset` 与 `sizes`**：这些属性指向不存在的尺寸文件，直接删除即可避免 404。
3. **下载缺失的 JS 文件**：从原站点 `https://macmasterimaritime.com/...` 拉取以下文件并放置到对应目录：
   - `nested-carousel.db797a097fdc5532ef4a.bundle.min.js`
   - `nav-menu.8521a0597c50611efdc6.bundle.min.js`
   - `text-editor.45609661e409413f1cef.bundle.min.js`
   - `section-frontend-handlers.d85ab872da118940910d.bundle.min.js`
   - `shared-frontend-handlers.03caa53373b56d3bab67.bundle.min.js`
   - `wp-emoji-release.min.js`
4. **使用脚本自动化**：
   - `fix_elementor_urls.py`：正则替换 Elementor 配置中的 URL。
   - `remove_srcset.py`：删除所有 `<img>` 的 `srcset` 与 `sizes` 属性。
5. **Git 工作流**：
   - `git add .` → `git commit -m "Fix carousel …"` → `git push origin main` 将本地修改同步到 GitHub。
   - 在服务器上 `git fetch && git reset --hard origin/main` 拉取最新代码。
6. **本地/服务器测试**：
   - 使用 `python -m http.server 8081` 本地启动临时服务器，访问 `http://localhost:8081/...` 验证。
   - 在阿里云服务器上 `nginx -s reload` 重新加载配置后访问 `http://<IP>/services/ships-registration/index.html`。

## 4️⃣ 关键技术点与概念
### 4.1 相对路径 vs 绝对路径
- **绝对路径**（`https://domain.com/...`）在不同域名或本地 `file://` 环境下失效。
- **相对路径**（`../../`）相对于当前 HTML 文件所在目录，适用于本地调试和服务器部署。

### 4.2 `srcset` 与 `sizes`
- 用于响应式图片，提供多分辨率图片 URL。
- 当对应的图片文件不存在时，浏览器会尝试请求导致 **404**，并可能阻塞渲染。
- 删除后浏览器只使用 `src`，避免错误。

### 4.3 Elementor 前端配置 (`elementorFrontendConfig`)
- WordPress 插件 Elementor 在页面中注入一个全局 JS 对象，包含 **assets、ajaxurl、uploadUrl** 等路径。
- 必须把这些路径改为相对路径，否则脚本加载失败。

### 4.4 JavaScript Bundle（Swiper、nested‑carousel）
- Elementor 使用 **Swiper** 实现轮播，`nested-carousel` 是其内部模块。
- 缺失的 bundle 会导致 `Uncaught ReferenceError: Swiper is not defined` 或 `elementorFrontend` 初始化错误。

### 4.5 Git 基础操作
| 命令 | 作用 |
|------|------|
| `git add .` | 将工作区所有修改加入暂存区 |
| `git commit -m "msg"` | 创建提交记录 |
| `git push origin main` | 推送到远程仓库 |
| `git fetch` | 拉取远程更新但不合并 |
| `git reset --hard origin/main` | 强制把本地分支指向远程最新提交（覆盖本地改动） |

### 4.6 本地临时服务器
- `python -m http.server <port>`：快速启动一个静态文件服务器，便于在本地通过 `http://localhost:<port>` 访问页面，避免 `file://` 的跨域限制。

## 5️⃣ 操作步骤回顾（按时间顺序）
1. **批量替换绝对 URL**（PowerShell `-replace`）
2. **编写 `fix_elementor_urls.py`**：正则替换 Elementor 配置中的 URL。
3. **编写 `remove_srcset.py`**：删除所有 `srcset` 与 `sizes`。
4. **运行脚本**：`python fix_elementor_urls.py && python remove_srcset.py`，确认 48/47 文件被修改。
5. **下载缺失的 JS 文件**（PowerShell `Invoke-WebRequest`）并保存到对应目录。
6. **本地测试**：启动 `python -m http.server 8081`，刷新页面，轮播正常。
7. **Git 提交并推送**：`git add . && git commit -m "Fix carousel …" && git push origin main`。
8. **服务器部署**：在阿里云服务器上执行 `git fetch && git reset --hard origin/main`，重新加载 Nginx。
9. **最终验证**：访问 `http://<IP>/services/ships-registration/index.html`，轮播显示正常。

## 6️⃣ 经验教训 & 小贴士
- **始终使用相对路径**，尤其在从 CMS 导出为静态站点时。
- **删除 `srcset`** 前先确认是否真的需要多分辨率图片；如果需要，最好保留对应的图片文件。
- **缺失的第三方库**（如 Elementor 的 JS）可以直接从原站点下载，或通过 npm/ CDN 替代。
- **Git 工作流**：在多人协作或服务器部署时，使用 `fetch + reset` 可以快速同步，避免冲突。
- **本地服务器**：比直接打开 `file://` 更接近真实部署环境，能提前发现跨域或路径问题。

---
**祝你在前端开发的道路上越走越远 🚀**
