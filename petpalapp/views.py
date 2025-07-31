from django.shortcuts import render,HttpResponse,get_object_or_404

from .models import Breed

from decimal import Decimal, InvalidOperation
from django.db.models import DecimalField
from .models import Accessory
from django.db.models import Min, Max


# Create your views here.
def Home(request):
    return render(request ,'pages/home.html')

def Login(request):
    return render(request,'pages/login.html')

def Register(request):
    return render(request,'pages/register.html')







def breed_detail(request, slug):
    breed = get_object_or_404(Breed, slug=slug)
    return render(request, 'pages/breed_detail.html', {'breed': breed})


def breed_list(request):
    breeds = Breed.objects.all()

    SIZE_CHOICES = ['Small', 'Medium', 'Large']
    LEVEL_CHOICES = ['Low', 'Medium', 'High']
    TRAINING_CHOICES = ['Easy', 'Moderate', 'Difficult']
    GROOMING_CHOICES = ['Low', 'Moderate', 'High']
    VOCALATY_CHOICE=['Low', 'Moderate', 'High']
    AFFECTION_CHOICE=['independent', 'balance', 'cuddly']


    filters = {
        "size": request.GET.get("size"),
        "energy_level": request.GET.get("energy_level"),
        "ease_of_training": request.GET.get("ease_of_training"),
        "grooming_requirement": request.GET.get("grooming_requirement"),
        "vocality": request.GET.get("vocality"),
        "affection_needs": request.GET.get("affection_needs"),
        "exercise_requirement": request.GET.get("exercise_requirement"),
    }

    for key, value in filters.items():
        if value:
            breeds = breeds.filter(**{f"{key}__iexact": value})

    kid_friendly = request.GET.get("kid_friendly")
    if kid_friendly == "yes":
        breeds = breeds.filter(good_with_kids=True)
    elif kid_friendly == "no":
        breeds = breeds.filter(good_with_kids=False)

    context = {
        'breeds': breeds,
        'kid_friendly': kid_friendly,
        'size_options': SIZE_CHOICES,
        'level_options': LEVEL_CHOICES,
        'training_options': TRAINING_CHOICES,
        'grooming_options': GROOMING_CHOICES,
        'vocality_options':VOCALATY_CHOICE,
        'affection_options':AFFECTION_CHOICE,
        **filters,
    }

    return render(request, 'pages/breed_list.html', context)



def accessories(request):
    all_accessories = Accessory.objects.all()
    categories = all_accessories.values_list('category', flat=True).distinct()
    min_price_db = all_accessories.aggregate(Min('price'))['price__min'] or 0
    max_price_db = all_accessories.aggregate(Max('price'))['price__max'] or 1000

    accessories = all_accessories

    search_query = request.GET.get('q')
    category_filter = request.GET.get('category')
    price_min = request.GET.get('price_min') or min_price_db
    price_max = request.GET.get('price_max') or max_price_db

    if search_query:
        accessories = accessories.filter(name__icontains=search_query)
    if category_filter:
        accessories = accessories.filter(category__iexact=category_filter)

    try:
        if price_min not in [None, '', 'null']:
            price_min_val = Decimal(int(float(price_min)))
            accessories = accessories.filter(price__gte=price_min_val)
    except (InvalidOperation, ValueError):
        pass

    try:
        if price_max not in [None, '', 'null']:
            price_max_val = Decimal(int(float(price_max)))
            accessories = accessories.filter(price__lte=price_max_val)
    except (InvalidOperation, ValueError):
        pass

    return render(request, 'pages/accessories.html', {
        'accessories': accessories,
        'categories': categories,
        'search_query': search_query,
        'category_filter': category_filter,
        'price_min': price_min,
        'price_max': price_max,
        'min_price_db': min_price_db,
        'max_price_db': max_price_db,
    })