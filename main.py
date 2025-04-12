from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich import box
from rich.text import Text
from rich.align import Align
from rich.live import Live
import msvcrt #-> this in window specific 
import time
import sys

class WayLander:
    def __init__(self):
        self.console = Console()
        self.current_input = ""
        self.last_update  = 0
        self.design = self.create_ui(self.current_input)
    
    def get_key(self):
        if msvcrt.kbhit():
            try:
                return msvcrt.getch().decode("utf-8")
                
            except:
                return None
        return None
    
    def create_ui(self, input_text=""):
        layout = Layout()

        if not hasattr(self, "_top_panel"):
            self._top_panel = Panel(
                Align.center("WayLander", style="bold red"),
                border_style="bright_blue",
                box=box.ROUNDED,
            )
     
        #splittiing 
        layout.split(
            Layout(self._top_panel,name="top", ratio=1),
            Layout(name="main", ratio=9),
        )    
        
        sample_text = """ It is not hard to make money in the market. What is hard to avoid is the alluring temptations to throw your money away on short, get-rich-quick speculative binges. TIt is an obivious lesson, but one frequently ignored."""
        input_content = Text(input_text if input_text else "type here...", style="yellow" if not input_text else "white")
        
        #main 
        mpx = layout["main"]
        mpx.split(
            Layout(
                Panel(
                    sample_text.strip(),
                title="STUFF TO TYPE",
                title_align="center",
                border_style="bright_blue",
                box=box.ROUNDED,
                padding=(1,1)
             ),
             name="text_panel",
             ratio=9
        ),
        Layout(
             Panel(
                 Align.left(input_content),
                 border_style="bright_green",
                 box=box.ROUNDED,
                 ),
                 name="input_panel",
                 ratio=1
             )
        )
        return layout     

    def run(self):
        with Live(self.design, refresh_per_second=120, screen=True) as live:
            try:
                while True:    
                    key = self.get_key()
                    if key:
                        if key == "\x03":
                            raise KeyboardInterrupt
                        elif key == "\x08": #for linux dev need to update it accordingly....
                            self.current_input = self.current_input[:-1]
                        elif key == "\r":
                            pass
                        elif key and key.isprintable():
                            self.current_input += key
                     
                        now = time.time()
                        if now - self.last_update > 0.016: #60 fps
                            live.update(self.create_ui(self.current_input))
                            self.last_update = now
                    

                    time.sleep(0.016)       
            except KeyboardInterrupt:
                self.console.print("\nExiting...")
                sys.exit(0) 

  
                    

#run after everything loaded only.. with live
if __name__ == "__main__":
    app = WayLander()
    app.run()


        