import json
import pandas as pd
from sklearn.cluster import DBSCAN
from math import radians, sin, cos, sqrt, atan2
import numpy as np

# Haversine 距离公式
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # 地球半径（公里）
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c * 1000  # 返回米

# 读取 location-history.json
with open('location-history.json', 'r') as f:
    data = json.load(f)

# 提取 visit 数据
visits = [entry for entry in data if "visit" in entry]
visit_data = []
for visit in visits:
    place_location = visit["visit"]["topCandidate"]["placeLocation"]
    lat = float(place_location.split(",")[0][4:])
    lon = float(place_location.split(",")[1])
    visit_data.append({
        "lat": lat,
        "lon": lon,
        "placeID": visit["visit"]["topCandidate"]["placeID"],
        "semanticType": visit["visit"]["topCandidate"]["semanticType"],
        "startTime": visit["startTime"],
        "endTime": visit["endTime"],
        "original_entry": visit
    })

df = pd.DataFrame(visit_data)

# 聚类（最大距离 1000 米）
coords = df[["lat", "lon"]].values
eps_in_radians = 1000 / (6371 * 1000)  # 100 米转换为弧度
db = DBSCAN(eps=eps_in_radians, min_samples=1, metric="haversine").fit(np.radians(coords))
df["cluster"] = db.labels_

# 统计每个簇的访问次数
cluster_counts = df.groupby("cluster").size().reset_index(name="visit_count")

# 筛选访问次数 >= 3 的簇
significant_clusters = cluster_counts[cluster_counts["visit_count"] >= 3]["cluster"]

# 输出结果
significant_locations = []
for cluster_id in significant_clusters:
    cluster_data = df[df["cluster"] == cluster_id]
    center_lat = cluster_data["lat"].mean()
    center_lon = cluster_data["lon"].mean()
    visits_in_cluster = cluster_data["original_entry"].tolist()
    significant_locations.append({
        "cluster_id": int(cluster_id),
        "center_location": f"geo:{center_lat},{center_lon}",
        "visit_count": int(cluster_counts[cluster_counts["cluster"] == cluster_id]["visit_count"].values[0]),
        "visits": visits_in_cluster
    })

# 保存到 JSON 文件
output_data = {"significant_locations": significant_locations}
with open('significant_locations.json', 'w') as f:
    json.dump(output_data, f, indent=2)

print(f"找到 {len(significant_locations)} 个访问次数 >= 3 的地点，已保存到 'significant_locations.json'")