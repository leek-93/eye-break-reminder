# make_blinkbuddy_icon.py
from PIL import Image, ImageDraw

# 크기 (아이콘은 256x256 이상이면 자동 축소 가능)
size = 256
img = Image.new("RGBA", (size, size), (255, 255, 255, 0))
draw = ImageDraw.Draw(img)

# 눈 (흰자)
draw.ellipse((40, 60, 100, 120), fill="white", outline="black", width=4)
draw.ellipse((156, 60, 216, 120), fill="white", outline="black", width=4)

# 동공
draw.ellipse((65, 80, 85, 100), fill="black")
draw.ellipse((181, 80, 201, 100), fill="black")

# 미소
draw.arc((70, 120, 190, 200), start=20, end=160, fill="black", width=6)

# 저장 (아이콘 파일)
img.save("blinkbuddy.ico", format="ICO")
print("✅ blinkbuddy.ico 아이콘 파일이 생성되었습니다!")
