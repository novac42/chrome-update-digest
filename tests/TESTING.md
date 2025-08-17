# 测试说明

本项目包含两个主要脚本的单元测试套件。

## 测试结构

```
tests/
├── __init__.py
├── test_process_enterprise_release.py  # 企业版发布说明处理器测试
├── test_convert.py                      # Chrome Digest 转换器测试
└── fixtures/                            # 测试数据
    ├── sample_enterprise_release_notes.md
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
pytest tests/test_process_enterprise_release.py -v

# 运行特定测试
pytest tests/test_convert.py::TestChromeDigestConverter::test_extract_version_info -v

# 生成覆盖率报告
pytest tests/ --cov=. --cov-report=html
```

### 使用 unittest
```bash
# 运行所有测试
python -m unittest discover tests

# 运行特定测试模块
python -m unittest tests.test_process_enterprise_release
```

## 测试覆盖范围

### test_process_enterprise_release.py
- 版本号提取
- 表格解析（当前和即将发布的功能）
- 功能状态识别（current/upcoming）
- 功能详情提取（描述、策略、平台）
- 特殊功能处理（新增/移除策略）
- 输出格式化和组织
- 完整文件处理流程

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