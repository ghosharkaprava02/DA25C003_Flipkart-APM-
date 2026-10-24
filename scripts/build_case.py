"""Editorial layout for the existing case. The prototype and its assets stay untouched."""
from pathlib import Path
from io import BytesIO
from html import escape
import re,json,argparse
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from pypdf import PdfReader,PdfWriter,Transformation

root=Path(__file__).resolve().parent.parent
parser=argparse.ArgumentParser();parser.add_argument('--template',required=True);args=parser.parse_args()
out=root/'submission';out.mkdir(exist_ok=True)
for name,file in [('Arial','arial.ttf'),('Arial-Bold','arialbd.ttf'),('Arial-Italic','ariali.ttf')]:
 pdfmetrics.registerFont(TTFont(name,str(Path(r'C:\Windows\Fonts')/file)))
pdfmetrics.registerFontFamily('Arial',normal='Arial',bold='Arial-Bold',italic='Arial-Italic',boldItalic='Arial-Bold')
W,H=A4;M=39;WIDTH=W-2*M;GAP=23;COL=(WIDTH-GAP)/2;RX=M+COL+GAP
P={k:colors.HexColor(v) for k,v in {'paper':'#F7F4EC','ink':'#202A38','muted':'#515B65','violet':'#66518B','line':'#D9D4C9','white':'#FFFCF6','teal':'#326C65','tealbg':'#E5EEEA','amber':'#865E22','amberbg':'#F3E9D6','coral':'#955148','coralbg':'#F2E3DD','violetbg':'#ECE6F2'}.items()}
body=ParagraphStyle('Body',fontName='Arial',fontSize=9.25,leading=12.05,textColor=P['ink'])
note=ParagraphStyle('Note',parent=body,fontSize=8,leading=10.4,textColor=P['muted'])
heading=ParagraphStyle('Heading',fontName='Arial-Bold',fontSize=10.5,leading=13,textColor=P['ink'])
micro=ParagraphStyle('Micro',parent=note,fontSize=7.5,leading=9.6)
md=(root/'docs/CASE_DRAFT.md').read_text(encoding='utf-8')
sections={m.group(1).strip():m.group(2).strip() for m in re.finditer(r'^### ([^\n]+)\n(.*?)(?=^### |^## |\Z)',md,re.M|re.S)}
buf=BytesIO();c=canvas.Canvas(buf,pagesize=A4)
c.setTitle('UNSCRIPTED | Flipkart APM Prompt 1 | Arkaprava Ghosh');c.setAuthor('Arkaprava Ghosh');boxes=[]
def para(text,x,y,width,style=body,tag='body',markup=False):
 p=Paragraph(text if markup else escape(text),style);_,ph=p.wrap(width,H)
 assert y-ph>=43,f'{tag} overflow: {y-ph}'
 p.drawOn(c,x,y-ph);boxes.append({'page':c.getPageNumber(),'kind':tag,'x':x,'top':y,'bottom':y-ph,'width':width,'font_pt':style.fontSize})
 return y-ph
def label(text,x,y,color='muted',size=7.1):
 c.setFont('Arial-Bold',size);c.setFillColor(P[color]);c.drawString(x,y,text)
def rect(x,y,w,h,fill,stroke=None,r=5):
 c.setFillColor(P[fill]);c.setStrokeColor(P[stroke or fill]);c.setLineWidth(.65);c.roundRect(x,y,w,h,r,stroke=bool(stroke),fill=1)
def chrome(num):
 # Keep the official template's corner logo visible in the original footer region.
 c.setFillColor(P['paper']);c.rect(0,44,W,H-44,fill=1,stroke=0)
 label('FLIPKART APM ’29  /  PROMPT 1',M,H-28,size=7)
 c.setFont('Arial',7);c.drawRightString(W-M,H-28,'ARKAPRAVA GHOSH  /  IIT MADRAS')
 c.setStrokeColor(P['line']);c.setLineWidth(.65);c.line(M,H-38,W-M,H-38);c.line(M,36,W-M,36)
 c.setFont('Arial',7);c.setFillColor(P['muted']);c.drawString(M,23,'UNSCRIPTED  /  Intelligence is not authority.')
 c.drawRightString(W-M,23,f'CASE {num} / 2' if isinstance(num,int) else 'REFERENCE APPENDIX')
def bold(text,phrases):
 t=escape(text)
 for phrase in phrases:t=t.replace(escape(phrase),'<b>'+escape(phrase)+'</b>')
 return t
def block(title,text,x,y,width=COL,phrases=()):
 y=para(title,x,y,width,heading,'heading')-7
 for p in text.split('\n\n'):y=para(bold(p,phrases),x,y,width,body,markup=True)-8
 return y
