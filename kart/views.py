from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from rest_framework.views import APIView
from .serializers import *
from .models import *
from rest_framework.response import Response

# Permission utility
class IsGETOrIsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        return request.user and request.user.is_authenticated


# Category Viewset
class CategoryViewset(ModelViewSet):
    permission_classes = [IsGETOrIsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# Product Viewset
class ProductViewset(ModelViewSet):
    permission_classes = [IsGETOrIsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# Cart Operation APIView
class CartOperationsAPI(APIView):
    permission_classes = [IsGETOrIsAuthenticated]

    # Utility method
    def get_product(self, id):
        try:
            return Product.objects.get(id=id)
        except Product.DoesNotExist:
            return None

    # GET controller
    def get(self, request):
        if request.user.id:
            return Response(CartSerializer(Cart.objects.get(user=request.user)).data)

    # POST controller
    def post(self, request):
        count = 0

        if request.user.id:
            # Check if product exist in param
            if "product" not in request.data:
                return Response([{"error":"product is required"}])
            
            product = self.get_product(request.data["product"])

            if product:
                cart = Cart.objects.get(user=request.user)

                # Cart operation if it is already in cart
                if product.id in cart.cartitem_set.all().values_list("product__id", flat=True):
                    already_in_cart = CartItem.objects.filter(cart=cart).filter(product=product)[0]
                    if "count" in request.data:
                        count  = request.data["count"]
                        already_in_cart.total_price  = product.price * count
                        already_in_cart.count  = count
                        already_in_cart.save()
                
                # If not in cart
                else:
                    item = CartItem.objects.create(product=product, cart=cart)
                    if "count" in request.data:
                        count  = request.data["count"]
                    else:
                        count = 1
                    item.total_price  = product.price * count
                    item.count  = count
                    item.save()

            else:
                return Response([{"error":"not a valid product"}])

            return Response(CartSerializer(Cart.objects.get(user=request.user)).data)

    # DELETE Operation
    def delete(self, request, id):
        if request.user.id:
            cart = Cart.objects.get(user=request.user)
            if int(id) in cart.cartitem_set.all().values_list("product__id", flat=True):
                product = self.get_product(id)
                if product:
                    CartItem.objects.filter(product__id=id).filter(cart=cart).delete()
                    return Response([{"delete":"Item is deleted"}])
                else:
                    return Response({"product does not exist"})
            else:
                return Response({"Item does not exist in the cart"})