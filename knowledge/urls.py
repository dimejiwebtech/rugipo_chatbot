from django.urls import path
from . import views

app_name = 'knowledge'

urlpatterns = [
    path('scrape/', views.trigger_scrape, name='trigger_scrape'),
    path('export/', views.export_qa_view, name='export_qa'),
]