def arrow(x,y,color='muted',length=13):
 c.setStrokeColor(P[color]);c.setLineWidth(.8);c.lines([(x,y,x+length,y),(x+length-3,y+2,x+length,y),(x+length-3,y-2,x+length,y)])

# Main page 1: the same problem argument, evidence and opportunity.
chrome(1)
c.setFillColor(P['violet']);c.setFont('Arial-Bold',37)
t=c.beginText(M,H-87);t.setCharSpace(1.1);t.textOut('UNSCRIPTED');t.setCharSpace(0);c.drawText(t)
c.setStrokeColor(P['violet']);c.setLineWidth(1.8);c.lines([(W-M-24,H-57,W-M,H-57),(W-M,H-57,W-M,H-81)])
c.setFont('Arial',11);c.setFillColor(P['ink']);c.drawString(M,H-108,'Intelligence is not authority.')
quote='“In 2040, your AI may know you better than you know yourself. But does that give it the right to decide for you?”'
qs=ParagraphStyle('Question',parent=body,fontName='Arial-Italic',fontSize=9.7,leading=13.5)
y=para(quote,M,H-126,WIDTH-10,qs,'opening')-14
c.setFillColor(P['violet']);c.setFont('Arial-Bold',10.6);c.drawString(M,y-4,'Prediction is not permission.');y-=27
left=block("A decision that almost wasn't yours",sections["A decision that almost wasn't yours"],M,y)
left=block('My scope and assumptions',sections['My scope and assumptions'],M,left-5)
why=sections['Why protect authority?'].split('\n\n')
ramifications,propagation=why[0].split('When agents transact',1)
left=block('Why protect authority?',ramifications.strip(),M,left-5)
right=block('Why this problem first?','When agents transact'+propagation+'\n\n'+why[1],RX,y)
right=block('The product opportunity',sections['The product opportunity'],RX,right-7)
right=block('Why capture intent before advice?',sections['Evidence that shaped the design'].split('\n\n')[-1],RX,right-7)
top=min(left,right)-6;label('EVIDENCE THAT SHAPED THE DESIGN',M,top,size=7.2);top-=12
cw=(WIDTH-20)/3;ch=100
stats=[('70%','INDIA','Willingness to independently delegate decisions and access to AI.','Ping Identity · 2026 [1]','violet','violetbg'),('87%','INDIA','Concern that an agent could misrepresent personality or values.','Ping Identity · 2026 [1]','coral','coralbg'),('61%','USA','Would like more control over how AI is used in their lives.','Pew Research Center · 2025 [2]','teal','tealbg')]
for i,(number,geo,caption,source,tone,bg) in enumerate(stats):
 x=M+i*(cw+10);bottom=top-ch;rect(x,bottom,cw,ch,bg)
 c.setFillColor(P[tone]);c.setFont('Arial-Bold',28);c.drawString(x+12,top-32,number)
 label(geo,x+cw-40,top-26,color=tone,size=7.3);para(caption,x+12,top-41,cw-24,note,'stat-caption')
 label(source,x+12,bottom+10,color=tone,size=7.5)
y=para('India: n=500 online consumers. USA: n=5,023 adults. Different questions and samples; no same-person overlap, country ranking or validated product demand. The 70% figure is attributed to the report narrative; item/base caveat in [1].',M,top-ch-9,WIDTH,micro,'evidence-caveat')-13
dh=66;bottom=y-dh;assert bottom>=47,f'Page 1 diagram needs more room: {bottom}'
rect(M,bottom,WIDTH,dh,'white','line');label('WHERE THE BOUNDARY BELONGS',M+12,y-13,size=7)
steps=[('AI knows preferences','“Stay in India” · 2036','muted'),('AI assumes authority','Treats preference as consent','amber'),('Consequential action','Proposes rejecting Tokyo','coral'),('UNSCRIPTED restores','Human decides before action','violet')]
sw=(WIDTH-24)/4
for i,(title,detail,tone) in enumerate(steps):
 x=M+12+i*sw;label(title,x,y-31,color=tone,size=7.35);para(detail,x,y-39,sw-13,micro,'boundary-caption')
 if i<3:arrow(x+sw-16,y-29,length=10)
c.showPage()

