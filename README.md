# OlivOSPluginTemplate

`./OlivOSPluginTemplate` 目录整体为[OlivOS](https://github.com/OlivOS-Team/OlivOS)插件默认模板，请结合使用。

## WebUI 模板

模板包含一个无需 Node.js 或前端构建的网页，发送文本后由插件 Python 回显。需要使用包含 WebUI 功能的 OlivOS 核心。

```text
OlivOSPluginTemplate/
├── __init__.py
├── main.py                 # Event.menu 分发及 webui_reply 回包
├── app.json                # webui_config 注册页面
└── webui/
    └── index.html          # 页面、样式和消息桥接示例
```

1. 将整个 `OlivOSPluginTemplate` 目录放入 OlivOS 的 `plugin/app/`，启动或重载插件。
2. 打开 OlivOS WebUI，默认地址为 `http://127.0.0.1:20480`，使用 `conf/webui_token.txt` 中的令牌登录。
3. 点击侧栏“插件页面”下的“插件模板”，输入消息并点击“发送”，页面显示 Python 返回的文本。

网页通过 `parent.postMessage` 发送 `OlivOSPluginTemplate_WebUI_Echo` 事件。宿主转发给 `Event.menu` 后，插件读取 `plugin_event.data.payload`，使用原事件的 `plugin_event.send('webui', request_id, response)` 回包。模板也处理输入校验、错误响应和请求超时。

页面位于沙箱 iframe 中，不读取 token、不直接请求核心 API，也不能直接访问父页面 DOM 或浏览器存储。示例将样式与脚本放在格式化后的 HTML 内，可直接随插件打包。静态页面直接在浏览器打开时，只能查看布局，消息回显需要通过 OlivOS WebUI 的入口运行。

修改插件名称时，同步修改目录和 Python 导入、`app.json` 的 `namespace`、`Event.menu` 中的命名空间判断，以及前后端使用的事件名。`app.json` 必须保存为 **UTF-8 无 BOM**。

现有 CI 会递归打包整个插件目录，`webui/index.html` 会自动进入 `.opk`；插件不需要运行核心的 `embed_webui.py`。手工打包时，应让 `app.json`、`main.py`、`__init__.py` 与 `webui/` 位于压缩包根目录。

完整接入说明见 [WebUI 插件开发文档](https://docs.olivos.run/DevPlugin/WebUI/)。
