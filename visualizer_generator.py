import bpy

from .audio_data import AudioData
from .audio_processor import AudioProcessor, ProcessingSettings


class VisualizerGenerator:
    def __init__(self):
        self.audio_data = AudioData()
        self.audio_processor = AudioProcessor()
        self.audio_processor_settings = ProcessingSettings()
        self.context = bpy.context

    def generate_visualizer(self, context, collection_name: str, scaling_factor: int = 15):
        self.context = context
        visualization_values = self.audio_processor.process(
            self.audio_data, self.audio_processor_settings
        )
        self._clear_previous_visualization(collection_name)
        self._create_animated_cubes(
            collection_name, visualization_values, scaling_factor
        )

    def load_audio_data(self, audio_path: str):
        self.audio_data.load(audio_path)

    def set_audio_processor_settings(self, settings: ProcessingSettings):
        self.audio_processor_settings = settings

    def _clear_previous_visualization(self, collection_name: str):
        if collection_name in bpy.data.collections:
            collection = bpy.data.collections[collection_name]
            meshes = set()
            for obj in collection.objects:
                meshes.add(obj.data)
                bpy.data.objects.remove(obj)
            for mesh in [m for m in meshes if m.users == 0]:
                bpy.data.meshes.remove(mesh)
            bpy.data.collections.remove(collection)

    def _create_visualizer_collection(self, collection_name: str):
        visualizer_collection = bpy.data.collections.new(collection_name)
        self.context.scene.collection.children.link(visualizer_collection)
        return visualizer_collection

    def _create_animated_cubes(self, visualization_values, scaling_factor):
        keyframe_offset = (
            self.audio_processor_settings.step_duration_s * self.context.scene.render.fps
        )
        scaled_visualization_data = visualization_values * scaling_factor

        visualizer_collection = self._create_visualizer_collection()
        material = bpy.data.materials.new(name="Material")
        starting_cursor_location = self.context.scene.cursor.location.copy()

        for i in range(self.audio_processor_settings.frequency_bands):
            freq_band_visualizer = self._create_freq_band_visualizer(material, i)

            self.context.scene.cursor.location = self.context.active_object.location
            self.context.scene.cursor.location.z -= 0.5
            bpy.ops.object.origin_set(type="ORIGIN_CURSOR")

            self._create_animation(
                scaled_visualization_data, keyframe_offset, i, freq_band_visualizer
            )

            visualizer_collection.objects.link(freq_band_visualizer)

        self.context.scene.cursor.location = starting_cursor_location

    def _create_animation(
        self, visualization_values, keyframe_offset, i, freq_band_visualizer
    ):
        for j in range(visualization_values.shape[0]):
            freq_band_visualizer.scale = (
                1,
                1,
                visualization_values[j, i],
            )
            freq_band_visualizer.keyframe_insert(
                data_path="scale", index=2, frame=(j * keyframe_offset + 1)
            )

    def _create_freq_band_visualizer(self, material, i):
        bpy.ops.mesh.primitive_cube_add(
            size=1,
            enter_editmode=False,
            align="WORLD",
            location=(i * 2, 0, 0),
            scale=(1, 1, 1),
        )
        freq_band_visualizer = self.context.active_object
        freq_band_visualizer.name = f"f{i}"
        freq_band_visualizer.data.materials.append(material)

        if len(freq_band_visualizer.users_collection) > 0:
            freq_band_visualizer.users_collection[0].objects.unlink(
                freq_band_visualizer
            )

        return freq_band_visualizer
