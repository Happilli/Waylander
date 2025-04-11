from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich import box
from rich.text import Text
from rich.align import Align
from rich.live import Live
import msvcrt #-> this in window specific 

def get_key():
    if msvcrt.kbhit():
        try:
           return msvcrt.getch().decode("utf-8")
        except UnicodeDecodeError:
            return None
    return None

def create_ui(input_text=""):
    layout = Layout()

    #splittiing 
    layout.split(
        Layout(name="top", ratio=1),
        Layout(name="main", ratio=9),
    )    
    heading = Text("WayLander", style="bold red")                
    layout["top"].update(
        Panel(
            Align.center(heading),
            border_style="bright_blue",
            box=box.ROUNDED,
        )
    )
    #Main
    layout["main"].split(
        Layout(name="text_panel", ratio=9),
        Layout(name="input_panel", ratio=1)
    )
    sample_text = """ It is not hard to make money in the market. What is hard to avoid is the alluring temptations to throw your money away on short, get-rich-quick speculative binges. TIt is an obivious lesson, but one frequently ignored."""
    
    #main split one
    layout["text_panel"].update(
        Panel(
            sample_text.strip(),
            title="STUFF TO TYPE",
            title_align="center",
            border_style="bright_blue",
            box=box.ROUNDED,
            padding=(1,1)
        )
    )
    #Main split two
    input_content = Text(input_text if input_text else "tye here...", style="yellow" if not input_text else "white")
    layout["input_panel"].update(
        Panel(
          Align.left(input_content),
            border_style="bright_green",
            box=box.ROUNDED,
        )
    )
    return layout
                    

#run after everything loaded only.. with live
if __name__ == "__main__":
    console = Console()
    current_input=""
    design = create_ui(current_input)


    with Live(design, refresh_per_second=120, screen=True) as live:
        try:
            while True:
                key = get_key()
                if not key:
                    continue
                
                ## handilng main keystrokes
                if key == "\x03":
                     raise KeyboardInterrupt
                elif key == "\x08": #for linux dev need to update it accordingly....
                    current_input = current_input[:-1]
                elif key == "\r":
                    pass
                elif key and key.isprintable():
                    current_input += key

                live.update(create_ui(current_input))  
        except KeyboardInterrupt:
            pass        
