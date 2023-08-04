from rest_framework import views, status, generics, viewsets
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser, Ticket
from .serializers import UserSerializer, TicketSerializer
from rest_framework.fields import CurrentUserDefault

from rest_framework.decorators import api_view

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from rest_framework.views import APIView
import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# from .forms import UploadFileForm

@api_view(['GET', 'POST'])
# def user_list_create(request):
def UserListCreateView(request):
    print("##")
    print(request.user)
    print("##")
    if request.method == 'GET':
        queryset = CustomUser.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(views.APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return Response({'id':user.id, 'firstName':user.first_name, 'lastName':user.last_name, 'email':user.username, 'role':user.role}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

# class TicketListCreateView(generics.ListCreateAPIView):
class TicketListCreateView(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

class TicketRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.userDz = request.user  # Set userDz to the currently logged-in user
        # instane.status = request.user
        # instance.save()
        # serializer = self.get_serializer(instance)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

@csrf_exempt
@api_view(['GET', 'POST'])
@login_required
def ticket_list(request):
    if request.method == 'GET':
        user_role = request.user.role
        user_id = request.user.id
        status = request.GET.get('status','todo')
     
        if(user_role == 'DZ'):
            if(status == 'todo'):
                tickets = Ticket.objects.filter(status='todo')
            else:
                tickets = Ticket.objects.filter(Q(status=status) & Q(userDz_id=user_id))
        elif(user_role == 'FR'):
            print(status)
            tickets = Ticket.objects.filter(Q(status=status) & Q(userFr_id=user_id))
            print(tickets)
        else:
            tickets = []

        # tickets = tickets.order_by('-id')

        ticket_data = [
            {
                'id': ticket.id,
                'title': ticket.title,
                'description' : ticket.description,
                'deadline': ticket.deadline,
                'status': ticket.status,
                'notes':ticket.notes,
                # 'userDz': ticket.userDz_id,
                # 'userFr': ticket.userFr_id
            }
            for ticket in tickets
        ]
        return JsonResponse(ticket_data, safe=False)

    if(request.method) == 'POST': 
        data = request.data
        title = data.get('title')
        description = data.get('description')
        notes = data.get('notes')
        deadline = data.get('deadline')
        status = 'todo' 
        user_fr = request.user.id

        ticket = Ticket.objects.create(
                title=title,
                description=description,
                notes=notes,
                deadline= deadline,
                status=status,
                userFr=CustomUser.objects.get(id=user_fr),
            )
        return JsonResponse({'message': 'Ticket created successfully', 'ticket_id': ticket.id})

class LogoutView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({'message': 'Logged out successfully'})






def index(request):
    html = f'''
    <html>
        <body>
            <h1>Hello!</h1>
        </body>
    </html>
    '''
    return HttpResponse(html)