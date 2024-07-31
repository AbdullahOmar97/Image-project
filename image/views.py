from django.shortcuts import render, get_object_or_404

# Create your views here.

from .models import Image
import requests

API_KEY = '45201566-8b2cd25dd9a1e8d33e0c90d98'
CATEGORY = 'food'

def fetch_images_from_api():
    url = f'https://pixabay.com/api/?key={API_KEY}&q={CATEGORY}'
    response = requests.get(url)
    data = response.json()
    return data['hits']

def store_images():
    if not Image.objects.exists():
        images = fetch_images_from_api()
        for image_data in images:
            Image.objects.create(
                title=image_data['tags'],
                image_url=image_data['webformatURL'],
                description=image_data['user']
            )

def image_list(request):
    store_images()
    images = Image.objects.all()
    return render(request, 'image/image_list.html', {'images': images})

def image_detail(request, id):
    image = get_object_or_404(Image, id=id)
    return render(request, 'image/image_detail.html', {'image': image})
