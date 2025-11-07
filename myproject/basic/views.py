from django.shortcuts import render
from django.http import HttpResponse 
from django.http import JsonResponse
from django.db import connection
# Create your views here.

def sample(requst):
    return HttpResponse("Hello World! Django is working fine 😊")

def sampleinfo(request):
    data = { "name": "naveen","age":22,"city":"hyd"}
    return JsonResponse(data)

def dynamicResponce(request):
    name=request.GET.get("name", ' ')
    return HttpResponse(f"hello{name}")


def calculate(requst):
    a=10
    b=20
    addition = a + b
    subtraction = a - b
    multiplication = a * b
    division = b / a

    result = f""" <h1> The calculation between a and b </h1> <br>
       given a value:{a} <br> given b value: {b} <br>
       additon: {addition} <br>
       subtraction: {subtraction} <br>
       multiplication: {multiplication} <br>
       division:  {division} """
    
    return HttpResponse(result)



# to testing database connection 
def health(reuest):
    try:
        with connection.cursor() as c:
            c.execute("SELECT 1")
        return JsonResponse({"status":"ok","db":"connected"})
    except Exception as e:
        return JsonResponse({"status":"error","db":str(e)})



    