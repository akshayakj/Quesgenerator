from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.views.generic import View

import spacy


def index(request):
     return render(request,'quest/index.html')

def get(request):
     # global ques
     # ques = ""
     if (request.POST):
          add_data = request.POST.copy()
          line = add_data.get("text")
          nlp1 = spacy.load('en_core_web_sm')
          # doc = nlp1(text)
          # list99 = list(doc.sents)

          if "because" in line:
               l = line.split('because')
               line1 = nlp1(str(l[0]))
               h = ""
               for token in line1:
                    print(token.text, token.dep_)
                    if "aux" in str(token.dep_):
                         h = h + token.text
                         break
               if h != "":
                    m = str(line1).split(h)
                    ques = 'Why' + ' ' + h + ' ' + m[0].lower() + m[1] + '?'
               else:
                    ques = 'Why' + ' ' + str(line1) + '?'
               # print(ques)

     return render(request,'quest/question.html',{'ques':ques})


