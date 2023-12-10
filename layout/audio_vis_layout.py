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
