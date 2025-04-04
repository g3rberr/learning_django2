import stripe
from http import HTTPStatus

from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.urls import reverse_lazy, reverse
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from orders.forms import OrderForm
from common.views import TitleMixin
from products.models import Basket
from orders.models import Order


stripe.api_key = settings.STRIPE_SECRET_KEY


class SuccessTemplateView(TitleMixin, TemplateView):
    template_name='orders/success.html'
    title = 'Store - Спасибо за заказ!'


class CanceledTemplateView(TitleMixin, TemplateView):
    template_name='orders/canceled.html'

class OrderListView(TitleMixin, ListView):
    template_name = 'orders/orders.html'
    title = 'Store - Заказы'
    queryset = Order.objects.all()
    ordering = ('-created')

    def get_queryset(self):
       queryset = super(OrderListView, self).get_queryset()
       return queryset.filter(initiator=self.request.user)


class OrderDetailView(DetailView):
    template_name = 'orders/order.html'
    model = Order

    def get_context_data(self, *args, **kwargs):
        context = super(OrderDetailView, self).get_context_data()
        context['title'] = f'Store - Заказ #{self.object.id}'
        return context

class OrderCreateView(TitleMixin, CreateView):
    template_name = 'orders/order_create.html'
    title = 'Оформление заказа'
    form_class = OrderForm
    success_url = reverse_lazy('orders:order_create')

    def post(self, request, *args, **kwargs):
        super(TitleMixin, self).post(request, *args, **kwargs)
        baskets = Basket.objects.filter(user=self.request.user)

        checkout_session = stripe.checkout.Session.create(
            line_items=baskets.stripe_products(),
            metadata={'order_id': self.object.id},
            mode='payment',
            success_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_success')),
            cancel_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_canceled')),
        )
        return HttpResponseRedirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)


    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super(OrderCreateView, self).form_valid(form)


@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    if sig_header is None:
      return HttpResponse("Missing Stripe-Signature header", status=400)

    event = None
    
    try:
      event = stripe.Webhook.construct_event(
        payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
      )
    except ValueError as e:
      # Invalid payload
      return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
      # Invalid signature
      return HttpResponse(status=400)
    if (
      event['type'] == 'checkout.session.completed'
      or event['type'] == 'checkout.session.async_payment_succeeded'
    ):
      fulfill_checkout(event['data']['object'])    

    return HttpResponse(status=HTTPStatus.OK)


def fulfill_checkout(session_id):
    order_id = int(session_id.metadata.order_id)
    order = Order.objects.get(id=order_id)
    order.update_after_payment()
