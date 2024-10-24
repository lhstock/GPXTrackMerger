# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import os
import time
import sys
import numpy as np
from shapely.geometry import LineString

def douglas_peucker(points, epsilon):
    """使用 Douglas-Peucker 算法简化轨迹"""
    if len(points) <= 2:
        return points

    line = LineString(points)
    simplified = line.simplify(epsilon, preserve_topology=False)
    return list(simplified.coords)

def gpx_file_generator(directory, year):
    """生成器函数，用于遍历符合条件的GPX文件"""
    for root, dirs, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith('.gpx') and year in file_name:
                yield os.path.join(root, file_name)

def loading_animation(elapsed_time):
    """显示加载动画和已用时间"""
    animation = "|/-\\"
    idx = int(elapsed_time * 10) % len(animation)
    sys.stdout.write(f"\r处理中 {animation[idx]} 已用时间: {elapsed_time:.1f}秒")
    sys.stdout.flush()

def merge_gpx_files(directory, year='2024', epsilon=0.0001):
    # 创建GPX根元素并设置命名空间
    merged_root = ET.Element('gpx', version="1.1", creator="GPX Merger")
    namespace = {'gpx': 'http://www.topografix.com/GPX/1/1'}
    ET.register_namespace('', namespace['gpx'])

    start_time = time.time()
    file_count = 0
    total_points = 0
    simplified_points = 0

    for file_path in gpx_file_generator(directory, year):
        file_count += 1
        tree = ET.parse(file_path)
        root_node = tree.getroot()
        points = []
        for trkpt in root_node.findall('.//gpx:trkpt', namespace):
            lat = float(trkpt.get('lat'))
            lon = float(trkpt.get('lon'))
            points.append((lon, lat))  # 注意：shapely使用(lon, lat)顺序
        
        total_points += len(points)
        
        # 使用 Douglas-Peucker 算法简化轨迹
        simplified = douglas_peucker(points, epsilon)
        simplified_points += len(simplified)
        
        # 将简化后的点添加到合并的根节点
        trk = ET.SubElement(merged_root, 'trk')
        trkseg = ET.SubElement(trk, 'trkseg')
        for lon, lat in simplified:  # 注意：这里需要交换回(lat, lon)顺序
            trkpt = ET.SubElement(trkseg, 'trkpt', attrib={'lat': str(lat), 'lon': str(lon)})
        
        # 显示加载动画和已用时间
        elapsed_time = time.time() - start_time
        loading_animation(elapsed_time)

    # 自动生成输出文件名
    output_file = f'merged{year}.gpx'
    
    # 使用minidom来格式化XML并写入文件
    xmlstr = minidom.parseString(ET.tostring(merged_root)).toprettyxml(indent="  ")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(xmlstr)
    
    # 显示完成信息
    elapsed_time = time.time() - start_time
    print(f"\n处理完成！共处理 {file_count} 个文件，用时 {elapsed_time:.1f} 秒")
    print(f"原始点数：{total_points}，简化后点数：{simplified_points}")
    print(f"简化率：{(1 - simplified_points / total_points) * 100:.2f}%")

# 示例用法
merge_gpx_files('./apple_health_export/workout-routes', year='2024', epsilon=0.0001)
