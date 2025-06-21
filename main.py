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
        self.start_typing = False
        self.current_input = ""
        self.last_update  = 0
        self.caret_visible = True
        self.caret_timer = 0
        self.sample_text = """It is not hard to make money in the market. What is hard to avoid is the alluring temptations to throw your money away on short, get-rich-quick speculative binges. TIt is an obivious lesson, but one frequently ignored."""
        self.words = self.sample_text.split()
        self.current_word_idx = 0
        self.word_positions = self.compute_word_positions()
        self.design = self.create_ui(self.current_input)
        self.wpm = 0
        self.correct_words_typed = 0
        self.start_time = None
        
    #this precomputes the index of each word.[more easy way]
    def compute_word_positions(self):
        positions = []
        idx = 0
        for word in self.words:
            idx = self.sample_text.find(word, idx)
            positions.append(idx)
            idx += len(word)
        return positions


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

        curent_word = self.words[self.current_word_idx]
        word_start = self.word_positions[self.current_word_idx]


        sample_display = Text()
        completed_text = self.sample_text[:word_start] 
        sample_display.append(Text(completed_text, style="green"))  

        # highlighted text with the caret 
        input_chars = list(input_text)
        word_chars = list(curent_word)

        # caret placing individualactive 
        for i, char in enumerate(word_chars):
            if self.caret_visible and i == len(input_chars):
                sample_display.append(Text("_", style="bold green"))


            if i<len(input_chars):
                if char == input_chars[i]:
                    sample_display.append(Text(char, style="bold green"))
                else:
                    sample_display.append(Text(char, style="bold red"))
            else:
                sample_display.append(Text(char, style="white"))     
        

        remaining_text_start = word_start+ len(curent_word)
        remaining_text = self.sample_text[remaining_text_start:]
        sample_display.append(Text(remaining_text, style="dim"))


        if not self.start_typing:
            input_content = Text("type here...", style="yellow")
        else:
            input_content =Text(self.current_input, style="white")

        #main 
        mpx = layout["main"]
        mpx.split(
            Layout(
                Panel(
                    sample_display,
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
    

    ## replacer menu after completion
    def final_screen(self):
        final_panel = Panel(
            Align.center(
                f"[bold magenta]WPM: [green]{self.wpm:.2f}[/green][/bold magenta]",
                vertical="middle",
            ),
            title="RESULT",
            title_align="center",
            border_style="bright_magenta",
            box = box.HEAVY,
            padding=(3,10)
        )
        layout = Layout()
        layout.split(Layout(final_panel, name="result", ratio=1))
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
                        elif key == " ":
                            current_word = self.words[self.current_word_idx]
                            if self.current_input == current_word:
                                self.correct_words_typed +=1

                                if self.start_time is None:
                                    self.start_time = time.time()
                                else:
                                    elapsed_min = (time.time()-self.start_time)/60
                                    if elapsed_min >0:
                                        self.wpm = self.correct_words_typed / elapsed_min

                                self.current_word_idx+=1
                                self.current_input =""


                                if self.current_word_idx >= len(self.words):
                                    live.update(self.final_screen())
                                    while True:
                                        if msvcrt.kbhit():
                                            break
                                        time.sleep(0.1)
                                    self.console.print("\nExiting")
                                    sys.exit(0)
                              
                        elif key.isprintable():
                            if not self.start_typing:
                                self.start_typing = True
                            self.current_input +=key

                    now = time.time()
                    if now - self.last_update > 0.016:
                        live.update(self.create_ui(self.current_input))
                        self.last_update = now

                    time.sleep(0.016)
            except KeyboardInterrupt:
                self.console.print("\n Exiting___")
                sys.exit(0)           
                
               


    
                              
  
                    

#run after everything loaded only.. with live
if __name__ == "__main__":
    app = WayLander()
    app.run()


        