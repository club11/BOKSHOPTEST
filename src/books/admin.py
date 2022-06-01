from django.contrib import admin

# Register your models here.
from . import models

class BookAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'book_name',
        'price',
        'currency_price',
        'author',
        'serie',
        'genre',
        'editor',
        'publishing_date',
        'pages',
        'binding',
        'format',
        'isbn',
        'weigh',
        'age_restrictions',
        'value_available',
        'available',
        'publication_date',
        'publication_edit_date',
        ]

####################################################
#доработать рейтинг
#class RatingStarAdmin(admin.ModelAdmin):
#    list_display= [
#        'value'
#    ]
#
#class RatingAdmin(admin.ModelAdmin):
#    list_display= [
#        'star'
#    ]
########################################################

admin.site.register(models.Book, BookAdmin)
#admin.site.register(models.RatingStar, RatingStarAdmin)
#admin.site.register(models.Rating, RatingAdmin)