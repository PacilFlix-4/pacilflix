import datetime
from django.http import JsonResponse
from django.shortcuts import redirect, render
from utils.query import query
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def show_packages(request):
    username = request.user.username

    active_package = query(
        f"""
        SELECT 
            t.nama_paket AS "Nama",
            p.harga AS "Harga",
            p.resolusi_layar AS "Resolusi_Layar",
            STRING_AGG(d.dukungan_perangkat, ', ') AS "Dukungan_Perangkat",
            t.start_date_time AS "Tanggal_Dimulai",
            t.end_date_time AS "Tanggal_Akhir"
        FROM TRANSACTION t
        JOIN PAKET p ON t.nama_paket = p.nama
        LEFT JOIN DUKUNGAN_PERANGKAT d ON t.nama_paket = d.nama_paket
        WHERE t.username = 'kudaponi11' AND t.end_date_time >= CURRENT_DATE
        GROUP BY t.nama_paket, p.harga, p.resolusi_layar, t.start_date_time, t.end_date_time;
        """
    )

    if not active_package:
        active_package = [{"Nama": "-", "Harga": "-", "Resolusi_Layar": "-", "Dukungan_Perangkat": "-", "Tanggal_Dimulai": "-", "Tanggal_Akhir": "-"}]

    available_packages = query(
        f"""
        SELECT 
            p.nama AS "Nama",
            p.harga AS "Harga",
            p.resolusi_layar AS "Resolusi_Layar",
            STRING_AGG(d.dukungan_perangkat, ', ') AS "Dukungan_Perangkat"
        FROM PAKET p
        LEFT JOIN DUKUNGAN_PERANGKAT d ON p.nama = d.nama_paket
        GROUP BY p.nama, p.harga, p.resolusi_layar
        ORDER BY p.harga ASC;
        """)

    if not available_packages:
        available_packages = [{"Nama": "-", "Harga": "-", "Resolusi_Layar": "-", "Dukungan_Perangkat": "-"}]

    transaction_history = query(
        f"""
        SELECT 
            t.nama_paket AS "Nama",
            t.start_date_time AS "Tanggal_Dimulai",
            t.end_date_time AS "Tanggal_Akhir",
            t.metode_pembayaran AS "Metode_Pembayaran",
            t.timestamp_pembayaran AS "Tanggal_Transaksi",
            p.harga AS "Harga"
        FROM TRANSACTION t
        JOIN PAKET p ON t.nama_paket = p.nama
        WHERE t.username = 'kudaponi11'
        GROUP BY t.nama_paket, t.start_date_time, t.end_date_time, t.metode_pembayaran, t.timestamp_pembayaran, p.harga
        ORDER BY t.start_date_time ASC;
        """
    )

    if not available_packages:
        available_packages = [{"Nama": "-", "Tanggal_Dimulai": "-", "Tanggal_Akhir": "-", "Metode_Pembayaran": "-", "Tanggal_Transaksi": "-", "Harga": "-"}]

    context = {
        'active_package': active_package,
        'available_packages': available_packages,
        'transaction_history': transaction_history
    }

    # print(active_package)

    # print(available_packages)

    # print(transaction_history)

    return render(request, "subscription.html", context)

def show_buy_packages(request, package_name):
    chosen_package = query(
        f"""
        SELECT 
            p.nama AS "Nama",
            p.harga AS "Harga",
            p.resolusi_layar AS "Resolusi_Layar",
            STRING_AGG(d.dukungan_perangkat, ', ') AS "Dukungan_Perangkat"
        FROM PAKET p
        LEFT JOIN DUKUNGAN_PERANGKAT d ON p.nama = d.nama_paket
        WHERE p.nama = '{package_name}'
        GROUP BY p.nama, p.harga, p.resolusi_layar
        ORDER BY p.harga ASC;
        """
    )
    context = {
        'chosen_package': chosen_package
    }

    return render(request, "buy.html", context)

@csrf_exempt
def insert_new_package(request):
    if request.method == 'POST':
        username = 'kudaponi11'
        nama_paket = request.POST.get('nama_paket') 
        metode_pembayaran = request.POST.get('metode_pembayaran') 
        timestamp_pembayaran = datetime.datetime.now()
        start_date_time = timestamp_pembayaran.date()
        end_date_time = (timestamp_pembayaran + datetime.timedelta(days=30)).date()

        print(username)
        print(nama_paket)
        print(metode_pembayaran)
        print(timestamp_pembayaran)
        print(start_date_time)
        print(end_date_time)

        new_package = query(
        f"""INSERT INTO TRANSACTION VALUES(
        '{username}', '{start_date_time}', '{end_date_time}', '{nama_paket}', 
        '{metode_pembayaran}', '{timestamp_pembayaran}'
        );
        """
        )

        if isinstance(new_package, Exception):
            return JsonResponse({'status': 'error', 'message': str(new_package)}, status=500)

        response_data = {'status': 'success', 'message': 'Pembayaran berhasil'}
        json_response = JsonResponse(response_data)
        return redirect('subscription:show_packages')
    
    else:
        return JsonResponse({'status': 'error', 'message': 'Forbidden HTTP Method'}, status=405)
