import ffmpeg

(    
    ffmpeg
    .input("youtube-dl test video ''_ä↭𝕐-BaW_jenozKc.mp4")
    .output("test.mkv")
    .run()
)