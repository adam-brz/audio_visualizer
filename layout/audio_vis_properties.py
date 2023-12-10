import bpy


class AudioVisProperties(bpy.types.PropertyGroup):
    audio_filepath: bpy.props.StringProperty(
        name="Audio File Path",
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
        description="Number of frequency bands to generate visualization",
        default=20,
        min=1,
        max=4000,
    )
    min_frequency: bpy.props.IntProperty(
        name="Min Frequency [Hz]",
        description="Minimum frequency of signal to visualize",
        default=60,
        min=1,
        max=20000,
    )
    max_frequency: bpy.props.IntProperty(
        name="Max Frequency [Hz]",
        description="Maximum frequency of signal to visualize",
        default=16000,
        min=1,
        max=20000,
    )
    sampling_duration_ms: bpy.props.FloatProperty(
        name="Sampling duration [ms]",
        description="Duration of sampling time for single step (the less duration, the faster changes can be visualized)",
        default=120,
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
