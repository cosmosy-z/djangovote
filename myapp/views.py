from django.shortcuts import render,HttpResponse,redirect

import json
from myapp import models
from django.db.models import  Q
# Create your views here.

def options(request):
    if request.method=="POST":
        # 将数据获取

        post_data = request.POST.get('post_data',None)
        post_data_dict = json.loads(post_data)
        print(post_data_dict)
        # 清除原有数据库的内容
        models.Options.objects.all().delete()
        # 将新数据保存入数据库
        for k,v in post_data_dict.items():
            models.Options.objects.create(name=v)

        return HttpResponse('ok')

    return render(request, 'options.html')


def vote(request):

    if request.method == "POST":
        post_data = request.POST.get('vote_data', None)
        print(post_data)
        if post_data:
            # 判断是否是浏览器发送过来的，而不是其他什么程序，这里我们假定只判定苹果电脑
            if "Safari" in request.META["HTTP_USER_AGENT"]:
                print("safari")
            else:
                # 如果不是浏览器打开的，就回复这句话
                return HttpResponse("请适用正确的方式提交")
            # 判断是否有cookie,有cookie
            if request.COOKIES.get('k'):
                  # 有cookie,就不能投票
                print("has_cookie")
                return HttpResponse("已经提交过,请勿重复提交")
            else:
                # 没有cookie,种下cookie,并且完成投票
                print("no_cookie")
                rep=HttpResponse('OK')
                rep.set_signed_cookie('k','123',salt='123',max_age=86400,path='/vote/')
                print("set_cookie")
                # 将投票的内容添加入数据库

                vote_number =  models.Options.objects.filter(name=post_data).values("vote")
                vote_number = list(vote_number)[0]["vote"]
                print("vote_number",vote_number)
                models.Options.objects.filter(name=post_data).update(vote=vote_number+1)

                # 返回正确信息
                return rep
        else:
            # 返回错误信息
            return HttpResponse("网络可能有点儿问题")
    ret = models.Options.objects.all().values("name","vote")
    ret = list(ret)

    return render(request, 'vote.html',{"ret":ret})


def vote_result(request):
    ret = models.Options.objects.all().values("name", "vote")
    ret = list(ret)
    return render(request,"vote_result.html",{"ret":ret})