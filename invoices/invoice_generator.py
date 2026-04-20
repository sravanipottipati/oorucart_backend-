from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# Register Helvetica replacement with rupee support
_FONT_REGISTERED = False
def _register_font():
    global _FONT_REGISTERED
    if _FONT_REGISTERED:
        return
    # Use NotoSans if available, else fallback to Rs.
    font_paths = [
        '/System/Library/Fonts/Supplemental/Arial Unicode.ttf',
        '/Library/Fonts/Arial Unicode.ttf',
        '/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf',
    ]
    for fp in font_paths:
        if os.path.exists(fp):
            try:
                pdfmetrics.registerFont(TTFont('UniFont', fp))
                _FONT_REGISTERED = True
                return
            except:
                pass
_register_font()
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from io import BytesIO
from datetime import datetime
from decimal import Decimal

UNIVERIN = {
    'name':    'Univerin Private Limited',
    'address': '4/11, Sankarapuram, Govindampalli, Obulavaripalle - 516105, Andhra Pradesh',
    'gstin':   '37AADCU8846J1ZP',
    'pan':     'AADCU8846J',
    'tan':     'HYDV12345A',
    'email':   'contact@univerin.in',
    'phone':   '9000869619',
}

BLUE  = colors.HexColor('#2563eb')
DARK  = colors.HexColor('#111827')
GRAY  = colors.HexColor('#6b7280')
LIGHT = colors.HexColor('#f3f4f6')
WHITE = colors.white

def _p(text, font='Helvetica', size=8, color=None, align='LEFT', bold=False):
    fn = 'Helvetica-Bold' if bold else font
    al = {'LEFT':0,'CENTER':1,'RIGHT':2}.get(align,0)
    c  = color or DARK
    return Paragraph(text, ParagraphStyle('s', fontName=fn, fontSize=size, textColor=c, alignment=al, leading=size+3))

def inv_num(order, prefix='INV'):
    y = datetime.now().year
    return f'{prefix}/{y}-{str(y+1)[-2:]}/{str(order.id)[:6].upper()}'

def header_table(order, title, extra=''):
    inv = inv_num(order, title)
    dt  = order.created_at.strftime('%d %b %Y')
    left  = _p('<b><font color="#2563eb" size="22">Univerin</font></b>', size=22)
    right = _p(f'<b>TAX INVOICE</b><br/><font size="8" color="#6b7280">No: {inv}</font><br/><font size="8" color="#6b7280">Date: {dt}</font><br/><font size="8" color="#6b7280">Order: {str(order.id)[:12].upper()}</font>{extra}', size=10, align='RIGHT')
    t = Table([[left, right]], colWidths=[90*mm, 90*mm])
    t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LINEBELOW',(0,0),(-1,0),0.5,colors.HexColor('#e5e7eb'))]))
    return t

