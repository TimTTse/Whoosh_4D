import whoosh_test as w
#import ntpath

if __name__ == "__main__":
    docsPath="C:/Users/ttse/Desktop/InternalApps/Documentation4D/Docs.4dbase/WebFolder/Doc_v15/4D/15/"
    indxPath=docsPath+"_index"
	##whoosh_test.docsToWhooshIndx(docsPath,indxPath) ##ONLY RUN ONCE TO BUILD INDEX

	

    # q=raw_input("")
    # print w.query(indxPath,q)

    userInput = raw_input("")
    # userInput="Query|C:/Users/ttse/Desktop/InternalApps/Documentation4D/Docs.4dbase/WebFolder/Doc_v15/4D/15/_index|render|1|15"
    args=userInput.split("|")
    print w.runChoiceFunction(args)

    # # q=hit.highlights("content")
    # q="Test"
    # results= w.queryGetResultObj(indxPath,q)
    # for r in results:
    #     print r