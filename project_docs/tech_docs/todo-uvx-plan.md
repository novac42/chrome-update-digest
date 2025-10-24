是的，可以使用 uvx 命令！让我解释两种方式的区别：
uvx vs uv run 的区别
1. 使用 uvx（工具执行模式）
{
  "mcpServers": {
    "chrome-digest": {
      "command": "uvx",
      "args": [
        "chrome-update-digest-mcp",
        "--base-path",
        "/path/to/chrome-update-digest"
      ]
    }
  }
}
uvx 特点：
用于运行已发布到 PyPI 的包或本地可安装的包
会创建临时隔离环境运行工具
适合运行独立的命令行工具
前提：包必须已经通过 uv pip install 或发布到 PyPI
2. 使用 uv run（项目执行模式）
{
  "mcpServers": {
    "chrome-digest": {
      "command": "uv",
      "args": [
        "run",
        "--project",
        "/path/to/chrome-update-digest",
        "chrome-update-digest-mcp",
        "--base-path",
        "/path/to/chrome-update-digest"
      ]
    }
  }
}
uv run 特点：
在项目的虚拟环境中运行
使用项目的所有依赖
适合开发环境
不需要先安装包
如何让 uvx 工作
要使用 uvx，你需要先安装这个包：
# 方式 1：本地开发安装
cd /path/to/chrome-update-digest
uv pip install -e .

# 方式 2：如果包已发布到 PyPI
uv pip install chrome-update-digest
安装后，就可以使用简化的 uvx 配置：
{
  "mcpServers": {
    "chrome-digest": {
      "command": "uvx",
      "args": [
        "chrome-update-digest-mcp",
        "--base-path",
        "/path/to/chrome-update-digest"
      ],
      "type": "stdio"
    }
  }
}
推荐
开发阶段：使用 uv run，因为它直接使用项目环境，修改代码后立即生效
生产环境：使用 uvx，因为它更简洁，且包已经稳定安装
你的 pm-studio-mcp 例子就是使用 uvx 运行已安装的工具，这种方式更简洁，但需要先安装包。