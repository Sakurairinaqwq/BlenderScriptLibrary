import bpy

def find_missing_textures():
    # 存储丢失贴图的模型和贴图信息
    missing_textures = []
    
    # 遍历场景中的所有物体
    for obj in bpy.data.objects:
        if obj.type == 'MESH' and obj.material_slots:
            for mat_slot in obj.material_slots:
                if mat_slot.material and mat_slot.material.node_tree:
                    # 检查材质中的节点
                    for node in mat_slot.material.node_tree.nodes:
                        if node.type == 'TEX_IMAGE' and node.image:
                            # 检查贴图文件是否存在
                            if not node.image.filepath or not bpy.path.abspath(node.image.filepath):
                                missing_textures.append({
                                    'object': obj.name,
                                    'material': mat_slot.material.name,
                                    'image': node.image.name
                                })
                            elif not bpy.data.images[node.image.name].has_data:
                                missing_textures.append({
                                    'object': obj.name,
                                    'material': mat_slot.material.name,
                                    'image': node.image.name
                                })
    
    # 输出结果
    if missing_textures:
        print("\n找到以下丢失的贴图：")
        for item in missing_textures:
            print(f"物体: {item['object']}, 材质: {item['material']}, 贴图: {item['image']}")
    else:
        print("\n没有找到丢失的贴图。")

# 运行脚本
find_missing_textures()