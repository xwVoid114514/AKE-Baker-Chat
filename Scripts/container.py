from Scripts import util
from PIL import Image


tileFolderDir = './Resources/Elements'


def MergeTiles(Variant: str, Width: int, Height: int) -> Image.Image | None:
  tileSizeList = [
    (30, 30),
    (Width - 60, 30),
    (30, 30),
    (30, Height - 60),
    (Width - 60, Height - 60),
    (30, Height - 60),
    (30, 30),
    (Width - 60, 30),
    (30, 30)
  ]
  tilePosList = [
    (0, 0),
    (30, 0),
    (Width - 30, 0),
    (0, 30),
    (30, 30),
    (Width - 30, 30),
    (0, Height - 30),
    (30, Height - 30),
    (Width - 30, Height - 30)
  ]
  
  canvas = Image.new(mode='RGBA', size=(Width, Height), color='#00000000')
  try:
    for i in range(0, 9):
      tile = util.ReadImageFile(f'{tileFolderDir}/{Variant}/{Variant}_{i}.png')
      if tile == None: raise Exception
      tile = tile.resize(tileSizeList[i])
      canvas.paste(tile, tilePosList[i], tile)
    return canvas  
  except:
    return None
  

def ChatBubble_Dark(Width: int, Height: int) -> Image.Image | None:
  return MergeTiles('bubble_dark', Width, Height)
  
  
def ChatBubble_Light(Width: int, Height: int) -> Image.Image | None:
  bubble = MergeTiles('bubble_light', Width, Height)
  if(bubble == None):
    return None
  else:
    return bubble.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
