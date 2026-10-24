"""Build the case with the actual supplied template and a preserved official cover.
Run using a Python environment containing reportlab and pypdf.
The supplied original is not redistributed as a separate file.
"""
from pathlib import Path
from io import BytesIO
import re
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from pypdf import PdfReader, PdfWriter, Transformation
import argparse

root=Path(__file__).resolve().parent.parent
parser=argparse.ArgumentParser()
parser.add_argument('--template',required=True)
args=parser.parse_args()
out=root/'submission'
out.mkdir(exist_ok=True)
pdfmetrics.registerFont(TTFont('Arial',r'C:\Windows\Fonts\arial.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Bold',r'C:\Windows\Fonts\arialbd.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Italic',r'C:\Windows\Fonts\ariali.ttf'))
pdfmetrics.registerFontFamily('Arial',normal='Arial',bold='Arial-Bold',italic='Arial-Italic',boldItalic='Arial-Bold')
W,H=A4; M=43; WIDTH=W-2*M
ink=colors.HexColor('#171c29');muted=colors.HexColor('#555b6d');purple=colors.HexColor('#675192');light=colors.HexColor('#f2eef9')
body=ParagraphStyle('body',fontName='Arial',fontSize=9.5,leading=13.1,textColor=ink,spaceAfter=8)
heading=ParagraphStyle('head',fontName='Arial-Bold',fontSize=10.4,leading=13.5,textColor=purple)
small=ParagraphStyle('small',fontName='Arial',fontSize=8.2,leading=12,textColor=muted)
md=(root/'docs/CASE_DRAFT.md').read_text(encoding='utf-8')
pages=re.split(r'^## Body page \d+ \| .+$',md,flags=re.M)[1:]
body_words=len(re.findall(r"\S+",' '.join(pages)))
assert body_words<=1200,body_words
print('Body words (including section headings):',body_words)
buf=BytesIO();c=canvas.Canvas(buf,pagesize=A4)
c.setTitle('UNSCRIPTED | Flipkart APM Prompt 1 | Arkaprava Ghosh')
c.setAuthor('Arkaprava Ghosh')
def para(text,y,style=body,x=M,width=WIDTH):
 p=Paragraph(text.replace('&','&amp;'),style);pw,ph=p.wrap(width,H)
 p.drawOn(c,x,y-ph);return y-ph
def chrome(num,kicker,title,subtitle):
 c.setStrokeColor(purple);c.setLineWidth(1);c.line(M,H-35,W-M,H-35)
 c.setFillColor(muted);c.setFont('Arial',7.2);c.drawString(M,H-25,'FLIPKART APM ’29 / PROMPT 1');c.drawRightString(W-M,H-25,'ARKAPRAVA GHOSH / IIT MADRAS')
 c.setFont('Arial-Bold',8);c.setFillColor(purple);c.drawString(M,H-58,kicker)
 c.setFont('Arial-Bold',24);c.setFillColor(ink);c.drawString(M,H-88,title)
 c.setFont('Arial',9.5);c.setFillColor(muted);c.drawString(M,H-106,subtitle)
 c.setStrokeColor(colors.HexColor('#d9d4e3'));c.line(M,36,W-M,36)
 c.setFont('Arial',7);c.setFillColor(muted);c.drawString(M,23,'UNSCRIPTED / Intelligence is not authority.');c.drawRightString(W-M,23,f'CASE {num} / 2')
 return H-128

def page_body(text,num):
 y=chrome(num,'01 / THE PROBLEM' if num==1 else '02 / THE PRODUCT',"The right to change your mind." if num==1 else 'Keep the authority. Delegate the work.', 'A personal AI intent firewall for a world of capable agents.' if num==1 else 'One engine. Scoped permissions. A human at the consequential boundary.')
 if num==2:
  c.setFillColor(light);c.roundRect(M,y-39,WIDTH,39,5,fill=1,stroke=0)
  c.setFillColor(purple);c.setFont('Arial-Bold',8.4)
  c.drawCentredString(W/2,y-16,'PROPOSED ACTION  >  INTENT / AUTHORITY / PRIVACY / CONSEQUENCE')
  c.setFont('Arial',8.3);c.drawCentredString(W/2,y-29,'EXECUTE within contract    /    REVIEW for current intent    /    BLOCK prohibited actions')
  y-=51
 for block in re.split(r'\n\s*\n',text.strip()):
  if block.startswith('### '):
   lines=block.split('\n',1)
   y-=4;y=para(lines[0][4:],y,heading);y-=5
   if len(lines)>1:y=para(lines[1].replace('\n',' '),y);y-=6
  else:y=para(block.replace('\n',' '),y);y-=6
 print('Body page',num,'ends at y=',round(y,1))
 if y<51:raise RuntimeError(f'Page {num} overflows: {y}')
 c.showPage()
for i,p in enumerate(pages):page_body(p,i+1)