def generate_buyer_invoice(order):
    buf = BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=15*mm, rightMargin=15*mm, topMargin=12*mm, bottomMargin=12*mm)
    s = []
    s.append(header_table(order, 'INV'))
    s.append(Spacer(1,3*mm))
    s.append(_p('Hyperlocal Marketplace', color=GRAY, align='CENTER'))
    s.append(Spacer(1,4*mm))
    buyer  = order.buyer
    vendor = order.vendor
    bn = buyer.full_name or buyer.phone_number
    sg = getattr(vendor,'gstin','N/A') or 'N/A'
    pd = [
        [_p('<b>Billed by (Platform)</b>',bold=True), _p('<b>Billed to (Buyer)</b>',bold=True), _p('<b>Sold by (Seller)</b>',bold=True)],
        [_p(UNIVERIN['name']+'\n'+UNIVERIN['address']+'\nGSTIN: '+UNIVERIN['gstin']+'\n'+UNIVERIN['email']),
         _p(f'{bn}\n{order.delivery_address or "N/A"}\nPh: {buyer.phone_number}'),
         _p(f'{vendor.shop_name}\nGSTIN: {sg}')]
    ]
    pt = Table(pd, colWidths=[60*mm,60*mm,60*mm])
    pt.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),LIGHT),('BOX',(0,0),(-1,-1),0.5,colors.HexColor('#e5e7eb')),('INNERGRID',(0,0),(-1,-1),0.5,colors.HexColor('#e5e7eb')),('VALIGN',(0,0),(-1,-1),'TOP'),('PADDING',(0,0),(-1,-1),5)]))
    s.append(pt)
    s.append(Spacer(1,4*mm))
    ih = [_p('<b>Item</b>',bold=True),_p('<b>HSN</b>',bold=True,align='CENTER'),_p('<b>Qty</b>',bold=True,align='CENTER'),_p('<b>Rate</b>',bold=True,align='RIGHT'),_p('<b>CGST</b>',bold=True,align='CENTER'),_p('<b>SGST</b>',bold=True,align='CENTER'),_p('<b>Amount</b>',bold=True,align='RIGHT')]
    rows = [ih]
    sub  = Decimal('0')
    for item in order.items.all():
        gr  = float(item.product.gst_percentage or 0)/2
        pr  = Decimal(str(item.price))
        lt  = pr * item.quantity
        ca  = lt * Decimal(str(gr)) / 100
        sub += lt
        rows.append([_p(item.product.name),_p(getattr(item.product,'hsn_code','') or '',align='CENTER'),_p(str(item.quantity),align='CENTER'),_p(f'Rs.{pr:.2f}',align='RIGHT'),_p(f'{gr:.1f}% Rs.{ca:.2f}',align='CENTER'),_p(f'{gr:.1f}% Rs.{ca:.2f}',align='CENTER'),_p(f'Rs.{lt+ca+ca:.2f}',align='RIGHT')])
    it = Table(rows, colWidths=[55*mm,15*mm,12*mm,20*mm,25*mm,25*mm,20*mm])
    it.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),LIGHT),('BOX',(0,0),(-1,-1),0.5,colors.HexColor('#e5e7eb')),('INNERGRID',(0,0),(-1,-1),0.5,colors.HexColor('#e5e7eb')),('PADDING',(0,0),(-1,-1),4)]))
    s.append(it)
    s.append(Spacer(1,3*mm))
    df = Decimal(str(order.delivery_fee or 35))
    pf = Decimal(str(order.platform_fee or 10))
    cd = df*Decimal('0.09'); sd = cd
    cp = pf*Decimal('0.09'); sp = cp
    gt = Decimal(str(order.total_amount))
    td = [
        [_p('Product subtotal (excl. GST)'), _p(f'Rs.{sub:.2f}',align='RIGHT')],
        [_p('Delivery charge'), _p(f'Rs.{df:.2f}',align='RIGHT')],
        [_p('CGST 9% on delivery'), _p(f'Rs.{cd:.2f}',align='RIGHT')],
        [_p('SGST 9% on delivery'), _p(f'Rs.{sd:.2f}',align='RIGHT')],
        [_p('Platform fee'), _p(f'Rs.{pf:.2f}',align='RIGHT')],
        [_p('CGST 9% on platform fee'), _p(f'Rs.{cp:.2f}',align='RIGHT')],
        [_p('SGST 9% on platform fee'), _p(f'Rs.{sp:.2f}',align='RIGHT')],
        [_p('<b>GRAND TOTAL</b>',bold=True,size=10,color=BLUE), _p(f'<b>Rs.{gt:.2f}</b>',bold=True,size=10,color=BLUE,align='RIGHT')],
    ]
    tt = Table(td, colWidths=[130*mm,40*mm], hAlign='RIGHT')
    tt.setStyle(TableStyle([('BOX',(0,0),(-1,-1),0.5,colors.HexColor('#e5e7eb')),('LINEABOVE',(0,-1),(-1,-1),1,BLUE),('BACKGROUND',(0,-1),(-1,-1),colors.HexColor('#eff6ff')),('PADDING',(0,0),(-1,-1),4)]))
    s.append(tt)
    s.append(Spacer(1,3*mm))
    pm = order.payment_mode.upper() if order.payment_mode else 'COD'
    s.append(_p(f'Payment method: {pm} Paid'))
    s.append(Spacer(1,4*mm))
    s.append(HRFlowable(width='100%',thickness=0.5,color=colors.HexColor('#e5e7eb')))
    for n in ['This is a computer-generated invoice and does not require a physical signature.','GST amounts are split equally as CGST & SGST (intra-state supply, Andhra Pradesh).','TCS @ 1% is collected by Univerin Private Limited as per Section 52 of CGST Act, 2017.',f'For support: {UNIVERIN["email"]} | Ph: {UNIVERIN["phone"]}']:
        s.append(_p('• '+n, color=GRAY, size=7))
    s.append(Spacer(1,3*mm))
    s.append(HRFlowable(width='100%',thickness=0.5,color=colors.HexColor('#e5e7eb')))
    s.append(_p(f'{UNIVERIN["name"]} | GSTIN: {UNIVERIN["gstin"]} | {UNIVERIN["email"]} | {UNIVERIN["phone"]}', color=GRAY, align='CENTER', size=7))
    s.append(_p('Thank you for shopping with Univerin!', bold=True, color=BLUE, align='CENTER'))
    doc.build(s)
    buf.seek(0)
    return buf

