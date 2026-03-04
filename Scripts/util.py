from PIL import Image, ImageDraw
import gradio as gr
import shutil, os


cacheDir = './Cache'


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

def LoadScriptFromFile(Path: str) -> str | None:
  try:
    Path = Path.strip()
    if Path == '':
      print(f'[ERROR] No file selected')
      return None
    if not Path.endswith(('.txt', '.TXT')): 
      print(f'[ERROR] Invalid file type')
      return None
    with open(Path, 'r', encoding='utf-8') as file:
      return file.read()
  except:
    print(f'[ERROR] Cannot open file: {Path}')
    return None
  

def ShowError(message: str) -> None:
  gr.Error(message, duration=5)


def ShowInfo(message: str) -> None:
  gr.Info(message, duration=5)


def ClearCache() -> None:
  shutil.rmtree(cacheDir)
  os.makedirs(cacheDir)
  