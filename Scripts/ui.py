import gradio as gr
from Scripts import chatgen, util


def CreateUI():
  with gr.Blocks(title='AKE Baker Chat') as MainBlock:
    with gr.Row():
      with gr.Column():
        with gr.Row(variant='panel'):
          FinalWidth = gr.Number(label='图片宽度', value=1080, minimum=720, maximum=2160, step=1)
          MarginWidth = gr.Number(label='边距宽度', value=20, minimum=0, maximum=100, step=1)
        with gr.Group():
          with gr.Row():
            ScriptFilePath = gr.Textbox(label='从txt文件加载', value='', placeholder='输入脚本文件路径', max_lines=1, scale=15)
            with gr.Column(min_width=70, scale=1):
              Button_LoadFromFile = gr.Button(value='加载', variant='secondary', size='lg')
              Button_Clear = gr.Button(value='清空', variant='secondary', size='lg')
          ChatScript = gr.TextArea(label='聊天脚本', value='', lines=20, max_lines=100, autoscroll=True)
        OutputDir = gr.Textbox(label='输出路径', value='./Outputs', max_lines=1)
        with gr.Row():
          Button_Render = gr.Button(value='生成', variant='primary')
          Button_Save = gr.Button(value='保存', variant='primary')
      with gr.Column():
        Preview = gr.Image(label='预览', format='png', type='filepath', value=None, interactive=False)
    
    Button_Clear.click(fn=lambda: None, outputs=[ChatScript])
    Button_LoadFromFile.click(fn=util.LoadScriptFromFile, inputs=[ScriptFilePath], outputs=[ChatScript])  
    Button_Render.click(fn=chatgen.RenderChat, inputs=[FinalWidth, MarginWidth, ChatScript], outputs=[Preview])
    Button_Save.click(fn=chatgen.SaveChat, inputs=[OutputDir, Preview], outputs=[])    
  
  MainBlock.launch(inbrowser=True)
