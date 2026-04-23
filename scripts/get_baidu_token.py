#!/usr/bin/env python3
"""
获取百度智能云 Access Token
用法: python scripts/get_baidu_token.py
"""

import httpx
import yaml
import sys
from pathlib import Path


def load_config():
    """加载配置文件"""
    config_path = Path(__file__).parent.parent / "config" / "baidu_api.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_access_token(api_key: str, secret_key: str) -> dict:
    """调用百度API获取Access Token"""
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {
        "grant_type": "client_credentials",
        "client_id": api_key,
        "client_secret": secret_key
    }
    
    try:
        response = httpx.post(url, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPError as e:
        print(f"❌ 请求失败: {e}")
        return None


def main():
    print("🔑 百度智能云 Access Token 获取工具")
    print("=" * 50)
    
    # 加载配置
    config = load_config()
    api_key = config["baidu"]["api_key"]
    secret_key = config["baidu"]["secret_key"]
    
    # 检查是否已配置
    if api_key == "YOUR_API_KEY_HERE" or secret_key == "YOUR_SECRET_KEY_HERE":
        print("\n⚠️  请先配置 API Key 和 Secret Key")
        print("编辑文件: config/baidu_api.yaml")
        print("\n获取方式:")
        print("1. 访问 https://cloud.baidu.com")
        print("2. 控制台 → 内容审核 → 创建应用")
        print("3. 复制 API Key 和 Secret Key 到配置文件")
        sys.exit(1)
    
    print(f"\n📡 正在使用 API Key: {api_key[:8]}... 获取 Token")
    
    # 获取Token
    result = get_access_token(api_key, secret_key)
    
    if result and "access_token" in result:
        token = result["access_token"]
        expires_in = result.get("expires_in", 2592000)
        
        print(f"\n✅ 获取成功!")
        print(f"📝 Access Token: {token[:20]}...")
        print(f"⏰ 有效期: {expires_in // 86400} 天")
        
        # 更新配置文件
        config["baidu"]["access_token"] = token
        config["baidu"]["token_expires_at"] = expires_in
        
        config_path = Path(__file__).parent.parent / "config" / "baidu_api.yaml"
        with open(config_path, "w", encoding="utf-8") as f:
            yaml.dump(config, f, allow_unicode=True, sort_keys=False)
        
        print(f"\n💾 已自动更新到: config/baidu_api.yaml")
        print("\n🚀 现在可以运行反诈检测了!")
        
    else:
        print(f"\n❌ 获取失败")
        if result:
            print(f"错误信息: {result}")
        sys.exit(1)


if __name__ == "__main__":
    main()
