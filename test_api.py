from api_client import BochaAPIClient

def main():
    # 创建API客户端实例
    client = BochaAPIClient()
    
    # 测试余额查询
    print("\n=== 测试余额查询 ===")
    balance_result = client.get_balance()
    print("余额查询结果:", balance_result)

    # 测试Web搜索
    print("\n=== 测试Web搜索 ===")
    web_search_result = client.web_search("Python编程")
    print("Web搜索结果:", web_search_result)

    # 测试AI搜索
    print("\n=== 测试AI搜索 ===")
    ai_search_result = client.ai_search("人工智能的发展趋势")
    print("AI搜索结果:", ai_search_result)

    # 测试Agent搜索
    print("\n=== 测试Agent搜索 ===")
    agent_search_result = client.agent_search("推荐一些Python学习资源")
    print("Agent搜索结果:", agent_search_result)

    # 测试语义重排
    print("\n=== 测试语义重排 ===")
    documents = [
        "Python是一种流行的编程语言",
        "JavaScript是网页开发的重要语言",
        "Python适合数据分析和人工智能开发"
    ]
    rerank_result = client.semantic_rerank("Python编程", documents)
    print("语义重排结果:", rerank_result)

if __name__ == "__main__":
    main()
