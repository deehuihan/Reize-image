from fastapi import FastAPI, File, UploadFile
from PIL import Image, ImageOps
from io import BytesIO
from starlette.responses import StreamingResponse

app = FastAPI()

@app.post("/resize-image/")
async def resize_image(file: UploadFile = File(...)):
    # 讀取圖片並處理
    image = Image.open(file.file)
    target_size = (3072, 3072)
    
    # 調整圖片大小，並將黑色背景填充在空白處
    img_aspect_ratio = image.width / image.height
    if img_aspect_ratio > 1:
        image = image.resize((target_size[0], int(target_size[0] / img_aspect_ratio)), Image.LANCZOS)
    else:
        image = image.resize((int(target_size[1] * img_aspect_ratio), target_size[1]), Image.LANCZOS)

    # 建立黑色背景畫布
    new_image = Image.new("RGB", target_size, (0, 0, 0))
    center_position = ((target_size[0] - image.width) // 2, (target_size[1] - image.height) // 2)
    new_image.paste(image, center_position)

    # 將圖片轉換為字節流，準備回傳
    img_byte_arr = BytesIO()
    new_image.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)

    return StreamingResponse(img_byte_arr, media_type="image/jpeg")