# One optional reference appendix; essential argument remains in the two body pages.
y=chrome('REF','REFERENCE APPENDIX / NON-EVALUATIVE','Evidence & definitions','Present-day research supports the question, not a claim of product effectiveness.')
refs=[
 ('[1] Ping Identity / 2026 Consumer Survey: AI Trust Report','Online Talker Research double-opt-in survey, 17–25 June 2026. Global n=11,000; India n=500 internet-connected consumers. The report narrative describes India’s 70% willingness to independently delegate decisions and access. The accessible report does not show that India-specific willingness item/base separately; the statistic is therefore attributed to the report. The displayed misrepresentation item totals 42% very + 45% somewhat concerned = 87%. Different questions; overlap is not established.','https://www.pingidentity.com/en-us/docs/assets/4423-2026-consumer-survey-ai-trust'),
 ('[2] Pew Research Center / 17 September 2025','How Americans View AI and Its Impact on People and Society. Survey of 5,023 US adults, 9–15 June 2025, weighted American Trends Panel. Full report p.16: 61% want more control over how AI is used; on a separate question, 57% have not too much/no control over whether AI is used in their lives. Not a comparison with India.','https://www.pewresearch.org/science/2025/09/17/how-americans-view-ai-and-its-impact-on-people-and-society/'),
 ('[3] Lee et al. / CHI 2025','The Impact of Generative AI on Critical Thinking: Self-Reported Reductions in Cognitive Effort and Confidence Effects From a Survey of Knowledge Workers. 319 workers; 936 examples. Higher confidence in GenAI was associated with lower reported critical-thinking effort. Association and self-report, not causal evidence. DOI: 10.1145/3706598.3713778.','https://doi.org/10.1145/3706598.3713778')]
for title,desc,url in refs:
 y=para(title,y,heading);y-=8;y=para(desc,y,body);y-=5
 p=Paragraph('<link href="'+url+'" color="#675192">Open primary source</link>',small);_,ph=p.wrap(WIDTH,H);p.drawOn(c,M,y-ph);y-=ph+26
y=para('Metric definitions',y,heading);y-=10
y=para('Valid authority: an enabled, unexpired, scoped contract with allowed recipient, within-limit amount and no prohibited exposure; high-impact execution additionally needs present, action-specific approval. Understandable authorization: the participant can correctly explain the action, recipient and commitment immediately after deciding. Unnecessary interruption: a permitted, low-risk, reversible task held for review. Unauthorized execution: an action executed without all applicable permissions.',y,body);y-=22
y=para('Prototype and evidence limits',y,heading);y-=10
y=para('All proposals, timestamps, tasks and outcomes in the demo are fictional simulations. No real agent is intercepted, no money moves, and no communication is sent. No participant study has been conducted. User intent is revisable. A first reaction is not proof of a true preference. Sources checked 24 October 2026. Full research notes are in docs/REFERENCES.md.',y,body)
if y<51:raise RuntimeError('Appendix overflow')
c.showPage();c.save();buf.seek(0)
body_pdf=PdfReader(buf)
original=PdfReader(args.template)

# Preserve original branding, statement and detail box. Replace only the candidate fields.
cover=original.pages[0]
over=BytesIO();oc=canvas.Canvas(over,pagesize=(1800,2250))
oc.setFillColor(colors.white);oc.rect(70,82,1655,570,fill=1,stroke=0)
oc.setFillColor(colors.HexColor('#1759c6'))
for txt,ypos,size in [('Arkaprava Ghosh',550,56),('Indian Institute of Technology Madras (IITM)',445,44),('DA25C003',340,50),('da25c003@smail.iitm.ac.in',235,48),('+91 8583992597',130,48)]:
 oc.setFont('Arial-Bold',size);oc.drawString(88,ypos,txt)
oc.save();over.seek(0);cover.merge_page(PdfReader(over).pages[0])
scale=W/1800;shift=(H-2250*scale)/2
writer=PdfWriter();cp=writer.add_blank_page(W,H)
cp.merge_transformed_page(cover,Transformation().scale(scale).translate(0,shift))
for i in range(2):
 # Keep the actual blank template body pages, including their original corner logo.
 bg=original.pages[i+2];p=writer.add_blank_page(W,H)
 p.merge_transformed_page(bg,Transformation().scale(W/1800,H/2250))
 p.merge_page(body_pdf.pages[i])
writer.add_page(body_pdf.pages[2])
writer.add_metadata({'/Title':'UNSCRIPTED - Flipkart APM Prompt 1','/Author':'Arkaprava Ghosh','/Subject':'Personal AI intent firewall - case and references'})
dest=out/'Arkaprava_Ghosh_IIT_Madras.pdf'
with dest.open('wb') as f:writer.write(f)
r=PdfReader(dest)
assert len(r.pages)==4
assert all(abs(float(p.mediabox.width)-W)<1 for p in r.pages)
assert all(abs(float(p.mediabox.height)-H)<1 for p in r.pages)
print('Created',dest,'with original cover + 2 body pages + 1 reference appendix')
