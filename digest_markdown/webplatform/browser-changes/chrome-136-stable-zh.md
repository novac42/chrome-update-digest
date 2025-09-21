# Chrome 136 稳定版 - 浏览器更改更新

## 区域摘要

Chrome 136 引入了现代化滚动条设计，作为视觉刷新计划的一部分。突出的更新是采用了与 Windows 11 设计语言保持一致的 Fluent 滚动条，不仅限于 Windows 平台，还扩展到了 Linux 平台。这种跨平台视觉一致性体现了 Chromium 对现代 UI 标准的承诺，同时保持了熟悉的功能性。此更新影响了覆盖式和非覆盖式滚动条实现，确保在不同操作系统和用户偏好下提供统一的用户体验。

## 详细更新

此版本专注于视觉现代化，通过单一但具有重大影响的浏览器界面增强功能，影响跨平台的基本滚动体验。

### Fluent Scrollbars

#### 新功能
Chrome 136 引入了遵循 Windows 11 Fluent 设计语言的现代化滚动条，覆盖 Windows 和 Linux 平台。覆盖式和非覆盖式滚动条变体都获得了视觉更新，创造了更现代且一致的浏览体验。

#### 技术细节
该实现更新了 Chromium 的滚动条渲染系统，以融入 Fluent 设计原则。非覆盖式 Fluent 滚动条在 Linux 和 Windows 上默认启用，确保跨平台一致性。设计更改适用于所有滚动条交互，同时保持现有功能和无障碍特性。

#### 使用场景
- **跨平台一致性**：用户在 Windows 或 Linux 上使用 Chrome 时体验统一的滚动条设计
- **现代 UI 对齐**：Web 应用程序和浏览器界面现在与当代操作系统设计语言保持一致
- **增强视觉体验**：更新的滚动条提供更精致和现代的浏览体验，而不改变功能行为

#### 参考资料
- [Tracking bug #1292117](https://bugs.chromium.org/p/chromium/issues/detail?id=1292117)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5023688844812288)