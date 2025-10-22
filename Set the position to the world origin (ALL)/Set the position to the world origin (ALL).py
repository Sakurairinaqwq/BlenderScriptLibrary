import bpy

# 进入对象模式
bpy.ops.object.mode_set(mode='OBJECT')

# 遍历所有物体
for obj in bpy.context.scene.objects:
    # 跳过非网格物体（如灯、空物体），可选
    if obj.type != 'MESH':
        continue
    
    # 选中物体作为活动对象
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    
    # 应用所有变换（彻底“烘焙”）
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    
    # 设置原点到几何中心（现在原点 = 几何中心）
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
    
    # 将位置重置到世界原点（几何中心移到 (0,0,0)）
    obj.location = (0.0, 0.0, 0.0)
    
    # 取消选中
    obj.select_set(False)

# 刷新视图
bpy.context.view_layer.update()

print("所有网格物体的中心点已彻底重置到世界原点！")