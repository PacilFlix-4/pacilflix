from django.shortcuts import redirect, render
from django.urls import reverse
from utils.query import query
from authentication.views import get_pengguna;

# Create your views here.
def show_main(request):
    if get_pengguna(request) == None:
        return redirect(reverse("show:show_main"))

    tipe = request.GET.getlist("tipe")
    if not tipe:
        tipe = ["sutradara", "pemain", "penulis_skenario"]
        
    tipe_str = ", ".join(f"'{t}'" for t in tipe)
    tipe_str = tipe_str.replace('_', ' ')

    contributors = query(
        f"""
        SELECT c.nama, STRING_AGG(t.tipe, ', ') AS tipe, c.jenis_kelamin, c.kewarganegaraan
        FROM CONTRIBUTORS c
        LEFT JOIN (
            SELECT id, 'sutradara' AS tipe FROM SUTRADARA
            UNION ALL
            SELECT id, 'penulis skenario' AS tipe FROM PENULIS_SKENARIO
            UNION ALL
            SELECT id, 'pemain' AS tipe FROM PEMAIN
        ) t ON c.id = t.id
        WHERE t.tipe IN ({tipe_str})
        GROUP BY c.id, c.nama, c.jenis_kelamin, c.kewarganegaraan
        ORDER BY c.nama ASC;
        """
    )

    context = {
        'contributors': contributors,
    }

    return render(request, "contributor.html", context)
