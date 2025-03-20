import json
import matplotlib.pyplot as plt

# 读取 enhanced_locations.json
with open('enhanced_locations.json', 'r') as f:
    data = json.load(f)

enhanced_locations = data["enhanced_locations"]

# 提取 name 和 visit_count
names = [location["place_details"]["name"] for location in enhanced_locations]
visit_counts = [location["visit_count"] for location in enhanced_locations]
print(names)    
# 创建条形图
plt.figure(figsize=(10, 6))  # 设置图形大小
plt.bar(names, visit_counts, color='skyblue')  # 绘制条形图，颜色为天蓝色

# 设置图表标题和标签
plt.title('Visit Count by Location', fontsize=14)
plt.xlabel('Location Name', fontsize=12)
plt.ylabel('Visit Count', fontsize=12)

# 旋转横轴标签（避免重叠）
plt.xticks(rotation=45, ha='right')

# 调整布局，确保标签显示完整
plt.tight_layout()

# 保存为 PNG 文件
plt.savefig('visit_count_bar_chart.png')

# 显示图表（可选）
plt.show()

print("条形图已生成并保存为 'visit_count_bar_chart.png'")