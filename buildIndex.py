import whoosh_test
#import ntpath

if __name__ == "__main__":
    docsPath="C:/Users/ttse/Desktop/InternalApps/Documentation4D/Docs.4dbase/WebFolder/Doc_v15/4D/15/"
    indxPath=docsPath+"_index"
    whoosh_test.docsToWhooshIndx(docsPath,indxPath) ##ONLY RUN ONCE TO BUILD INDEX