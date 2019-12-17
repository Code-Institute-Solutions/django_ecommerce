from django.shortcuts import render, redirect, reverse
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string

from .forms import OrderForm
from .models import Order, OrderLineItem
from products.models import Product
from profiles.models import UserProfile
from profiles.forms import UserProfileForm


def checkout(request):

	if request.method == 'POST':
		cart = request.session.get('cart', {})

		form_data = {
			'full_name': request.POST['full_name'],
			'email': request.POST['email'],
			'phone_number': request.POST['phone_number'],
			'country': request.POST['country'],
			'postcode': request.POST['postcode'],
			'town_or_city': request.POST['town_or_city'],
			'street_address1': request.POST['street_address1'],
			'street_address2': request.POST['street_address2'],
			'county': request.POST['county'],
		}

		order_form = OrderForm(form_data)
		if order_form.is_valid():
			order = order_form.save()
			for item_id, item_data in cart.items():
				try:
					product = Product.objects.get(id=item_id)
					# If we're working w/ an item with no sizes, item_data will be the quantity
					if isinstance(item_data, int):
						order_line_item = OrderLineItem(
							order = order, 
							product = product, 
							quantity = item_data
						)
						order_line_item.save()
					# Otherwise we need to add order lineitems for each size
					else:
						for size, quantity in item_data['items_by_size'].items():
							order_line_item = OrderLineItem(
								order = order, 
								product = product, 
								quantity = quantity,
								product_size = size
							)
							order_line_item.save()
				except Product.DoesNotExist:
					messages.error(request, (
						"One of the products in your bag wasn't found in our database. "
						"Please call us for assistance! Your card was not charged.")
					)
					order.delete()
					return redirect(reverse('view_cart'))

			###################################
			# TODO: Actual Stripe charge here #
			###################################

			# Save the info to the user's profile if all is well
			request.session['save_info'] = 'save-info' in request.POST

			return(redirect(reverse('checkout_success', args=[order.order_number])))
		else:
			messages.error(request, 'There was an error with your form. Please double check your information.')
	else:
		cart = request.session.get('cart', {})
		if not cart:
			messages.error(request, f"You don't have anything in your bag at the moment. Try adding some products before checking out.")
			return redirect('products')
		# Attempt to prefill the form with any info the user maintains in their profile
		try:
			profile = UserProfile.objects.get(user=request.user)
			order_form = OrderForm(initial={
				'full_name': profile.user.get_full_name(),
				'email': profile.user.email,
				'phone_number': profile.default_phone_number,
				'country': profile.default_country,
				'postcode': profile.default_postcode,
				'town_or_city': profile.default_town_or_city,
				'street_address1': profile.default_street_address1,
				'street_address2': profile.default_street_address2,
				'county': profile.default_county,
			})
		except UserProfile.DoesNotExist:
			order_form = OrderForm()

	stripe_public_key = settings.STRIPE_PUBLIC_KEY

	if not stripe_public_key:
		messages.warning(request, 'Stripe public key is missing. Did you forget to set it in your environment?')
		
	template = 'checkout/checkout.html'
	context = {
		'stripe_public_key': stripe_public_key,
		'order_form': order_form,
	}

	return render(request, template, context)


def checkout_success(request, order_number):
	# Check the session to see if the user wanted to save their info
	save_info = request.session.get('save_info')

	order = Order.objects.get(order_number=order_number)
	no_errors = True

	# Attach the order to the user's profile
	# Handle issues w/ appropriate warnings
	try:
		user_profile = UserProfile.objects.get(user=request.user)

		# User the standard UserProfileForm to save to profile
		if save_info:
			form_data = {
				'default_phone_number': order.phone_number,
				'default_country': order.country,
				'default_postcode': order.postcode,
				'default_town_or_city': order.town_or_city,
				'default_street_address1': order.street_address1,
				'default_street_address2': order.street_address2,
				'default_county': order.county,
			}
			user_profile_form = UserProfileForm(form_data, instance=user_profile)
			if user_profile_form.is_valid():
				user_profile_form.save()
			else:
				no_errors = False
				messages.warning(request, (
					f'Your order was successfully processed, but your information '
					f'could not be saved to your profile. Please try adding it '
					f'manually on your profile page. Your order number is {order_number}. '
					f'A confirmation email has been sent to {order.email}.')
				)
		# Now attempt to attach the order to the user's profile
		try:
			order.user_profile = user_profile
			order.save()
		except:
			no_errors = False
			messages.warning(request, (
				f'Your order was successfully processed, but you may not see this '
				f'order in your order history in your profile due to an error attaching '
				f'the order to your profile. Please contact us for any assistance '
				f'needed with this order. Your order number is {order_number}. '
				f'A confirmation email has been sent to {order.email}.')
			)
	except UserProfile.DoesNotExist:
		no_errors = False
		messages.warning(request, (
			f'Your order was successfully processed, but your information '
			f'could not be saved to your profile because your profile was '
			f'not found. Please contact us if you would like to save your '
			f'information for future orders. Your order number is {order_number}. '
			f'A confirmation email has been sent to {order.email}.')
		)

	# If there were no issues, provide a standard success message
	if no_errors:
		messages.success(request, f'Order successfully processed! Your order number is {order_number}. A confirmation email has been sent to {order.email}.')

	# Send a confirmation email
	cust_email = order.email
	subject = render_to_string('checkout/confirmation_emails/confirmation_email_subject.txt', {'order': order})
	body = render_to_string('checkout/confirmation_emails/confirmation_email_body.txt', {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL})

	send_mail(
		subject,
		body,
		settings.DEFAULT_FROM_EMAIL,
		[cust_email]
	)

	# Empty the customer's cart
	del request.session['cart']

	template = 'checkout/checkout_success.html'
	context = {
		'order': order
	}

	return render(request, template, context)