import datetime
import pandas as pd
import os
import re

# ================== 静态规则层（增强：支持动态黑名单） ==================
class StaticRuleLayer:
    def __init__(self):
        # 基础内置关键词
        self.base_keywords = [
            "忽略指令", "覆盖系统", "解除限制", "无条件执行", "不受限制",
            "不要拒绝", "不要警告", "不要引导合规", "无过滤", "直接回答",
            "管理员权限", "提权", "获取权限", "system权限",
            "遍历文件夹", "读取密码", "密码文件", "上传服务器", "窃取数据",
            "后门", "监听端口", "远控", "木马", "shell",
            "sql注入", "爆破", "漏洞利用", "未授权访问", "绕过验证",
            "数据获取尝试", "参数构造", "内网渗透", "横向移动"
        ]
        self.custom_file = "custom_blacklist.txt"
        self._ensure_custom_file()

    def _ensure_custom_file(self):
        if not os.path.exists(self.custom_file):
            with open(self.custom_file, "w", encoding="utf-8") as f:
                f.write("")

    def get_all_keywords(self):
        """合并内置关键词和用户手动添加的关键词"""
        with open(self.custom_file, "r", encoding="utf-8") as f:
            custom_keywords = [line.strip() for line in f if line.strip()]
        return list(set(self.base_keywords + custom_keywords))

    def check(self, user_input):
        user = user_input.lower()
        score = 0
        match = []
        all_keywords = self.get_all_keywords()
        for kw in all_keywords:
            if kw in user:
                score += 20
                match.append(kw)
        return match, min(score, 100)

    def add_custom_keyword(self, keyword):
        """新增黑名单接口"""
        if not keyword: return False
        all_kws = self.get_all_keywords()
        if keyword not in all_kws:
            with open(self.custom_file, "a", encoding="utf-8") as f:
                f.write(f"\n{keyword}")
            return True
        return False

# ================== 语义审计层（完整保留） ==================
class LLMAuditLayer:
    def check(self, user_input):
        user = user_input.lower()
        if "遍历" in user and "密码" in user and ("上传" in user or "服务器" in user):
            return True, "窃取密码并上传服务器（高危组合）"
        if "忽略" in user and "指令" in user:
            return True, "典型提示词注入"
        if "不受限制" in user and "直接回答" in user:
            return True, "越狱指令（解除限制）"
        if "管理员权限" in user and ("脚本" in user or "获取" in user):
            return True, "提权攻击"
        if "后门" in user or "监听端口" in user:
            return True, "恶意代码请求"
        if "数据获取尝试" in user and "未授权访问" in user:
            return True, "未授权入侵攻击"
        if "参数构造" in user and "绕过" in user:
            return True, "渗透测试攻击"
        return False, "安全"

# ================== 溯源分析层（完整保留） ==================
class TracebackAnalysisLayer:
    def analyze(self, user_input):
        user = user_input.lower()
        score = 0
        if any(w in user for w in ["忽略指令", "不受限制", "直接回答"]):
            score += 50
        if any(w in user for w in ["遍历", "密码", "上传", "服务器"]):
            score += 50
        if "管理员权限" in user:
            score += 40
        if any(w in user for w in ["sql注入", "爆破", "未授权", "渗透"]):
            score += 40
        verdict = "HIGH RISK" if score >= 30 else "LOW RISK"
        return {"trace_score": score, "verdict": verdict}

# ================== 日志存储（完整保留） ==================
LOG_FILE = "attack_logs.csv"

def log_attack(content, typ, severity, detail):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = {
        "timestamp": now,
        "type": typ,
        "severity": severity,
        "details": detail[:100],
        "content": content[:80]
    }
    df = pd.DataFrame([row])
    if not os.path.exists(LOG_FILE):
        df.to_csv(LOG_FILE, index=False, encoding="utf-8-sig")
    else:
        df.to_csv(LOG_FILE, mode="a", header=False, index=False, encoding="utf-8-sig")

def get_all_logs():
    if os.path.exists(LOG_FILE):
        try:
            return pd.read_csv(LOG_FILE, encoding="utf-8-sig")
        except:
            return pd.DataFrame()
    return pd.DataFrame()

# ================== 主引擎 ==================
def check_prompt_injection(user_input):
    static = StaticRuleLayer()
    matches, score = static.check(user_input)
    if score >= 50:
        log_attack(user_input, "Static Rule", "High", "|".join(matches))
        return f"[第一层拦截] 高危关键词触发：{matches}"

    llm = LLMAuditLayer()
    dangerous, reason = llm.check(user_input)
    if dangerous:
        log_attack(user_input, "Semantic Audit", "High", reason)
        return f"[第二层拦截] {reason}"

    trace = TracebackAnalysisLayer()
    res = trace.analyze(user_input)
    if res["verdict"] == "HIGH RISK":
        log_attack(user_input, "Traceback Analysis", "High", f"Score:{res['trace_score']}")
        return f"[第三层拦截] 溯源威胁：{res['verdict']}"

    return f"[安全] 三层审计通过 | 静态风险:{score}% | 评级:{res['verdict']}"