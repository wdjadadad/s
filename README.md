# E听说答案提取 · etsx（现代化版）

> 零安装依赖的 Python 后端 + 免构建现代前端 + **edge-tts 朗读** + **独立应用窗口（不弹浏览器标签页）** + **图形安装器**。
> 从 ETS（E听说）听力 / 口语缓存里提取「朗读 / 交际应答 / 复述·表达」的参考答案。

---

## 特性

- 🔍 **一键扫描**：自动发现题目文件夹（数字命名或任意命名均可），并按题号排序。
- 🧠 **三类题型解析**：`朗读`、`交际应答`、`复述 / 表达`，自动分组、去 HTML 标签。
- 🔊 **edge-tts 朗读**：题干、单条答案均可朗读；8 种中英文音色可选，音频本地缓存。
- 🎧 **批量导出音频**：一键把「朗读」部分合成 MP3 并打包成 ZIP 下载。
- 🖥️ **独立应用窗口**：不打开浏览器标签页；基于 Edge / WebView2 的 `--app` 无边框窗口（无地址栏、无标签），启动时显示自绘启动弹窗。
- 🎯 **答案数量可调**：交际、复述/表达每题答案条数可配置并持久化。
- 📋 **复制 / 导出**：单题、整节、整卷复制，导出 UTF-8 `.txt`。
- 🌗 **深浅色主题**：手动切换或跟随系统。
- 📦 **图形安装器**：一键安装到 `%APPDATA%\ETS`，自动生成 `uninstall.bat` 与桌面快捷方式。
- 🧪 **零依赖 + 可测试**：后端逻辑仅用标准库；第三方依赖全部内置在 `vendor/`，无需 `pip install`。

## 目录结构

```
etsx/
├─ run.py                     # 启动入口（默认打开应用窗口）
├─ start.bat                  # Windows 一键启动
├─ test.bat                   # 运行单元测试（含 vendor）
├─ installer.py               # 图形安装器（安装 / 卸载脚本 / 快捷方式）
├─ info.json                  # 版本信息
├─ ETS.ico                    # 应用图标
├─ pyproject.toml             # 包元数据 / ruff / mypy
├─ vendor/                    # 内置依赖：edge-tts、aiohttp 等（约 10 MB）
├─ src/etsx/
│  ├─ __main__.py             # CLI（--web / --no-open / --root / --port）
│  ├─ server.py               # 本地 HTTP 服务 + JSON API + 静态托管
│  ├─ desktop.py              # 原生窗口（Edge --app）+ 启动弹窗
│  ├─ tts.py                   # edge-tts 朗读（含磁盘缓存）
│  ├─ models.py               # Answer / Question / Section / Paper
│  ├─ config.py               # config.json（含 voice）
│  ├─ textutils.py            # 去 HTML、文本清洗
│  ├─ scanner.py              # 扫描目录、发现题目文件夹
│  ├─ parser.py               # 解析 content2.json / info.json → Paper
│  ├─ extractor.py            # 按配置裁剪答案、渲染导出文本
│  └─ web/                    # 免构建前端（index.html / app.js / styles.css）
├─ tests/                     # unittest 测试 + 合成样本
├─ scripts/
│  ├─ inspect_papers.py       # 开发用：扫描目录并打印结构清单
│  └─ verify_api.mjs          # 开发用：HTTP 契约校验（Node 18+）
└─ desktop/                   # 可选 Electron 外壳（备选方案）
```

## 快速开始

需要 **Python 3.10+**（无需安装任何第三方库，依赖已随 `vendor/` 内置）。

```bat
cd etsx
python run.py            :: 打开独立应用窗口（推荐）
python run.py --web      :: 在默认浏览器中打开（开发模式）
python run.py --no-open  :: 只启动本地服务，不开窗口
```

也可以直接双击 **`start.bat`**：它会自动定位 Python（含便携版 `python\` / `python310\`），优先用 `pythonw.exe` **静默启动（不弹控制台）**，支持参数透传（如 `start.bat --web`），找不到 Python 时给出明确提示。

常用参数：

```bat
python run.py --root "D:\ETS"      :: 指定扫描目录
python run.py --port 8765          :: 固定端口
```

## 安装版（推荐给最终用户）

```bat
cd etsx
python installer.py
```

或直接双击 **`安装.bat`**（等价于 `python installer.py`，会先检查 Python）。

> 🔐 **安装器会自动申请管理员权限（UAC）**：部分安全软件（火绒、Windows Defender 的"受控文件夹访问"等）会阻止**未签名程序**写入用户目录，
> 提权后通常即可通过。点击「是」授权即可；不想提权可加参数 `--no-elevate`。
> 若提权后仍被拦截，请把 `python.exe`（或安装器 exe）加入安全软件信任区，或改用 `安装.bat`。

安装器会：

1. 把 `run.py`、`src/`、`vendor/`、`info.json`、`ETS.ico` 等复制到 **`%APPDATA%\ETS`**；
2. 写入 `config.json`，并将 `last_root` 设为安装目录；
3. 生成 `uninstall.bat`（双击即可彻底卸载）；
4. 在桌面创建「E听说答案提取」快捷方式（指向 `pythonw.exe run.py`，无控制台窗口）；
5. 可选安装完成后立即启动。

也支持静默安装（便于部署 / 测试）：

```bat
python installer.py --silent --target "D:\ETS" --no-launch
```

## 题目读取位置（指定路径）

桌面版默认从**应用安装目录**读取题目：安装到 `%APPDATA%\ETS` 后，把 ETS 下载的题目文件夹（数字命名）放进该目录即可。

也可以在界面左侧输入任意目录（会记住为 `last_root`）。旧版本要求程序与题目同目录，这里默认行为保持一致，但不再强制。

## 朗读（edge-tts）

- 后端接口：`GET /api/tts?text=...&voice=...` → `audio/mpeg`；`GET /api/voices` 返回可选音色。
- 前端：题干与每条答案旁均有播放按钮，可播放/停止；一次只播放一条。
- 音频缓存在 `<应用目录>/cache/tts/`，重复朗读秒开。
- 需要联网（调用 Microsoft Edge 在线语音服务）；离线时按钮会提示失败，其余功能不受影响。
- 音色在「设置」中选择并保存到 `config.json` 的 `voice` 字段。

## 配置文件（`config.json`）

| 字段 | 说明 | 默认 |
|------|------|------|
| `jiaoji` | 交际应答每题答案数 | 8 |
| `fushu` | 复述 / 表达每题答案数 | 4 |
| `biaoda` | 表达预留 | 4 |
| `voice` | edge-tts 音色 id | `zh-CN-XiaoxiaoNeural` |
| `theme` | `dark` / `light` | `dark` |
| `follow_system_theme` | 跟随系统主题 | `false` |
| `last_root` | 上次扫描目录 | `""` |

可用环境变量 `ETSX_HOME` 指定配置 / 缓存目录。

## HTTP API

服务仅监听 `127.0.0.1`。

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/health` | 健康检查 |
| GET | `/api/meta` | 应用名、版本、默认目录、配置 |
| GET | `/api/scan?root=<目录>` | 扫描题目文件夹 |
| GET | `/api/paper?path=<试卷目录>` | 解析并按配置裁剪答案 |
| GET/POST | `/api/config` | 读写配置 |
| POST | `/api/export` | 导出文本 `{path}` → `{filename, content}` |
| GET | `/api/voices` | 可选音色列表 |
| GET/POST | `/api/tts?text=...` | 合成朗读音频（MP3） |
| POST | `/api/export-audio` | 批量导出朗读音频 `{path, scope}` → ZIP |

错误统一返回 `{"error": {"code": "...", "message": "..."}}`。

## 测试

```bat
cd etsx
test.bat
```

等价于：

```bat
set PYTHONPATH=src;vendor
python -m unittest discover -s tests -v
```

另可对运行中的服务做接口契约断言：

```bat
python run.py --no-open --port 8766
node scripts/verify_api.mjs http://127.0.0.1:8766 "D:\ETS"
```

## 桌面窗口说明

- 主方案：调用系统已安装的 **Microsoft Edge / WebView2**，以 `--app` 模式打开无边框窗口（无地址栏 / 无标签页），关闭窗口即退出。
- 启动时**不创建任何 tkinter 窗口**（此前的启动弹窗在部分 Python 3.14 + Tcl/Tk 环境会崩溃并拖垮服务进程，已移除），服务就绪后直接打开应用窗口。
- 备选：`desktop/` 下保留了 **Electron** 外壳（`npm install && npm start`），以及 Tauri 的说明（需 Rust）。
- 为什么不用 pywebview：其 .NET 桥接在当前 Python 3.14 环境无法加载（`Python.Runtime.Loader.Initialize` 解析失败）。

## Electron 桌面打包（可选）

`desktop/` 是完整的 Electron 打包工程，**发布者署名 `yuxiaole_awa`**：

```bat
cd desktop
npm install
npm start          :: 开发调试
npm run dist:win   :: 生成 NSIS 安装包 + 便携版（输出到 release/）
```

- 打包时把 `run.py / src / vendor / info.json / ETS.ico` 作为 `extraResources` 放进 `resources\etsx\`。
- 目标机若没有 Python，可在 `resources\etsx\python\python.exe` 放一个便携运行时。
- 详情见 [desktop/README.md](desktop/README.md)。

## 仓库与发布

本地已初始化 git，分支 `ai超绝现代化版`，remote 指向：

`https://github.com/yuxiaole-bili/ETS_ANSWER_GETTER`

推送（需要你的 GitHub 凭据；沙箱内无法直连 GitHub）：

```bat
cd etsx
git add -A
git commit -m "feat: 现代化重写（Web UI + edge-tts 朗读 + 安装器 + Electron）"
git push -u origin ai超绝现代化版
```

## 分发说明

本项目**不含代码签名**。`.bat` / `.py` 是脚本，无法携带 Windows 发布者签名，未签名时系统提示"未知发布者"属于正常现象。

- 个人 / 小范围使用：直接分发文件夹（含 `src`、`vendor`、`run.py`），双击 `安装.bat` 或用 `python installer.py` 安装到 `%APPDATA%\ETS`；
- 面向公众分发：建议购买代码签名证书并对打包后的 exe（PyInstaller / Electron 产物）签名，否则 SmartScreen 仍会提示"未知发布者"。

## 自行打包安装器

```bat
pip install pyinstaller
python -m PyInstaller --noconfirm --onedir --windowed --name "ETS答案提取v2.0.0-Setup" ^
  --icon ETS.ico ^
  --add-data "run.py;." --add-data "src;src" --add-data "vendor;vendor" ^
  --add-data "info.json;." --add-data "ETS.ico;." --add-data "start.bat;." ^
  --add-data "README.md;." --add-data "requirements.txt;." --add-data "LICENSE;." ^
  installer.py
```

- **务必使用 `--onedir`**：`--onefile` 在 TEMP 路径含非 ASCII 字符（例如中文用户名）时会报
  `Could not create temporary directory!` 而无法启动。
- 产物在 `dist\ETS答案提取v2.0.0-Setup\`，把**整个目录**压缩后分发；双击其中的 exe 即为图形安装器。
- 安装器会把 `src`、`vendor` 等复制到 `%APPDATA%\ETS`，生成 `uninstall.bat` 与桌面快捷方式。

## 旧版 → 新版对照

| 旧版 | 新版 |
|------|------|
| `E听说答案提取.py`（Tkinter 混写） | `web/` 前端 + `parser.py`/`extractor.py` 纯逻辑 |
| `启动E听说答案提取.py`（启动器） | `desktop.py`（应用窗口）+ `server.py` |
| `installer.py`（复制内嵌 Python） | `installer.py`（复制内置 `vendor/`，无需 Python 自带依赖） |
| `settings.json` | `config.json`（新增 `voice`） |
| `ETS答案.txt` 追加写入 | 「导出 TXT」按需下载 |
| 无朗读 | edge-tts 朗读（题干 / 答案） |

## 许可

MIT · 作者：yuxiaole_awa
