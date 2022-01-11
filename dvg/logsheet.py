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


    # *** options
    options = [
        ['Campaign SO points', clength.so, None],
        ['Random squadron',     6*clength.level, None],
        ['Aircraft costs',   sum([p.so_bonus(game) for p in game.pilots]), None],
        ['Pilot promotion',  None, None],
        ['Pilot skills',     None, None],
        ['Aces',             None, None],
        ['±1 pilot',           -3*clength.level, 'cb'],
        ['High stress attack', -3*clength.level, 'cb'],
        ['Damaging target',    -3*clength.level, 'cb'],
    ]
    if bg.alias == 'HLCAO':
        options.append(['Night missions',      0, 'cb'])
        options.append(['Large deck marines', -3*clength.level, 'cb'])
    elif bg.alias == 'ZL':
        options.append(['Pulling rank', -2*clength.level, 'cb'])
    elif bg.alias == 'IAFL':
        options.append(['Succesful AtA Cannon', -1*clength.level, 'cb'])
    elif bg.alias == 'PL':
        options.append(['Early AIM-9 Sidewinders', 3*clength.level, 'cb'])

    options.append(['Total', None, None])

    xoption = pdf.get_x()
    yoption = pdf.get_y()
    pdf.set_text_color(WHITE)
    pdf.set_fill_color(GREYD)
    woption_txt = 30
    woption_so  = 10
    woptions = woption_txt + woption_so
    pdf.set_font('DejaVu', '', 10)
    pdf.cell(woptions, height, 'Options', 1, 1, 'C', 1)
    pdf.set_text_color(BLACK)
    pdf.set_fill_color(WHITE)
    for option, so, cb in options:
        txtso = '' if so is None else f'{so:+d}'
        pdf.set_font('DejaVu', '', 6)
        if option == 'Total':
            pdf.set_fill_color(GREYL2)
            pdf.cell(woption_txt, height, option, 1, 0, '', 1)
            pdf.cell(woption_so, height, txtso, 1, 1, 'C', 1)
            pdf.set_fill_color(WHITE)
        else:
            pdf.cell(woption_txt, height, option, 1, 0)
            if cb == 'cb':
                x = pdf.get_x()
                y = pdf.get_y()
                pdf.cell(woption_so, height, '\u25a1', 0, 0, 'L')
                pdf.set_xy(x,y)
                pdf.cell(woption_so, height, txtso, 0, 0, 'R')
                pdf.set_xy(x,y)
                pdf.cell(woption_so, height, '', 1, 1, 'C')

            else:
                pdf.cell(woption_so, height, txtso, 1, 1, 'C')
    youtcome = pdf.get_y() + height / 2


    # difficulty
    odifficult = [
        'More difficult',
        'Extra Stress', 'Improved sites/bandits', 'Extra sites/bandits',
        'Reduced SO',
        'Less difficult',
        'Less Stress', 'Downgraded sites/bandits', 'Fewer sites/bandits',
        'Increased SO']


    pad = 5 / 2
    xdifficulty = xoption+woptions+pad
    ydifficulty = yoption
    pdf.set_xy(xdifficulty, yoption)
    pdf.set_text_color(WHITE)
    pdf.set_fill_color(GREYD)
    woption_txt = 30
    woption_cb  = 5
    wdifficulty = woption_txt + woption_cb
    pdf.set_font('DejaVu', '', 10)
    pdf.cell(wdifficulty, height, 'Difficulty', 1, 1, 'C', 1)
    pdf.set_text_color(BLACK)
    pdf.set_fill_color(WHITE)
    pdf.set_font('DejaVu', '', 6)
    for option in odifficult:
        ydifficulty += height
        pdf.set_xy(xdifficulty, ydifficulty)

        if option.find('difficult') != -1:
            pdf.set_fill_color(GREYL2)
            pdf.cell(wdifficulty, height, option, 1, 1, '', 1)

        else:
#            pdf.set_fill_color(GREYL2)
            pdf.cell(woption_txt, height, option, 1, 0)
            pdf.cell(woption_cb, height, '\u25a1', 1, 1, 'C')

    # Outcome
    xoutcome = xoption
    woutcome = woptions + pad + wdifficulty
    pdf.set_xy(xoutcome, youtcome)
    pdf.set_text_color(WHITE)
    pdf.set_fill_color(GREYD)
    pdf.set_font('DejaVu', '', 10)
    pdf.cell(woutcome, height, 'Outcome & Notes', 1, 1, 'C', 1)
    pdf.set_text_color(BLACK)
    pdf.set_fill_color(WHITE)
    houtcome = (
        (hfull - margin - (nb_pilots+1) * height - height/2)
        - youtcome - height
    )
    pdf.cell(woutcome, houtcome, '', 1)
    pdf.set_xy(xoutcome, youtcome + height)
    pdf.set_font('DejaVu', '', 8)
    outcomes = ('Great', 'Good', 'Adequate', 'Poor', 'Dismal')
    txtlen = woutcome / len(outcomes)
    for outcome in outcomes:
        txt = f'\u25a1 {outcome}'
        pdf.cell(txtlen, height, txt, 0, 0, 'C')

    if bg.alias == 'IAFL':
        pdf.set_font('DejaVu', '', 6)
        pdf.set_xy(xoutcome, youtcome + height*2)
        pdf.cell(woutcome, height, 'AIM limit:', 0, 1)
        pdf.cell(woutcome, height, 'Pilot loss penalty:', 0, 1)


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
        'Day', ['Primary', 'Secondary', 'End of day'], 'Mission #', 'Day/Night',
        'Target #', 'Target status', 'Victory Points', 'Total VP', '', *tracks, '',
        'Starting SO', 'Ordnance', 'SO lost', 'SO gained', '',
        'WP modifier', 'XP', 'Stress'

    ] 

    cury = (
        hfull - margin - (nb_pilots+1) * height - height -
        len(rows)*height + (len([r for r in rows if r ==''])+1)*height/2
    )

    for row in rows:
        if row == '':
            pdf.ln()
            # go to next line
            cury += height/2

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

