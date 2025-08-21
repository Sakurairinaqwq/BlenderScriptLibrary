import bpy
import hashlib
from mathutils import Matrix

def get_mesh_hash(mesh):
    # 获取网格的顶点坐标作为哈希依据（排序以确保一致性）
    verts = sorted([tuple(v.co[:]) for v in mesh.vertices])
    # 使用 hashlib 生成哈希（因为 tuple 可能太大直接 hash）
    vert_str = str(verts).encode('utf-8')
    return hashlib.sha256(vert_str).hexdigest()

def get_matrix_hash(matrix):
    # 获取变换矩阵的哈希（将矩阵展平为元组）
    mat_flat = tuple(matrix.to_4x4())  # 转换为 4x4 矩阵并展平为元组
    mat_str = str(mat_flat).encode('utf-8')
    return hashlib.sha256(mat_str).hexdigest()

def remove_duplicate_models():
    # 存储已见过的模型键（mesh_hash + matrix_hash）
    seen = set()
    to_delete = []
    deleted_info = []

    # 遍历场景中的所有网格物体
    for obj in list(bpy.data.objects):  # 使用 list 以避免迭代中修改
        if obj.type == 'MESH':
            mesh = obj.data
            mesh_hash = get_mesh_hash(mesh)
            matrix_hash = get_matrix_hash(obj.matrix_world)
            key = (mesh_hash, matrix_hash)
            
            if key in seen:
                to_delete.append(obj)
                deleted_info.append({
                    'name': obj.name,
                    'location': obj.location[:],
                    'reason': '相同几何体和变换的重复模型'
                })
            else:
                seen.add(key)

    # 删除重复物体
    for obj in to_delete:
        bpy.data.objects.remove(obj, do_unlink=True)

    # 输出报告
    print("\n=== 重复模型去除报告 ===")
    if deleted_info:
        print("\n已去除的重复模型：")
        for item in deleted_info:
            print(f"物体名称: {item['name']}, 位置: {item['location']}, 原因: {item['reason']}")
    else:
        print("\n没有找到重复模型。")

# 运行脚本
remove_duplicate_models()