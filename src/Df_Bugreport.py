from PySide.QtCore import *
from PySide import QtGui
import Df, os, platform, subprocess, sys
from utils import *
import Df_Dialog, string


head = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
<HTML>
<HEAD>
    <META HTTP-EQUIV="CONTENT-TYPE" CONTENT="text/html; charset=windows-1252">
    <TITLE></TITLE>
    <META NAME="GENERATOR" CONTENT="LibreOffice 3.5  (Windows)">
    <META NAME="CREATED" CONTENT="20120607;16120700">
    <META NAME="CHANGED" CONTENT="20120626;9044166">
    <META NAME="Originator" CONTENT="Microsoft Word 14">
    <META NAME="ProgId" CONTENT="Word.Document">
    <STYLE TYPE="text/css">
    <!--
        P { color: #000000 }
        H2 { color: #000000 }
        H2.western { font-family: "Albany", sans-serif; font-size: 14pt; font-style: italic }
        H2.cjk { font-family: "HG Mincho Light J"; font-size: 14pt; font-style: italic }
        H2.ctl { font-family: "Arial Unicode MS"; font-size: 14pt; font-style: italic }
        A:link { color: #0000ff; so-language: zxx }
        A:visited { color: #800080 }
    -->
    </STYLE>
</HEAD>
<BODY LANG="en-US" TEXT="#000000" LINK="#0000ff" VLINK="#800080" DIR="LTR">
<H2 CLASS="western" STYLE="font-variant: normal; font-style: normal; text-decoration: none">
<FONT FACE="Arial, sans-serif"><FONT SIZE=5 STYLE="font-size: 20pt">Oops!
It seems Dragonfly Navigator crashed...</FONT></FONT></H2>
<P><FONT FACE="Arial, sans-serif"><FONT SIZE=4 STYLE="font-size: 16pt">Below
is an error message from the program. Please copy the message and
send it to <A HREF="mailto:henrik@dflynav.com">henrik@dflynav.com</A></FONT></FONT></P>
<P><FONT FACE="Arial, sans-serif"><FONT SIZE=4 STYLE="font-size: 16pt">Many
thanks for your patience...</FONT></FONT></P>
<P><FONT FACE="Arial, sans-serif"><FONT SIZE=4 STYLE="font-size: 16pt">Error
message:</FONT></FONT></P>
<P><FONT FACE="Courier New, monospace"><FONT SIZE=4 STYLE="font-size: 16pt"><pre>"""

tail="""</pre></FONT></FONT></P>
<P><FONT FACE="Arial, sans-serif"><FONT SIZE=4 STYLE="font-size: 16pt"> </FONT></FONT></P>
<P STYLE="margin-bottom: 0cm"><BR>
</P>
</BODY>
</HTML>"""

test = """Hej
  alla
barn
"""
def CheckForCrashReport():
    #Df.d.previousLog = test
    if Df.d.previousLog == "":
        return
    #log = string.replace(Df.d.previousLog, "\n", "<br>")
    log = Df.d.previousLog
    text = head + log + tail
    Df_Dialog.TextDialog("Oops", text, None)

