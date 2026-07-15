"""MCP 汇率工具 —— 接 exchangerate-api.com（免费，无需 API Key）"""

import requests


def get_exchange_rate(from_currency: str = "CNY", to_currency: str = "JPY") -> dict:
    """
    查汇率。传入货币代码：CNY=人民币 JPY=日元 EUR=欧元 USD=美元 THB=泰铢 SGD=新加坡元
    """
    try:
        url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
        resp = requests.get(url, timeout=10)
        data = resp.json()

        rate = data["rates"].get(to_currency)
        if rate is None:
            return {"error": f"不支持的货币: {to_currency}"}

        return {
            "from": from_currency,
            "to": to_currency,
            "rate": round(rate, 4),
            "updated": data.get("date", "unknown"),
            "description": f"1 {from_currency} = {round(rate,4)} {to_currency}",
        }
    except Exception:
        # API 挂了降级为常用汇率硬编码
        fallback = {
            ("CNY", "JPY"): 20.5,
            ("CNY", "EUR"): 0.128,
            ("CNY", "USD"): 0.138,
            ("CNY", "THB"): 4.95,
            ("CNY", "SGD"): 0.186,
        }
        rate = fallback.get((from_currency, to_currency))
        if rate is None:
            return {"error": f"不支持: {from_currency}→{to_currency}"}
        return {
            "from": from_currency,
            "to": to_currency,
            "rate": rate,
            "updated": "fallback",
            "description": f"1 {from_currency} ≈ {rate} {to_currency}（离线估算）",
        }
