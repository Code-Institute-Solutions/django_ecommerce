from django.contrib import admin
from .models import Order, OrderLineItem


class OrderLineAdminInline(admin.TabularInline):
	model = OrderLineItem
	readonly_fields = ('lineitem_total',)
	

class OrderAdmin(admin.ModelAdmin):
	inlines = (OrderLineAdminInline, )
	readonly_fields = ('order_number', 'date', 'user_profile',)
	fields = (
		'order_number',
		'date',
		'user_profile',
		'full_name',
		'phone_number',
		'country',
		'postcode',
		'town_or_city',
		'street_address1',
		'street_address2',
		'county',
		'shipping_cost',
		'order_total',
	)

	list_display = (
		'order_number', 
		'date',
		'user_profile',
		'full_name', 
		'order_total', 
		'shipping_cost', 
		'grand_total',
	)
	ordering = ('-date',)


admin.site.register(Order, OrderAdmin)