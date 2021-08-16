#!/bin/sh

Input=%1

OutputWidth="960"
palette="palette.png"
filters="fps=25,scale=$OutputWidth:-1:flags=lanczos"


PathBase=$(dirname "$0")
PathSource="$PathBase/Source/*"


PathMp4="$PathBase/mp4/"
PathWebm="$PathBase/webm/"
PathJpg="$PathBase/jpg/"
PathGif="$PathBase/gif/"
LogLevel='error'

MP4Codec="-codec:v libx264 -movflags +faststart -profile:v High -level 4.0 -preset slow -b:v 1000k -bufsize 1000k"
WebMCodec="-codec:v libvpx -quality good -cpu-used 0 -b:v 500k -qmin 10 -qmax 42 -maxrate 500k -bufsize 1000k"

if [ -z "$1" ]
    then
        for File in $PathSource
        do
            FileBaseName=$(basename $File .mp4)


            echo "Making jpg from: $File"
            JpgOutput="$PathJpg$FileBaseName.jpg"
            # -ss 0.5
            ffmpeg -loglevel $LogLevel -i $File -vframes 1 -vf scale=$OutputWidth:-2 $JpgOutput -y


            echo "Making mp4 from: $File"
            MP4Output="$PathMp4$FileBaseName.mp4"
            ffmpeg -loglevel $LogLevel -i $File $MP4Codec -vf "scale=$OutputWidth:-2, lutyuv=y=gammaval(1.0)" $MP4Output -y


            echo "Making webm from: $File"
            WebMOutput="$PathWebm$FileBaseName.webm"
            ffmpeg -loglevel $LogLevel -i $File $WebMCodec -vf "scale=$OutputWidth:-2" $WebMOutput -y


            echo "Making gif from: $File"
            GifOutput="$PathGif$FileBaseName.gif"
            ffmpeg -loglevel $LogLevel -i $File -vf "$filters,palettegen" -y $palette
            ffmpeg -loglevel $LogLevel -i $File -i $palette -lavfi "$filters [x]; [x][1:v] paletteuse" -y $GifOutput

        done

    else
        echo "$1"
fi


# JPGPATH="Z:/path/thumbs/jpg/*"
# OUTPATH="Z:/path/thumbs/jpg/temp/"


# # for File in $PathMp4
# # do
# #     echo "Making jpg: $File"
# #     FileBaseName=$(basename $File .mp4)
# #     Output="$PathJpg$FileBaseName.jpg"
# #     # -ss 0.5
# #     ffmpeg -i $File -vframes 1 -vf scale=400:-1 $Output -y
# # done

