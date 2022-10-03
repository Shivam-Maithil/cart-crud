from rest_framework import serializers 
from .models import *



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model  = Category



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model  = Product



class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'count', 'total_price', 'product']
        model = CartItem
        depth = 1



class CartSerializer(serializers.ModelSerializer):

    items = serializers.SerializerMethodField('get_items')
    def get_items(self, cart):
        items = CartItem.objects.filter(cart=cart)
        cart_items = CartItemSerializer(items, many=True)
        return cart_items.data

    amount_to_be_paid = serializers.SerializerMethodField('get_amount')
    def get_amount(self, cart):
        prices = CartItem.objects.filter(cart=cart).values_list("total_price", flat=True)
        return sum(prices)

    class Meta:
        fields = ['user', 'amount_to_be_paid', 'items']
        model  = Cart


