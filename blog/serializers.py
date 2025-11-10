from rest_framework import serializers
from .models import Blog, BlogCategory


class BlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = ["id", "name", "slug", "created_at", "updated_at"]


class BlogSerializer(serializers.ModelSerializer):
    # Frontend sends category as slug (e.g. "seo-services")
    category = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=BlogCategory.objects.all(),
        allow_null=True,
        required=False,
    )

    class Meta:
        model = Blog
        fields = [
            "id",
            "title",
            "slug",
            "status",
            "category",

            "hero_title",
            "hero_kicker_top",
            "hero_kicker_bottom",
            "main_heading",

            "author_name",
            "author_title",
            "published_date",
            "last_updated",
            "read_time",

            "featured_image",
            "featured_image_url",

            "intro",
            "whats_inside",
            "sections",
            "faqs",

            "cta_text",
            "cta_button_label",
            "cta_button_link",

            "extra_categories",

            "excerpt",
            "content",

            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]
