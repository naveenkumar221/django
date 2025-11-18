from django.http import JsonResponse
import re,json
from basic.models import StudentNew, Users



class basicMiddleware:
    def __init__(self,get_response):
        self.get_response=get_response

    def __call__(self,request):
        # print(request,"hello")
        if(request.path=="/student/"):
            print(request.method,"method")
            print(request.path)
        response= self.get_response(request)
        return response

# class signupMiddleware:
#     def __init__(self,get_response):
#         self.get_response=get_response
#     def __call__(self,request):
#         data=json.loads(request.body)
#         username=data.get("username")
#         email=data.get("email")
#         dob=data.get("dob")
#         password=data.get("pswd")
#         #check username rules with regex
#         #check email rules with regex
#         #check dob rules with regex
#         #check password rules with regex

class SscMiddleware:
    def __init__(self,get_response):
        self.get_response=get_response
    def __call__(self,request):
        if(request.path in ["/job1/","/job2/"]):
            ssc_result=request.GET.get("ssc")
            print(ssc_result,'hello')
            if(ssc_result !='True'):
                return  JsonResponse({"error":"u should qualify atleast ssc for applying this job"},status=400)
        return self.get_response(request)

 
class MedicalFitMiddleware:
    def __init__(self,get_response):
        self.get_response=get_response
    def __call__(self,request):
        if(request.path == "/job1/"):
            medical_fit_result=(request.GET.get("medically_fit"))
            if(medical_fit_result !='True'):
                return JsonResponse({"error":"u not medically fit to apply for this job role"},status=400)
        return self.get_response(request)
 
class AgeMiddleware:
    def __init__(self,get_response):
        self.get_response=get_response
    def __call__(self,request):
        if (request.path in ["/job1/","/job2/"]):
            Age_checker=int(request.GET.get("age",17))
            if Age_checker < 18 or Age_checker > 25:
                return JsonResponse({"error":"age must be in b/w 18 and 25"},status=400)
        return self.get_response(request)

class UsernameMiddleware:
    def __init__(self,get_response):
        self.get_response=get_response
    def __call__(self,request):
        if (request.path == "/signup/"):
            data=json.loads(request.body)
            username=data.get("username","")
            #checks username is empty or not
            if not username:
                return JsonResponse({"error":"username is required"},status=400)
            #checks length    
            if len(username)<3 or len(username)>20:
                return JsonResponse({"error":"username should contains 3 to 20 characters"},status=400)
            #checks starting and ending
            if username[0] in "._" or username[-1] in "._":
                return JsonResponse({"error":"username should not starts or ends with . or _"},status=400) 
            #checks allowed characters
            if not re.match(r"^[a-zA-Z0-9._]+$",username):
                return JsonResponse({"error":"username  should contains letters,numbers,dot,underscore"},status=400)
            #checks .. and  __
            if ".." in username or "__" in username:
                return JsonResponse({"error:cannot have .. or __"},status=400)   
        return self.get_response(request)        
    


class EmailMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        if request.path == "/signup/":
            data = json.loads(request.body)
            email = data.get("email", "")
            if not email:
                return JsonResponse({"error": "email is required"}, status=400)
            email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
            if not re.match(email_regex, email):
                return JsonResponse({"error": "invalid email format"}, status=400)
            if Users.objects.filter(email=email).exists():
                return JsonResponse({"error": "email already exists"}, status=400)
        return self.get_response(request)
    





class PasswordMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        if request.path == "/signup/":
            data = json.loads(request.body)
            password = data.get("password", "")
            
            # Check empty
            if not password:
                return JsonResponse({"error": "password is required"}, status=400)

            # No spaces allowed
            if " " in password:
                return JsonResponse({"error": "password should not contain spaces"}, status=400)

            # Minimum length
            if len(password) < 8:
                return JsonResponse({"error": "password must be at least 8 characters long"}, status=400)

            #Strong password regex
            strong_pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]+$"
            if not re.match(strong_pattern, password):
                return JsonResponse({
                    "error": "password must contain uppercase, lowercase, number, and special character"
                }, status=400)
        return self.get_response(request)