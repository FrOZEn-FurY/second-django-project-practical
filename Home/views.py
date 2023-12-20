from django.shortcuts import render
from django.views import View
from accounts.models import PostModel
from .forms import SearchInListForm
class HomeView(View):
    form_class = SearchInListForm

    def get(self, request):
        Posts = PostModel.objects.all()
        if request.GET.get('search'):
            Posts = Posts.filter(title__contains=request.GET['search'])
        return render(request, 'Home/Home.html', {'Posts':Posts, 'form':self.form_class})