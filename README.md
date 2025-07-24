# Bocha API测试项目

这个项目提供了一个用于测试博查API接口的Python客户端实现。

## 项目结构

- `config.py`: 配置文件，包含API密钥和端点URL
- `api_client.py`: API客户端类实现
- `test_api.py`: API测试示例代码

## 使用说明

1. 首先在`config.py`中配置你的API密钥：
   ```python
   API_KEY = "your-api-key-here"  # 替换为你的实际API密钥
   ```

2. 安装依赖：
   ```bash
   pip install requests
   ```

3. 运行测试脚本：
   ```bash
   python test_api.py
   ```

## API接口说明

该客户端实现了以下API接口：

1. 余额查询 API
   - 用于查询账户余额
   - 方法：`get_balance()`

2. Web搜索 API
   - 用于执行网页搜索
   - 方法：`web_search(query, **params)`

3. AI搜索 API
   - 用于执行AI增强的搜索
   - 方法：`ai_search(query, **params)`

4. Agent搜索 API
   - 用于执行代理搜索
   - 方法：`agent_search(query, **params)`

5. 语义重排 API
   - 用于对文档进行语义重排序
   - 方法：`semantic_rerank(query, documents, **params)`

## 示例代码

```python
from api_client import BochaAPIClient

client = BochaAPIClient()

# 查询余额
balance = client.get_balance()

# 执行Web搜索
results = client.web_search("Python编程")
```

## 注意事项

- 使用前请确保已经获取了有效的API密钥
- 所有API调用都包含了基本的错误处理
- 可以通过传递额外的参数来自定义API调用
