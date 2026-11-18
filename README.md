# OlivOSPluginTemplate

`./OlivOSPluginTemplate` 目录整体为[OlivOS](https://github.com/OlivOS-Team/OlivOS)插件默认模板，请结合使用。

## 测试

仓库自带少量模板契约测试，见 [`tests/README.md`](tests/README.md)。请在该目录继续添加插件自己的业务测试。
CI 固定按 `flake8 -> tests + coverage -> build` 顺序执行，测试失败时不会打包 OPK。
