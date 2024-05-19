from django.db import connection
from django.http import HttpResponseNotAllowed
from django.urls import reverse
from django.shortcuts import redirect, render
from authentication.views import get_pengguna

def get_daftar_favorit(username):
    query = f"""
        SELECT judul, timestamp
        FROM DAFTAR_FAVORIT
        WHERE username = '{username}';
    """

    cursor = connection.cursor()
    cursor.execute(query)
    daftar_favorit = cursor.fetchall()
    cursor.close()

    return daftar_favorit

def get_tayangan_favorit(username, timestamp):
    query = f"""
        SELECT t.judul, t.id, subquery.timestamp
        FROM TAYANGAN t
        JOIN (
            SELECT tmdf.id_tayangan, tmdf.timestamp
            FROM TAYANGAN_MEMILIKI_DAFTAR_FAVORIT tmdf
            JOIN DAFTAR_FAVORIT df ON tmdf.timestamp = df.timestamp AND tmdf.username = df.username
            WHERE tmdf.username = '{username}' AND tmdf.timestamp = '{timestamp}'
        ) AS subquery ON t.id = subquery.id_tayangan;
    """

    cursor = connection.cursor()
    cursor.execute(query)
    tayangan_favorit = cursor.fetchall()
    cursor.close()

    return tayangan_favorit

def show_favorite(request):
    if get_pengguna(request) == None:
        return redirect(reverse("authentication:login"))
    
    username = get_pengguna(request)
    daftar_favorit = get_daftar_favorit(username)
    
    context = {
        'pengguna': username,
        'daftar_favorit': daftar_favorit
    }

    return render(request, "daftar_favorit.html", context)

def show_tayangan_favorit(request, timestamp):
    username = get_pengguna(request)
    daftar_favorit = get_daftar_favorit(username)
    tayangan_favorit = get_tayangan_favorit(username, timestamp)

    context = {
        'pengguna': username,
        'daftar_favorit': daftar_favorit[0][0],
        'tayangan_favorit': tayangan_favorit
    }

    return render(request, "tayangan_favorit.html", context)

def add_tayangan_favorit(request, timestamp, id_tayangan):
    username = get_pengguna(request)

    if request.method == 'POST':
        query_update = f"""
            INSERT INTO TAYANGAN_MEMILIKI_DAFTAR_FAVORIT (id_tayangan, timestamp, username)
            VALUES ('{id_tayangan}', '{timestamp}', '{username}')
        """

        cursor = connection.cursor()
        cursor.execute(query_update)
        row_added = cursor.rowcount
        cursor.close()

        if row_added > 0:
            return redirect('favorite:show_tayangan_favorit', timestamp=timestamp)
        else:
            return redirect('favorite:show_tayangan_favorit', timestamp=timestamp)
        
    else:
        if request.method == 'GET':
            return HttpResponseNotAllowed(['POST'], 'This action can only be performed with POST.')
        else:
            return HttpResponseNotAllowed(['POST'])
        
def delete_daftar_favorit(request, timestamp):
    username = get_pengguna(request)

    if request.method == 'POST':
        query_update = f"""
            DELETE FROM DAFTAR_FAVORIT
            WHERE timestamp = '{timestamp}' AND username = '{username}';
        """

        cursor = connection.cursor()
        cursor.execute(query_update)
        row_deleted = cursor.rowcount
        cursor.close()

        if row_deleted > 0:
            return redirect('favorite:show_favorite')
        else:
            return redirect('favorite:show_favorite')
        
    else:
        if request.method == 'GET':
            return HttpResponseNotAllowed(['POST'], 'This action can only be performed with POST.')
        else:
            return HttpResponseNotAllowed(['POST'])
        
def delete_tayangan_favorit(request, timestamp, id_tayangan):
    username = get_pengguna(request)

    if request.method == 'POST':
        query_update = f"""
            DELETE FROM TAYANGAN_MEMILIKI_DAFTAR_FAVORIT
            WHERE id_tayangan = '{id_tayangan}' AND timestamp = '{timestamp}' AND username = '{username}';
        """

        cursor = connection.cursor()
        cursor.execute(query_update)
        row_deleted = cursor.rowcount
        cursor.close()

        if row_deleted > 0:
            return redirect('favorite:show_tayangan_favorit', timestamp=timestamp)
        else:
            return redirect('favorite:show_tayangan_favorit', timestamp=timestamp)
        
    else:
        if request.method == 'GET':
            return HttpResponseNotAllowed(['POST'], 'This action can only be performed with POST.')
        else:
            return HttpResponseNotAllowed(['POST'])