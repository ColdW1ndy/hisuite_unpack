import sqlite3
import os

# 打开SQLite数据库文件
db_path = ''#你需要解密的app备份的db路径
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 查询apk_file_data表中所有数据，并按file_index和data_index排序
cursor.execute("SELECT file_index, data_index, file_data FROM apk_file_data ORDER BY file_index, data_index")
data_rows = cursor.fetchall()

# 查询apk_file_info表中所有数据
cursor.execute("SELECT file_index, file_path FROM apk_file_info")
info_rows = cursor.fetchall()

# 创建一个file_index到file_path的映射
file_index_to_path = {row[0]: row[1] for row in info_rows}

# 存储所有文件数据的字典，key为file_index，value为所有片段合并后的数据
file_data_dict = {}

# 遍历apk_file_data表中的每一行数据，按照file_index将file_data合并
for row in data_rows:
    file_index = row[0]
    file_data = row[2]  # 直接获取bytes类型的file_data
    
    # 如果该file_index还没有在字典中，先初始化一个空的字节数组
    if file_index not in file_data_dict:
        file_data_dict[file_index] = b''

    # 将当前片段的file_data追加到对应file_index的文件数据中
    file_data_dict[file_index] += file_data

# 按照file_index依次保存文件到相应路径
for file_index, full_file_data in file_data_dict.items():
    if file_index in file_index_to_path:
        # 获取对应的文件路径
        file_path = file_index_to_path[file_index]
        
        # 确保文件夹路径存在，如果不存在则创建
        output_dir = os.path.dirname(file_path)
        os.makedirs(output_dir, exist_ok=True)

        # 将合并后的数据保存到指定的路径并重命名
        with open(file_path, 'wb') as f:
            f.write(full_file_data)

        print(f"文件已保存：{file_path}")
    else:
        print(f"没有找到file_index {file_index} 对应的路径信息，跳过该文件")

# 关闭数据库连接
conn.close()

print("所有文件已合并并保存到对应路径！")
