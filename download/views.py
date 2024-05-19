import datetime
from django.db import connection
from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.http import HttpResponseNotAllowed, JsonResponse
from authentication.views import get_pengguna

def get_unduhan(username):
    query = f"""
        SELECT t.judul, t.id, tu.timestamp
        FROM TAYANGAN T
        JOIN TAYANGAN_TERUNDUH tu
        ON t.id = tu.id_tayangan
        WHERE tu.username = '{username}';
    """

    cursor = connection.cursor()
    cursor.execute(query)
    unduhan = cursor.fetchall()
    cursor.close()

    return unduhan

def show_download(request):
    username = get_pengguna(request)
    daftar_favorit = get_unduhan(username)
    
    context = {
        'pengguna': username,
        'daftar_unduhan': daftar_favorit
    }

    return render(request, "download.html", context)

def add_unduhan(request, id_tayangan):
    username = get_pengguna(request)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if request.method == 'POST':
        query_update = f"""
            INSERT INTO TAYANGAN_TERUNDUH (id_tayangan, username, timestamp)
            VALUES ({id_tayangan}, {username}, {timestamp})
        """

        cursor = connection.cursor()
        cursor.execute(query_update)
        row_added = cursor.rowcount
        cursor.close()

        if row_added > 0:
            return redirect('download:show_download')
        else:
            return redirect('download:show_download')
        
    else:
        if request.method == 'GET':
            return HttpResponseNotAllowed(['POST'], 'This action can only be performed with POST.')
        else:
            return HttpResponseNotAllowed(['POST'])

def delete_unduhan(request, id_tayangan, timestamp):
    username = get_pengguna(request)

    if request.method == 'POST':
        try:
            query_update = f"""
                DELETE FROM TAYANGAN_TERUNDUH
                WHERE id_tayangan = '{id_tayangan}' AND timestamp = '{timestamp}' AND username = '{username}';
            """

            cursor = connection.cursor()
            cursor.execute(query_update)
            row_deleted = cursor.rowcount
            cursor.close()

            if row_deleted > 0:
                return redirect('download:show_download')
            else:
                return redirect('download:show_download')

        except IntegrityError as e:
            error_message = "Tayangan minimal harus berada di daftar unduhan selama 1 hari agar bisa dihapus"

        if error_message:
            context = {'error_message': error_message}
            return render(request, "download.html", context)
        else:
            return redirect('download:show_download')

    else:
        return HttpResponseNotAllowed(['POST'], 'This action can only be performed with POST.')
