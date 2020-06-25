import PyPDF4
#import time

pdfFileObj = open(
    '/Users/yokey/OneDrive/吉珠/Project/大一下线上工作室/code/HowWeLearnThings.pdf', 'rb')
pdfReader = PyPDF4.PdfFileReader(pdfFileObj)
p_cnt = pdfReader.numPages
wordfre = {}
wordlist = []
#start = time.clock()

for i in range(p_cnt):
    pageObj = pdfReader.getPage(i)
    wordlist += pageObj.extractText().split()

cnt = 0
for w in wordlist:
    cnt += 1
    if w not in wordfre:
        wordfre[w] = 1
    else:
        wordfre[w] += 1

sorted_fre = []
for key in wordfre:
    sorted_fre.append([wordfre[key], key])

#end = time.clock()
# print("程序耗时"+str(end-start)+"秒完成计算")

sorted_fre = sorted(sorted_fre, key=lambda x: -x[0])
print("以下默认打印词频最高的前15项:")
for i in range(15):
    print(
        f"#{i+1:<5}{sorted_fre[i][1]:<20}出现次数:  {sorted_fre[i][0]:<10}占总次数比例:  {sorted_fre[i][0]/cnt*100:.2f}%")
