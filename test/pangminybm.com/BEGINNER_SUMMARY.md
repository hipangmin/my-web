# 初学者实战总结：网站修复与部署

恭喜你！你成功修复了一个复杂的网站迁移问题。这个过程涵盖了前端调试、自动化脚本编写、Git 版本控制以及服务器运维等多个核心领域。

以下是本次实战的操作复盘与核心知识点总结。

---

## 1. 问题排查 (Debugging)

### 现象
- 网站轮播图不显示。
- 浏览器控制台 (F12 -> Console) 出现大量红色报错 (404 Not Found)。
- **手机访问慢**：图片未优化，且 Google reCAPTCHA 在国内加载超时。
- **子页面 404**：在深层目录（如 `/services/class-and-statutory/...`）下，资源路径错误。

### 核心知识点
- **404 Not Found**: 表示浏览器请求的资源（图片、JS 文件等）在服务器上找不到。
- **Webpack Chunks**: 现代前端框架（如 Elementor/React/Vue）通常会把代码拆分成多个小文件（chunks），按需动态加载。
  - *问题*: 我们只下载了主文件，没下载这些动态加载的小文件，导致功能缺失。
- **相对路径陷阱**:
  - `../../` 只能回退两层。如果页面在三层深度的目录中，它就回不到根目录了。
  - *解决*: 必须根据当前 HTML 文件的深度，动态计算回退层级（如 `../../../`）。

---

## 2. 自动化修复 (Automation)

### 操作 A: 下载缺失文件
我们编写了 Python 脚本 (`download_webpack_chunks.py`) 来自动分析和下载缺失文件。
- **正则提取**: 从 `webpack-runtime.js` 中提取 chunk 文件名。
- **伪装请求**: 添加 `User-Agent` 防止被服务器拦截 (406 错误)。

### 操作 B: 深度路径修复 (关键)
我们编写了 `fix_relative_paths_v2.py`，解决了深层目录下的 404 问题。
- **动态深度计算**: 脚本会自动判断每个 HTML 文件距离根目录有几层，生成正确的 `../` 前缀。
- **修复 JSON 配置**: Elementor 的配置 (`elementorFrontendConfig`) 藏在 `<script>` 标签里，脚本利用正则表达式精准定位并修复了其中的 `assets` 路径。
- **修复 wpemojiSettings**: 同样修复了 WordPress Emoji 设置中的路径。

### 操作 C: 优化国内访问
编写了 `optimize_recaptcha.py`。
- **替换源**: 将 `www.google.com/recaptcha` 批量替换为 `www.recaptcha.net/recaptcha`（Google 官方国内镜像）。
- *效果*: 解决了手机端因连接 Google 超时导致的页面卡顿。

---

## 3. Git 版本控制与运维 (Git & Ops)

### 操作
在服务器上同步代码时遇到了网络和权限问题。

### 核心知识点
- **版本一致性**: 使用 `git rev-parse HEAD` 对比本地和服务器的 Commit ID。
- **网络故障处理**:
  - 当 `git pull` 卡住时，使用 `until` 循环脚本不断重试。
- **权限问题 (Permission denied)**:
  - *现象*: `error: cannot open .git/FETCH_HEAD: Permission denied`
  - *原因*: 当前用户没有权限修改 `.git` 目录（可能属于 root）。
  - *解决*: 使用 `sudo git pull` 提升权限。

---

## 4. 品牌升级 (Branding)

### Logo 设计提示词
为了生成符合网站风格的 Logo，我们提取了 CSS 中的核心色值：
- **主色 (Navy Blue)**: `#101828`
- **副色 (Steel Blue)**: `#475467`
- **点缀色 (Accent Blue)**: `#444CE7`

**AI 提示词 (Prompt)**:
> Minimalist vector logo for maritime company "CMCS CLASS". Colors: #101828 (Navy) and #475467 (Steel). Symbol: Stylized shield merged with ocean waves. Style: Flat, geometric, professional.

---

## 5. 经验总结

1. **不要相信 `file://`**: 本地测试一定要起服务 (`python -m http.server`)。
2. **看报错信息**: F12 控制台的红色 404 是解决问题的藏宝图。
3. **路径是关键**: 静态网站迁移最容易错的就是路径。遇到 404，先检查路径层级对不对。
4. **自动化思维**: 超过 3 个文件的重复操作，就值得写个脚本来做。
5. **Git 是真理**: 遇到服务器表现奇怪，先对比 Commit ID，确保代码版本一致。

加油！你已经从一个单纯的代码修改者，进阶到了能处理部署运维问题的开发者了！🚀
