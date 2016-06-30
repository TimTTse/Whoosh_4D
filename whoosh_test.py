from pyquery import PyQuery as pq
import re
from os import walk, mkdir
from os.path import join, exists
from whoosh.index import create_in, open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser, MultifieldParser
from whoosh.highlight import highlight
from whoosh.searching import Results, ResultsPage
from whoosh.lang.porter import stem
from json import JSONEncoder
import ntpath

def prepareDoc(document):
    with open(document, 'r') as myfile:
        html=myfile.read().replace('\n', '')
        
    d=pq(html)
    d('script').remove()
    d('.tdc_hiddenItem').remove()
    d('#article_usage_ul').remove()

    d('#pwrd_by_4d').remove()
    d('.footer_bloc').remove()


    title=d('title').eq(0).text()
    title=re.sub("4D Doc Center : ","",title)

    return title, d.text()

def getDocPaths4D(directory):
    files=[]
    for (dirpath, dirnames, filenames) in walk(directory):
        files.extend(join("/Doc4D/",x) for x in filenames)
        # files.extend(filenames)
    return files

def getDocumentsAbs(directory):
    files=[]
    for (dirpath, dirnames, filenames) in walk(directory):
        files.extend(join(dirpath,x) for x in filenames)
    return files

def createWriterData(documents):
    l=[]
    for document in documents:
        title,content=prepareDoc(document)
        d={
            "title" : title,
            "content" : content,
            "absPath" : document,
            "path" : "/Docs/"+ntpath.basename(document)
        }
        l.append(d)
    return l

def createWhooshIndx(path):
    schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT(stored=True))
    if not exists(path):
        mkdir(path)
    ix = create_in(path, schema)

def addDoc(indxPath,titleT,pathT,contentT):
    titleT=unicode(titleT)
    pathT=unicode(pathT)
    contentT=unicode(contentT)
    if not exists(indxPath):
        createWhooshIndx(indxPath)
    ix = open_dir(indxPath)
    writer = ix.writer()
    writer.add_document(title=titleT, path=pathT, content=contentT)
    writer.commit()

def docsToWhooshIndx(docsPath,indxPath):
    documents=getDocumentsAbs(docsPath)
    writerData=createWriterData(documents)
    for data in writerData:
        t=data["title"]
        p=data["path"]
        c=data["content"]
        # print p
        addDoc(indxPath,t,p,c)  

def query(indxPath,q,currentPage=1,resPerPage=15):
    ix = open_dir(indxPath)
    with ix.searcher() as searcher:
        #query = QueryParser("content", ix.schema).parse("Array ")
        query=MultifieldParser(["title", "content"], schema=ix.schema).parse(q)
        results = searcher.search_page(query, currentPage, pagelen=resPerPage)
        # results = searcher.search(query, limit=10)

        return parseResults(results)

def runChoiceFunction(args):
    choice=args[0]
    if(choice=="Query"):
        indxPath=args[1]
        q=args[2]
        page=int(args[3])
        pagelen=int(args[4])
        # print page
        return query(indxPath,q,page,pagelen)


def parseResults(results):
    numRes=results.total
    titles=[]
    paths=[]
    contents=[]
    if numRes>=0:
        for hit in results:
            title=hit["title"].encode('utf-8')
            path=hit["path"].encode('utf-8')
            content=hit.highlights("content").encode('utf-8')

            titles.append(title)
            paths.append(path)
            contents.append(content)


        normTitles=JSONEncoder().encode(titles)
        normPaths=JSONEncoder().encode(paths)
        normContents=str(JSONEncoder().encode(contents)) ##Not sure if str() is necessary. JSONEncoder() may return other formats
        # print normPaths
       

        # normTitles=', '.join(['"{}"'.format(value) for value in titles])
        # normPaths=', '.join(['"{}"'.format(value) for value in paths])
        # normContents=str(contents)

        numPages=results.pagecount
        resPerPage=results.pagelen
        currentPage=results.pagenum
        runtime=results.results.runtime

        resObj='{"NumResults":' + str(numRes)+', "NumPages":'+str(numPages)+', "Runtime":' + str(runtime)+', "ResPerPage":'+str(resPerPage)+', "CurrentPage":'+str(currentPage)+'}'
        return '{"Titles":' + normTitles+ ',"Paths":'+normPaths+',"Contents":'+normContents+', "Result":'+resObj+'}'
        # return '{"Titles":[' + normTitles+ '],"Paths":['+normPaths+'],"Contents":'+normContents+', "Result":'+resObj+'}'
