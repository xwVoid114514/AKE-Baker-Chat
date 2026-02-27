from PIL import Image, ImageDraw


def ReadImageFile(Path: str) -> Image.Image | None:
  try:
    return Image.open(Path).convert('RGBA')
  except:
    print(f'[ERROR] Cannot open file: {Path}')
    return None
  
  
def SaveImage(Img: Image.Image, Path: str) -> bool:
  try:
    Img.save(Path)
    print(f'[INFO] Saved image: {Path}')
    return True
  except:
    print(f'[ERROR] Cannot save image: {Path}')
    return False
  
  
def ExpandDown(Img: Image.Image, DeltaHeight: int, FillColor: str) -> Image.Image:
  canvas = Image.new('RGBA', (Img.width, Img.height + DeltaHeight), FillColor)
  canvas.paste(Img, (0, 0))
  return canvas


def AddMargin(Img: Image.Image, Margin: int, FillColor: str) -> Image.Image:
  canvas = Image.new('RGBA', (Img.width + Margin * 2, Img.height + Margin * 2), FillColor)
  canvas.paste(Img, (Margin, Margin))
  return canvas


def RestrictWidth(Img: Image.Image, Width: int) -> Image.Image:
  return Img.resize((Width, int(Img.height * Width / Img.width)))


def RoundedRectMask(Width: int, Height: int, Radius: int) -> Image.Image:
  mask = Image.new('L', (Width, Height), 0)
  ImageDraw.Draw(mask).rounded_rectangle((0, 0, Width, Height), radius=Radius, fill=255, outline=None, corners=(True, True, True, True))
  return mask
