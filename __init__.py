bl_info = {
    "name": "VertexGroupsCleaner",
    "author": "takec",
    "version": (1, 0),
    "blender": (3, 1, 0),
    "location": "Object Data Properties > Vertex Groups > Vertex Groups Specials > clean vertex group",
    "description": "weightが全て0のVertexGroupを削除",
    "category": "Object"
}

if "bpy" in locals():
    import imp
    imp.reload(vertex_groups_cleaner)
else:
    from . import vertex_groups_cleaner

import bpy

def menu_func(self, context):
    self.layout.separator()
    self.layout.operator(vertex_groups_cleaner.CleanVertexGroup.bl_idname)

classes = [
    vertex_groups_cleaner.CleanVertexGroup,
]

def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.MESH_MT_vertex_group_context_menu.append(menu_func)

def unregister():
    bpy.types.MESH_MT_vertex_group_context_menu.remove(menu_func)
    for c in classes:
        bpy.utils.unregister_class(c)

if __name__ == "__main__":
    register()