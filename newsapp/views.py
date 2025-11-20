from django.shortcuts import render

def news_list(request):
    titles = ["ダミーニュース1", "ダミーニュース2"]
    context = {"titles": titles}
    return render(request, 'newsapp/news_list.html', context)
