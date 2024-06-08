from .cart import Cart

#Create context processor so our cart can work on all pages of the site. 
def cart(request):
    #return default data from our cart
    return {'cart': Cart(request)}