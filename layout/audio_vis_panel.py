from .audio_vis_operator import OBJECT_OT_AudioVis
from .audio_vis_layout import AudioVisLayout

import bpy


class AudioVisPropertiesPanelBase(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Tool"


class VIEW3D_PT_AudioVis(AudioVisPropertiesPanelBase):
    bl_label = "Audio Visualizer"

    def draw(self, _):
        layout = self.layout
        col = layout.column()
        col.operator(OBJECT_OT_AudioVis.bl_idname)


class VIEW3D_PT_AudioVisSettingsPanel(AudioVisPropertiesPanelBase, AudioVisLayout):
    bl_parent_id = "VIEW3D_PT_AudioVis"
    bl_label = "Audio Visualizer Settings"
