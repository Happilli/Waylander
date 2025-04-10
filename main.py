from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich import box
from rich.text import Text
from rich.align import Align
from rich.live import Live
from time import sleep

def create_ui():
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
    input_placholder = Text("type here...", style="yellow")
    layout["input_panel"].update(
        Panel(
          Align.left(input_placholder),
            border_style="bright_green",
            box=box.ROUNDED,
        )
    )
    return layout
                    

#run after everything loaded only.. with live
if __name__ == "__main__":
    console = Console()
    design = create_ui()

    with Live(design, refresh_per_second=4, screen=True) as live:
        try:
            while True:
                sleep(0.1)
        except KeyboardInterrupt:
            pass        
