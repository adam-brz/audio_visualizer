from .audio_vis_layout import AudioVisLayout
from ..processing.visualizer_generator import VisualizerGenerator, VisualizerSettings
from ..processing.audio_processor import ProcessingSettings

import bpy


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
