from flask import Flask, render_template, request
from operator import itemgetter
import pandas as pd
import json
import csv
import os
from codeForApp import removePunctuationAndToStringArray

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    tag_names=["contest_mode", "brand_safe", "can_gild", "hide_score", "is_crosspostable", "is_reddit_media_domain", "is_video", "locked", "no_follow", "send_replies", "spoiler", "stickied", "is_robot_indexable", "allow_live_comments", "author_premium"]
    tag_values = ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"]
    for i in range(len(tag_values)):
        try:
            tag_values[i] = request.form[tag_names[i]]
        except:
            tag_values[i] = "0"
        
    search_query = request.form['search']
    sort_category = request.form['sort_category']
    ascending = request.form['ascending']
    try:
        search_author = request.form['search_author']
    except:
        search_author = '0'
    try:    
        search_titles = request.form['search_titles']
    except:
        search_titles='0'
    
    try:
        selected_categories = str(request.form['selected_categories'])
    except:
        selected_categories = []
    try:    
        selectedCategoriesOrder=request.form['selected_categories_order']
    except:    
        selectedCategoriesOrder=[]
        
    boolOrder = []
    for i in range(len(selectedCategoriesOrder)):
        if(selectedCategoriesOrder[i]=="T"):
            boolOrder.append(True)
        elif(selectedCategoriesOrder[i]=="F"):
            boolOrder.append(False)
        else:
            pass
    selected_categories = removePunctuationAndToStringArray(selected_categories)
    
    #for val in selected_categories:
    #    print(val)
    #print(selected_categories)
    #print(boolOrder)
    
    if(ascending=="True"):
        ascending=True
    else:
        ascending=False
    
    results = []
    target = os.path.join(app.static_folder, 'Games.csv')

    with open(target, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        if(search_query != ""):
            for row in reader:
                if(search_author=='0' and search_titles=='0'):
                    if(search_query.lower() in row['title'].lower() or search_query.lower() in row['author'].lower() ):
                        results.append(row)
                elif(search_author=='1'):
                    if(search_query.lower() in row['author'].lower() ):
                        results.append(row)
                elif(search_titles=='1'):
                    if(search_query.lower() in row['title'].lower()):
                        results.append(row)
        else:
            results = []
            for row in reader:
                results.append(row)

    

    for j in range(len(tag_names)):
        if(tag_values[j]=="1"):
            x = len(results)
            for i in range(x):
                if(results[x-i-1].get(tag_names[j]) == "0.0" or results[x-i-1].get(tag_names[j]) == ""):
                    results.pop(x-i-1)
                else:
                    pass


    #if(len(boolOrder)==2):
        #results.sort(reverse=boolOrder[1], key=lambda x: x[selected_categories[1]])
        #results.sort(reverse=boolOrder[0], key=lambda x: x[selected_categories[0]])
        #print(1)
    #else:
    #results.sort(reverse=ascending, key=lambda x: x[sort_category])    
        #print(len(selected_categories))
        #print(0)
    if(len(selected_categories)!=0):
        z=len(selected_categories)
        for i in range(z):
            results.sort(reverse=boolOrder[z-1-i], key=lambda x: x[selected_categories[z-1-i]])
    else:
        results.sort(reverse=True, key=lambda x: x['created_utc'])    

    
 

    return render_template('results.html', results=results, search_query=search_query)

if __name__ == '__main__':
    app.run(debug=True)