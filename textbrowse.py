""" 
Text file browsing (and displaying) / Art gallery script for x/84
-----------------------------------------------------------------

This script lets the user browse the filesystem and look at text/ansi files.
The root dir is set by changing the startfolder variable.

You can also pass a textfile as an argument to the script.

Enjoy!
"""

from x84.bbs import getsession, echo, getch, gosub, getterminal, showart, Lightbar
from common import waitprompt
from textwrap import wrap
import os
import codecs

__author__ = 'Hellbeard'
__version__ = 2.0

LIGHTBAR_X = 5
LIGHTBAR_Y = 8
STARTFOLDER = os.path.join(os.path.dirname(__file__)+'/art/textfiles/', )

# ---------------------------------------------------

def banner():
    artfile = os.path.join(os.path.dirname(__file__), 'art', 'textbrowse.ans')
    banner = ''
    for line in showart(artfile, center=True):
        banner = banner + line
    return banner

# ---------------------------------------------------

def displayfile(filename):
    term = getterminal()
    session = getsession()
    asciitext = []
    text = []
    offset = 0
    quit = False
    dirty = True
    echo(term.clear)

    if os.path.splitext(filename)[1][1:].lower() == 'txt': #
        bengt = codecs.open(filename,encoding='cp437')
        for line in bengt:
            text.append(line+'\r')
    else:
        for line in showart(filename):
            text.append(line)

    while not quit:
        if dirty:
            echo(term.move(0,0)+term.normal)
            for i in range (0, term.height-1):
                if len(text) > i+offset:
                    echo(term.clear_eol+term.move_x(max(0,(term.width/2)-40))+text[i+offset])
        event, data = session.read_events(('input', 'refresh'))

        if event == 'refresh':
            echo(term.clear()) # to ensure there are no leftovers when resizing the window
            dirty = True
        if event == 'input':
            dirty = True
            session.buffer_input(data, pushback=True)
            inp = term.inkey(0)
            while inp:
                if inp.lower() == u'q' or inp.code == term.KEY_ESCAPE or inp.code == term.KEY_ENTER:
                    quit = True
                    break
                elif inp.code == term.KEY_HOME and offset > 0:
                    offset = 0
                elif inp.code == term.KEY_END and len(text) > term.height:
                    offset = len(text) - term.height+1
                elif inp.code == term.KEY_DOWN and len(text) > offset+term.height-1:
                    offset = offset + 1
                elif inp.code == term.KEY_UP and offset > 0:
                    offset = offset -1
                elif (inp.code == term.KEY_LEFT or inp.code == term.KEY_PGUP) and offset > 0:
                    if offset > term.height:
                        offset = offset - term.height+2
                    else:
                        offset = 0
                elif (inp.code == term.KEY_RIGHT or inp.code == term.KEY_PGDOWN) and offset+term.height-1 < len(text):
                    if (offset+term.height*2)-1 < len(text):
                        offset = offset + term.height-2
                    else:
                        offset = max(0, len(text) - term.height+1)
                else:
                    dirty = False
                inp = term.inkey(0)
         
# ---------------------------------------------------

def getfilelist(folder):
    term = getterminal()
    lb_names = []
    filenames = []

    for fn in sorted(os.listdir(folder)):
        filenames.append(fn)
        if os.path.isfile(folder+fn):
            fn = ' '+ fn + ' ' *(52-len(fn))+term.cyan+'[ File      ]'
            lb_names.append(fn)
        else:
            fn = u' '+ fn + '/' + ' ' *(51-len(fn))+term.cyan+'[ Directory ]'
            lb_names.append(fn)
    filelist = zip (filenames,lb_names)
    # converts the lightbar names and file names into tuples. keys / names for
    # the lightbar class to handle
    return filelist

# ---------------------------------------------------

def update_lightbar(lbar, term, filelist):
    if term.width > 79:
         lbar.height = 14
    else:
         lbar.height = max(4,term.height)
    if term.height > 22:
         lbar.yloc = LIGHTBAR_Y
    else:
         lbar.yloc = 0
    lbar.width = min(69,term.width)
    lbar.xloc = max(0,LIGHTBAR_X+(term.width/2)-40)
    lbar.update(filelist)
    echo(u''.join([lbar.refresh()])) 

# ---------------------------------------------------

def main(file=None, invert=False, Showart=True):
    """ Main procedure. """
    if file != None:
        displayfile(file)
        return
    session = getsession()
    term = getterminal()
    session.activity = 'Reading text files'
    currentfolder = []
    stored_lbar_pos = []
    filelist = getfilelist(STARTFOLDER)
    dirty = True
    inp = None
    lbar = Lightbar(height = 0, width = 0, xloc = 0, yloc = 0, colors={'highlight': term.bold_white_on_red})
    # sets up a lightbar. update_lightbar will give it it's actual values.

    echo(term.clear+banner()+term.hide_cursor)
    while 1:
        if dirty:
            update_lightbar(lbar,term,filelist)
            dirty = False
        while not inp:
            inp = getch(0.2)
            if session.poll_event('refresh'):
                echo(term.clear)
                if term.width > 79: echo(banner())
                update_lightbar(lbar,term,filelist)
                dirty = True
        lbar.process_keystroke(inp)
        if lbar.quit: 
            echo(term.normal_cursor)
            return
        echo(lbar.refresh_quick())
        if inp == term.KEY_ENTER:
            if lbar.selection[1] == '( .. ) GO BACK' or os.path.isdir(STARTFOLDER+u''.join(currentfolder)+lbar.selection[0]):
                if lbar.selection[1] == '( .. ) GO BACK':
                    del currentfolder[-1]
                    filelist = getfilelist(STARTFOLDER+u''.join(currentfolder))
                    lbar.update(filelist)
                    lbar.goto(stored_lbar_pos[-1])
                    del stored_lbar_pos[-1]
                else:
                    currentfolder.append(lbar.selection[0]+u'/')
                    stored_lbar_pos.append(lbar.index)
                    filelist = getfilelist(STARTFOLDER+u''.join(currentfolder))                        
                    lbar.goto(0)
                if len(currentfolder) > 0:
                    filelist.insert(0,['( .. ) GO BACK','( .. ) GO BACK'])
                lbar.update(filelist)
            else:
                displayfile(STARTFOLDER+u''.join(currentfolder)+lbar.selection[0])
                echo(term.clear+banner())
            dirty = True
        inp = None
