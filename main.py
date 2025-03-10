from manim import *
from pydub import AudioSegment
from pathlib import Path
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService
import numpy as np
from scipy.io import wavfile
from scipy.signal import resample
import os
import tempfile
from scipy.fft import fft  # Add FFT import


class AudioReactiveSquare(VoiceoverScene):
    def construct(self):
        # Configure the voiceover service
        self.set_speech_service(GTTSService())

        # Create a square
        square = Square(side_length=2, color=BLUE)

        # Create a frequency-reactive polygon that will replace the square
        # Start with square points
        num_points = 150  # Number of points around the perimeter (more points = smoother visualization)
        square_points = []

        # Generate points around a square (going clockwise)
        side_length = 2
        half_length = side_length / 2

        # Top side (left to right)
        for i in range(num_points // 4):
            x = -half_length + i * side_length / (num_points // 4)
            y = half_length
            square_points.append([x, y, 0])

        # Right side (top to bottom)
        for i in range(num_points // 4):
            x = half_length
            y = half_length - i * side_length / (num_points // 4)
            square_points.append([x, y, 0])

        # Bottom side (right to left)
        for i in range(num_points // 4):
            x = half_length - i * side_length / (num_points // 4)
            y = -half_length
            square_points.append([x, y, 0])

        # Left side (bottom to top)
        for i in range(num_points // 4):
            x = -half_length
            y = -half_length + i * side_length / (num_points // 4)
            square_points.append([x, y, 0])

        # Create the polygon using these points
        freq_polygon = Polygon(*square_points, color=BLUE)

        # Keep a reference to the original points
        self.original_points = np.array(square_points)

        self.play(Create(freq_polygon))

        # Function to make the polygon react to frequency bands
        def update_square(mob: Mobject, audio_array: np.ndarray, dt: float):
            if len(audio_array) == 0:
                return

            # Get current time and find corresponding audio sample
            t = self.renderer.time - self.start_time
            if t <= 0 or t >= len(audio_array) / self.sample_rate:
                return

            # Get audio segment around current time for FFT
            window_size = 1024  # Size of the FFT window
            index = int(t * self.sample_rate)

            if index + window_size >= len(audio_array):
                window_size = len(audio_array) - index
                if window_size <= 0:
                    return

            # Extract audio window for frequency analysis
            window = audio_array[index : index + window_size]

            # Apply FFT to get frequency data
            fft_result = fft(window)
            fft_magnitude = np.abs(fft_result[: window_size // 2]) / window_size

            # Map frequency bands to points on the polygon
            num_bands = min(40, len(fft_magnitude))  # Match number of points

            # Divide the spectrum into bands, one for each point
            bands = []
            for i in range(num_bands):
                start_idx = int(i * len(fft_magnitude) / num_bands)
                end_idx = int((i + 1) * len(fft_magnitude) / num_bands)
                band_value = np.mean(fft_magnitude[start_idx:end_idx])
                bands.append(band_value)

            # Normalize bands for consistent visualization
            max_band_value = max(bands) if max(bands) > 0 else 1
            normalized_bands = [band / max_band_value for band in bands]

            # Create new points by scaling each original point based on its frequency band
            new_points = []
            for i, point in enumerate(self.original_points):
                # Get the band that corresponds to this point
                band_idx = i % len(normalized_bands)
                scale_factor = (
                    1 + normalized_bands[band_idx] * 0.5
                )  # Scale between 1x and 1.5x

                # Scale the point from origin
                x, y, z = point
                direction = np.array([x, y, 0])
                if np.linalg.norm(direction) > 0:
                    direction = direction / np.linalg.norm(direction)
                else:
                    direction = np.array([1, 0, 0])  # Default direction if at origin

                # Calculate new position
                magnitude = np.sqrt(x**2 + y**2) * scale_factor
                new_x = direction[0] * magnitude
                new_y = direction[1] * magnitude
                new_points.append([new_x, new_y, 0])

            # Update the polygon with new points
            mob.become(Polygon(*new_points, color=BLUE))

            # Apply rotation (independent of the frequency response)
            # Use average of high frequency bands for rotation speed
            high_freq_bands = normalized_bands[len(normalized_bands) // 2 :]
            rotation_speed = np.mean(high_freq_bands) * 0.5 if high_freq_bands else 0
            mob.rotate(rotation_speed)

        # Record and process the voiceover
        with self.voiceover(
            """This is an example of a square that vibrates with my voice.
            As I speak, the square's shape changes based on different frequency bands.
            The pattern represents a frequency spectrum, similar to an audio equalizer."""
        ) as tracker:
            # Save the current time as start time
            self.start_time = self.renderer.time

            # Get the audio file path
            audio_file_path = str(
                (
                    Path(self.speech_service.cache_dir) / tracker.data["final_audio"]
                ).absolute()
            )

            # Process the audio file to get amplitude data
            # Convert mp3 to wav first since scipy only supports wav
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav:
                # Check if file exists and print debug info
                if not os.path.exists(audio_file_path):
                    raise FileNotFoundError(
                        f"Audio file not found at: {audio_file_path}"
                    )

                try:
                    sound = AudioSegment.from_mp3(audio_file_path)
                    sound.export(temp_wav.name, format="wav")
                    sample_rate, audio_data = wavfile.read(temp_wav.name)
                except Exception as e:
                    raise Exception(
                        f"Error processing audio file {audio_file_path}: {str(e)}"
                    )
            if len(audio_data.shape) > 1:  # Stereo to mono if needed
                audio_data = np.mean(audio_data, axis=1)

            self.sample_rate = sample_rate
            self.max_amplitude = np.max(np.abs(audio_data)) or 1

            # Add the update function to the polygon
            freq_polygon.add_updater(lambda m, dt: update_square(m, audio_data, dt))

            # Wait for the voiceover to finish
            self.wait(tracker.duration)

        # Remove the updater when finished
        freq_polygon.clear_updaters()
        self.wait(1)


if __name__ == "__main__":
    # Set a custom output file name
    output_file = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False)
    output_file.close()

    # Run the scene
    config.output_file = output_file.name
    scene = AudioReactiveSquare()
    scene.render()

    # Open the video file
    os.system(f"start {output_file.name}")
