from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.views.generic import View

import spacy


def index(request):
     return render(request,'quest/index.html')

def home(request):
     return render(request,'quest/home.html')

def fli(request):
     return render(request,'quest/fli.html')

def get(request):
     # global ques

     if (request.method=='POST' and 'wh' in request.POST):
          add_data = request.POST.copy()
          line = add_data.get("text")
          nlp1 = spacy.load('en_core_web_sm')
          nlp = spacy.load('en_coref_sm')
          doc = nlp(line)
          list1 = list(doc.sents)
          c = -1
          k = 1
          ans = ""
          for x in list1:
               line = str(x)
               # print(line)
               line09 = nlp1(line)
               cnt = 0
               cnta = 0
               cntb = 0
               cntc = 0
               cntd = 0
               c = c + 1
               if ":" in line:
                    l = line.split(':')
                    m = nlp(l[0])
                    for token in m:
                         if (token.tag_ == "VBP"):
                              b = str(token.text)
                              n = str(m).split(b)
                              ques = str(k) + ") " + "What " + b + " " + n[0].lower() + n[1] + '?'
                              q = nlp(ques)
                              for t in q:
                                   if str(t.tag_) == "NN":
                                        b = 1
                                        break
                              if b == 1:
                                   # print(str(k)+") "+ques)
                                   ans = ans + str(k) + ") " + ques + '\n'
                                   k = k + 1
                                   break
               elif "when" in line:
                    l = line.split('when')
                    line1 = nlp1(str(l[0]))
                    print(str(l[0]))
                    h = ""
                    for token in line1:
                         # print(token.text,token.dep_)
                         if "aux" in str(token.dep_):
                              h = h + token.text
                              break
                    if h != "":
                         m = str(line1).split(h)
                         ques = 'When' + ' ' + h + ' ' + m[0].lower() + m[1] + '?'
                    else:
                         ques = 'When' + ' ' + str(line1) + '?'
                    # print(str(k)+") "+ques)
                    ans = ans + str(k) + ") " + ques + '\n'
                    k = k + 1
               elif "because" in line.lower():
                    l = line.lower().split('because')
                    line1 = nlp1(str(l[0]))
                    h = ""
                    if str(l[0]) == " ":
                         l1 = line.split(',')
                         m = nlp1(str(l1[1]))
                         for token in m:
                              if str(token.tag_) == "DT":
                                   n = str(m).split(str(token.text))
                                   n[1] = n[1].replace(n[1][-1], '?')
                                   ques = "Which" + "" + n[1].lower()
                                   # print(str(k)+") "+ques)
                                   ans = ans + str(k) + ") " + ques + '\n'
                                   k = k + 1
                    else:
                         for token in line1:
                              # print(token.text,token.dep_,token.tag_)
                              if "aux" in str(token.dep_):
                                   h = h + token.text
                                   break
                              if h != "":
                                   m = str(line1).split(h)
                                   ques = 'Why' + ' ' + h + ' ' + m[0].lower() + m[1] + '?'
                              else:
                                   ques = 'Why' + ' ' + str(line1).lower() + '?'
                              q = nlp(ques)
                              for t in q:
                                   if str(t.tag_) == "NN":
                                        b = 1
                                        break
                              if b == 1:
                                   # print(str(k)+") "+ques)
                                   ans = ans + str(k) + ") " + ques + '\n'
                                   k = k + 1
                              break
               elif "called" in line:
                    b = 0
                    l = line.split('called')
                    m = nlp(l[0])
                    for token in m:
                         ques = 'What' + " " + str(m[-1:]) + " " + str(m[:-1]).lower() + " called ?"
                         q = nlp(ques)
                         for t in q:
                              if str(t.tag_) == "NN":
                                   b = 1
                                   break
                         if b == 1:
                              # print(str(k)+") "+ques)+'\n'
                              ans = ans + str(k) + ") " + ques + '\n'
                              k = k + 1
                         break
               elif "As a result" in line:
                    l = line.split('As a result,')
                    m = nlp(l[1])
                    h = ""
                    for token in m:
                         # print(token.text,token.dep_,token.tag_)
                         if "aux" in str(token.dep_):
                              h = h + token.text
                              break
                    if h != "":
                         n = str(m).split(h)
                         p = n[1]
                         ques = 'Why' + ' ' + h + ' ' + n[0].lower() + p[:-1] + '?'
                         # print(str(k)+") "+ques)
                         ans = ans + str(k) + ") " + ques + '\n'
                    else:
                         for token in m:
                              if (token.tag_ == "VBP"):
                                   a = "do"
                              elif (token.tag_ == "VBD"):
                                   a = "did"
                              elif (token.tag_ == "VBZ"):
                                   a = "does"
                    n = str(m)
                    for token in m:
                         if (token.tag_ == "VBD" or token.tag_ == "VBP" or token.tag_ == "VBZ"):
                              n = re.sub(str(token.text), str(token.lemma_), n)
                    ques = 'Why' + ' ' + a + ' ' + n.lower() + '?'
                    # print(str(k)+") "+ques)
                    ans = ans + str(k) + ") " + ques + '\n'
                    k = k + 1
                    break
               elif "for example" in line.lower() or "for instance" in line.lower():
                    if "for example" in line.lower():
                         b = "for example"
                    else:
                         b = "for instance"
                    l = line.lower().split(b)
                    if not l[0]:
                         ques = 'Give an example:' + ' ' + str(list1[c - 1]).lower()
                    else:
                         if "-" in str(l[0]).lower():
                              l = str(l[0]).lower().split('-')
                              ques = 'Give an example:' + ' ' + str(l[1]).lower()
                         else:
                              ques = 'Give an example:' + ' ' + str(l[0]).lower()
                         if ques[-1] == ",":
                              ques = ques.replace(ques[-1], '.')
                    # print(str(k)+") "+ques)
                    ans = ans + str(k) + ") " + ques + '\n'
                    k = k + 1
               elif "since" in line:
                    z = 0
                    l = line.split('since')
                    line1 = nlp1(str(l[0]))
                    line3 = nlp1(str(l[1]))
                    for ent in line3.ents:
                         if str(ent.label_) == 'TIME' or str(ent.label_) == 'DATE':
                              z = 1
                              break
                    for token in line3:
                         if str(token.lemma_) == 'start' or str(token.lemma_) == 'end' or str(token.lemma_) == 'begin':
                              z = 1
                              break
                    h = ""
                    for token in line1:
                         # print(token.text,token.dep_)
                         if "aux" in str(token.dep_):
                              h = h + token.text
                              break
                    if z == 0:
                         if h != "":
                              m = str(line1).split(h)
                              ques = 'Why' + ' ' + h + ' ' + m[0].lower() + m[1] + '?'
                         else:
                              line2 = str(line1)
                              line2 = line2.replace(line2[-1], " ")
                              ques = 'Why' + ' ' + line2.lower() + '?'
                    else:
                         if h != "":
                              m = str(line1).split(h)
                              ques = 'Since when' + ' ' + h + ' ' + m[0].lower() + m[1] + '?'
                         else:
                              ques = 'Since when' + ' ' + str(line1) + '?'
                    # print(str(k)+") "+ques)
                    ans = ans + str(k) + ") " + ques + '\n'
                    k = k + 1
               elif "hence" in line.lower() or "thus" in line.lower() or "therefore" in line.lower():
                    if "hence" in line.lower():
                         l = (line.lower()).split('hence')
                    elif "thus" in line.lower():
                         l = (line.lower()).split('thus')
                    elif "therefore" in line.lower():
                         l = (line.lower()).split('therefore')
                    ques = 'Explain why' + ' ' + str(l[1]) + '?'
                    # print(str(k)+") "+ques)
                    ans = ans + str(k) + ") " + ques + '\n'
                    k = k + 1
               elif "although" in line or "though" in line or "however" in line:
                    if "although" in line:
                         l = line.split('although')
                    elif "though" in line:
                         l = line.split('though')
                    else:
                         l = line.split('however')
                    line100 = nlp1(line)
                    for token in line100:
                         # print(token.text,token.dep_,token.tag_)
                         line1 = nlp1(str(l[1]))
                         line2 = nlp1(str(l[0]))
                    h = ""
                    for token in line1:
                         # print(token.text,token.dep_,token.tag_)
                         if "aux" in str(token.dep_):
                              h = h + token.text
                              break
                    if h != "":
                         m = str(line1).split(h)
                         p = m[1]
                         ques = h.capitalize() + ' ' + m[0].lower() + p[:-1] + '?'
                         # print(str(k)+") "+ques)
                         ans = ans + str(k) + ") " + ques + '\n'
                         k = k + 1
                         h1 = h + '\'t'
                         ques = h1.capitalize() + ' ' + m[0].lower() + p[:-1] + '?'
                         # print(str(k)+") "+ques)
                         ans = ans + str(k) + ") " + ques + '\n'
                         k = k + 1
                    # print(str(k)+") "+ques)
                    ans = ans + str(k) + ") " + ques + '\n'
                    k = k + 1
                    break
               elif "-" in line:
                    l = line.split('-')
                    m = nlp(l[0])
                    if str((l[1][:1]).isupper()) == "True":
                         for token in m:
                              if str(token.tag_) == "-RRB-":
                                   h = token.text
                                   l[0] = str(m).split(h)
                                   m = l[0][1]
                              ques = "Write in detail about " + str(m).lower() + "?"
                         # print(str(k)+") "+ques)
                         ans = ans + str(k) + ") " + str(ques) + '\n'
                         k = k + 1
               elif str(line.isupper()) == "True" and "SUMMARY" not in line:
                    b = 0
                    ques = "Write short note on " + line.lower()
                    ques = nlp(ques)
                    for token in ques:
                         if (str(token.tag_) == "-RRB-"):
                              b = 1
                              break
                    if b == 0:
                         # print(str(k)+") "+str(ques))
                         ans = ans + str(k) + ") " + str(ques) + '\n'
                         k = k + 1
          #print(ans)
          sq = ans


     if (request.method == 'POST' and 'fib' in request.POST):
          add_data = request.POST.copy()
          line = add_data.get("text")
          nlp1 = spacy.load('en_core_web_sm')
          nlp = spacy.load('en_coref_sm')
          doc = nlp(line)
          list1 = list(doc.sents)
          ans = ""
          k=1
          c = -1
          for x in list1:
               line = str(x)
               line09 = nlp(line)
               c = c + 1
               if "means" in line:
                    l = line.split('means')
                    m = nlp(l[1])
                    for token in m:
                         ques = "______ means" + str(m)
                         # print(str(k)+") "+ques)
                         ans = ans + str(k) + ") " + ques + '\n'
                         k = k + 1
                         break
               elif "called" in line:
                    b = 0
                    l = line.split("called")
                    m = nlp(l[0])
                    for token in m:
                         ques = str(m) + " called______."
                         ques = nlp(ques)
                    for token in ques:
                         if str(token.tag_) == 'NN' or str(token.tag_) == 'JJ':
                              b = 1
                              break
                    if b == 1:
                         # print(str(k)+") "+str(ques))
                         ans = ans + str(k) + ") " + str(ques) + '\n'
                         k = k + 1
               for e in line09.ents:
                    if str(e.label_) == 'LAW':
                         line = line.replace(e.text, "________")
                         # print(str(k)+") "+line)
                         for token in nlp(line):
                              if str(token.text) == "this" or str(token.text) == "these" or str(token.text) == "that":
                                   line = str(list1[c - 1]) + line
                         # print(str(k)+") "+line)
                         ans = ans + str(k) + ") " + line + '\n'
                         k = k + 1
                         break
                    elif str(e.label_) == 'DATE':
                         line = line.replace(e.text, "________")
                         # print(str(k)+") "+line)
                         for token in nlp(line):
                              if str(token.text) == "this" or str(token.text) == "these" or str(token.text) == "that":
                                   line = str(list1[c - 1]) + line
                         # print(str(k)+") "+line)
                         ans = ans + str(k) + ") " + line + '\n'
                         k = k + 1
                         break
          print(ans)
          sq = ans

         # sq = ['What is name of school?','what will be done after this?','How are u?']


     return render(request,'quest/question.html',{'sq':sq})


def final(request):
     if (request.method == 'POST'):
          ques = request.POST.getlist('text')

     return render(request,'quest/final.html',{'ques':ques})

     # doc = nlp1(text)
     # list99 = list(doc.sents)

     # if "because" in line:
     #      l = line.split('because')
     #      line1 = nlp1(str(l[0]))
     #      h = ""
     #      for token in line1:
     #           print(token.text, token.dep_)
     #           if "aux" in str(token.dep_):
     #                h = h + token.text
     #                break
     #      if h != "":
     #           m = str(line1).split(h)
     #           ques = 'Why' + ' ' + h + ' ' + m[0].lower() + m[1] + '?'
     #      else:
     #           ques = 'Why' + ' ' + str(line1) + '?'
     #      # print(ques)