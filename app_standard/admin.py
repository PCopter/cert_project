from django.contrib import admin
from app_standard.models import MinimumStandard



# Register your models here.

class MinimumStandardAdmin(admin.ModelAdmin):
    list_display = ['number' , 'item_test', 'specification','type','thailand','usa_canada','malaysia','indonisia','europe_PED','uae']
    search_fields = ['thailand','usa_canada','malaysia','indonisia','europe_PED','uae']
    list_filter = ['thailand','usa_canada','malaysia','indonisia','europe_PED','uae']


admin.site.register(MinimumStandard,MinimumStandardAdmin)
