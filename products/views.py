# backend/products/views.py
from rest_framework import viewsets, filters, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from .permissions import IsAdminOrReadOnly
import logging

logger = logging.getLogger(__name__)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # TEMPORARY: Allow all permissions for testing
    # permission_classes = [IsAdminOrReadOnly]
    permission_classes = []  # Remove all permissions temporarily
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'slug']

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('category').all().order_by('-id')  # ✅ newest first
    serializer_class = ProductSerializer
    # TEMPORARY: Allow all permissions for testing
    permission_classes = []  # Remove all permissions temporarily
    parser_classes = [MultiPartParser, FormParser]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description', 'category__name']

    def get_queryset(self):
        qs = super().get_queryset()
        category = self.request.query_params.get('category')  # slug
        active = self.request.query_params.get('active')      # 'true'/'false'
        
        if category:
            qs = qs.filter(category__slug=category)
        if active is not None:
            qs = qs.filter(is_active=active.lower() == 'true')
            
        return qs

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request  # ensures absolute image URL
        return context
    
    def create(self, request, *args, **kwargs):
        """Enhanced create method with better debugging"""
        logger.info(f"Creating product with data: {request.data}")
        logger.info(f"Files: {request.FILES}")
        
        # Validate required fields
        required_fields = ['name', 'price', 'category_id']
        missing_fields = []
        
        for field in required_fields:
            if not request.data.get(field):
                missing_fields.append(field)
                
        if missing_fields:
            return Response(
                {'error': f'Missing required fields: {", ".join(missing_fields)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                product = serializer.save()
                logger.info(f"Product created successfully: {product.id}")
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                logger.error(f"Serializer errors: {serializer.errors}")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            logger.error(f"Error creating product: {str(e)}")
            return Response(
                {'error': f'Failed to create product: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def update(self, request, *args, **kwargs):
        """Enhanced update method with better debugging"""
        logger.info(f"Updating product {kwargs.get('pk')} with data: {request.data}")
        
        try:
            return super().update(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error updating product: {str(e)}")
            return Response(
                {'error': f'Failed to update product: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )