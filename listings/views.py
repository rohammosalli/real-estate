from django.shortcuts import render
from .models import Listing
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .choices import price_choices, bedroom_choices, state_choices

def index(request):
    listings = Listing.objects.order_by('-list_date').filter(is_published=True)

    paginator = Paginator(listings, 6)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)  
    context = {
        'listings': paged_listings
    }
    return render(request, 'listings/listings.html', context)

def listing(request, listing_id):
    return render(request, 'listings/listing.html')

def search(request):
    queryset_list = Listing.objects.order_by('-list_date')

    #Keywords
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(description__icontains=keywords)


    #City
    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            queryset_list = queryset_list.filter(city__iexact=city)


    #State
    if 'state' in request.GET:
        state = request.GET['state']
        if state:
            queryset_list = queryset_list.filter(state__iexact=state)

    #Bedrooms
    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            queryset_list = queryset_list.filter(price__lte=price) 

    #Price
    if 'bedrooms' in request.GET:
        bedrooms = request.GET['bedrooms']
        if bedrooms:
            queryset_list = queryset_list.filter(bedrooms__lte=bedrooms) 

    context = {
        'state_choices':state_choices,
        'bedroom_choices':bedroom_choices,
        'price_choices':price_choices,
        'listings': queryset_list,
        'values': request.GET,



    }
    return render(request, 'listings/search.html', context)