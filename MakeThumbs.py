import subprocess
import sys
import os


def ExecFFmpeg(Args):

    print 'Args: {0}'.format(Args)
    Proc = subprocess.Popen('ffmpeg {}'.format(Args), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    # Read stdout and print each new line
    for Line in iter(Proc.stdout.readline, b''):
        Line = Line.rstrip()
        print ("\tFFMpeg >> " + Line)

        if '[NULL' in Line:
            exit(Line)
        

def Main():

    Input = sys.argv[-1]

    OutputWidth="960"

    OuputDir = os.path.dirname(Input)
    OutputFile = os.path.basename(Input)
    OutputFileNoExt = OutputFile[:-(len(OutputFile.split('.')[-1])+1)] + '-thumb'

    print 'OutputFileNoExt: {0}'.format(OutputFileNoExt)



    # PathMp4="$PathBase/mp4/"
    # PathWebm="$PathBase/webm/"
    # PathJpg="$PathBase/jpg/"
    # PathGif="$PathBase/gif/"
    JPGCodec="-q:v 1"
    MP4Codec="-codec:v libx264 -movflags +faststart -profile:v High -level 4.0 -preset slow -b:v 1000k -bufsize 1000k"
    WebMCodec="-codec:v libvpx -quality good -cpu-used 0 -b:v 500k -qmin 10 -qmax 42 -maxrate 500k -bufsize 1000k"
    
    LogLevel='error'
    palette="palette.png"
    GIFFilters="fps=25,scale={}:-1:flags=lanczos".format(OutputWidth)

    # JPG
    Extension = 'jpg'
    OutputPath = '{}/{}.{}'.format(OuputDir, OutputFileNoExt, Extension)

    Args = '-loglevel {LL} -y -i {Input} -vframes 1 {JPGCodec} -vf scale={OutputWidth}:-2 {Output}'.format(LL=LogLevel, JPGCodec=JPGCodec, Input=Input, OutputWidth=OutputWidth, Output=OutputPath)

    ExecFFmpeg(Args=Args)


    # GIF
    Extension = 'gif'
    OutputPath = '{}/{}.{}'.format(OuputDir, OutputFileNoExt, Extension)

    Args = '-loglevel {LL} -y -i {Input} -vf "{GIFFilters},palettegen" {Output}'.format(LL=LogLevel, Input=Input, GIFFilters=GIFFilters, Output=palette)
    ExecFFmpeg(Args=Args)

    Args = '-loglevel {LL} -y -i {Input} -i {palette} -lavfi "{GIFFilters} [x]; [x][1:v] paletteuse" {Output}'.format(LL=LogLevel, Input=Input, palette=palette, GIFFilters=GIFFilters, Output=OutputPath)
    ExecFFmpeg(Args=Args)


    # WebM
    Extension = 'webm'
    OutputPath = '{}/{}.{}'.format(OuputDir, OutputFileNoExt, Extension)

    Args = '-loglevel {LL} -y -i {Input} {Codec} -vf scale={OutputWidth}:-2 {Output}'.format(LL=LogLevel, Input=Input, Codec=WebMCodec, OutputWidth=OutputWidth, Output=OutputPath)
    ExecFFmpeg(Args=Args)

    # MP4
    Extension = 'mp4'
    OutputPath = '{}/{}.{}'.format(OuputDir, OutputFileNoExt, Extension)

    Args = '-loglevel {LL} -y -i {Input} {Codec} -vf scale={OutputWidth}:-2 {Output}'.format(LL=LogLevel, Input=Input, Codec=MP4Codec, OutputWidth=OutputWidth, Output=OutputPath)
    ExecFFmpeg(Args=Args)


if __name__ == '__main__':
    Main()