from art import *
body = (sky("sh", [(0,"#1b1640"),(1,"#4a2a5a")]) + ground(1700, "#3a2a20", INK)
  + hanuman("h1", 200, 1650, .55) + hanuman("h2", 540, 1650, .55, arms=(160,-160), gada=False, mood="determined")
  + hanuman("h3", 880, 1650, .55, mood="think")
  + lakshman("l1", 200, 820, .5) + sushen("s1", 540, 820, .5) + mountain("m1", 850, 760, .45, herbs=30, underside=True)
  + hanuman("h4", 300, 1180, .4, rot=65, arms=(160,0)) + lakshman("l2", 600, 1150, .4, rot=88, eyes_shut=True, bow=False)
  + arrow("a1", 880, 1000, .8) + herb_icon("hi", 900, 1150, .7))
html = f'<html><body style="margin:0">{SHARED_DEFS}<svg viewBox="0 0 1080 1920" width="1080" height="1920">{body}</svg></body></html>'
open("sheet.html","w").write(html)
