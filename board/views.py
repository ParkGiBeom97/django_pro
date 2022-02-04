from django.shortcuts import redirect, render
from .models import Board, Reply
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib import messages

# Create your views here.


def index(request):

    cate = request.GET.get("cate", "")
    kw = request.GET.get("kw", "")
    pg = request.GET.get("page", 1)

    if kw:
        if cate == "sub":
            b = Board.objects.filter(subject__startswith=kw)
        elif cate == "wri":
            from acc.models import User
            try:
                u = User.objects.get(username=kw)
                b = Board.objects.filter(writer=u).order_by('-pubdate')
            except:
                b = Board.objects.none().order_by('-pubdate')
        elif cate =="con":
            b = Board.objects.filter(content__contains=kw)
    else:
        b = Board.objects.all().order_by('-pubdate')

    pag = Paginator(b, 10)
    obj = pag.get_page(pg)

    content = {
        "blist": obj,
        "cate": cate,
        "kw": kw,
    }

    return render(request, "board/index.html", content)


def detail(request, bpk):
    b = Board.objects.get(id=bpk)
    r = b.reply_set.all()
    context = {
        "b": b,
        "rlist": r,
    }
    return render(request, "board/detail.html", context)


def delete(request, bpk):
    b = Board.objects.get(id=bpk)
    if b.writer == request.user:
        b.delete()
    else:
        messages.info(request, "삭제권한이 없습니다.")
    return redirect('board:index')


def create(request):
    if request.method == "POST":
        s = request.POST.get("sub")
        c = request.POST.get("con")
        Board(subject=s, writer=request.user,
              content=c, pubdate=timezone.now()).save()
        return redirect("board:index")
    return render(request, "board/create.html")


def update(request, bpk):
    b = Board.objects.get(id=bpk)

    # 다른 사람이 접속했을때 예외처리
    if request.user != b.writer:
        return redirect("board:index")

    if request.method == "POST":
        b.subject = request.POST.get("sub")
        b.content = request.POST.get("con")
        b.save()
        return redirect("board:detail", bpk)
    context = {
        "b": b
    }
    return render(request, 'board/update.html', context)


def creply(request, bpk):
    b = Board.objects.get(id=bpk)
    c = request.POST.get("com")
    Reply(b=b, replyer=request.user, comment=c, pubdate=timezone.now()).save()
    return redirect("board:detail", bpk)


def dreply(request, bpk, rpk):
    r = Reply.objects.get(id=rpk)
    if r.replyer == request.user:
        r.delete()
    else:
        messages.info(request, "삭제권한이 없습니다.")
    return redirect("board:detail", bpk)

def likey(request, bpk):
    b = Board.objects.get(id=bpk)
    b.likey.add(request.user)
    return redirect('board:detail', bpk)

def unlikey(request, bpk):
    b = Board.objects.get(id=bpk)
    b.likey.remove(request.user)

    return redirect('board:detail', bpk)
