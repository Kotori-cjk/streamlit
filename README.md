# 双人成行双视角标注抽检

独立仓库 `Kotori-cjk/streamlit`，公开地址：https://kotori-cjk.github.io/streamlit/ 。

2026-10-30 接收 H100 交付的 `itt_basic20_static.zip`，替换旧 GTA / DL3DV 展示。20 组、40 个视频，包含基本事实描述、助手初审、旧版对照及浏览器人工记录导出。页面和资源均使用相对路径，不需要后端、Python 或 CDN。

运行 `python -m http.server 8080` 本地预览。推送 `main` 后通过 GitHub Actions 发布。

展示视频为网页压缩版，保留 640×640、24 FPS 和全部帧，未改动训练原视频。初审仅针对已见开发样本，不代表全量准确率或独立人工认证；单视角 31/40 通过、5 个错误、4 个待确认，双视角共同通过 14/20。所有原始 human_reviewed、qualified_for_training 均为 false。

人工记录保存在当前浏览器 localStorage，可导出 JSON，不修改服务器或训练数据。原交付说明见 `HANDOFF.md`。旧站可通过 Git 历史恢复（替换前提交 `8cd692f`）。
