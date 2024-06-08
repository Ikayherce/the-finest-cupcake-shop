class Cart():
    def __init__(self,request):
        self.session = request.session

    #Get the current session key if it exists
    cart = self.session.get('session_key')

    #If the user is new there is no session key, we create one
    if 'session_key' not in request.session:
        cart=self.session['session_key'] = {}

    #make sure cart is available on all pages
    self.cart = cart