# Main page 2: product behavior, priorities, feasibility and how to test success.
chrome(2);label('02 / THE PRODUCT AND THE TEST',M,H-58,color='violet',size=7.4)
c.setFillColor(P['ink']);c.setFont('Arial-Bold',23);c.drawString(M,H-87,'Keep the authority. Delegate the work.')
y=para('A personal AI intent firewall: a shared, deterministic engine checks each structured proposal. An agent can explain a rule; it cannot expand its permission.',M,H-105,WIDTH,body)-10
eh=77;eb=y-eh;rect(M,eb,WIDTH,eh,'white','line');label('SOVEREIGNTY ENGINE',M+12,y-14,color='violet')
rect(M+12,eb+15,89,34,'violetbg');para('<b>Proposed action</b><br/>Agent submits a scope',M+19,eb+42,76,micro,'engine',markup=True);arrow(M+108,eb+32,length=15)
rect(M+132,eb+9,191,46,'paper','line');para('<b>Intent freshness</b> · <b>Authority</b><br/>Third-party exposure · Consequence',M+142,eb+43,172,note,'engine',markup=True);arrow(M+329,eb+32,length=14)
for text,tone,bg,off in [('EXECUTE / within contract','teal','tealbg',48),('REVIEW / current intent','amber','amberbg',28),('BLOCK / prohibited action','coral','coralbg',8)]:
 rect(M+353,eb+off,WIDTH-365,17,bg,r=3);label(text,M+363,eb+off+5,color=tone,size=7.7)
y=para('Intent Contracts define scope, recipients, limits and expiry. A Decision Passport records the original assumption, first response, contract snapshot, rule, authorization and simulated outcome.',M,eb-10,WIDTH,body)-10
scenarios=sections['Three boundaries, one system'].split('\n\n')
scenarios[0]=scenarios[0].replace('Exploring never means accepting the job; deferring does not stop the deadline.','Exploring is not accepting. Deferring does not stop the deadline.')
scenarios[1]=scenarios[1].replace('Changing a permission is not making a transaction.','Changing a limit is not approving a transaction.')
scenarios[2]=scenarios[2].replace("The user cannot grant themselves another person's consent.",'Consent for oneself is not consent for another.')
principles=['Exploring is not accepting.','Changing a limit is not approving a transaction.','Consent for oneself is not consent for another.']
label('THREE BOUNDARIES, ONE SYSTEM',M,y,size=7.2);y-=12
for title,text,tone in zip(['CAREER / TOKYO','MONEY / INR 200,000','PRIVACY / NON-USERS'],scenarios,['violet','amber','coral']):
 start=y;c.setFillColor(P[tone]);c.rect(M,y-12,2.2,12,fill=1,stroke=0)
 a=para(title,M+10,y,105,ParagraphStyle('ScenarioHead',parent=micro,fontName='Arial-Bold',textColor=P[tone]),'scenario-label')
 b=para(bold(re.sub(r'^(Career|Money|Privacy): ','',text),principles),M+126,start,WIDTH-126,body,'scenario',markup=True);y=min(a,b)-8
left=right=y-1;mvp=sections['What I build first, and what I defer'].split('\n\n')
left=block('What I build first, and defer',mvp[0],M,left)
left=block('Feasibility and the failure boundary',mvp[1],M,left-5)
metrics=sections['How I would know it works'].split('\n\n')
metrics[0]=metrics[0].replace('Pair this with overall task completion so blocking everything cannot look successful.','Blocking everything is not success. Pair this with overall task completion.')
right=block('How I would know it works',metrics[0],RX,right,phrases=['Blocking everything is not success.'])
right=block('The first test',metrics[1],RX,right-5)
y=block('The trade-off and the path in',sections['The trade-off and the path in'],M,min(left,right)-5,WIDTH)-3
cb=y-35;assert cb>=46,f'Page 2 CTA overflows: {cb}'
url='https://ghosharkaprava02.github.io/DA25C003_Flipkart-APM-/'
rect(M,cb,WIDTH,35,'tealbg');label('TRY THE PROTOTYPE / ALL ACTIONS ARE SIMULATED',M+12,cb+21,color='teal',size=7.5)
para(url,M+12,cb+15,WIDTH-24,micro,'cta')
c.linkURL(url,(M,cb,W-M,cb+35),relative=0,thickness=0);c.showPage()

