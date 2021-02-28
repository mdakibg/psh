from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from .models import Product, categoryList, Contact, Enquiry
from cart.cart import Cart


quantity_options = [1, 2, 3, 5, 10, 20, 30, 50, 75, 100, 150, 200, 300, 500]
# Create your views here.
def index(request):
    products_list = list()

    for category in categoryList:
        products_list.append({
            'category': category[0],
            'products': Product.objects.all().filter(category=category[0])[:10]
        })

    return render(request, 'shop/index.html', {
        'products_list': products_list,
        'featured': Product.objects.all().filter(featured=True)
    })


def cart_add(request, id):
    if "quantity" in request.POST:
        quantity = int(request.POST['quantity'])
        product = Product.objects.get(id=id)

        if "cart" not in request.session:
            request.session["cart"] = dict()
            request.session['cart'][str(id)] = {
                'userid': None,
                'product_id': product.id,
                'name': product.name,
                'quantity': quantity,
                'price': str(product.price),
                'image': product.image.url,
                'minbuy': product.minbuy
            }
            request.session.modified = True
            messages.info(request, "Sucessfully Added Item in Cart!")
            return HttpResponse('<script>history.back();</script>')

        if str(id) in request.session['cart']:
            if quantity == request.session['cart'][str(id)]['quantity']:
                messages.info(request, "Item Already Exists in Cart!")
                return HttpResponse('<script>history.back();</script>')
            request.session['cart'][str(id)]['quantity'] = quantity
            request.session.modified = True
            messages.info(request, "Updated Item Quantity!")
            return HttpResponse('<script>history.back();</script>')

        request.session['cart'][str(id)] = {
            'userid': None,
            'product_id': product.id,
            'name': product.name,
            'quantity': quantity,
            'price': str(product.price),
            'image': product.image.url,
            'minbuy': product.minbuy
        }
        request.session.modified = True
        messages.info(request, "Sucessfully Added Item in Cart!")
        return HttpResponse('<script>history.back();</script>')

    if "cart" not in request.session:
        cart = Cart(request)
        product = Product.objects.get(id=id)
        cart.add(product=product)
        messages.info(request, "Sucessfully Added Item in Cart!")
        return HttpResponse('<script>history.back();</script>')

    if str(id) in request.session["cart"]:
        messages.info(request, "Item Already Exists in Cart!")
        return HttpResponse('<script>history.back();</script>')

    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    messages.info(request, "Sucessfully Added Item in Cart!")
    return HttpResponse('<script>history.back();</script>')


def enquiry(request):
    if request.method == "POST":
        if "name" in request.POST and "email" in request.POST and "address1" in request.POST and "city" in request.POST and "state" in request.POST and "zip_code" in request.POST and "phone" in request.POST and "amount" in request.POST:
            if len(request.session['cart']) == 0:
                messages.info(request, "Your cart is empty. Couldn't submit Enquiry!")
                return render(request, "shop/enquiry.html", {
                    "alert": "danger"
                })

            address = request.POST['address1'] + " | " + request.POST['address2']
            cartcontent = str(request.session['cart'])
            enquiry = Enquiry(name=request.POST['name'], email=request.POST['email'], address=address, city=request.POST['city'], state=request.POST['state'],
                       zip_code=request.POST['zip_code'], phone=request.POST['phone'], cartcontent=cartcontent, amount=request.POST['amount'])
            enquiry.save()
            messages.info(request, "Successfully Submitted Enquiry! We'll get back to you sooner!")
            return render(request, "shop/enquiry.html", {
                "alert": "success"
            })

        if "quantity" in request.POST:
            quantity = int(request.POST["quantity"].split('-')[1])
            product_id = request.POST["quantity"].split('-')[0]

            request.session['cart'][product_id]['quantity'] = quantity
            request.session.modified = True

            messages.info(request, "Successfully Updated Quantity!")
            return redirect("shop:enquiry")

        messages.info(request, "Please fill all mandatory fields!")
        return render(request, "shop/enquiry.html", {
            "alert": "danger"
        })

    return render(request, 'shop/enquiry.html', {
        'quantity_options': quantity_options
    })


