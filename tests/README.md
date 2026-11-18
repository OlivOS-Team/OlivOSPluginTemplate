# OlivOSPluginTemplate 测试

这里保留一组最小的模板契约测试，用来确认以下内容没有被改坏：

- `app.json` 的命名空间、消息模式和单页 WebUI 声明；
- `main.Event` 的常用回调入口；
- 被动回复与 WebUI 消息桥示例。

模板使用者应在本目录继续添加自己的业务测试。不要把真实账号、真实模型请求或本地开发者配置写进测试。

## 本地运行

```powershell
$env:OLIVOS_SOURCE = 'D:\MyProject\run\OlivOS-dev'
python -m pytest tests -q
```

## 覆盖率

```powershell
New-Item -ItemType Directory -Force test-results | Out-Null
python -m pytest tests `
  --cov=OlivOSPluginTemplate `
  --cov-branch `
  --cov-context=test `
  --cov-report=term-missing `
  --cov-report=xml:test-results/coverage.xml `
  --cov-report=json:test-results/coverage.json `
  --cov-report=html:test-results/html `
  --junitxml=test-results/junit.xml
```

覆盖率默认不设门槛；模板使用者稳定后可以自行加入 `--cov-fail-under`。

## 初始基线

- 测试数：5
- 行覆盖率：48.48%（32 / 66）
- 分支覆盖率：20.59%（7 / 34）
- 行与分支综合覆盖率：39.00%

这个数字刻意偏低：模板只覆盖公共入口，具体业务分支应由使用者随实现一起补充。

## CI 顺序

`.github/workflows/ci.yml` 固定为 `flake8 -> tests + coverage -> build`，前一步失败时后续任务不会执行。
