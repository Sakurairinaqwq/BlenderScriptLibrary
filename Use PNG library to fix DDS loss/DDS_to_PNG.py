import bpy
import os
from pathlib import Path

# 定义贴图文件夹路径
TEXTURE_FOLDER = r"C:\Users\youname\Desktop\新建文件夹\fuckEA\texture"

def fix_missing_textures():
    # 存储修复结果
    fixed_textures = []
    not_found_textures = []

    # 遍历场景中的所有物体
    for obj in bpy.data.objects:
        if obj.type == 'MESH' and obj.material_slots:
            for mat_slot in obj.material_slots:
                if mat_slot.material and mat_slot.material.node_tree:
                    for node in mat_slot.material.node_tree.nodes:
                        if node.type == 'TEX_IMAGE' and node.image:
                            # 检查贴图是否丢失
                            if not node.image.filepath or not os.path.exists(bpy.path.abspath(node.image.filepath)):
                                # 获取贴图文件名（去掉路径和扩展名）
                                old_image_name = node.image.name
                                # 移除可能的后缀（如 .001）
                                base_name = old_image_name.split('.')[0]
                                # 构造新的 PNG 贴图路径
                                new_image_path = os.path.join(TEXTURE_FOLDER, f"{base_name}.png")
                                
                                if os.path.exists(new_image_path):
                                    # 加载新的 PNG 贴图
                                    try:
                                        new_image = bpy.data.images.load(new_image_path)
                                        node.image = new_image
                                        fixed_textures.append({
                                            'object': obj.name,
                                            'material': mat_slot.material.name,
                                            'image': old_image_name,
                                            'new_path': new_image_path
                                        })
                                    except Exception as e:
                                        not_found_textures.append({
                                            'object': obj.name,
                                            'material': mat_slot.material.name,
                                            'image': old_image_name,
                                            'error': str(e)
                                        })
                                else:
                                    not_found_textures.append({
                                        'object': obj.name,
                                        'material': mat_slot.material.name,
                                        'image': old_image_name,
                                        'error': f"PNG file not found at {new_image_path}"
                                    })

    # 输出修复结果
    print("\n=== 贴图修复报告 ===")
    if fixed_textures:
        print("\n成功修复的贴图：")
        for item in fixed_textures:
            print(f"物体: {item['object']}, 材质: {item['material']}, 原贴图: {item['image']}, 新路径: {item['new_path']}")
    else:
        print("\n没有成功修复的贴图。")

    if not_found_textures:
        print("\n未找到的贴图：")
        for item in not_found_textures:
            print(f"物体: {item['object']}, 材质: {item['material']}, 贴图: {item['image']}, 错误: {item['error']}")
    else:
        print("\n所有贴图都已处理，无未找到的贴图。")

# 运行脚本
fix_missing_textures()