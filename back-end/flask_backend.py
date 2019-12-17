# encoding: utf-8
import re
import json
import pickle
import time
import subprocess

from flask import Flask, jsonify, request, url_for
from flask import render_template
from util import getCmd, mark, getCompEle
app = Flask(__name__)
sentences = {}


@app.route('/')
def home():
    return render_template('index.html')

search_term = ''
result_list = []

@app.route('/search', methods = ['GET'])
def search():
    display_items = 15
    term = request.args.get('term')
    result_page = request.args.get('page', 1)
    result_page = int(result_page)

    global search_term
    global result_list

    if search_term == term :
        return_json = {"page": result_page, "sentences":result_list[(result_page - 1) * display_items : result_page * display_items], "search_time": 0.1, "total_results":len(result_list)}
        return jsonify(return_json)

    else :
        search_term = term
        result_list = []


    if term == None:
        return jsonify({"page":0, "senetences":[], "search_time":0, "total_result": 0})

    print(term)
    count = 0


    start = time.clock()
    cmd, terms, fieldQ = getCmd(term)
    result = subprocess.check_output(cmd, encoding='utf-8', errors="ignore")
    end = time.clock()
    search_time = end - start

    print(type(result))
    # esult = result.decode(encoding='utf-8')
    print(len(result))
    rec_detail = ''
    match_count = 0
    if(len(result) < 10):
        return jsonify({"page":0, "senetences":[], "search_time":0, "total_result": 0})

    for i in result.split('[ REC ABOVE ] Total match:'):
        if i.startswith('@Gais'):
            rec_detail = i
        else :
            s = i.split('@Gais')
            match_count = int(s[0])
            rec_fields = []
            field = ''
            rec_name = ''
            rec_body = ''
            rec_url = ''
            rec_img_link = ''
            for rec in re.split(r'(@\w+:)', rec_detail):
                if rec.startswith('@'):
                    field = rec
                elif field != '':
                    rec_fields.append({
                        "field": field[1:],
                        "detail": rec
                    })
                    if field.find("title") > 0:
                        if fieldQ == 'title' or fieldQ == '':
                            rec_name = mark(rec, terms)
                        else:
                            rec_name = rec

                    elif field.find("body") > 0:
                        if fieldQ == 'body' or fieldQ == '':
                            rec_body = mark(rec, terms)
                        else:
                            rec_body = rec if len(rec) < 150 else rec[:150]

                    elif field.find("url") > 0:
                        rec_url = rec

                    elif field.find("image_links") > 0:
                        rec_img_link = rec

            result_list.append({"name":rec_name, "count":match_count, "fields": rec_fields,
                                "body": rec_body, "url": rec_url, "img_link": rec_img_link})
            if(len(s) > 1):
                rec_detail = '@Gais' + s[1]
    """
    for s in sentences:
        find_idx = s[0].find(term)
        if find_idx >= 0:
            before = s[0][:find_idx]
            after = s[0][find_idx+len(term):]
            find_term = s[0][find_idx: find_idx+len(term)]
            sen = before + '<mark>' + find_term + '</mark>' + after
            result_list.append({"name":sen, "count":s[1]})
    """

    result_list.sort(key=getCompEle, reverse=True)
    return_json = {"page": result_page, "sentences":result_list[(result_page - 1) * display_items : result_page * display_items], "search_time": search_time, "total_results":len(result_list)}
    print(return_json["total_results"])

    return jsonify(return_json)

if __name__ == '__main__':
    #with open('../../news_data/sentences.bdata', 'rb') as fp:
        #sentences = pickle.load(fp)

    app.run(debug=True)

