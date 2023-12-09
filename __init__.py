import bpy

from .visualizer_generator import VisualizerGenerator
from .audio_processor import ProcessingSettings

bl_info = {
    "name": "Audio Visualizer",
    "description": "Generates audio visualization in form of animated cubes for given input file.",
    "blender": (2, 80, 0),
    "version": (1, 0),
    "support": "COMMUNITY",
    "category": "Animation",
}


class AudioVisProperties(bpy.types.PropertyGroup):
    audio_filepath: bpy.props.StringProperty(name="Audio Filepath", subtype="FILE_PATH")
    collection_name: bpy.props.StringProperty(
        name="Output Collection Name", default="Visualizer"
    )
    frequency_band_count: bpy.props.IntProperty(
        name="Frequency Bands", default=20, min=1, max=4000
    )
    min_frequency: bpy.props.IntProperty(
        name="Min Frequency [Hz]", default=60, min=1, max=20000
    )
    max_frequency: bpy.props.IntProperty(
        name="Max Frequency [Hz]", default=16000, min=1, max=20000
    )
    sampling_duration_ms: bpy.props.FloatProperty(
        name="Sampling duration [ms]", default=100, min=1e-6, max=1e6
    )
    use_log_y: bpy.props.BoolProperty(
        name="Logarithmic Scale", default=True
    )
    scaling_factor: bpy.props.FloatProperty(
        name="Scaling Factor", default=15
    )


class AudioVisLayout:
    def draw(self, context):
        props = context.window_manager.audio_vis
        layout = self.layout
        col = layout.column()

        col.label(text="Processing Options")
        col.prop(props, "audio_filepath")
        col.prop(props, "min_frequency")
        col.prop(props, "max_frequency")
        col.prop(props, "frequency_band_count")
        col.prop(props, "sampling_duration_ms")

        col.label(text="Output Options")
        col.prop(props, "collection_name")
        col.prop(props, "scaling_factor")
        col.prop(props, "use_log_y")


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


class OBJECT_OT_AudioVis(AudioVisLayout, bpy.types.Operator):
    bl_idname = "object.audio_vis"
    bl_label = "Create Audio Visualizer"
    bl_options = {"REGISTER", "UNDO"}
    vis_generator = VisualizerGenerator()

    def execute(self, context):
        props = context.window_manager.audio_vis
        self.vis_generator.load_audio_data(props.audio_filepath)
        self.vis_generator.set_audio_processor_settings(
            ProcessingSettings(
                props.sampling_duration_ms / 1e3,
                props.frequency_band_count,
                props.min_frequency,
                props.max_frequency,
                props.use_log_y,
            )
        )
        self.vis_generator.generate_visualizer(context, props.collection_name, props.scaling_factor)
        return {"FINISHED"}


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
