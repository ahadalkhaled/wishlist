from django.shortcuts import render, redirect
from items.models import Item, FavoriteItem
from .forms import UserRegisterForm, UserLoginForm
from django.contrib.auth import login, logout, authenticate
from django.db.models import Q
from django.http import JsonResponse

def item_wish(request, item_id):
    item_obj = Item.objects.get(id=item_id)
    if request.user.is_anonymous:
        return redirect('user-login')
    wish_obj, created = FavoriteItem.objects.get_or_create(item=item_obj, user=request.user)

    if created:
        action = "wish"
    else:
        action = "unwish"
        wish_obj.delete()


    response = {
        "action": action
    }

    return JsonResponse(response)

def wishlist(request):
    wishlist = []
    items = Item.objects.all()
 
    query = request.GET.get("q")
    if query:
        items = Item.objects.filter(
            Q(name__icontains=query)|
            Q(description__icontains=query)
        ).distinct()
    if request.user.is_authenticated:
        favorite_objects = request.user.favoriteitem_set.all()
    for item in items:
        for favorite in favorite_objects:
            if item.id == favorite.item_id:
                wishlist.append(item)
    context = {
        "wishlist": wishlist
    }

   
    return render(request, 'wishlist.html', context)    
    

def item_list(request):
    items = Item.objects.all()
    
    wishlist = []
    if request.user.is_authenticated:
        my_wishlist = FavoriteItem.objects.filter(user=request.user)
        wishlist = [wish.item for wish in my_wishlist] 

    query = request.GET.get("q")
    if query:
        items = items.filter(
            Q(name__icontains=query)|
            Q(description__icontains=query)
        ).distinct()

   

    context = {
        "items": items,
        "wishlist": wishlist,
        # "wish_list": wish_list
    }
    return render(request, 'item_list.html', context)

def item_detail(request, item_id):
    context = {
        "item": Item.objects.get(id=item_id)
    }
    return render(request, 'item_detail.html', context)

def user_register(request):
    register_form = UserRegisterForm()
    if request.method == "POST":
        register_form = UserRegisterForm(request.POST)
        if register_form.is_valid():
            user = register_form.save(commit=False)
            user.set_password(user.password)
            user.save()
            login(request, user)
            return redirect('item-list')
    context = {
        "register_form": register_form
    }
    return render(request, 'user_register.html', context)

def user_login(request):
    login_form = UserLoginForm()
    if request.method == "POST":
        login_form = UserLoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            authenticated_user = authenticate(username=username, password=password)
            if authenticated_user:
                login(request, authenticated_user)
                return redirect('item-list')
    context = {
        "login_form": login_form
    }
    return render(request, 'user_login.html', context)

def user_logout(request):
    logout(request)

    return redirect('item-list')
