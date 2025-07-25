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

    def semantic_rerank(self, query, documents, model="gte-rerank", top_n=None, return_documents=False):
        """语义重排API
        
        使用博查语义重排模型对文档列表进行排序，根据查询与文档的语义相关性给出排序结果和得分。
        
        Args:
            query (str): 用户的搜索词，可以是自然语言
            documents (list): 需要排序的文档数组，最多50个文档
            model (str, optional): 排序使用的模型版本. 默认为"gte-rerank"
                可选值:
                - bocha-semantic-reranker-cn (邀测中)
                - bocha-semantic-reranker-en (邀测中)
                - gte-rerank (已开放，限时免费)
            top_n (int, optional): 排序返回的Top文档数量。默认与documents数量相同
            return_documents (bool, optional): 排序结果是否返回文档原文。默认False
        
        Returns:
            dict: 排序结果，包含模型信息和排序后的文档列表（带相关性得分）
                得分范围0-1，含义如下：
                0.75~1: 高度相关
                0.5~0.75: 相关但缺乏细节
                0.2~0.5: 部分相关
                0.1~0.2: 略微相关
                0~0.1: 不相关
        """
        try:
            # 验证参数
            if not query or not documents:
                print("错误：query和documents参数不能为空")
                return None
                
            if len(documents) > 50:
                print("错误：documents数量不能超过50个")
                return None
                
            # 构建请求体
            payload = {
                "model": model,
                "query": query,
                "documents": documents,
            }
            
            # 添加可选参数
            if top_n is not None:
                payload["top_n"] = top_n
            if return_documents is not None:
                payload["return_documents"] = return_documents
                
            response = requests.post(
                ENDPOINTS['semantic_rerank'],
                headers=self.headers,
                json=payload
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
            print(f"语义重排出错: {e}")
            return None
