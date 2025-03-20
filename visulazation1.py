import json
import folium

# 读取 enhanced_locations.json
with open('enhanced_locations.json', 'r') as f:
    data = json.load(f)

enhanced_locations = data["enhanced_locations"]

# 假设有 8 个地点，提取 center_location 和 name
locations = []
for location in enhanced_locations:
    center_location = location["center_location"]
    lat = float(center_location.split(",")[0][4:])  # 提取纬度
    lon = float(center_location.split(",")[1])      # 提取经度
    name = location["place_details"]["name"]        # 从 place_details 中获取 name
    locations.append({"lat": lat, "lon": lon, "name": name})

# 定义颜色映射（为不同 name 分配不同颜色）
# 这里假设有 8 个不同的 name，使用 8 种颜色
color_map = {
    locations[0]["name"]: "red",
    locations[1]["name"]: "blue",
    locations[2]["name"]: "green",
    locations[3]["name"]: "purple",
    locations[4]["name"]: "orange",
    locations[5]["name"]: "pink",
    locations[6]["name"]: "gray",
    locations[7]["name"]: "black"
}

# 如果 name 有重复，仍然使用对应颜色；如果少于 8 个唯一 name，未使用的颜色将被忽略

# 创建地图，中心设为第一个地点
m = folium.Map(location=[locations[0]["lat"], locations[0]["lon"]], zoom_start=12)

# 在地图上标记每个地点
for loc in locations:
    color = color_map.get(loc["name"], "blue")  # 如果 name 不在 color_map 中，默认蓝色
    folium.Marker(
        location=[loc["lat"], loc["lon"]],
        popup=loc["name"],  # 点击标记时显示 name
        icon=folium.Icon(color=color, icon="info-sign")
    ).add_to(m)

# 保存地图为 HTML 文件
m.save("location_map.html")

print("地图已生成并保存为 'location_map.html'，请打开查看。")