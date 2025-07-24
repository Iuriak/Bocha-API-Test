import requests
import json
from config import API_KEY, ENDPOINTS

class BochaAPIClient:
    def __init__(self):
        self.headers = {
            'Authorization': f'Bearer {API_KEY}',
            'Content-Type': 'application/json'
        }
    
    def get_balance(self):
        """查询账户余额"""
        try:
            response = requests.get(ENDPOINTS['balance'], headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error querying balance: {e}")
            return None
    
    def web_search(self, query, freshness="noLimit", summary=False, count=10, include=None, exclude=None):
        """Web搜索API
        
        Args:
            query (str): 搜索关键词
            freshness (str, optional): 搜索时间范围. 可选值: "noLimit"(默认), "oneDay", "oneWeek", "oneMonth", "oneYear"
                                     也可以是具体日期范围："2025-01-01..2025-04-06" 或具体日期："2025-04-06"
            summary (bool, optional): 是否显示文本摘要. 默认False
            count (int, optional): 返回结果数量, 范围1-50. 默认10
            include (str, optional): 指定搜索的网站范围, 如"qq.com|m.163.com"
            exclude (str, optional): 排除搜索的网站范围, 如"qq.com|m.163.com"
        
        Returns:
            dict: 搜索结果，包含网页、图片等信息
        """
        try:
            # 构建请求参数
            payload = {
                "query": query,
                "freshness": freshness,
                "summary": summary,
                "count": min(max(count, 1), 50)  # 确保count在1-50范围内
            }
            
            # 添加可选参数
            if include:
                payload["include"] = include
            if exclude:
                payload["exclude"] = exclude
                
            response = requests.post(
                ENDPOINTS['web_search'],
                headers=self.headers,
                data=json.dumps(payload)  # 使用data参数并序列化为JSON
            )
            
            # 处理常见错误
            if response.status_code == 400:
                if "Missing parameter" in response.text:
                    print("错误: 请求参数缺失")
                elif "API KEY is missing" in response.text:
                    print("错误: Header缺少Authorization")
                return None
            elif response.status_code == 401:
                print("错误: API KEY无效")
                return None
            elif response.status_code == 403:
                print("错误: 账户余额不足，请前往 https://open.bochaai.com 充值")
                return None
            elif response.status_code == 429:
                print("错误: 达到请求频率限制")
                return None
            elif response.status_code == 500:
                print("错误: 服务器内部错误")
                return None
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Web搜索出错: {e}")
            return None

    def ai_search(self, query, **params):
        """AI搜索API"""
        try:
            response = requests.post(
                ENDPOINTS['ai_search'],
                headers=self.headers,
                json={'query': query, **params}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error in AI search: {e}")
            return None

    def agent_search(self, query, **params):
        """Agent搜索API"""
        try:
            response = requests.post(
                ENDPOINTS['agent_search'],
                headers=self.headers,
                json={'query': query, **params}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error in agent search: {e}")
            return None

    def semantic_rerank(self, query, documents, **params):
        """语义重排API"""
        try:
            response = requests.post(
                ENDPOINTS['semantic_rerank'],
                headers=self.headers,
                json={
                    'query': query,
                    'documents': documents,
                    **params
                }
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error in semantic rerank: {e}")
            return None
