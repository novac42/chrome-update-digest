# 测试说明

本项目包含WebPlatform相关功能的单元测试套件。

## 测试结构

```
tests/
├── __init__.py
├── test_release_monitor_unit.py         # 发布监控核心功能单元测试
├── test_release_monitor.py              # 发布监控集成测试
├── test_fastmcp_basic.py                # FastMCP基础功能测试
├── test_fastmcp_error_handling.py       # FastMCP错误处理测试
├── test_fastmcp_html.py                 # FastMCP HTML生成测试
├── test_direct_tools.py                 # 直接工具调用测试
├── test_convert.py                      # Chrome Digest 转换器测试
└── fixtures/                            # 测试数据
    └── sample_digest_markdown.md
```

## 运行测试

### 使用测试运行脚本
```bash
python tests/run_tests.py
```

### 使用 pytest
```bash
# 运行所有测试
pytest tests/ -v

# 运行特定测试文件
pytest tests/test_release_monitor_unit.py -v

# 运行特定测试
pytest tests/test_fastmcp_basic.py::test_load_prompt_resources -v

# 生成覆盖率报告
pytest tests/ --cov=. --cov-report=html
```

### 使用 unittest
```bash
# 运行所有测试
python -m unittest discover tests

# 运行特定测试模块
python -m unittest tests.test_release_monitor_unit
```

## 测试覆盖范围

### test_release_monitor_unit.py
- ReleaseMonitorCore核心功能测试
- 版本扫描和检测
- WebPlatform和WebGPU版本处理
- 文件系统操作和版本追踪
- MCP工具包装器测试

### test_fastmcp_*.py 系列
- FastMCP服务器基础功能测试
- WebPlatform digest生成
- HTML转换和模板渲染
- 错误处理和边界情况
- 资源加载和文件操作

### test_convert.py
- 文件名版本信息提取
- Markdown 章节解析
- HTML 处理功能：
  - H3 标题卡片包装
  - 链接处理和分类
- 内容处理管道
- 单文件转换
- 批量文件转换
- 增量转换逻辑
- 版本管理和排序

### test_release_monitor.py
- 发布监控集成测试
- 版本检测和缺失分析
- WebPlatform和WebGPU版本追踪

## 依赖项

测试依赖已添加到 `requirements.txt`：
- pytest>=7.0.0
- pytest-cov>=4.0.0
- unittest-xml-reporting>=3.0.0

## 注意事项

1. 测试在虚拟环境中运行，确保先激活虚拟环境：
   ```bash
   source .venv/bin/activate
   ```

2. 测试使用临时文件和目录，运行后会自动清理

3. 某些测试需要模板文件，测试会自动创建必要的模拟模板

4. 测试专注于WebPlatform功能，不包含Enterprise相关代码

5. FastMCP相关测试需要相应的依赖包，请确保已安装fastmcp