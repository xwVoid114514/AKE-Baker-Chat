from Scripts import util
from PIL import Image


tileFolderDir = './Resources/Elements'

# Grid - (Row, Column)
def SplitAtlas(Path: str, Grid: tuple[int, int], ChunkSize: int = 32) -> tuple[Image.Image] | None:
  atlas = util.ReadImageFile(Path)
  if atlas == None: return None
  chunkList = []
  for y in range(0, Grid[0] * ChunkSize, ChunkSize):
    for x in range(0, Grid[1] * ChunkSize, ChunkSize):
      chunkList.append(atlas.crop((x, y, x + ChunkSize, y + ChunkSize)))
  return tuple(chunkList)  # 图块顺序为先行后列


def Render3x3(Variant: str, Size: tuple[int, int], ChunkSize: int) -> Image.Image | None:
  Size = (max(Size[0], ChunkSize * 2 + 1), max(Size[1], ChunkSize * 2 + 1))  # 保证图片边长至少为2倍分块边长  
  chunkFinalSizeList = [
    (ChunkSize, ChunkSize),
    (Size[0] - 2 * ChunkSize, ChunkSize),
    (ChunkSize, ChunkSize),
    (ChunkSize, Size[1] - 2 * ChunkSize),
    (Size[0] - 2 * ChunkSize, Size[1] - 2 * ChunkSize),
    (ChunkSize, Size[1] - 2 * ChunkSize),
    (ChunkSize, ChunkSize),
    (Size[0] - 2 * ChunkSize, ChunkSize),
    (ChunkSize, ChunkSize)
  ]
  chunkFinalPosList = [
    (0, 0),
    (ChunkSize, 0),
    (Size[0] - ChunkSize, 0),
    (0, ChunkSize),
    (ChunkSize, ChunkSize),
    (Size[0] - ChunkSize, ChunkSize),
    (0, Size[1] - ChunkSize),
    (ChunkSize, Size[1] - ChunkSize),
    (Size[0] - ChunkSize, Size[1] - ChunkSize)
  ]
  chunkList = SplitAtlas(f'{tileFolderDir}/atlas_{Variant}.png', (3, 3), ChunkSize)
  if chunkList == None: return None
  canvas = Image.new(mode='RGBA', size=Size, color='#00000000')
  for i in range(0, 9):
    chunk = chunkList[i].resize(chunkFinalSizeList[i])
    canvas.paste(chunk, chunkFinalPosList[i], chunk)
  return canvas
  

def ChatBubble_Dark(Width: int, Height: int) -> Image.Image | None:
  return Render3x3('bubble_dark', (Width, Height), 32)
  
  
def ChatBubble_Light(Width: int, Height: int) -> Image.Image | None:
  bubble = Render3x3('bubble_light', (Width, Height), 32)
  if(bubble == None):
    return None
  else:
    return bubble.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