def generate_commission_invoice(order):
    buf = BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=15*mm, rightMargin=15*mm, topMargin=12*mm, bottomMargin=12*mm)
    s = []
    s.append(header_table(order, 'COMMISSION'))
    s.append(Spacer(1,3*mm))
    s.append(_p('Hyperlocal Marketplace', color=GRAY, align='CENTER'))
    s.append(Spacer(1,4*mm))
    vendor = order.vendor
    sg = getattr(vendor,'gstin','N/A') or 'N/A'
    sub  = Decimal(str(order.subtotal or order.total_amount))
    cr   = Decimal(str(order.commission_rate or 6))
    ca   = sub * cr / 100
    cgst = ca * Decimal('0.09')
    sgst = cgst
    total = ca + cgst + sgst
    pd = [
        [_p('<b>From (Univerin)</b>',bold=True), _p('<b>To (Seller)</b>',bold=True)],
        [_p(UNIVERIN['name']+'\n'+UNIVERIN['address']+'\nGSTIN: '+UNIVERIN['gstin']),
         _p(f'{vendor.shop_name}\nGSTIN: {sg}\nCategory: {vendor.category or "N/A"}')]
    ]
    pt = Table(pd, colWidths=[90*mm,90*mm])
    pt.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),LIGHT),('BOX',(0,0),(-1,-1),0.5,colors.HexColor('#e5e7eb')),('INNERGRID',(0,0),(-1,-1),0.5,colors.HexColor('#e5e7eb')),('VALIGN',(0,0),(-1,-1),'TOP'),('PADDING',(0,0),(-1,-1),5)]))
    s.append(pt)
    s.append(Spacer(1,4*mm))
    ct = Table([
        [_p('<b>Description</b>',bold=True),_p('<b>Order value</b>',bold=True,align='RIGHT'),_p('<b>Rate</b>',bold=True,align='CENTER'),_p('<b>SAC</b>',bold=True,align='CENTER'),_p('<b>Commission</b>',bold=True,align='RIGHT')],
        [_p(f'Commission on {vendor.category or "Groceries"} sales'),_p(f'Rs.{sub:.2f}',align='RIGHT'),_p(f'{cr:.1f}%',align='CENTER'),_p('998599',align='CENTER'),_p(f'Rs.{ca:.2f}',align='RIGHT')]
    ], colWidths=[55*mm,35*mm,25*mm,20*mm,35*mm])
    ct.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),LIGHT),('BOX',(0,0),(-1,-1),0.5,colors.HexColor('#e5e7eb')),('INNERGRID',(0,0),(-1,-1),0.5,colors.HexColor('#e5e7eb')),('PADDING',(0,0),(-1,-1),4)]))
    s.append(ct)
    s.append(Spacer(1,3*mm))
    td = [
        [_p('Commission (excl. GST)'), _p(f'Rs.{ca:.2f}',align='RIGHT')],
        [_p('CGST @ 9% on commission'), _p(f'Rs.{cgst:.2f}',align='RIGHT')],
        [_p('SGST @ 9% on commission'), _p(f'Rs.{sgst:.2f}',align='RIGHT')],
        [_p('<b>Total commission payable</b>',bold=True,size=10,color=BLUE), _p(f'<b>Rs.{total:.2f}</b>',bold=True,size=10,color=BLUE,align='RIGHT')],
    ]
    tt = Table(td, colWidths=[130*mm,40*mm], hAlign='RIGHT')
    tt.setStyle(TableStyle([('BOX',(0,0),(-1,-1),0.5,colors.HexColor('#e5e7eb')),('LINEABOVE',(0,-1),(-1,-1),1,BLUE),('BACKGROUND',(0,-1),(-1,-1),colors.HexColor('#eff6ff')),('PADDING',(0,0),(-1,-1),4)]))
    s.append(tt)
    s.append(Spacer(1,4*mm))
    s.append(HRFlowable(width='100%',thickness=0.5,color=colors.HexColor('#e5e7eb')))
    for n in ['This commission is charged by Univerin Private Limited for marketplace services rendered per order.','GST of 18% (CGST 9% + SGST 9%) is applicable on commission as per SAC 998599.','Commission will be deducted from your order settlement.',f'For disputes: {UNIVERIN["email"]} | Ph: {UNIVERIN["phone"]}']:
        s.append(_p('• '+n, color=GRAY, size=7))
    s.append(Spacer(1,3*mm))
    s.append(HRFlowable(width='100%',thickness=0.5,color=colors.HexColor('#e5e7eb')))
    s.append(_p(f'{UNIVERIN["name"]} | GSTIN: {UNIVERIN["gstin"]} | {UNIVERIN["email"]} | {UNIVERIN["phone"]}', color=GRAY, align='CENTER', size=7))
    s.append(_p('Powering your local business.', bold=True, color=BLUE, align='CENTER'))
    doc.build(s)
    buf.seek(0)
    return buf
