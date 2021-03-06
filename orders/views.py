from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.conf import settings

import stripe
from django.contrib.auth.models import Permission

class OrderPageView(TemplateView):
    template_name = 'orders/purchase.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['stripe_key'] = settings.STRIPE_TEST_PUBLISHABLE_KEY
        return context

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

def charge(request):
    permission = Permission.objects.get(codename='special_status')
    u = request.user
    
    if request.method == 'POST':
        charge = stripe.Charge.create(
            amount=3900,
            currency='usd',
            description='Purchase all books',
            source=request.POST['stripeToken']
        )
        u.user_permissions.add(permission)
        return render(request,'orders/charge.html')

