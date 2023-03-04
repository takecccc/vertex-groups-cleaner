import bpy

class CleanVertexGroup(bpy.types.Operator):
    bl_idname = "object.clean_vertex_group"
    bl_label = "clean vertex group"
    bl_description = "weightが全て0のVertexGroupを削除"
    bl_options = {"REGISTER", "UNDO"}

    # preserve_flipped_empty_group: bpy.props.BoolProperty(
    #     name="preserve flipped empty group",
    #     description="preserve flipped empty group",
    #     default=True
    # )

    def execute(self, context):
        obj = context.active_object

        if(obj.type != "MESH"):
            print(obj.type)
            return {"CANCELLED"}
        
        vg_max_weights_by_index = {}
        vg_name_by_index = {}
        vg_index_by_name = {}

        for vg in obj.vertex_groups:
            vg_max_weights_by_index[vg.index] = 0
            vg_name_by_index[vg.index] = vg.name
            vg_index_by_name[vg.name] = vg.index

        # verticesから、各vertex_groupのmag_weightsを取得
        for v in obj.data.vertices:
            for g in v.groups:
                group_index = g.group
                w = obj.vertex_groups[group_index].weight(v.index)
                if(
                    (vg_max_weights_by_index.get(group_index) is None) or
                    (w > vg_max_weights_by_index[group_index])
                    ):
                    vg_max_weights_by_index[group_index] = w
        

        # vertex groupのインデックスを逆順でリストとして取得(indexが変化しないよう、後ろから削除していくため)
        idx_list = list(vg_max_weights_by_index.keys())
        idx_list.sort(reverse=True)

        # 削除するグループか判定
        remove_flags = {}
        for idx in idx_list:
            if remove_flags.get(idx) is not None:
                # 既にフラグ格納済み
                continue
            # 最大重みが0ならば、削除する物としてフラグ格納
            remove_flags[idx] = (vg_max_weights_by_index[idx] == 0)

            # フリップしたvertex groupが存在する場合、フリップしたvertex groupの重みが0で無ければ削除しない。
            group_name = vg_name_by_index[idx]
            flipped_name = bpy.utils.flip_name(group_name)
            flipped_idx = vg_index_by_name.get(flipped_name)
            if (
                flipped_idx is not None
                # and self.preserve_flipped_empty_group
            ):
                if vg_max_weights_by_index[flipped_idx] > 0:
                    remove_flags[idx] = False
        
        # 削除フラグを参照して、後ろから削除
        for idx in idx_list:
            if remove_flags[idx]:
                obj.vertex_groups.remove(obj.vertex_groups[idx])
                print(f"delete {vg_name_by_index[idx]}")

        return {"FINISHED"}
