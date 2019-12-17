from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower

from .models import Product, Category
from .forms import ProductForm

def all_products(request):
	products = Product.objects.all()
	query = None
	sort = None
	direction = None
	categories = None
	if request.GET:
		if 'sort' in request.GET:
			sortkey = request.GET['sort']
			sort = sortkey
			# If filtering on name we need to annotate
			# to allow case-insensitive sorting
			if sortkey == 'name':
				sortkey = 'lower_name'
				products = products.annotate(lower_name=Lower('name'))
			if 'direction' in request.GET:
				direction = request.GET['direction']
				if direction == 'desc':
					sortkey = f'-{sortkey}'
			
			products = products.order_by(sortkey)

		if 'category' in request.GET:
			categories = request.GET['category'].split(',')
			products = products.filter(category__name__in=categories)
			# Get the actual category objects to use in the template
			categories = [Category.objects.get(name=c) for c in categories]

		if 'q' in request.GET:
			query = request.GET['q']
			if not query:
				messages.error(request, "You didn't enter any search criteria!")
				return redirect(reverse('products'))

			queries = Q(name__icontains=query) | Q(description__icontains=query)
			products = products.filter(queries)

	current_sorting = f'{sort}_{direction}'

	context = {
		'products': products,
		'search_term': query,
		'current_sorting': current_sorting,
		'current_categories': categories,
	}

	return render(request, 'products/products.html', context)


def product_detail(request, product_id):
	# del request.session['cart']
	product = get_object_or_404(Product, pk=product_id)
	context = {'product': product}

	return render(request, 'products/product_detail.html', context)


def add_product(request):
	
	if request.method == 'POST':
		form = ProductForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			messages.success(request, 'Successfully added product')
			return redirect(reverse('add_product'))

		messages.error(request, 'Failed to add product. Make sure your form is valid')
		return redirect(reverse('add_product'))

	
	form = ProductForm()

	template = 'products/add_product.html'
	context = {
		'form': form
	}

	return render(request, template, context)

def edit_product(request, product_id):
	product = None 

	if request.user.is_superuser:
		if request.method == 'POST':
			product = Product.objects.get(pk=product_id)
			form = ProductForm(request.POST, request.FILES, instance=product)
			if form.is_valid():
				form.save()
				messages.success(request, 'Product successfully updated!')
				return redirect(reverse('products'))
			else:
				messages.error(request, 'Error updating product. Make sure your form is valid')
				return redirect(reverse('edit_product', args=[product.id]))
		else:
			try:
				product = Product.objects.get(pk=product_id)
				form = ProductForm(instance=product)
				messages.info(request, f'You are editing {product.name}')

			except Product.DoesNotExist:
				messages.error(request, 'Product not found. Are you sure it exists?')
				form = ProductForm()
	else:
		messages.error(request, 'You must be a store manager to do this.')

	template = 'products/edit_product.html'
	context = {
		'form': form,
		'product': product
	}

	return render(request, template, context)


def delete_product(request, product_id):
	if request.user.is_superuser:
		try:
			Product.objects.get(pk=product_id).delete()
			messages.success(request, 'Product deleted!')
			return redirect(reverse('products'))

		except Product.DoesNotExist:
			messages.error(request, 'Product not found. Please try deleting it through the admin panel.')
			return redirect(reverse('products'))

	else:
		messages.error(request, 'You must be a store manager to do this.')
		return redirect(reverse('products'))


