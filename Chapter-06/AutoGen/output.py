'''
Author: NanluQingshi
Date: 2026-07-12 23:51:39
LastEditors: NanluQingshi
LastEditTime: 2026-07-12 23:51:42
Description: AutoGen 输出价格监控页面
'''
import streamlit as st
import requests
import logging
from datetime import datetime

# 配置日志
logging.basicConfig(level=logging.INFO)

API_URL = "https://api.binance.com/api/v3/ticker/24hr"
SYMBOL = "BTCUSDT"
REQUEST_TIMEOUT = 10

def fetch_price_data():
    try:
        resp = requests.get(API_URL, params={"symbol": SYMBOL}, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
        price = float(data["lastPrice"])
        change_amount = float(data["priceChange"])
        change_percent = float(data["priceChangePercent"])
        return {
            "price": price,
            "change_amount": change_amount,
            "change_percent": change_percent,
            "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    except requests.exceptions.RequestException as e:
        logging.error(f"网络请求异常: {e}")
        raise RuntimeError("网络连接出现问题，请稍后重试。")
    except Exception as e:
        logging.error(f"数据解析错误: {e}")
        raise RuntimeError("数据格式异常，无法解析价格。")

def main():
    st.set_page_config(page_title="比特币价格监控", page_icon="₿", layout="centered")
    st.title("₿ 比特币实时价格 (USD)")

    if "price_data" not in st.session_state:
        st.session_state.price_data = None
    if "error" not in st.session_state:
        st.session_state.error = None

    col1, col2 = st.columns([1, 3])
    with col1:
        refresh = st.button("🔄 刷新价格", use_container_width=True)
    with col2:
        if st.session_state.price_data:
            st.caption(f"最后更新: {st.session_state.price_data['last_update']}")

    # 数据获取逻辑
    if refresh or st.session_state.price_data is None:
        with st.spinner("加载中..."):
            try:
                st.session_state.price_data = fetch_price_data()
                st.session_state.error = None
            except Exception as e:
                st.session_state.error = str(e)

    if st.session_state.error:
        st.error(f"⚠️ {st.session_state.error}")

    if st.session_state.price_data:
        data = st.session_state.price_data
        price = data["price"]
        change_amount = data["change_amount"]
        change_percent = data["change_percent"]

        # 使用 st.metric 展示价格与变化
        st.metric(
            label="当前价格 (USD)",
            value=f"${price:,.2f}",
            delta=f"{change_amount:+.2f} ({change_percent:+.2f}%)"
        )
        st.divider()
        st.caption("数据来源: Binance公开API")
    elif not st.session_state.error:
        st.info("正在连接服务...")  # 仅在无数据且无错误时提示

if __name__ == "__main__":
    main()