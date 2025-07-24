from api_client import BochaAPIClient
from pprint import pprint

def test_web_search():
    client = BochaAPIClient()
    
    # 测试基本搜索
    print("\n=== 测试基本搜索 ===")
    results = client.web_search("Python编程")
    if results:
        print(f"找到约 {results.get('data', {}).get('webPages', {}).get('totalEstimatedMatches', 0)} 个结果")
        # 打印第一个结果
        if results.get('data', {}).get('webPages', {}).get('value'):
            first_result = results['data']['webPages']['value'][0]
            print("\n第一个搜索结果:")
            print(f"标题: {first_result.get('name')}")
            print(f"URL: {first_result.get('url')}")
            print(f"摘要: {first_result.get('snippet')}")
    
    # 测试带摘要的搜索
    print("\n=== 测试带摘要的搜索 ===")
    results = client.web_search("Python机器学习", summary=True, count=2)
    if results:
        web_pages = results.get('data', {}).get('webPages', {}).get('value', [])
        for page in web_pages:
            print(f"\n标题: {page.get('name')}")
            print(f"摘要: {page.get('summary', '无摘要')}")
    
    # 测试时间范围搜索
    print("\n=== 测试时间范围搜索（一周内） ===")
    results = client.web_search("人工智能新闻", freshness="oneWeek", count=3)
    if results:
        web_pages = results.get('data', {}).get('webPages', {}).get('value', [])
        for page in web_pages:
            print(f"\n标题: {page.get('name')}")
            print(f"发布时间: {page.get('datePublished')}")
    
    # 测试特定网站搜索
    print("\n=== 测试特定网站搜索 ===")
    results = client.web_search(
        "深度学习",
        include="csdn.net",
        count=2
    )
    if results:
        web_pages = results.get('data', {}).get('webPages', {}).get('value', [])
        for page in web_pages:
            print(f"\n标题: {page.get('name')}")
            print(f"网站: {page.get('siteName')}")
    
    # 测试排除特定网站
    print("\n=== 测试排除特定网站 ===")
    results = client.web_search(
        "Python教程",
        exclude="csdn.net",
        count=2
    )
    if results:
        web_pages = results.get('data', {}).get('webPages', {}).get('value', [])
        for page in web_pages:
            print(f"\n标题: {page.get('name')}")
            print(f"网站: {page.get('siteName')}")

if __name__ == "__main__":
    test_web_search()
