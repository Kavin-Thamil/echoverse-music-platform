from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import SongForm, RegisterForm
from .models import Song
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden

def home(request):
    songs = Song.objects.all()
    selected_genre = request.GET.get('genre')
    search_query = request.GET.get('search')
    if selected_genre:
        songs = songs.filter(
            genre__iexact=selected_genre
        )
    if search_query:
        songs = songs.filter(
            title__icontains=search_query
        )
    songs = songs.order_by('-created_at')
    genres = Song.objects.values_list(
        'genre',
        flat=True
    ).distinct()

    return render(request, 'echo/home.html', {
        'songs': songs,
        'selected_genre': selected_genre,
        'search_query': search_query,
        'genres': genres
    })

@login_required
def upload_song(request):
    if request.method == 'POST':
        form = SongForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            song = form.save(commit=False)
            song.uploaded_by = request.user
            song.save()

            return redirect('home')
    else:
        form = SongForm()

    return render(
        request,
        'echo/upload.html',
        {
            'form': form
        }
    )

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('login')
    else:
        form = RegisterForm()

    return render(
        request,
        'echo/register.html',
        {
            'form': form
        }
    )

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(
            data=request.POST
        )
        if form.is_valid():
            user = form.get_user()
            login(
                request,
                user
            )

            return redirect('home')
    else:

        form = AuthenticationForm()

    return render(
        request,
        'echo/login.html',
        {
            'form': form
        }
    )

def user_logout(request):
    logout(request)

    return redirect('home')

def song_detail(request, song_id):
    song = get_object_or_404(
        Song,
        id=song_id
    )
    related_songs = Song.objects.filter(
        genre=song.genre
    ).exclude(
        id=song.id
    )[:3]

    return render(
        request,
        'echo/song_detail.html',
        {
            'song': song,
            'related_songs': related_songs
        }
    )

def profile(request, user_id):
    user_songs = Song.objects.filter(
        uploaded_by_id=user_id
    )
    profile_user = get_object_or_404(
        User,
        id=user_id
    )

    return render(
        request,
        'echo/profile.html',
        {
            'user_songs': user_songs,
            'profile_user': profile_user
        }
    )

@login_required
def delete_song(request, song_id):
    song = get_object_or_404(
        Song,
        id=song_id
    )
    if song.uploaded_by != request.user:
        return HttpResponseForbidden(
            "You cannot delete this song."
        )
    if request.method == "POST":
        song.delete()
        return redirect('home')

    return render(
        request,
        'echo/delete_song.html',
        {
            'song': song
        }
    )

@login_required
def my_uploads(request):
    songs = Song.objects.filter(
        uploaded_by=request.user
    ).order_by('-created_at')

    return render(
        request,
        'echo/my_uploads.html',
        {
            'songs': songs
        }
    )

@login_required
def toggle_favorite(request, song_id):
    song = get_object_or_404(
        Song,
        id=song_id
    )
    if request.user in song.favorites.all():
        song.favorites.remove(
            request.user
        )
    else:
        song.favorites.add(
            request.user
        )

    return redirect(
        'song_detail',
        song_id=song.id
    )

@login_required
def my_favorites(request):
    songs = request.user.favorite_songs.all().order_by(
        '-created_at'
    )

    return render(
        request,
        'echo/my_favorites.html',
        {
            'songs': songs
        }
    )