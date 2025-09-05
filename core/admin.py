from django.contrib import admin

from .models import UserProfile


def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)


make_refund_accepted.short_description = 'Update orders to refund granted'





admin.site.register(UserProfile)

class PricingModel(admin.ModelAdmin):
    list_display = [
        'item_name',
        'currency',
        'amount',
        'period',
    ]
    list_filter = ['item_name']
    search_fields = []


from .models import Contact,Post,ConverterTools,ColorOptions,FullFeature,FAQs,Pricing,PricingFaqs,ImageHistory,ActivateCode

admin.site.register(Contact)
admin.site.register(Post)
admin.site.register(ConverterTools)
admin.site.register(ColorOptions) 
admin.site.register(FullFeature) 
admin.site.register(FAQs) 
admin.site.register(PricingFaqs) 
# admin.site.register(User) 
admin.site.register(Pricing,PricingModel)
admin.site.register(ImageHistory)
admin.site.register(ActivateCode)