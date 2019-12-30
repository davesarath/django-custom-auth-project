from django.http import FileResponse,HttpResponse
from .settings import BASE_DIR

# this function openfile and return that file 
def forStatic(request,u):
    file = BASE_DIR+'\\static\\'+u
    print(file)
    response = FileResponse(open(file, 'rb'))
    return response


def forMediaDp(request,u):
    file = BASE_DIR+'\\media\\dp\\'+u
    print(file)
    response = FileResponse(open(file, 'rb'))
    return response


def forMediaThumb(request,u):
    file = BASE_DIR+'\\media\\thumbnail\\'+u
    print(file)
    response = FileResponse(open(file, 'rb'))
    return response