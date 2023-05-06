# Model
```python
# models.py

class Place(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    bookmark = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='bookmarked_places', blank=True)

    def __str__(self):
        return str(self.name)

class Photo(models.Model):
    def photo_path(instance, filename):
        return f'places/{instance.place.pk}/{filename}'

    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='photos')
    photo = models.ImageField(upload_to=photo_path)

    def __str__(self):
        return str(self.place)
```

# Form
```python
# forms.py

from django import forms
from .models import Place, Photo, Review

class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ('name', 'address', )

class PhotoForm(forms.ModelForm):
    photo = forms.ImageField(widget=forms.FileInput(attrs={'multiple': True}))
    class Meta:
        model = Photo
        fields = ('photo',)

class PhotoUpdateForm(forms.ModelForm):
    photo = forms.ImageField(widget=forms.ClearableFileInput)
    class Meta:
        model = Photo
        fields = ('photo',)
```

# 다중 이미지 업로드
## view
```python
# views.py

def create(request):
    if request.user.is_staff:
        if request.method == 'POST':
            form = PlaceForm(request.POST)
            photos = request.FILES.getlist('photo')
            if form.is_valid():
                place = form.save()
                if photos:
                    for photo in photos:
                        Photo.objects.create(place=place, photo=photo)
            return redirect('places:index')
        else:
            form = PlaceForm()
            photoform = PhotoForm()
        context = {
            'form': form,
            'photoform': photoform,
        }
        return render(request, 'places/create.html', context)
    return redirect('places:index')
```

## template
```html
<form action="{% url 'places:create' %}" method="POST" enctype="multipart/form-data">
  {% csrf_token %}
  {{ form }}
  {{ photoform }}
  <input type="submit">
</form>
```

# 다중 이미지 수정
## signal
```python
# signals.py

import os
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

@receiver(pre_save, sender=Photo)
def pre_save_photo(sender, instance, *args, **kwargs):
    try:
        old_photo = instance.__class__.objects.get(pk=instance.pk).photo.path
        try:
            new_photo = instance.photo.path
        except:
            new_photo = None
        if new_photo != old_photo:
            if os.path.exists(old_photo):
                os.remove(old_photo)
    except:
        pass
```

## view
```python
# views.py

def update(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    photos = place.photos.all()

    PhotoFormSet = modelformset_factory(Photo, form=PhotoUpdateForm, can_delete=True, extra=0)
    photoaddform = PhotoForm()

    if request.method == 'POST':
        form = PlaceForm(request.POST, instance=place)
        formset = PhotoFormSet(request.POST, request.FILES, queryset=photos)
        new_photos = request.FILES.getlist('photo')

        if form.is_valid() and formset.is_valid():
            updated_place = form.save()
            instances = formset.save(commit=False)
            for instance in instances:
                instance.place = updated_place
                instance.save()
            formset.save()

            for new_photo in new_photos:
                print(new_photo)
                Photo.objects.create(place=updated_place, photo=new_photo)

            return redirect('places:detail', place.pk)
    else:
        form = PlaceForm(instance=place)
        formset = PhotoFormSet(queryset=photos)

    context = {
        'form': form,
        'formset': formset,
        'place': place,
        'photoaddform': photoaddform,
    }
    return render(request, 'places/update.html', context) 
```

## template
```html
<form action="{% url 'places:update' place.pk %}" method="POST" enctype="multipart/form-data">
  {% csrf_token %}
  {{ form }}
  {{ formset.management_form }}
  {% for photoform in formset %}
    {{ photoform }}
  {% endfor %}
  {{ photoaddform }}
  <input type="submit">
</form>
```

# 다중 이미지 삭제
글을 삭제하면 이미지와 폴더도 삭제된다.

## signal
```python
# signals.py

@receiver(post_delete, sender=Photo)
def delete_place_photo(sender, instance, *args, **kwargs):
    try:
        instance.photo.delete(save=False)
    except:
        pass
```

## view
```python
# views.py

def delete(request, place_pk):
    if request.user.is_staff:
        place = get_object_or_404(Place, pk=place_pk)
        media_dir = os.path.join(settings.MEDIA_ROOT, 'places', str(place.pk))
        place.delete()
        if os.path.exists(media_dir):
            try: os.rmdir(media_dir)
            except: pass
        return redirect('places:index')
    return redirect('places:detail', place_pk)
```