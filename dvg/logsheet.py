# -*- coding: utf8 -*-

from datetime import datetime
from fpdf import FPDF 

from dvg.logger import log

WHITE  = 255
GREYL1 = 240
GREYL2 = 230
GREYD  = 100
BLACK  = 0

def generate_pdf(game):
    bg = game.bg
    campaign = game.campaign
    clength  = game.clength

    has_aces = bg.alias in {'CL', 'ZL'}

    margin = 10
    width  = 4  # default cell width
    height = 5  # default row height
    wfull = 297
    hfull = 210
    wreal = wfull - 2 * margin
    hreal = hfull - 2 * margin
    xleft  = margin
    xright = wfull - margin
    ytop    = margin
    ybottom = hfull - margin
    nb_days   = 15
    nb_pilots = 15
    wdays   = nb_days * 3 * width
    
    pdf = FPDF(orientation='L')
    pdf.set_auto_page_break(False)
    pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)


    pdf.add_page()

    # *** first line: boardgame, campaign, date
    pdf.set_xy(margin, margin)
    pdf.set_font('DejaVu', '', 10)
    pdf.set_fill_color(BLACK)
    pdf.set_text_color(WHITE)
    wbg = pdf.get_string_width(bg.name)+5
    pdf.cell(wbg, height, bg.name, 1, 0, 'C', 1, '')

    today = datetime.today().strftime('%Y-%m-%d')
    wtoday = pdf.get_string_width(today)+5

    pdf.set_text_color(BLACK)
    pdf.set_font('DejaVu', '', 10)
    wcampaign = wreal - wbg - wtoday
    pdf.cell(
        wcampaign, height,
        f'{campaign.name} - {campaign.service} - {campaign.year} - {clength.label} ({clength.days} days)',
        1, 0, 'C', 0, '')
    pdf.cell(wtoday, height, today, 1, 1, 'C', 0, '')
    pdf.ln()

    # FIXME AIM limit IAFL
    # FIXME checkboxes pilot selected

    # outcome
