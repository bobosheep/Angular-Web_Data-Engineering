def mark(rec, terms):
    text = rec
    #print(terms)
    for i in range(len(terms)):
        mark = ''
        find_idx = text.find(terms[i])
        before = ''
        after = text
        while find_idx >= 0:
            before = after[:find_idx]
            after = after[find_idx+len(terms[i]):]
            mark += before + '<mark>' + terms[i] + '</mark>'
            find_idx = after.find(terms[i])
    
        text = mark + after
    
    mark1B = text.find("<mark>")
    if mark1B >= 100:
        text = '...' + text[mark1B - 35:]
    mark1E = text.find("</mark>")
    mark2B = -1
    mark2E = -1

    while mark1B >= 0 and mark1E >= 0:
        leng = len(text)
        mark2B = text.find("<mark>", mark1B + 5)
        mark2E = text.find("</mark>", mark1E + 5)
        if mark2B >= 0 and mark2E >= 0:
            if mark2B - mark1E >= 40:
                text = text[:mark1E + 15] + '...' + text[mark2B + 10:]
        elif leng - mark1E >= 50:
            #print('berfore:'+text)
            text = text[:mark1E + 35] + '...'
            #print('after:'+text)

        mark1B = mark2B
        mark1E = mark2E 

    return text

def getCmd(inputTerm):
    cmd = ["C:/Users/user/Documents/course/108-1/DataEngineering/DE_Project_3/rgrep.exe",
                                      "-rb", "@Gais"]
    terms = []
    fieldQ = ''
    parse = inputTerm.split(" ")
    if len(parse) > 1 :
        for term in parse:
            idx = term.find(":")
            if idx > 0 and term[:idx] == "field":
                fieldQ = term[idx + 1:]
            else:
                terms.append(term)

        if fieldQ != '':
            cmd.append("-fq")
            cmd.append(fieldQ)
        if len(terms) > 1:
            cmd.append("-mt")
            cmd.append(str(len(terms)))
            for term in terms:
                cmd.append(term)
        else:
            cmd.append(terms[0])

    else:
        terms.append(parse[0])
        cmd.append(parse[0])
    cmd.append("../../DE_Project_2/pettoday.rec")
    return cmd, terms, fieldQ

def getCompEle(item):
    return item["count"]