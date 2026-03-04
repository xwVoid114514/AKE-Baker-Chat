# ---------- 脚本格式 ----------
# 标题：h|[内容]
# 例：h|Z7行动组
#
# 聊天文本：<tl|tr>|<ID>|<昵称>|[内容]
# 例：tr|endmin|管理员|拉电线哈哈！
#
# 聊天图片：<pl|pr>|<ID>|<昵称>|[图片路径]
# 例：pl|chenqy|陈千语|./chatimg/noobchen.png
#
# 横幅消息: b|[内容]
# 例：b|超级炸弹人 被禁言1天


from Scripts import widget, util
from PIL import Image
import random, os, shutil


chatScriptLines: list[str] = []
lineIndex = 0

finalWidth = 1080
margin = 20

cacheDir = './Cache'
  

def SplitChatScript(Script: str, FirstRun: bool) -> list[str] | None:
  global chatScriptLines, lineIndex
  
  if FirstRun:
    chatScriptLines = Script.splitlines(False)
    lineIndex = 0
    print(f'[INFO] Loaded {len(chatScriptLines)} line(s).')
    return None
  
  csLine = chatScriptLines[lineIndex].lstrip(' ')
  lineIndex += 1
    
  argCount = 0
  if csLine.startswith('h|'):
    argCount = 1
  elif csLine.startswith('b|'):
    argCount = 1
  elif csLine.startswith('tl|') or csLine.startswith('tr|'):
    argCount = 3
  elif csLine.startswith('pl|') or csLine.startswith('pr|'):
    argCount = 3
  else:
    return None
  return csLine.split('|', argCount)
  

def RenderChat(FinalWidth: int, MarginWidth: int, ChatScript: str) -> str:
  global chatScriptLines, lineIndex, finalWidth, margin
  
  finalWidth = FinalWidth
  margin = MarginWidth
  
  chatImg = Image.new(mode='RGBA', size=(1764, 2000), color='#1F1F1FFF') # 1F1F1FFF
  
  SplitChatScript(ChatScript, True)
  hasSetTitle = False
  msg = None
  elementPos = (27, 135)
  interval = 18
  prevSpeaker = ''
  while lineIndex < len(chatScriptLines):
    csArgs = SplitChatScript(ChatScript, False)
    if csArgs == None: continue
    
    if csArgs[0] == 'h':  # 标题
      wgt = widget.Widget_Title(csArgs[1])
      if wgt != None:
        chatImg.paste(wgt, (0, 0), wgt)
        hasSetTitle = True
        continue
      
    elif csArgs[0] == 'b':  # 横幅消息
      widget.Widget_Banner(chatImg, csArgs[1], elementPos[1])
      elementPos = (27, elementPos[1] + 40)
      continue
      
    elif csArgs[0] == 'tl':  # 左侧文本消息
      #说话人与前一条相同，不显示此条消息的说话人
      msg = widget.Widget_Text_Left(csArgs[1], csArgs[2], csArgs[3], (csArgs[1] != prevSpeaker))
      elementPos = (27, elementPos[1])
      interval = 18
      prevSpeaker = csArgs[1]
      
    elif csArgs[0] == 'tr':  # 右侧文本消息
      msg = widget.Widget_Text_Right(csArgs[1], csArgs[2], csArgs[3], (csArgs[1] != prevSpeaker))
      if msg == None: continue
      elementPos = (chatImg.width - 27 - msg.width, elementPos[1])
      interval = 18
      prevSpeaker = csArgs[1]
      
    elif csArgs[0] == 'pl':  # 左侧图片消息
      msg = widget.Widget_Pic_Left(csArgs[1], csArgs[2], csArgs[3], (csArgs[1] != prevSpeaker))
      elementPos = (27, elementPos[1])
      interval = 12
      prevSpeaker = csArgs[1]
      
    elif csArgs[0] == 'pr':  # 右侧图片消息
      msg = widget.Widget_Pic_Right(csArgs[1], csArgs[2], csArgs[3], (csArgs[1] != prevSpeaker))
      if msg == None: continue
      elementPos = (chatImg.width - 27 - msg.width, elementPos[1])
      interval = 12
      prevSpeaker = csArgs[1]
      
    if msg == None: continue
    if elementPos[1] + msg.height + 50 >= chatImg.height:
      chatImg = util.ExpandDown(chatImg, elementPos[1] + msg.height + 50 - chatImg.height, '#1F1F1FFF')
    chatImg.paste(msg, elementPos, msg)
    elementPos = (elementPos[0], elementPos[1] + msg.height + interval)
  
  # 设置默认标题    
  if hasSetTitle == False:
    wgt = widget.Widget_Title('未标题')
    if wgt != None:
      chatImg.paste(wgt, (0, 0), wgt) 
    
  widget.Widget_MainPanel(chatImg, chatImg.height - 98, 98)
  
  chatImg = util.AddMargin(util.RestrictWidth(chatImg, finalWidth - margin * 2), margin, '#1F1F1FFF')
  
  if not os.path.exists(cacheDir):
    os.makedirs(cacheDir)
  filename = f'{hex(random.randint(0x00000000, 0xFFFFFFFF))[2:]}.png'
  util.SaveImage(chatImg, f'{cacheDir}/{filename}')
  
  return f'{cacheDir}/{filename}'


def SaveChat(OutputDir: str, CacheImagePath: str) -> None:
  try:
    if CacheImagePath == None: return
    if not os.path.exists(OutputDir):
      os.makedirs(OutputDir)
    shutil.copyfile(CacheImagePath, f'{OutputDir}/chat_{os.path.basename(CacheImagePath)}')
    util.ShowInfo(f'成功保存聊天图片：chat_{os.path.basename(CacheImagePath)}')
  except:
    util.ShowError('保存聊天图片时出错！')
