#!/usr/bin/env python3
"""
智慧龙虾开发工作流管理工具
Usage: python scripts/dev_workflow.py [command]
"""

import sys
import subprocess
import argparse
from pathlib import Path
from typing import List


class WorkflowManager:
    """开发工作流管理器"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        
    def run_command(self, cmd: List[str], description: str) -> bool:
        """运行命令并显示结果"""
        print(f"\n{'='*60}")
        print(f"🚀 {description}")
        print(f"{'='*60}")
        print(f"$ {' '.join(cmd)}\n")
        
        result = subprocess.run(cmd, cwd=self.project_root)
        if result.returncode != 0:
            print(f"❌ {description} 失败")
            return False
        print(f"✅ {description} 完成")
        return True
    
    def format_code(self) -> bool:
        """格式化代码"""
        return self.run_command(
            ["python", "-m", "black", ".", "--line-length", "100"],
            "代码格式化 (black)"
        )
    
    def lint_code(self) -> bool:
        """代码检查"""
        return self.run_command(
            ["python", "-m", "flake8", ".", "--max-line-length", "100"],
            "代码检查 (flake8)"
        )
    
    def run_tests(self) -> bool:
        """运行测试"""
        return self.run_command(
            ["python", "-m", "pytest", "tests/", "-v", "--tb=short"],
            "运行测试 (pytest)"
        )
    
    def check_all(self) -> bool:
        """完整检查流程"""
        print("\n" + "="*60)
        print("🔍 开始完整代码检查流程")
        print("="*60)
        
        steps = [
            (self.format_code, "格式化"),
            (self.lint_code, "检查"),
            (self.run_tests, "测试"),
        ]
        
        for step_func, step_name in steps:
            if not step_func():
                print(f"\n❌ {step_name} 步骤失败，停止检查")
                return False
        
        print("\n" + "="*60)
        print("✅ 所有检查通过！可以提交代码了")
        print("="*60)
        return True
    
    def git_push(self, message: str = None) -> bool:
        """Git 提交并推送"""
        if not message:
            message = input("请输入提交信息: ")
        
        commands = [
            (["git", "add", "."], "添加更改"),
            (["git", "commit", "-m", message], "提交更改"),
            (["git", "push", "origin", "main"], "推送到远程"),
        ]
        
        for cmd, desc in commands:
            if not self.run_command(cmd, desc):
                return False
        
        print("\n✅ 代码已推送到 GitHub")
        print("   主机执行: git pull origin main")
        return True
    
    def sync_to_host(self) -> bool:
        """同步到主机"""
        print("\n" + "="*60)
        print("🔄 同步代码到主机")
        print("="*60)
        
        # 先检查
        if not self.check_all():
            print("\n⚠️  检查未通过，是否继续推送? (y/n)")
            response = input().lower()
            if response != 'y':
                return False
        
        # 获取提交信息
        message = input("\n请输入提交信息: ")
        if not message:
            message = "Update from VM"
        
        return self.git_push(message)


def main():
    parser = argparse.ArgumentParser(
        description="智慧龙虾开发工作流管理工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python scripts/dev_workflow.py format    # 格式化代码
  python scripts/dev_workflow.py lint      # 代码检查
  python scripts/dev_workflow.py test      # 运行测试
  python scripts/dev_workflow.py check     # 完整检查
  python scripts/dev_workflow.py push      # 提交并推送
  python scripts/dev_workflow.py sync      # 检查+推送（推荐）
        """
    )
    
    parser.add_argument(
        "command",
        choices=["format", "lint", "test", "check", "push", "sync"],
        help="要执行的命令"
    )
    
    args = parser.parse_args()
    
    manager = WorkflowManager()
    
    commands = {
        "format": manager.format_code,
        "lint": manager.lint_code,
        "test": manager.run_tests,
        "check": manager.check_all,
        "push": manager.git_push,
        "sync": manager.sync_to_host,
    }
    
    success = commands[args.command]()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()