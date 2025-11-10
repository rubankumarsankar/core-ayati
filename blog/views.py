from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import BlogCategory, Blog
from .serializers import BlogCategorySerializer, BlogSerializer
from .permissions import IsAdminOrReadOnly


class BlogCategoryViewSet(viewsets.ModelViewSet):
  queryset = BlogCategory.objects.all()
  serializer_class = BlogCategorySerializer
  permission_classes = [IsAdminOrReadOnly]
  filter_backends = [filters.SearchFilter]
  search_fields = ["name", "slug"]


class BlogViewSet(viewsets.ModelViewSet):
  queryset = Blog.objects.select_related("category").all()
  serializer_class = BlogSerializer
  permission_classes = [IsAdminOrReadOnly]
  filter_backends = [filters.SearchFilter, filters.OrderingFilter]
  search_fields = ["title", "slug", "excerpt", "content"]
  ordering_fields = ["created_at", "updated_at"]
  ordering = ["-created_at"]

  def get_queryset(self):
      qs = super().get_queryset()
      category_slug = self.request.query_params.get("category")
      status_param = self.request.query_params.get("status")

      if category_slug:
          qs = qs.filter(category__slug=category_slug)
      if status_param:
          qs = qs.filter(status=status_param)

      return qs
