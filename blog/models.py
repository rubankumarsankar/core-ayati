from django.db import models
from django.utils.text import slugify


class BlogCategory(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Blog Category"
        verbose_name_plural = "Blog Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Blog(models.Model):
    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("published", "Published"),
    )

    # Core SEO / routing
    title = models.CharField(max_length=240)
    slug = models.SlugField(max_length=260, unique=True)

    category = models.ForeignKey(
        BlogCategory,
        related_name="blogs",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=16, choices=STATUS_CHOICES, default="draft"
    )

    # Hero + meta
    hero_title = models.CharField(max_length=240, blank=True)
    hero_kicker_top = models.CharField(max_length=120, blank=True)
    hero_kicker_bottom = models.CharField(max_length=260, blank=True)
    main_heading = models.CharField(max_length=260, blank=True)

    author_name = models.CharField(max_length=120, blank=True)
    author_title = models.CharField(max_length=160, blank=True)

    published_date = models.DateField(blank=True, null=True)
    last_updated = models.DateField(blank=True, null=True)
    read_time = models.PositiveIntegerField(default=0, blank=True)

    # Featured image
    featured_image = models.ImageField(
        upload_to="blog/",
        blank=True,
        null=True,
    )
    # Optional: if you store external URL instead of upload
    featured_image_url = models.URLField(blank=True)

    # AEO structure fields
    intro = models.TextField(blank=True)

    whats_inside = models.JSONField(blank=True, null=True)
    # [{ "label": "Intro" }, ...]

    sections = models.JSONField(blank=True, null=True)
    # [{ "heading": "", "body": "<p>..</p>", "image_url": "" }, ...]

    faqs = models.JSONField(blank=True, null=True)
    # [{ "question": "", "answer": "" }, ...]

    cta_text = models.TextField(blank=True)
    cta_button_label = models.CharField(max_length=160, blank=True)
    cta_button_link = models.URLField(blank=True)

    extra_categories = models.JSONField(blank=True, null=True)
    # ["SEO Services", "Digital Marketing"]

    # Rendered / combined content (for frontend consumption, SEO, etc.)
    excerpt = models.TextField(blank=True)
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
          self.slug = slugify(self.title)[:250]
        if not self.hero_title:
          self.hero_title = self.title
        super().save(*args, **kwargs)
