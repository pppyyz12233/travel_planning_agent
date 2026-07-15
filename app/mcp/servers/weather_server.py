"""MCP 天气工具 —— 接 wttr.in 真实天气（免费，无需 API Key）"""

import requests


def _fetch(city: str) -> dict:
    """调 wttr.in，拿原始 JSON 数据"""
    url = f"https://wttr.in/{city}?format=j1"
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    return resp.json()


def get_weather(city: str) -> dict:
    """查当前天气"""
    try:
        data = _fetch(city)
        cur = data["current_condition"][0]
        return {
            "city": city,
            "temp_c": cur["temp_C"],
            "weather": cur["weatherDesc"][0]["value"],
            "humidity": cur["humidity"],
            "wind_kmh": cur["windspeedKmph"],
            "feels_like": cur["FeelsLikeC"],
        }
    except Exception:
        # wttr.in 挂了时返回默认数据，不中断主流程
        return {
            "city": city,
            "temp_c": "N/A",
            "weather": "获取失败",
            "humidity": "N/A",
            "wind_kmh": "N/A",
            "feels_like": "N/A",
        }


def get_forecast(city: str, days: int = 3) -> list[dict]:
    """查未来几天预报"""
    try:
        data = _fetch(city)
        forecasts = []
        for day in data["weather"][:days]:
            forecasts.append({
                "date": day["date"],
                "max_c": day["maxtempC"],
                "min_c": day["mintempC"],
                "avg_c": day["avgtempC"],
                "sun_hours": day["sunHour"],
            })
        return forecasts
    except Exception:
        return []
