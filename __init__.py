import bpy

from .visualizer_generator import VisualizerGenerator, VisualizerSettings
from .audio_processor import ProcessingSettings

bl_info = {
    "name": "Audio Visualizer",
    "description": "Generates audio visualization in form of animated cubes for given input file.",
    "blender": (2, 80, 0),
    "version": (1, 0),
    "author": "Andrew2a1",
    "support": "COMMUNITY",
    "category": "Animation",
}


class AudioVisProperties(bpy.types.PropertyGroup):
    audio_filepath: bpy.props.StringProperty(
        name="Audio Filepath",
        description="Path to audio file to process",
        subtype="FILE_PATH",
    )
    collection_name: bpy.props.StringProperty(
        name="Output Collection Name",
        description="Name of collection for generated objects",
        default="Visualizer",
    )
    frequency_band_count: bpy.props.IntProperty(
        name="Frequency Bands",
        description="Number of frequency bands to generate visualization for",
        default=20,
        min=1,
        max=4000,
    )
    min_frequency: bpy.props.IntProperty(
        name="Min Frequency [Hz]",
        description="Minimum frequency of signal to process",
        default=60,
        min=1,
        max=20000,
    )
    max_frequency: bpy.props.IntProperty(
        name="Max Frequency [Hz]",
        description="Maximum frequency of signal to process",
        default=16000,
        min=1,
        max=20000,
    )
    sampling_duration_ms: bpy.props.FloatProperty(
        name="Sampling duration [ms]",
        description="Duration of sampling time for single step (the less duration, the faster changes can be visualized)",
        default=100,
        min=1e-6,
        max=1e6,
    )
    use_log_y: bpy.props.BoolProperty(
        name="Logarithmic Scale",
        description="Use logarithmic scale for frequency band height",
        default=True,
    )
    scaling_factor: bpy.props.FloatProperty(
        name="Scaling Factor",
        description="Multiplier for frequency band height",
        default=15,
    )
    freq_band_spacing: bpy.props.FloatProperty(
        name="Spacing Between",
        default=1,
        description="Amount of space between frequency bands",
    )
    two_sided: bpy.props.BoolProperty(
        name="Two Sided Visualizer",
        description="Scale frequency band in both directions",
        default=False,
    )
    freq_band_scale_xy: bpy.props.FloatVectorProperty(
        name="Frequency Band Scale",
        description="X and Y scale of frequency band",
        default=(1.0, 1.0),
        size=2,
    )


class AudioVisLayout:
    def draw(self, context):
        props = context.window_manager.audio_vis
        layout = self.layout

        col = layout.column(heading="Processing Options")
        col.prop(props, "audio_filepath")
        col.prop(props, "min_frequency")
        col.prop(props, "max_frequency")
        col.prop(props, "frequency_band_count")
        col.prop(props, "sampling_duration_ms")
        col.prop(props, "use_log_y")
        col.separator()

        col = layout.column(heading="Output Options")
        col.prop(props, "collection_name")
        col.prop(props, "freq_band_scale_xy")
        col.prop(props, "scaling_factor")
        col.prop(props, "freq_band_spacing")
        col.prop(props, "two_sided")


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
        self.vis_generator.generate_visualizer(
            context,
            props.collection_name,
            VisualizerSettings(
                props.freq_band_spacing,
                props.freq_band_scale_xy[0],
                props.freq_band_scale_xy[1],
                props.scaling_factor,
                props.two_sided,
            ),
        )

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
