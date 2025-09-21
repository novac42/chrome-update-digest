# 性能摘要 - Chrome 136 稳定版

## 领域总结

Chrome 136 通过双模性能时序理解引入了 Web 应用性能测量能力的重大进展。此更新解决了性能监控中的关键缺口，帮助开发者识别和分析由应用程序控制范围之外的外部因素导致的性能变化。该功能通过区分不同的操作状态（如冷启动场景与热应用状态）实现更准确的性能评估。此增强功能在为开发者提供更细致的性能洞察方面代表了重要进步，允许更好的优化策略和更现实的性能预期。

## 详细更新

基于增强性能可见性的核心主题，此版本专注于为开发者提供更好的工具来理解真实世界性能模式的复杂性。

### Enable web applications to understand bimodal performance timings

#### 新功能
Web 应用现在可以通过增强的时序 API 更好地理解和分析页面加载性能中的双模分布模式。此功能有助于识别由应用程序直接控制范围之外的外部因素导致的性能变化。

#### 技术细节
该实现利用 Navigation Timing 规范提供更精细的性能数据，可以区分不同的系统状态。当用户代理执行"冷启动"时，昂贵的初始化任务会竞争系统资源，与热启动相比创建可测量的不同性能特征。该功能通过可以检测和报告这些双模模式的增强 API 暴露这些时序差异。

#### 用例
开发者可以使用此功能来：
- 构建更准确的性能监控仪表板，考虑系统状态变化
- 基于检测到的性能条件实现自适应加载策略
- 创建考虑冷启动场景的更现实的性能预算
- 通过根据检测到的性能模式调整应用程序行为来改善用户体验

#### 参考资料
- [Origin Trial](https://developer.chrome.com/origintrials/#/trials/active)
- [Tracking bug #1413848](https://bugs.chromium.org/p/chromium/issues/detail?id=1413848)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5037395062800384)
- [Spec](https://w3c.github.io/navigation-timing/)