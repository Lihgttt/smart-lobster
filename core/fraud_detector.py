#!/usr/bin/env python3
"""
文本反诈检测模块
支持百度API + AI深度分析
"""

import httpx
import yaml
from pathlib import Path
from typing import Dict, Optional
from dataclasses import dataclass


@dataclass
class FraudCheckResult:
    """反诈检测结果"""
    risk_level: str  # high/medium/low/none
    risk_type: str
    confidence: float
    reason: str
    action: str  # block/warn/pass
    raw_response: Optional[Dict] = None


class FraudDetector:
    """反诈检测器"""
    
    def __init__(self):
        self.config = self._load_config()
        self.access_token = self.config["baidu"]["access_token"]
    
    def _load_config(self) -> Dict:
        """加载配置"""
        config_path = Path(__file__).parent.parent / "config" / "baidu_api.yaml"
        with open(config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    
    async def check_with_baidu(self, text: str) -> FraudCheckResult:
        """使用百度API检测"""
        url = self.config["endpoints"]["text_censor"]
        params = {"access_token": self.access_token}
        data = {"text": text}
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url,
                    params=params,
                    data=data,
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                    timeout=10
                )
                result = response.json()
                
                # 解析百度API响应
                return self._parse_baidu_result(result)
                
        except Exception as e:
            return FraudCheckResult(
                risk_level="unknown",
                risk_type="error",
                confidence=0,
                reason=f"API调用失败: {str(e)}",
                action="warn",
                raw_response=None
            )
    
    def _parse_baidu_result(self, result: Dict) -> FraudCheckResult:
        """解析百度API返回结果"""
        conclusion = result.get("conclusion", "合规")
        
        if conclusion == "不合规":
            data = result.get("data", [{}])[0]
            msg = data.get("msg", "未知风险")
            
            # 映射风险等级
            risk_map = {
                "存在涉政内容": ("high", "政治敏感"),
                "存在色情内容": ("high", "色情低俗"),
                "存在暴恐内容": ("high", "暴力恐怖"),
                "存在违禁内容": ("high", "违禁违规"),
                "存在广告内容": ("medium", "商业广告"),
                "存在辱骂内容": ("medium", "辱骂攻击"),
            }
            
            risk_level, risk_type = risk_map.get(msg, ("medium", "其他违规"))
            
            return FraudCheckResult(
                risk_level=risk_level,
                risk_type=risk_type,
                confidence=95.0,
                reason=msg,
                action="block" if risk_level == "high" else "warn",
                raw_response=result
            )
        
        return FraudCheckResult(
            risk_level="none",
            risk_type="正常",
            confidence=99.0,
            reason="内容合规",
            action="pass",
            raw_response=result
        )
    
    async def check_with_ai(self, text: str) -> FraudCheckResult:
        """使用AI深度分析（基于OpenClaw Agent）"""
        # 这里会调用你的Agent进行深度分析
        # 目前返回占位符，后续集成Agent
        return FraudCheckResult(
            risk_level="pending",
            risk_type="待AI分析",
            confidence=0,
            reason="需要AI深度分析",
            action="warn"
        )


# 测试代码
if __name__ == "__main__":
    import asyncio
    
    async def test():
        detector = FraudDetector()
        
        test_cases = [
            "你好，请问今天天气怎么样？",  # 正常
            "兼职刷单，日赚300，加微信xxx",  # 诈骗
            "点击链接领取免费iPhone",  # 可疑
        ]
        
        for text in test_cases:
            print(f"\n📝 检测文本: {text}")
            result = await detector.check_with_baidu(text)
            print(f"   风险等级: {result.risk_level}")
            print(f"   风险类型: {result.risk_type}")
            print(f"   置信度: {result.confidence}%")
            print(f"   建议操作: {result.action}")
    
    asyncio.run(test())