def searchMatch(text, product):
    '''return true only if query matches the item'''
    if text.lower() in product.description.lower() or text in product.name.lower() or text in product.category.lower() or text in product.material.lower() or text in product.color.lower():
        return True
    else:
        return False
def search(request):
    search_term = request.GET.get('search').lower()

    search_words = search_term.split(" ")

    if len(search_term) < 4:
        messages.info(request, "Please Enter Valid Input!")
        return render(request, "shop/search.html", {
            "alert": "warning"
        })

    products = list()
    temp_products = Product.objects.all()

    if len(search_words) == 1:
        for product in temp_products:
            if searchMatch(search_term, product):
                products.append(product)

    for product in temp_products:
        flag = True
        for word in search_words:
            if not searchMatch(word, product):
                flag = False
                break
        if flag:
            products.append(product)


    if len(products) == 0:
        messages.info(request, f'No Results Found for "{search_term}"!')
        return render(request, "shop/search.html", {
            "alert": "danger"
        })

    return render(request, "shop/search.html", {
        "products": products
    })


def singleproductview(request, id):
    category = Product.objects.all().values_list("category").filter(id=id)


    if "cart" in request.session and str(id) in request.session['cart']:
        return render(request, "shop/singleproduct.html", {
            'product': Product.objects.get(id=id),
            'quantity': request.session["cart"][str(id)]['quantity'],
            'products': Product.objects.filter(category=category[0][0]).exclude(id=id)[:10],
            'quantity_options': quantity_options
        })

    return render(request, "shop/singleproduct.html", {
        'product': Product.objects.get(id=id),
        'products': Product.objects.filter(category=category[0][0]).exclude(id=id)[:10],
        'quantity_options': quantity_options
    })


def productsview(request, category, price_sort):
    if "category" in request.POST and "price_sort" in request.POST:
        return HttpResponseRedirect(reverse("shop:products",args=(request.POST['category'], request.POST['price_sort'],)))

    if category == 'all':
        if price_sort == 'lh':
            return render(request, "shop/productgrid.html", {
                'products': Product.objects.all().order_by('price'),
                'category': category, 'price_sort': price_sort
            })
        if price_sort == 'hl':
            return render(request, "shop/productgrid.html", {
                'products': Product.objects.all().order_by('-price'),
                'category': category, 'price_sort': price_sort
            })
        return render(request, "shop/productgrid.html", {
            'products': Product.objects.all(),
            'category': category, 'price_sort': price_sort
        })

    if price_sort == 'lh':
        return render(request, "shop/productgrid.html", {
            'products': Product.objects.all().filter(category=category).order_by('price'),
            'category': category, 'price_sort': price_sort
        })
    if price_sort == 'hl':
        return render(request, "shop/productgrid.html", {
            'products': Product.objects.all().filter(category=category).order_by('-price'),
            'category': category, 'price_sort': price_sort
        })
    return render(request, "shop/productgrid.html", {
        'products': Product.objects.all().filter(category=category),
        'category': category, 'price_sort': price_sort
    })


def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    messages.info(request, "Successfully Removed Item!")
    return redirect("shop:enquiry")


def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    messages.info(request, "Successfully Removed All Item(s)!")
    return redirect("shop:enquiry")


def contact(request):
    if request.method == "POST":
        if "name" in request.POST and "email" in request.POST and "phone" in request.POST and "text" in request.POST:
            contact = Contact(name=request.POST['name'], email=request.POST['email'], phone=request.POST['phone'], text=request.POST['text'])
            contact.save()
            messages.info(request, "Thank you for contacting us, We'll get back to you sooner!")
            return render(request, "shop/contact.html", {
                "alert": "success"
            })

        messages.info(request, "Please fill all mandatory fields!")
        return render(request, "shop/contact.html", {
            "alert": "danger"
        })


    return render(request, "shop/contact.html")


def about(request):
    return render(request, "shop/about.html")