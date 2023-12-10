from .layout.audio_vis_panel import (
    VIEW3D_PT_AudioVis,
    VIEW3D_PT_AudioVisSettingsPanel,
    OBJECT_OT_AudioVis,
)

from .layout.audio_vis_properties import AudioVisProperties

import bpy

bl_info = {
    "name": "Audio Visualizer",
    "description": "Generate audio frequency spectrum visualization in the form of animation data.",
    "blender": (2, 80, 0),
    "version": (1, 0),
    "author": "Andrew2a1",
    "support": "COMMUNITY",
    "category": "Animation",
}

classes = (
    AudioVisProperties,
    VIEW3D_PT_AudioVis,
    VIEW3D_PT_AudioVisSettingsPanel,
    OBJECT_OT_AudioVis,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.WindowManager.audio_vis = bpy.props.PointerProperty(
        type=AudioVisProperties
    )


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.WindowManager.audio_vis


if __name__ == "__main__":
    register()
