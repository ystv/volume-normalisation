volume-normalisation
====================

A Python tool to normalise video volume using FFMPEG and EBU R128 loudness units

Requires ffmpeg with the relevant encoders and filters enabled. To level a file to -23 LUFS using fdk_aac at 192kbps, run

    python volumeNormalise.py input_file output_file -l -23 -c libfdk_aac -b 192000

Released under GPLv3
