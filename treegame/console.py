import pygame
import time
import copy
from . import settings

class console(object):
    def __init__(self,maininstance):
        self.main = maininstance
        self.messages = []
        self.size = settings.console_pos_lt - settings.console_pos_lt
        self.pos_lb = settings.console_pos_lt; self.pos_lb[1] = settings.console_pos_rb[1] 

    def draw(self):
        # TBI : plot the latest messages (that fit?) at the respective window position
        # q: qhat to do about multi-line messages? --> smaller text 
        msg_lcenter = copy.copy(self.pos_lb)
        for i,message in enumerate(reversed(self.messages)):
            if message.toscreen==False:
                if message.printed is False:
                    print(message)    
            else:
                #message goes to screen ... draw it!
                msgstr = str(message)   
                text = self.main.gui.font.render(msgstr,False,[0,0,0])   
                width,height = text.get_size()   
                msg_lcenter[1] -= height # first add the height, since screen.blit uses pos as upper left position
                self.main.gui.screen.blit(text,msg_lcenter)
                msg_lcenter[1] -= settings.console_line_offset 
                if msg_lcenter[1] - height >= settings.console_pos_lt[1]:
                    # there is no more space for older messages, exit loop!
                    break 

            
        return

    def log_to_file(self):
        # TBI
        return

    def add_message(self,message_str,toscreen=True):
        self.messages.append(message(self,text=message_str,toscreen=toscreen))
        return

    def __call__(self,message_str,toscreen=True):
        self.add_message(message_str,toscreen=toscreen)
        return

class message(object):
    def __init__(self,console_inst,text=None,toscreen=True):
        self.console = console_inst
        self.text = text
        self.time = time.time()
        self.toscreen = toscreen
        self.mxlen = settings.console_text_maxlen
        self.printed = False
        return
    
    def draw(self):
        # not yet sure if that should go here ... 
        return

    def timestring(self):
        elapsed = self.time - self.console.main.time_zero
        if self.toscreen is False:
            elapsed_str = '%02d:%08.5f' % (int(elapsed/60), elapsed % 60)
        else:
            elapsed_str = '%02d:%02d' % (int(elapsed/60), int(elapsed % 60))
        return elapsed_str

    def __str__(self):
        self.printed = True
        return(self.timestring()+' '+self.text)
        
    