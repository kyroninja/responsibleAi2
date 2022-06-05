"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest, FileResponse
from app.chatbotfunc import chat, cloud

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)

    if (request.GET.get('tbutton')):
        chat( str(request.GET.get('utext')) )
        cloud()

    if (request.GET.get('dbutton')):
        #response = FileResponse(open('static/app/output.wav', 'rb'), as_attachment = True)
        response = FileResponse(open('media/output.wav', 'rb'), as_attachment = True)
        return response

    if (request.GET.get('pbutton')):
        #response = FileResponse(open('static/app/output.wav', 'rb'), as_attachment = True)
        response = FileResponse(open('media/wordcl.png', 'rb'), as_attachment = True)
        return response

    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )
