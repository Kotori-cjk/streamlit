# 视频数据样本展示

独立站点，与 `space/` 同级。仓库：`Kotori-cjk/streamlit`；发布地址：https://kotori-cjk.github.io/streamlit/ 。主站仓库无需修改。

`index.html` 使用官方 [Stlite](https://github.com/whitphx/stlite) 的 `@stlite/browser@0.85.1` 在浏览器内运行 `app.py`。`public-files.json` 列出挂载进浏览器虚拟文件系统的应用与 JSON 文件；视频通过同站 HTTPS URL 按需读取。运行环境依赖 jsDelivr/Pyodide CDN，首次启动需要下载。`preview.html` 提供无需 Python 环境的视频预览。

只发布经过整理的 9 个演示样本及配套相机数据。不包含生产目录、凭据、控制接口或本地 Python 环境。

当前素材版本为 `20261017-multirate`：6 条 GTA 视频均包含原生多段流速变化，展示端不改变播放倍率；页面提供世界时间、差分倍率与时间程序。Sandy Shores 两轮同源、握手及人犬的执行计划派生相机等边界按原清单保留。新素材使用新 ID，旧恒速与冻结展示素材已移除。

推送到 `main` 后，GitHub Actions 发布静态站点；没有 Python 服务器、外网隧道或额外托管平台。
