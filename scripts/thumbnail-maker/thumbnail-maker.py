
# PIL -> 

#Bili = 1146*717
#yT = 1280*720

# hard crop（只能裁剪 不能补足/缩放）
#使用-s参数实现，语法：ffmpeg  -i  input_file  -s  wxh  output_file (wxh是宽x高，比如320x240)
# or
# ffmpeg -i 屏幕截图\ 2021-05-17\ 101021.png -vf scale=1146x717 1.mp4

# 压制字幕
#ffmpeg -i 1.mp4 -ss 0 -f image2 title.jpg