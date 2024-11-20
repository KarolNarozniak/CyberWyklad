import os
import ffmpeg

class FfmpegModule:
    def __init__(self, output_filename: str, audio_dir: str, images_dir: str,
                 audio_file_prefix: str, image_file_prefix: str, **ffmpeg_args) -> None:
        self.output_filename: str = output_filename
        self.ffmpeg_args: dict[str, str] = ffmpeg_args
        self.audio_dir: str = audio_dir
        self.images_dir: str = images_dir
        self.audio_file_prefix: str = audio_file_prefix
        self.image_file_prefix: str = image_file_prefix

    def generate_video(self):
        video_streams = []
        audio_streams = []

        # Assuming the number of audio and image files are the same and indexed from 1
        index = 1
        while True:
            audio_file = os.path.join(self.audio_dir, f"{self.audio_file_prefix}_{index}.wav")
            image_file = os.path.join(self.images_dir, f"{self.image_file_prefix}_{index}.png")

            if not os.path.exists(audio_file) or not os.path.exists(image_file):
                break

            audio_duration = ffmpeg.probe(audio_file)['format']['duration']
            video_streams.append(ffmpeg.input(image_file, loop=1, t=audio_duration).video)
            audio_streams.append(ffmpeg.input(audio_file).audio)

            index += 1

        video_concat = ffmpeg.concat(*video_streams, v=1, a=0)
        audio_concat = ffmpeg.concat(*audio_streams, v=0, a=1)

        # Merge video and audio streams
        output = ffmpeg.output(video_concat, audio_concat, self.output_filename, **self.ffmpeg_args)
        ffmpeg.run(output)
