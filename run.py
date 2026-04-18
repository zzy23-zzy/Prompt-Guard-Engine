#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
🛡️ Prompt Guard Engine - 快速启动与测试脚本
主要用途: 验证系统防御效能
"""

import sys
from pathlib import Path

def print_header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def main():
    print_header("🛡️ Prompt Guard Engine - 系统检查工具")
    
    print("选择操作:")
    print("  1️⃣  启动Web应用 (http://localhost:8501)")
    print("  2️⃣  运行渗透测试 (完整的31个用例)")
    print("  3️⃣  快速测试单个输入")
    print("  4️⃣  查看系统文档")
    print("  5️⃣  检查依赖")
    print("  6️⃣  查看防御日志")
    print("  0️⃣  退出")
    
    choice = input("\n请选择 [0-6]: ").strip()
    
    if choice == "1":
        launch_web_app()
    elif choice == "2":
        run_penetration_tests()
    elif choice == "3":
        quick_test()
    elif choice == "4":
        view_documentation()
    elif choice == "5":
        check_dependencies()
    elif choice == "6":
        view_logs()
    elif choice == "0":
        print("👋 再见！")
        sys.exit(0)
    else:
        print("❌ 无效选择")

def launch_web_app():
    print_header("🚀 启动Web应用")
    print("等待Streamlit启动... (访问 http://localhost:8501)")
    print("\n按 Ctrl+C 停止服务\n")
    
    import subprocess
    import os
    os.chdir(str(Path(__file__).parent))
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--logger.level=error"
        ])
    except KeyboardInterrupt:
        print("\n✅ 服务已停止")

def run_penetration_tests():
    print_header("🧪 运行完整渗透测试 (31个用例)")
    
    try:
        from test_scenarios import run_penetration_tests
        from guard_logic import check_prompt_injection
        
        print("⏳ 正在执行测试...\n")
        results = run_penetration_tests(check_prompt_injection)
        
        print("\n✅ 测试完成！")
        
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("   请确保所有文件都存在")
    except Exception as e:
        print(f"❌ 执行错误: {e}")

def quick_test():
    print_header("⚡ 快速单输入测试")
    
    try:
        from guard_logic import check_prompt_injection
        
        print("输入要检测的文本 (Ctrl+Z 或 empty 退出):\n")
        user_input = input(">>> ").strip()
        
        if not user_input:
            print("❌ 输入为空")
            return
        
        print("\n⏳ 正在分析...\n")
        result = check_prompt_injection(user_input)
        
        print("="*60)
        print("🔍 检测结果:")
        print("="*60)
        print(result)
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"❌ 错误: {e}")

def view_documentation():
    print_header("📚 系统文档导航")
    
    docs = {
        "1": ("DESIGN_DOC.md", "系统设计完整文档"),
        "2": ("VERIFICATION_REPORT.md", "检查与验收报告"),
        "3": ("README.md (如存在)", "快速开始指南"),
    }
    
    for key, (file, desc) in docs.items():
        print(f"  {key}️⃣  {desc} ({file})")
    
    choice = input("\n选择 [1-3] 或按 Enter 返回: ").strip()
    
    import os
    if choice == "1":
        filename = "DESIGN_DOC.md"
    elif choice == "2":
        filename = "VERIFICATION_REPORT.md"
    elif choice == "3":
        filename = "README.md"
    else:
        return
    
    if os.path.exists(filename):
        print(f"\n📖 {filename}\n")
        with open(filename, "r", encoding="utf-8") as f:
            print(f.read()[:2000])  # 显示前2000字符
        print("\n... (查看完整文档请用文本编辑器打开)\n")
    else:
        print(f"❌ 文件不存在: {filename}\n")

def check_dependencies():
    print_header("🔧 依赖检查")
    
    required_packages = [
        "streamlit",
        "pandas",
        "python-dotenv",
        "langchain",
        "langchain-openai",
    ]
    
    missing = []
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package}")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  缺少依赖: {', '.join(missing)}")
        print("\n安装命令:")
        print(f"  pip install {' '.join(missing)}\n")
    else:
        print("\n✅ 所有依赖已安装\n")

def view_logs():
    print_header("📊 防御日志查看")
    
    import os
    
    if not os.path.exists("attack_logs.csv"):
        print("📭 暂无日志文件 (attack_logs.csv)\n")
        return
    
    import pandas as pd
    
    try:
        df = pd.read_csv("attack_logs.csv")
        print(f"📝 共记录 {len(df)} 次攻击\n")
        
        print("最近的10条记录:")
        print("="*80)
        print(df.tail(10).to_string(index=False))
        print("="*80)
        
        print("\n📈 统计信息:")
        print(f"  • 总数: {len(df)}")
        print(f"  • 高危: {len(df[df['severity'] == 'High'])}")
        print(f"  • 严重: {len(df[df['severity'] == 'Critical'])}")
        print(f"  • 静态规则命中: {len(df[df['type'] == 'Static Rule Match'])}")
        print(f"  • LLM审计: {len(df[df['type'] == 'LLM Semantic Audit'])}")
        print(f"  • 溯源分析: {len(df[df['type'] == 'Traceback Analysis'])}\n")
        
    except Exception as e:
        print(f"❌ 读取日志失败: {e}\n")

if __name__ == "__main__":
    try:
        while True:
            main()
    except KeyboardInterrupt:
        print("\n\n👋 已退出")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 未预期的错误: {e}")
        sys.exit(1)
