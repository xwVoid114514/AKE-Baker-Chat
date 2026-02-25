import gradio as gr
from Scripts import chatgen


def CreateUI():
  with gr.Blocks() as MainBlock:
    with gr.Row():
      with gr.Column():
        with gr.Row():
          FinalWidth = gr.Number(label='图片宽度', value=1080, minimum=720, maximum=2160, step=1)
          MarginWidth = gr.Number(label='边距宽度', value=20, minimum=0, maximum=100, step=1)
        OutputDir = gr.Textbox(label='输出路径', value='./Outputs', max_lines=1)
        ChatScript = gr.TextArea(label='聊天脚本', value='', lines=20, max_lines=100, autoscroll=True)
        Button_Run = gr.Button(value='生成', variant='primary')
        
      with gr.Column():
        Preview = gr.Image(label='预览', format='png', type='filepath', value=None, interactive=False)
        
    Button_Run.click(fn=chatgen.ChatGen_Run, inputs=[FinalWidth, MarginWidth, OutputDir, ChatScript], outputs=[Preview])    
  
  MainBlock.launch(inbrowser=True)
