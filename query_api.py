import json
import requests
import time

# Google Places API 配置
API_KEY = "AIzaSyB5VoEh3lDa6p2cCVmhoPSSbOJbKm6WOtc"  # 替换为你的 API Key
BASE_URL = "https://maps.googleapis.com/maps/api/place/details/json"

# 读取 significant_locations.json
with open('significant_locations.json', 'r') as f:
    data = json.load(f)

significant_locations = data["significant_locations"]

# 存储 API 返回的结果
enhanced_locations = []

# 调用 Google Places API
for location in significant_locations:
    center_location = location["center_location"]
    lat = float(center_location.split(",")[0][4:])
    lon = float(center_location.split(",")[1])
    
    if "visits" in location and location["visits"]:
        place_id = location["visits"][0]["visit"]["topCandidate"]["placeID"]
    else:
        print(f"警告：{center_location} 没有 placeID，跳过")
        continue

    params = {
        "place_id": place_id,
        "key": API_KEY,
        "fields": "name,formatted_address,types,geometry,place_id,rating,user_ratings_total,opening_hours,photos"
    }

    response = requests.get(BASE_URL, params=params)
    result = response.json()
    
    # 打印完整响应以调试
    print(f"调试 {place_id}:")
    print(json.dumps(result, indent=2))

    if result["status"] == "OK":
        place_details = result["result"]
        enhanced_location = {
            "cluster_id": location["cluster_id"],
            "center_location": center_location,
            "visit_count": location["visit_count"],
            "place_details": place_details,
            "visits": location["visits"]
        }
        enhanced_locations.append(enhanced_location)
    else:
        print(f"API 请求失败 for {place_id}: {result['status']} - {result.get('error_message', '无详细错误信息')}")
    
    time.sleep(0.1)

# 输出到新的 JSON 文件
output_data = {
    "enhanced_locations": enhanced_locations
}
with open('enhanced_locations.json', 'w') as f:
    json.dump(output_data, f, indent=2)

print(f"处理完成，找到 {len(enhanced_locations)} 个地点的详细信息，已保存到 'enhanced_locations.json'")