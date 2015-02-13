Text browser / Ansi Art gallery script for x/84
-----------------------------------------------------------------
This script enables the user to browse the filesystem and look at ascii/ansi files.

Installation instructions
-------------------------
1. Copy textbrowse.py to your default script directory.
2. Copy textbrowse.ans to your art directory.
3. Change the 'startfolder' variable in textbrowse.py to whatever directory you want to use as a starting point for the script.

You can also pass a textfile as an argument to the script.

Using the script to display .txt files in fbrowse.py
----------------------------------------------------
As the fbrowse.py script is being updated constantly there can't be any precise installation instructions.

1. Search for 'if lightbar.selected or inp in (term.KEY_LEFT, term.KEY_RIGHT,):' in fbrowse.py
2. Add the following lines of code beneath that line:

   ```python
   if ext in COLLY_EXTENSIONS
           and (lightbar.selected or inp is term.KEY_RIGHT):
       gosub('textbrowse',filepath,'/',filename)
       draw_interface(term, lightbar)
   ```
   
Enjoy!
