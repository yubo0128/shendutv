import json


def convert_to_srt(json_file, srt_file):
    with open(json_file, 'r') as f:
        data = json.load(f)

    with open(srt_file, 'w') as f:
        for i, word in enumerate(data['words']):
            start_time = word['start']
            end_time = word['end']
            text = word['word']

            start_time_srt = format_time(start_time)
            end_time_srt = format_time(end_time)

            f.write(f"{i + 1}\n")
            f.write(f"{start_time_srt} --> {end_time_srt}\n")
            f.write(f"{text}\n\n")


def format_time(seconds):
    millis = int((seconds % 1) * 1000)
    seconds = int(seconds)
    minutes = seconds // 60
    hours = minutes // 60
    seconds = seconds % 60
    minutes = minutes % 60
    return f"{hours:02}:{minutes:02}:{seconds:02},{millis:03}"


json_file = "字幕.json"
srt_file = "output.srt"
convert_to_srt(json_file, srt_file)