# The original evidence and metric definitions, retained in one optional appendix.
chrome('REF');label('REFERENCE APPENDIX / NON-EVALUATIVE',M,H-58,color='violet')
c.setFont('Arial-Bold',25);c.setFillColor(P['ink']);c.drawString(M,H-90,'Evidence & definitions')
y=para('Present-day research supports the question, not a claim of product effectiveness.',M,H-105,WIDTH,body)-24
refs=[
('[1] Ping Identity / 2026 Consumer Survey: AI Trust Report','Online Talker Research double-opt-in survey, 17-25 June 2026. Global n=11,000; India n=500 internet-connected consumers. The report narrative describes India’s 70% willingness to independently delegate decisions and access. The accessible report does not show that India-specific willingness item/base separately; the statistic is therefore attributed to the report. The displayed misrepresentation item totals 42% very + 45% somewhat concerned = 87%. Different questions; overlap is not established.','https://www.pingidentity.com/en-us/docs/assets/4423-2026-consumer-survey-ai-trust'),
('[2] Pew Research Center / 17 September 2025','How Americans View AI and Its Impact on People and Society. Survey of 5,023 US adults, 9-15 June 2025, weighted American Trends Panel. Full report p.16: 61% want more control over how AI is used; on a separate question, 57% have not too much/no control over whether AI is used in their lives. Not a comparison with India.','https://www.pewresearch.org/science/2025/09/17/how-americans-view-ai-and-its-impact-on-people-and-society/'),
('[3] Lee et al. / CHI 2025','The Impact of Generative AI on Critical Thinking: Self-Reported Reductions in Cognitive Effort and Confidence Effects From a Survey of Knowledge Workers. 319 workers; 936 examples. Higher confidence in GenAI was associated with lower reported critical-thinking effort. Association and self-report, not causal evidence. DOI: 10.1145/3706598.3713778.','https://doi.org/10.1145/3706598.3713778')]
for title,desc,source in refs:
 y=block(title,desc,M,y,WIDTH)
 y=para('<link href="'+source+'" color="#66518B">Open primary source</link>',M,y,WIDTH,note,'source-link',markup=True)-22
y=block('Metric definitions','Valid authority: an enabled, unexpired, scoped contract with allowed recipient, within-limit amount and no prohibited exposure; high-impact execution additionally needs present, action-specific approval. Understandable authorization: the participant can correctly explain the action, recipient and commitment immediately after deciding. Unnecessary interruption: a permitted, low-risk, reversible task held for review. Unauthorized execution: an action executed without all applicable permissions.',M,y,WIDTH)-11
y=block('Prototype and evidence limits','All proposals, timestamps, tasks and outcomes in the demo are fictional simulations. No real agent is intercepted, no money moves, and no communication is sent. No participant study has been conducted. User intent is revisable. A first reaction is not proof of a true preference. Sources checked 24 October 2026. Full research notes are in docs/REFERENCES.md.',M,y,WIDTH)-10
label('PROTOTYPE',M,y,color='teal');para('<link href="'+url+'" color="#326C65">'+url+'</link>',M,y-9,WIDTH,note,'prototype-link',markup=True)
c.showPage();c.save();buf.seek(0)

# Preserve the actual official cover and body-page branding, rather than recreating a template.
body_pdf=PdfReader(buf);original=PdfReader(args.template)
cover=original.pages[0];over=BytesIO();oc=canvas.Canvas(over,pagesize=(1800,2250))
oc.setFillColor(colors.white);oc.rect(70,82,1655,570,fill=1,stroke=0);oc.setFillColor(colors.HexColor('#1759c6'))
for txt,ypos,size in [('Arkaprava Ghosh',550,56),('Indian Institute of Technology Madras (IITM)',445,44),('DA25C003',340,50),('da25c003@smail.iitm.ac.in',235,48),('+91 8583992597',130,48)]:
 oc.setFont('Arial-Bold',size);oc.drawString(88,ypos,txt)
oc.save();over.seek(0);cover.merge_page(PdfReader(over).pages[0])
scale=W/1800;shift=(H-2250*scale)/2
writer=PdfWriter();cp=writer.add_blank_page(W,H);cp.merge_transformed_page(cover,Transformation().scale(scale).translate(0,shift))
for i in range(2):
 p=writer.add_blank_page(W,H);p.merge_transformed_page(original.pages[i+2],Transformation().scale(W/1800,H/2250));p.merge_page(body_pdf.pages[i])
writer.add_page(body_pdf.pages[2]);writer.add_metadata({'/Title':'UNSCRIPTED - Flipkart APM Prompt 1','/Author':'Arkaprava Ghosh','/Subject':'Personal AI intent firewall - editorial case and references'})
dest=out/'Arkaprava_Ghosh_IIT_Madras.pdf'
with dest.open('wb') as f:writer.write(f)
r=PdfReader(dest);counts=[len(r.pages[i].extract_text().split()) for i in [1,2]]
assert len(r.pages)==4 and sum(counts)<=1200,(len(r.pages),counts)
assert all(abs(float(p.mediabox.width)-W)<1 and abs(float(p.mediabox.height)-H)<1 for p in r.pages)
(root/'tmp/pdf-redesign-layout.json').write_text(json.dumps({'main_page_words':counts,'total_main_words':sum(counts),'body_font_pt':9.25,'body_font_css_px':9.25*96/72,'boxes':boxes},indent=2))
print('Created',dest);print('Main pages, all extracted words:',counts,'total',sum(counts));print('Body: 9.25 pt / 12.33 px. Cover + 2 main pages + 1 appendix.')
