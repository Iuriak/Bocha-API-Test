"""
配置文件，存储API密钥和基础URL
"""

# 在这里替换为你的API密钥
API_KEY = "your-api-key-here"

# API基础URL
BASE_URL = "https://api.bochaai.com"

# API版本
API_VERSION = "v1"

# API端点
ENDPOINTS = {
    "balance": f"{BASE_URL}/{API_VERSION}/fund/remaining",
    "web_search": f"{BASE_URL}/{API_VERSION}/web/search",
    "ai_search": f"{BASE_URL}/{API_VERSION}/ai/search",
    "agent_search": f"{BASE_URL}/{API_VERSION}/agent/search",
    "semantic_rerank": f"{BASE_URL}/{API_VERSION}/semantic/rerank"
}
