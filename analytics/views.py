from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse 
from analytics.sheet.fb.pages import generate_excel
import time
import os

EXCEL_PATH = os.path.join(os.path.dirname(__file__), "report", "data.xlsx")

# Create your views here.
def index(request):
    error_message = request.session.pop("message", None)
    return render(request, "analytics/index.html", {
        "message": error_message
    })

def generate(request):
    if not os.path.exists(EXCEL_PATH):    
        generate_excel(EXCEL_PATH)
        # time.sleep(3)
    return redirect(reverse("index"))
    
def download(request):
    try:
        with open(EXCEL_PATH, 'rb') as f:
            excel_file = f.read()
            os.remove(EXCEL_PATH)
        return HttpResponse(
            excel_file,
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": 'attachment; filename="data.xlsx"'
            }
        )
    except FileNotFoundError:
        request.session["message"] = "Excel not generated, unable to download."
        return redirect(reverse("index"))
        