#    cury = pdf.get_y()

    # *** days
    wdtitle = 15
    xdays = wfull - margin - wdays - wdtitle

    tracks = ['Recon', 'Intel']
    if bg.alias == 'HLCAO':
        tracks.append('Infra')
    elif bg.alias == 'IAFL':
        tracks.extend(['Infra', 'Invasion'])
    elif bg.alias == 'PL':
        tracks.append('Politics')
    rows = [
        'Day', ['Primary', 'Secondary', 'End of day'],
        'Mission #', 'Target #', 'Target status', 'Victory Points',
        'Total VP', '', *tracks, '',
        'Starting SO', 'Ordnance', 'SO lost', 'SO gained', '',
        'XP', 'Stress'

    ] 

    cury = hfull - margin - (nb_pilots+1) * height - height - len(rows)*height

    for row in rows:
        if row == '':
            pdf.ln()

        else:
            pdf.set_xy(xdays, cury)
            pdf.set_text_color(WHITE)
            pdf.set_fill_color(GREYD)
            if isinstance(row, list):
                pdf.cell(wdtitle, height, '', 1, 0, 'R', 1)
                l = len(row)
                h = height / l
                for i in range(0, l):
                    y = cury + i*h
                    pdf.set_xy(xdays, y)
                    pdf.set_font('DejaVu', '', 4)
                    pdf.cell(wdtitle, h, row[i], 0, 0, 'R')
                # reset pos & font
                curx = pdf.get_x()
                pdf.set_xy(curx, cury)
                pdf.set_font('DejaVu', '', 6)
            else:
                pdf.set_font('DejaVu', '', 6)
                pdf.cell(wdtitle, height, row, 1, 0, 'R', 1)

            pdf.set_text_color(BLACK)
            pdf.set_fill_color(GREYL2)
            for i in range(1, nb_days+1):
                if row == 'Day':
                    pdf.cell(3*width, height, str(i), 1, 0, 'C')

                elif row == 'Mission #':
                    txt = '1' if i == 1 else ''
                    pdf.cell(width, height, txt, 1, 0, 'C')
                    pdf.cell(width, height, '', 1)
                    pdf.cell(width, height, 'x', 1, 0, 'C', 1)

                elif isinstance(row, list):
                    pdf.cell(width, height, 'P', 1, 0, 'C')
                    pdf.cell(width, height, 'S', 1, 0, 'C')
                    pdf.set_fill_color(GREYL2)
                    pdf.cell(width, height, 'D', 1, 0, 'C', 1)

                elif row == 'Stress':
                    pdf.cell(width, height, '', 1, 0, 'C')
                    pdf.cell(width, height, '', 1)
                    pdf.cell(width, height, '', 1, 0, 'C', 1)

                else:
                    pdf.cell(width, height, '', 1, 0, 'C')
                    pdf.cell(width, height, '', 1)
                    pdf.cell(width, height, 'x', 1, 0, 'C', 1)

        # go to next line
        cury += height



    # *** pilots
    cury = hfull - margin - (nb_pilots * height)
    widthes = [  4,      28,        9,         15,      6,    4,          17]
    labels  = ['#', 'Pilot', 'Skills', 'Aircraft', 'Rank', 'XP', 'XP gained']
    if has_aces:
        widthes.append(10)
        labels.append('Aces \u2606')
    else:
        widthes[6] += 10
    widthes.extend([4])
    labels.extend(['\u2744']) # cool

    # - pilot title line
    pdf.set_fill_color(GREYD)
    pdf.set_text_color(WHITE)
    pdf.set_font('DejaVu', '', 6)
    pdf.set_xy(margin, cury-height)
    for curw, row  in zip(widthes, labels):
        pdf.cell(curw, height, row, 1, 0, 'C', 1)
    pdf.cell(wdays, height, 'Pilot stress record', 1, 0, 'C', 1)
    pdf.set_fill_color(WHITE)
    pdf.set_text_color(BLACK)

    # - pilot lines
    for i in range(1, nb_pilots+1):
        cury2 = cury + height/2
        curyb = cury + height

        curlabels = [str(i)]
        
        if i <= len(game.pilots):
            has_pilot = True
            p = game.pilots[i-1]
            so_bonus = p.so_bonus(game)
            line2 = f'{p.aircraft.role} [{so_bonus:+d}SO]' if so_bonus else p.aircraft.role
            curlabels.extend([p.elite_name, '', [p.aircraft.name, line2]])
        else:
            has_pilot = False
            curlabels.extend(['', '', ''])

        boxes = '\u25a1' * 5
#        curlabels.extend(['', '', [' '.join([boxes]*2)]*2])
        curlabels.extend(['', ''])
        curlabels.append('')

        if has_aces:
            stars = '\u2606' * 5
            curlabels.append([stars]*2)
        curlabels.append('') # cool

        # line background
        pdf.set_fill_color(WHITE if i%2 == 0 else GREYL1)
        pdf.rect(margin, cury, wreal, height, 'FD')

        pdf.set_xy(margin, cury)
        for curw, t, row in zip(widthes, labels, curlabels):
            curx  = pdf.get_x()
            align = '' if t == 'Pilot' else 'C'

            if isinstance(row, list):
                l = len(row)
                h = height / l
                for i in range(0, l):
                    y = cury + i*h
                    pdf.set_xy(curx, y)
                    pdf.set_font('DejaVu', '', 6 if t=='Aces \u2606' else 4)
                    pdf.cell(curw, h, row[i], 0, 0, align)

            elif t == 'XP gained':
                wi = 2
                mi = 1
                mi2 = mi/2
                hi = (height/2)-mi2
                pdf.set_x(curx+mi)
                pdf.set_line_width(0.1)
                xi = curx + mi
                i = 0
                while xi + wi < curx + curw:
                    i += 1
                    pdf.set_xy(xi, cury+mi2)
                    pdf.cell(wi, hi, '', 1)
                    pdf.set_xy(xi, cury2)
                    pdf.cell(wi, hi, '', 1)
                    xi = pdf.get_x()
                    if i % 5 == 0:
                        pdf.set_xy(xi, cury+mi2)
                        pdf.cell(mi2, hi, '')
                        pdf.set_xy(xi, cury2)
                        pdf.cell(mi2, hi, '')
                        xi = pdf.get_x()

