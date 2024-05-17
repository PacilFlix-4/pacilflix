import datetime
from django.db import connection
from django.shortcuts import redirect, render

# Create your views here.
def ulasan(request, id_tayangan):
    ulasans = []
    with connection.cursor() as cursor:
        cursor.execute(
            f"SELECT * FROM ULASAN WHERE id_tayangan = '{id_tayangan}'")
        ulasans = cursor.fetchall()

        cursor.execute(
            f"SELECT id, judul FROM TAYANGAN WHERE id = '{id_tayangan}'")
        judul = cursor.fetchone()

    context = {
        'judul' : judul,
        'ulasans': ulasans,
    }
    response = render(request, 'ulasan.html', context)
    return response

def submit_ulasan(request, id_tayangan):
    if request.method == 'POST':
        username = request.COOKIES.get('username')
        rating = request.POST.get('rating')
        deskripsi = request.POST.get('deskripsi')
        timestamp = datetime.datetime.now()

        query = """
        INSERT INTO ULASAN (id_tayangan, username, timestamp, rating, deskripsi)
        VALUES (%s, %s, %s, %s, %s)
        """
        
        with connection.cursor() as cursor:
            cursor.execute(query, [id_tayangan, username, timestamp, rating, deskripsi])

    return render(request, 'ulasan.html')