from django.shortcuts import render
from utils.query import query

# Create your views here.
def show_contributors(request):
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
    print(tipe_str)
    print("\n")
    print(contributors)
    return render(request, "contributor.html", context)