#                for i in range(1, int(curw/wi)+1):
#                    xi = pdf.get_x()
#                    pdf.set_xy(xi, cury+mi2)
#                    pdf.cell(wi, hi, '', 1)
#                    pdf.set_xy(xi, cury2)
#                    pdf.cell(wi, hi, '', 1)
                pdf.set_xy(curx+curw, cury)
                pdf.set_line_width(0.2)

            elif t == 'Rank':
                w = curw / 3
                h = height / 2
                pdf.set_font('DejaVu', '', 4)
                pdf.set_xy(curx, cury)
                pdf.cell(w, h, 'N', 1, 0, 'C')
                pdf.cell(w, h, 'G', 1, 0, 'C')
                pdf.cell(w, h, 'A', 1, 0, 'C')
                pdf.set_xy(curx, cury2)
                pdf.cell(w, h, 'S', 1, 0, 'C')
                pdf.cell(w, h, 'V', 1, 0, 'C')
                pdf.cell(w, h, 'L', 1, 0, 'C')

                if has_pilot:
                    rank = p.rank
                    curx1 = curx + w
                    curx2 = curx + w*2
                    curx3 = curx + w*3
                    greater = {'green', 'average', 'skilled', 'veteran', 'legendary', 'ace'}
                    if rank in greater:
                        pdf.line(curx,cury2,curx1,cury)
                        pdf.line(curx1,cury2,curx,cury)
                    greater -= {'green'}
                    if rank in greater:
                        pdf.line(curx1,cury2,curx2,cury)
                        pdf.line(curx2,cury2,curx1,cury)
                    greater -= {'average'}
                    if rank in greater:
                        pdf.line(curx2,cury2,curx3,cury)
                        pdf.line(curx3,cury2,curx2,cury)
                    greater -= {'skilled'}
                    if rank in greater:
                        pdf.line(curx,curyb,curx1,cury2)
                        pdf.line(curx1,curyb,curx,cury2)
                    greater -= {'veteran'}
                    if rank in greater:
                        pdf.line(curx1,curyb,curx2,cury2)
                        pdf.line(curx2,curyb,curx1,cury2)
                    greater -= {'legendary'}
                    if rank in greater:
                        pdf.line(curx2,curyb,curx3,cury2)
                        pdf.line(curx3,curyb,curx2,cury2)


            else:
                pdf.set_font('DejaVu', '', 6)
                pdf.cell(curw, height, row, 0, 0, align)

            # add the pilot service
            if t == 'Pilot' and has_pilot:
                pdf.set_font('DejaVu', '', 3)
                pdf.set_xy(curx, cury + 2*height/3)
                pdf.cell(curw, height/3, p.service, 0, 0, 'R')

            curx = pdf.get_x()
            pdf.line(curx, cury, curx, curyb)

        # missions
        curx = pdf.get_x()
        pdf.set_xy(curx, cury)
        pdf.set_line_width(0.4)
        pdf.line(curx, cury, curx, curyb)
        pdf.set_line_width(0.2)
        for i in range(1, nb_days+1):
            pdf.cell(width, height, '', 1)
            pdf.cell(width, height, '', 1)
            pdf.set_fill_color(GREYL2)
            pdf.cell(width, height, '', 1, 0, 'C', 1)

        cury += height



    pdf.output('logsheet.pdf', 'F')

