# GPXTrackMerger

GPXTrackMerger 是一个用于处理和合并 iOS 健身数据中的 GPX 轨迹文件的 Python 工具。它使用 Douglas-Peucker 算法来简化轨迹，并将多个 GPX 文件合并为一个单一的文件，方便查看和分析长期的运动轨迹数据。

主要功能：
- 从指定目录读取 GPX 文件
- 使用 Douglas-Peucker 算法简化轨迹点
- 合并多个 GPX 文件为一个文件
- 提供处理进度和统计信息

这个工具特别适合那些想要分析和可视化长期健身数据的 iOS 用户。

## 项目结构

- `apple_health_export_main.py`: 主 Python 脚本，用于提取、合并和过滤 GPX 文件。
- `apple_health_export/`: 存储导出的 iOS 健身数据的目录。
- `merged2024.gpx`: 合并后的 2024 年 GPX 文件输出。
- `.vscode/launch.json`: VS Code 的调试配置文件。

## 先决条件

在运行此项目之前，请确保已安装以下软件：

- Python 3.x
- `scikit-learn` 库：用于 DBSCAN 聚类
- Visual Studio Code（可选）：用于编辑和调试代码

## 安装

1. 克隆或下载此项目到本地。
2. 安装所需的 Python 库：

   ```bash
   pip install scikit-learn
   ```

## 使用方法

1. 将导出的 iOS 健身数据放入 `apple_health_export/` 目录中。
2. 确保所有 GPX 文件位于 `apple_health_export/workout-routes/` 目录中。
3. 打开 `apple_health_export_main.py` 并根据需要调整参数。
4. 使用以下命令运行脚本：

   ```bash
   python apple_health_export_main.py
   ```

   或者在 Visual Studio Code 中，使用配置好的 `launch.json` 进行调试运行。

## 查看合并后的轨迹

合并后的 GPX 文件可以通过 [gpx.studio](https://gpx.studio/app#1.17/0/0) 导入查看。只需打开网站并上传 `merged2024.gpx` 文件，即可查看对应的轨迹数据。

## 注意事项

- 当前脚本仅处理文件名中包含“2024”的 GPX 文件。
- 可以通过调整 `filter_points_with_dbscan` 函数中的 `eps` 和 `min_samples` 参数来优化聚类效果。

## 贡献

欢迎提交问题和请求。请通过 GitHub 提交。

## 许可证

此项目采用 MIT 许可证。
