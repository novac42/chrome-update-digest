# Digest Markdown Review Findings

## Summary
- 跨版本与按领域浏览的主要结构已经成形，但 Chrome 140 仅在 legacy `webplatform` 目录出现，`/versions` 与 `/areas` 下缺失相应内容。
- `digest_markdown/_layouts/default.html` 保留了 WebPlatform 与 Enterprise 入口，现为死链，需要更新。
- `config/output_configuration.md` 仍描述早期 enterprise/webplatform 并行管线，内容与当前架构不符。
- 首页快速链接包含 “Version Comparison” 项目但未指向实际页面。
- 领域索引页面在单数量时仍显示 “Updates in 1 versions”，属文案残留。
- 各领域页的 Front Matter `title` 仅写版本号，导致 Header 缺乏领域上下文。

## Generation Flow Notes
- GitHub Pages 导航由 `src/tools/generate_github_pages_navigation.py` 控制：`scan_content()` 将 `upstream_docs/processed_releasenotes/processed_forwebplatform/areas` 下的 `chrome-{version}-stable.md` 映射到版本/领域；`generate_version_pages()` 与 `generate_area_pages()` 负责写入 `digest_markdown/versions` 与 `digest_markdown/areas`；`update_main_index()` 更新首页最新版本文案。
- 脚本会以版本号逆序排序并把首个版本标记为 Latest，因此每个 release 完成后需重新运行脚本才能把首页 “Latest Stable” 指向新版本。
- `clean_old_structure()` 会删除旧的 `digest_markdown/webplatform` 目录，但当前仓库里该目录仍在，说明 140 之后没有执行导航生成脚本。
- `scan_content()` 未覆盖 `isolated-web-apps` 等新增领域目录，导致最新内容即使生成也会被漏掉，需要同步更新 `area_display_names` 映射。

## TODO
1. 运行或集成 `src/tools/generate_github_pages_navigation.py`，使其在每次 release 后刷新 `digest_markdown/index.md`、`/versions` 与 `/areas`，并清理遗留的 `webplatform` 目录。
2. 扩充脚本中的 `area_display_names` 以包含 `isolated-web-apps` 等新领域；必要时同步 upstream 领域列表，避免漏写。
3. 在脚本输出阶段调整单复数文案以及领域页面 Front Matter，确保标题包含领域名称（脚本内可直接格式化 `title`）。
4. 更新 `digest_markdown/_layouts/default.html` 和 `config/output_configuration.md` 以删除 Enterprise/WebPlatform 残留描述，并加入实际可用的导航链接/配置说明。
5. 为首页 Quick Links 中的 “Version Comparison” 提供真实入口；若暂无落地方案则从模板中移除。
6. 补齐 Chrome 140 及后续版本的 `/versions/chrome-{version}` 与 `/areas/*/chrome-{version}.md`，确保最新版本可通过 Index 浏览；若生成脚本暂时不可用，可手动复制现有内容以保持一致性。

## 建议
1. 更新默认布局、首页与配置文档以去除 Enterprise/WebPlatform 遗留，并补充真实链接。
2. 明确 Chrome 140 及后续版本的产出路径：若沿用 Jekyll 视图则生成 `/versions/chrome-140/` 与对应 `/areas/*/chrome-140.md`；如改策略，则隐藏或移除空目录。
3. 调整领域索引的统计字符串以区分单复数，并在领域页面 Front Matter 中加入领域名称，便于导航和 SEO。
4. 验证 quick links（如 Version Comparison）是否仍需保留，若保留则实现对应内容。
