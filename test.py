import whoosh_test
import json
from json import JSONEncoder
#import ntpath

if __name__ == "__main__":
	l=[]
	l.append('only effect is to <b class="match term0">render</b> the information')
	l.append("test2")
	l.append('')
	# print JSONEncoder().encode({"foo": str(l)})
	print JSONEncoder().encode(l)