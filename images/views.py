from django.shortcuts import render
from images.models import *
from django.http import HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage

# Create your views here.
def index(request):
    if request.method == "GET":
        imgs=[]
        page_list=Page.objects.values("id")
        for pid in page_list:
            title=Page.objects.get(id=pid.get("id")).title
            firstimg=Page.objects.get(id=pid.get("id")).firstimg
            imgs.append({"pid":pid.get("id"),"firstimg":firstimg,"title":title})
        paginator = Paginator(imgs, 6)
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('p')
        try:
            imglist = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            imglist = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            imglist = paginator.page(paginator.num_pages)

        return render(request,'index.html',{"data":imglist})

def page(request,i_id):
    page_arr=Page.objects.get(id=i_id)
    imgs=[]
    tags = []
    time= page_arr.sendtime
    typeid=page_arr.typeid
    type=Type.objects.get(id=typeid).type
    title=page_arr.title
    taglist=page_arr.tagid
    tag_arr=taglist.replace("[","").replace("]","").split(",")
    for t_id in tag_arr:
        tagid=t_id.strip(" ")
        tag=Tag.objects.get(id=tagid).tag
        tags.append({"tname":tag,"tid":tagid})
    imglist=Image.objects.filter(pageid=i_id)
    for img_arr in imglist:
        img=img_arr.imageurl
        imgs.append(img)
    return render(request, 'page.html', {"data": imgs,"tag":tags,"title":title,"type":type,"typeid":typeid,"time":time,"similar":similar(typeid)})

def tag(request,tid):
    if request.method == "GET":
        # istagid=Tag.objects.get(tag=tag).id
        imgs = []
        page_list = Page.objects.values("id")
        for pid in page_list:
            if tid in Page.objects.get(id=pid.get("id")).tagid:
                title = Page.objects.get(id=pid.get("id")).title
                firstimg = Page.objects.get(id=pid.get("id")).firstimg
                imgs.append({"pid": pid.get("id"), "firstimg": firstimg, "title": title})
        paginator = Paginator(imgs, 6)
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('p')
        try:
            imglist = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            imglist = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            imglist = paginator.page(paginator.num_pages)

        return render(request, 'index.html', {"data": imglist})


def type(request,tid):
    if request.method == "GET":
        imgs = []
        page_list = Page.objects.values("id")
        for pid in page_list:
            if tid in Page.objects.get(id=pid.get("id")).typeid:
                title = Page.objects.get(id=pid.get("id")).title
                firstimg = Page.objects.get(id=pid.get("id")).firstimg
                imgs.append({"pid": pid.get("id"), "firstimg": firstimg, "title": title})
        paginator = Paginator(imgs, 6)
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('p')
        try:
            imglist = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            imglist = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            imglist = paginator.page(paginator.num_pages)
        return render(request, 'index.html', {"data": imglist})




def similar(id):
    similarlist=[]
    sidlist=Page.objects.filter(typeid=id)
    i = 0
    for s in sidlist:
        if i <6:
            stitle=s.title
            pid=s.id
            tid=s.typeid
            similarlist.append({"stitle":stitle,"tid":tid,"pid":pid})
            i+=1
    return similarlist

def search(request):
    if request.method=="POST":
        imgs=[]
        context=request.POST['s']
        pagelist=Page.objects.filter(title__contains=context)
        for page in pagelist:
            title = page.title
            firstimg =page.firstimg
            imgs.append({"pid": page.id, "firstimg": firstimg, "title": title})
        paginator = Paginator(imgs, 6)
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('p')
        try:
            imglist = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            imglist = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            imglist = paginator.page(paginator.num_pages)

        return render(request,'index.html',{"data":imglist})



