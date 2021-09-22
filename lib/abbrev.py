

def abbrev(words):
    abbrev = {}
    for word in words:
        length = len(word)-1
        while length > 0:
            subw = word[0:length]
            length -= 1
            if subw not in abbrev:
                # first word so far to have this abbreviation
                abbrev[subw] = word
            else:
                # second word to have this abbreviation, can't use it
                del abbrev[subw]
                # no need to continue
                length = 0

    # non-abbrevs always get entered, even if they aren't unique
    for word in words:
        abbrev[word] = word
    print(abbrev)

    return abbrev
