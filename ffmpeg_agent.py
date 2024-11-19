from typing import List
import ffmpeg

class ffmpegAgent:
    def __init__(self, output_filename: str, **ffmpeg_args) -> None:
        self.output_filename: str = output_filename
        self.ffmpeg_args: dict[str, str] = ffmpeg_args

    def generate_video(self, images: List[str], audio: List[str]):
        if len(images) != len(audio):
            raise ValueError("Number of images and audio files must be the same")

        video_streams = []
        audio_streams = []

        for image, audio_file in zip(images, audio):
            audio_duration = ffmpeg.probe(audio_file)['format']['duration']
            video_streams.append(ffmpeg.input(image, loop=1, t=audio_duration).video)
            audio_streams.append(ffmpeg.input(audio_file).audio)

        video_concat = ffmpeg.concat(*video_streams, v=1, a=0)
        audio_concat = ffmpeg.concat(*audio_streams, v=0, a=1)

        # Merge video and audio streams
        output = ffmpeg.output(video_concat, audio_concat, self.output_filename, **self.ffmpeg_args)
        ffmpeg.run(output)
