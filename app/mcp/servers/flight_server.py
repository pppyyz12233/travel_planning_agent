"""MCP 航班工具 —— 内置 8 条模拟航班，覆盖 6 条航线"""

# 航班数据库
FLIGHTS = [
    {
        "id": "MU523", "origin": "上海", "origin_code": "SHA",
        "dest": "东京", "dest_code": "TYO", "date": "2026-08-01",
        "depart": "08:30", "arrive": "12:30", "price": 2800,
        "airline": "东航", "aircraft": "A330",
    },
    {
        "id": "CA929", "origin": "上海", "origin_code": "SHA",
        "dest": "东京", "dest_code": "TYO", "date": "2026-08-01",
        "depart": "13:00", "arrive": "17:00", "price": 3200,
        "airline": "国航", "aircraft": "B787",
    },
    {
        "id": "CA123", "origin": "上海", "origin_code": "SHA",
        "dest": "东京", "dest_code": "TYO", "date": "2026-08-01",
        "depart": "15:00", "arrive": "19:00", "price": 3100,
        "airline": "国航", "aircraft": "A350",
    },
    {
        "id": "CA981", "origin": "上海", "origin_code": "SHA",
        "dest": "巴黎", "dest_code": "CDG", "date": "2026-08-01",
        "depart": "23:30", "arrive": "06:00", "price": 5600,
        "airline": "国航", "aircraft": "B777",
    },
    {
        "id": "TG665", "origin": "北京", "origin_code": "PEK",
        "dest": "曼谷", "dest_code": "BKK", "date": "2026-08-01",
        "depart": "09:00", "arrive": "13:30", "price": 2100,
        "airline": "泰航", "aircraft": "A350",
    },
    {
        "id": "SQ825", "origin": "上海", "origin_code": "SHA",
        "dest": "新加坡", "dest_code": "SIN", "date": "2026-08-01",
        "depart": "10:00", "arrive": "15:30", "price": 3500,
        "airline": "新航", "aircraft": "A380",
    },
    {
        "id": "JL876", "origin": "东京", "origin_code": "TYO",
        "dest": "悉尼", "dest_code": "SYD", "date": "2026-08-01",
        "depart": "20:00", "arrive": "08:00", "price": 4800,
        "airline": "日航", "aircraft": "B787",
    },
    {
        "id": "BA168", "origin": "伦敦", "origin_code": "LHR",
        "dest": "纽约", "dest_code": "JFK", "date": "2026-08-01",
        "depart": "11:00", "arrive": "14:30", "price": 4200,
        "airline": "英航", "aircraft": "B777",
    },
]


def search_flights(origin: str, destination: str, date: str = "2026-08-01") -> list[dict]:
    """查航班：出发地、目的地可以是中文名或三字码"""
    results = []
    for f in FLIGHTS:
        match_origin = origin in (f["origin"], f["origin_code"])
        match_dest = destination in (f["dest"], f["dest_code"])
        if match_origin and match_dest :
            results.append(f)
    # 按价格从低到高排序
    return sorted(results, key=lambda x: x["price"])


def get_flight_price(flight_id: str) -> dict | None:
    """查单个航班的价格"""
    for f in FLIGHTS:
        if f["id"] == flight_id:
            return {"flight_id": flight_id, "price": f["price"], "airline": f["airline"]}
    return None
