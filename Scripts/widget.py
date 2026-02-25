from Scripts import util, container
from PIL import Image, ImageFont, ImageDraw
import textwrap


elementDir = './Resources/Elements'
avatarDir = './Resources/Avatars'
fontDir = './Resources/Fonts'


def RenderAvatar(Name: str):
  canvas = Image.new(mode='RGBA', size=(110, 110), color='#00000000')
  
  frame = util.ReadImageFile(f'{elementDir}/avatar_frame.png')
  if frame == None: return None
  canvas.paste(frame, (0, 0), frame)
  
  avtPic = util.ReadImageFile(f'{avatarDir}/avt_{Name}.png')
  if avtPic == None: return None
  avtPic = avtPic.resize((110, 110))
  avtMask = util.ReadImageFile(f'{elementDir}/avatar_mask.png')
  if avtMask == None: return None
  canvas.paste(avtPic, (0, 0), avtMask.convert('L'))
  
  return canvas


def RenderTextMsg(Text: str, Color: str):
  mlString = textwrap.fill(Text, width=30)
  canvas = Image.new(mode='RGBA', size=(850, 850), color='#00000000')
  font = ImageFont.truetype(font=f'{fontDir}/HarmonyOS_Sans_SC_Regular.ttf', size=28)
  ImageDraw.Draw(canvas).multiline_text(text=mlString, font=font, xy=(0, 0), fill=Color, spacing=12)
  canvas = canvas.crop(canvas.getbbox())
  return canvas
  

def Widget_Title(Canvas: Image.Image, Text: str):
  titlePanel = util.ReadImageFile(f'{elementDir}/title_panel.png')
  if titlePanel == None:
    return False
  Canvas.paste(titlePanel, (0, 0), titlePanel)
  font = ImageFont.truetype(font=f'{fontDir}/HarmonyOS_Sans_SC_Regular.ttf', size=32)
  ImageDraw.Draw(Canvas).text(text=Text, font=font, anchor='lt', xy=(64, 32), fill='#FFFFFF')
  return True


def Widget_MainPanel(Canvas: Image.Image, Height: int, PosY: int):
  tileSizeList = [(1764, 20), (1764, Height - 48), (1764, 28)]
  tilePosList = [(0, PosY), (0, PosY + 20), (0, PosY + Height - 28)]
  for i in range(0, 3):
    tile = util.ReadImageFile(f'{elementDir}/main_panel_{i}.png')
    if tile == None:
      return False
    tile = tile.resize(tileSizeList[i])
    Canvas.paste(tile, tilePosList[i], tile)
  return True
        

def Widget_Banner(Canvas: Image.Image, Text: str, PosY: int):  
  font = ImageFont.truetype(font=f'{fontDir}/HarmonyOS_Sans_SC_Regular.ttf', size=20)
  ImageDraw.Draw(Canvas).text(text=Text, font=font, anchor='mt', xy=(882, PosY), fill='#A2A2A2')
  

def Widget_Text_Left(Speaker: str, Name: str, Text: str, ShowSpeaker: bool):
  textImg = RenderTextMsg(Text, '#FFFFFF')  
  bubble = container.ChatBubble_Dark(textImg.width + 60, textImg.height + 40)
  if bubble == None: return None
  
  canvas = Image.new(mode='RGBA', size=(bubble.width + 125, bubble.height), color='#00000000')
  bubbleOffset = (125, 0)
  if ShowSpeaker:
    font = ImageFont.truetype(font=f'{fontDir}/HarmonyOS_Sans_SC_Regular.ttf', size=28)
    ImageDraw.Draw(canvas).text(text=Name, font=font, anchor='lt', xy=(125, 0), fill='#A7A7A7')    
    bubbleOffset = (125, 45)
    canvas = util.ExpandDown(canvas, max(140 - canvas.height, 45), '#00000000')
    avt = RenderAvatar(Speaker)
    if avt == None: return None    
    canvas.paste(avt, (0, 30), avt)
  canvas.paste(bubble, bubbleOffset, bubble)
  canvas.paste(textImg, (bubbleOffset[0] + 30, bubbleOffset[1] + 20), textImg)
  
  return canvas
    
    
def Widget_Text_Right(Speaker: str, Name: str, Text: str, ShowSpeaker: bool):
  textImg = RenderTextMsg(Text, '#000000')
  bubble = container.ChatBubble_Light(textImg.width + 60, textImg.height + 40)
  if bubble == None: return None
  
  canvas = Image.new(mode='RGBA', size=(bubble.width + 125, bubble.height), color='#00000000')
  bubbleOffset = (0, 0)
  if ShowSpeaker:
    bubbleOffset = (0, 45)
    canvas = util.ExpandDown(canvas, max(140 - canvas.height, 45), '#00000000')
    avt = RenderAvatar(Speaker)
    if avt == None: return None    
    canvas.paste(avt, (canvas.width - avt.width, 30), avt)
  canvas.paste(bubble, bubbleOffset, bubble)
  canvas.paste(textImg, (bubbleOffset[0] + 30, bubbleOffset[1] + 20), textImg)
  
  return canvas


def Widget_Pic_Left(Speaker: str, Name: str, PicPath: str, ShowSpeaker: bool):
  pic = util.ReadImageFile(PicPath)
  if pic == None: return None
  if pic.width > 500:  # 宽度大于500px则进行压缩
    pic = util.RestrictWidth(pic, 500)
  
  canvas = Image.new(mode='RGBA', size=(pic.width + 125, pic.height), color='#00000000')
  picOffset = (125, 0)
  if ShowSpeaker:
    font = ImageFont.truetype(font=f'{fontDir}/HarmonyOS_Sans_SC_Regular.ttf', size=28)
    ImageDraw.Draw(canvas).text(text=Name, font=font, anchor='lt', xy=(125, 0), fill='#A7A7A7')    
    picOffset = (125, 45)
    canvas = util.ExpandDown(canvas, max(140 - canvas.height, 45), '#00000000')
    avt = RenderAvatar(Speaker)
    if avt == None: return None    
    canvas.paste(avt, (0, 30), avt)
  canvas.paste(pic, picOffset, util.RoundedRectMask(pic.width, pic.height, 10))
  
  return canvas
  

def Widget_Pic_Right(Speaker: str, Name: str, PicPath: str, ShowSpeaker: bool):
  pic = util.ReadImageFile(PicPath)
  if pic == None:
    return None
  if pic.width > 500:  # 宽度大于500px则进行压缩
    pic = util.RestrictWidth(pic, 500)
    
  canvas = Image.new(mode='RGBA', size=(pic.width + 125, pic.height), color='#00000000')
  picOffset = (0, 0)
  if ShowSpeaker:
    picOffset = (0, 45)
    canvas = util.ExpandDown(canvas, max(140 - canvas.height, 45), '#00000000')
    avt = RenderAvatar(Speaker)
    if avt == None: return None
    canvas.paste(avt, (canvas.width - avt.width, 30), avt)    
  canvas.paste(pic, picOffset, util.RoundedRectMask(pic.width, pic.height, 10))
  
  return canvas
