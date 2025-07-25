import streamlit as st
import json
from api_client import BochaAPIClient
from config import BASE_URL

def display_json(data):
    """格式化显示JSON数据"""
    if data:
        st.code(
            json.dumps(data, indent=2, ensure_ascii=False),
            language="json"
        )
    else:
        st.error("请求失败，未返回数据")

def main():
    st.set_page_config(
        page_title="博查API测试工具",
        page_icon="🔍",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # 自定义CSS样式
    st.markdown("""
        <style>
        .main {
            max-width: 1200px;
            margin: 0 auto;
            padding: 1rem;
        }
        .stButton>button {
            width: 100%;
        }
        .block-container {
            max-width: 95%;
            padding-top: 1rem;
            padding-right: 1rem;
            padding-left: 1rem;
            padding-bottom: 1rem;
        }
        
        /* 设置基础列样式 */
        [data-testid="column"] {
            padding: 0;
        }
        
        /* 设置左列的滚动 */
        [data-testid="column"]:first-child {
            position: fixed;
            left: 0;
            width: calc(50% - 1rem);
            height: calc(100vh - 80px);
            overflow-y: auto;
            padding: 1rem;
        }
        
        /* 设置右列的滚动 */
        [data-testid="column"]:last-child {
            position: fixed;
            right: 0;
            width: calc(50% - 1rem);
            height: calc(100vh - 80px);
            overflow-y: auto;
            padding: 1rem;
            border-left: 1px solid #e6e6e6;
            background-color: white;
        }
        
        /* 修改代码块的样式 */
        .stCode {
            max-height: 300px !important;
            overflow-y: auto !important;
            margin: 0.5rem 0;
        }
        
        /* JSON显示框的样式 */
        .element-container div.stJson {
            max-height: calc(100vh - 200px) !important;
            overflow-y: auto !important;
            background-color: #f0f2f6 !important;
            border-radius: 4px !important;
            margin-top: 0.5rem !important;
        }
        
        /* 设置响应区域的样式 */
        .element-container {
            margin-bottom: 0.5rem;
        }
        
        /* 调整expander内部间距 */
        .streamlit-expanderHeader {
            padding: 0.5rem;
        }
        .streamlit-expanderContent {
            padding: 0.5rem;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # 创建容器来控制主界面宽度
    with st.container():
        st.header("Web Search API")
    
    # 创建两列布局
    col1, col2 = st.columns(2)
    
    # 初始化右侧响应区域
    with col2:
        st.subheader("响应结果")
        response_container = st.container()
        
    with col1:
        api_key = st.text_input("API Key", placeholder="API KEY请先前往https://open.bochaai.com获取", type="password")

        st.subheader("请求参数")

        # Full Request URL
        st.text_input(
            "Request URL",
            value="{}/v1/web-search".format(BASE_URL),
            disabled=True
        )

        # 查询参数
        query = st.text_input("搜索关键词", placeholder="输入要搜索的内容")
        
        # 高级参数（可折叠）
        with st.expander("高级参数"):
            freshness = st.selectbox(
                "时间范围",
                ["noLimit", "oneDay", "oneWeek", "oneMonth", "oneYear"],
                index=0
            )
            
            summary = st.checkbox("显示摘要", value=False)
            
            count = st.slider("返回结果数量", min_value=1, max_value=50, value=10)
            
            include = st.text_input(
                "包含搜索网站",
                placeholder="例如：qq.com|m.163.com"
            )
            
            exclude = st.text_input(
                "排除搜索网站",
                placeholder="例如：qq.com|m.163.com"
            )
        
        # 显示请求信息
        with st.expander("完整请求信息", expanded=True):
            # Headers
            with st.expander("Headers"):
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
                st.code(json.dumps(headers, indent=2, ensure_ascii=False), language="json")
            
            # Request Body
            with st.expander("Request Body", expanded=True):
                request_body = {
                    "query": query,
                    "freshness": freshness,
                    "summary": summary,
                    "count": count
                }
                if include:
                    request_body["include"] = include
                if exclude:
                    request_body["exclude"] = exclude
                    
                st.code(json.dumps(request_body, indent=2, ensure_ascii=False), language="json")
            
        
        # 创建按钮列
        col1_1, col1_2 = st.columns(2)
        
        # 发送请求按钮
        with col1_1:
            search_clicked = st.button("发送请求", type="primary")
        
        # Reranker按钮（初始状态禁用）
        with col1_2:
            # 使用会话状态存储搜索结果
            if 'search_results' not in st.session_state:
                st.session_state.search_results = None
                
            # 只有当有搜索结果时才启用Reranker按钮
            rerank_clicked = st.button(
                "语义重排",
                disabled=not st.session_state.search_results,
                help="对搜索结果进行语义重排序，提升相关性"
            )
        
        if search_clicked:
            if not query:
                st.error("请输入搜索关键词")
            else:
                with st.spinner("搜索中..."):
                    client = BochaAPIClient()
                    results = client.web_search(
                        apiKey=api_key,
                        query=query,
                        freshness=freshness,
                        summary=summary,
                        count=count,
                        include=include or None,
                        exclude=exclude or None
                    )
                    
                    # 存储搜索结果
                    st.session_state.search_results = results
                    # 在右侧显示响应
                    response_container.json(results)
        
        if rerank_clicked and st.session_state.search_results:
            with st.spinner("重排中..."):
                # 从搜索结果中提取snippets
                web_pages = st.session_state.search_results.get('data', {}).get('webPages', {}).get('value', [])
                documents = [page.get('snippet', '') for page in web_pages if page.get('snippet')]
                
                if documents:
                    client = BochaAPIClient()
                    rerank_results = client.semantic_rerank(
                        apiKey=api_key,
                        query=query,
                        documents=documents,
                        model="gte-rerank",
                        return_documents=True
                    )
                    
                    if rerank_results:
                        # 在右侧显示重排结果
                        response_container.json(rerank_results)

if __name__ == "__main__":
    main()
