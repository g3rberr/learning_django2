from allauth.socialaccount.models import SocialApp

from .models import Basket

def baskets(request):
    user = request.user if request.user.is_authenticated else None
    if user is None:
        return {'baskets': []}
    return {'baskets': Basket.objects.filter(user=user)}


