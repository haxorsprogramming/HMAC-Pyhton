from django.shortcuts import render

# Create your views here.
def login_page(request):
    ip_address = request.META['REMOTE_ADDR']
    context = {
        'aplikasi' : '-',
        'developer' : 'Diana Vita',
        'ip_address' : ip_address
    }
    return render(request, 'login_page/login_page.html', context)