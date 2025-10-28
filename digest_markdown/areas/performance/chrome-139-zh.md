---
layout: default
title: chrome-139-zh
---

## 领域摘要

Chrome 139 (stable) 通过将后台页面及其关联 workers 在被冻结前的时间从五分钟缩短为一分钟，强化了 Android 上的后台资源控制。此更改是本次发布中与性能相关的主要主题，对依赖长期后台执行的开发者影响最大。通过减少移动设备的空闲 CPU 和电池使用量，它推动了 Web 平台 的进步。团队应将长时间运行的后台任务视为易失，并适应更积极的冻结行为。

## 详细更新

以下是与上述摘要相关的、以性能为重点的更新。

### Faster background freezing on Android（Android 上更快的后台冻结）

#### 新增内容
将 Android 上后台页面（及其关联 workers）被冻结的时间从五分钟缩短为一分钟。

#### 技术细节
Chrome 现在将 Android 上冻结非活动后台上下文的阈值降至一分钟，强制更早地暂停后台页面及与之相关的任何 workers。可通过下列链接获取跟踪和状态信息。

#### 适用场景
- 执行后台处理的移动网站和应用应假定连续执行的时间窗口更短，并将工作迁移到前台交互或服务器端处理。  
- 后台定时器、长时间运行的 WebWorkers 或任何后台轮询逻辑可能会更早被冻结；在需要时使用前台触发器、推送消息或其他平台机制来恢复工作。  
- 总体好处是降低 Android 设备的 CPU 和电池消耗，提升感知性能和设备寿命。

#### 参考资料
- [Tracking bug](https://issues.chromium.org/issues/435623337)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5386725031149568)

保存路径：`digest_markdown/webplatform/Performance/chrome-139-stable-en.md`
