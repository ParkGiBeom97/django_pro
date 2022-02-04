from django.shortcuts import render
from googletrans import Translator
import googletrans


 
def index(request):
    context={
        "ndict" : googletrans.LANGUAGES
    }
    
    if request.method == "POST":
        bf = request.POST.get("bf")
        src = request.POST.get("src")
        dest = request.POST.get("dest")
        translator = Translator()
        trans1 = translator.translate(bf, src=src, dest=dest)
        context.update({
            "af" : trans1.text,
            "bf" : bf,
            "src" : src,
            "dest" : dest,
        })
    return render(request, 'trans/index.html', context)
