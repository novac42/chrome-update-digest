import asyncio
import os
import json
import sys
from pathlib import Path

# 确保可以引用项目源码
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from chrome_update_digest.mcp.tools.release_monitor import ReleaseMonitorTool

async def main():
    # 初始化工具，workspace_root 指向项目根目录
    workspace_root = Path(__file__).resolve().parents[1]
    tool = ReleaseMonitorTool(workspace_root)
    
    print(f"Checking updates in {workspace_root}...")
    
    # 模拟 MCP 请求参数
    # 如果你也关心 beta/dev，可以调整 channel 或多次调用
    check_args = {
        "release_type": "webplatform",
        "channel": "stable" 
    }
    
    # 调用核心检查逻辑
    # check_latest_releases 返回的是 JSON 字符串
    try:
        result_json = await tool.check_latest_releases(None, check_args)
        result = json.loads(result_json)
    except Exception as e:
        print(f"Error invoking check_latest_releases: {e}")
        sys.exit(1)
    
    if result.get("status") == "error":
        print(f"Error checking releases: {result.get('error')}")
        sys.exit(1)

    # 分析结果
    # ReleaseMonitorTool 会在 summary.missing_releases 里列出缺少的版本
    missing_releases = result.get("summary", {}).get("missing_releases", [])
    
    # 设置 GitHub Action Outputs
    github_output = os.environ.get("GITHUB_OUTPUT")
    
    if missing_releases:
        print(f"Found missing releases: {missing_releases}")
        msg = ", ".join(missing_releases)
        if github_output:
            with open(github_output, "a") as f:
                f.write("new_release_found=true\n")
                f.write(f"release_list={msg}\n")
    else:
        print("Everything is up to date.")
        if github_output:
            with open(github_output, "a") as f:
                f.write("new_release_found=false\n")

if __name__ == "__main__":
    asyncio.run(main())
