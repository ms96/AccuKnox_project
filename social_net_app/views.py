# from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
# from ratelimit.exceptions import Ratelimited
# from rest_framework.decorators import api_view, ratelimit
from rest_framework import status, generics
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .serializers import *
from .models import *
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .pagination import CustomPagination
# Create your views here.
from django.contrib.auth.hashers import check_password

def custom_authenticate(email, password):
    try:
        user = User.objects.get(email=email)
        if check_password(password, user.password):
            return user
    except User.DoesNotExist:
        pass
    return None

class UserLogin(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        # import pdb;
        # pdb.set_trace()

        user = custom_authenticate(email=email, password=password)
        # user = authenticate(username = user_obj.email, password = password)
        
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({'error':'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class UserSignup(APIView):
    def post(self, request):
       serializer = UserSignupSerializer(data=request.data)
       if serializer.is_valid():
           serializer.save()
           response_data = {'success': 'User signed up successfully', 'data': serializer.data}
           return Response(response_data, status=status.HTTP_201_CREATED)

       return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserList(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_objs = User.objects.all()
        serializers = UserLoginSerializer(user_objs, many = True)
        print(request.user)
        return Response({'status' : 200, 'data' : serializers.data})

class UserSearchAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    pagination_class = CustomPagination

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserSignupSerializer

    def get_queryset(self):
        search_keyword = self.request.query_params.get('search')
        if search_keyword:
            queryset = User.objects.filter(Q(email__iexact=search_keyword) | Q(username__icontains=search_keyword))
            return queryset
        return User.objects.none()


# @method_decorator(ratelimit(key='ip', rate='3/m', method='POST', block=True))
class SendFriendRequestAPIView(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = FriendRequestSerializer

    # @method_decorator(ratelimit(key='ip', rate='3/m', block=True))
    # def dispatch(self, *args, **kwargs):
    #     try:
    #         return super().dispatch(*args, **kwargs)
    #     except Ratelimited as e:
    #         return Response({'error': 'Rate limit exceeded. You cannot send more than 3 requests per minute.'}, status=status.HTTP_429_TOO_MANY_REQUESTS)

    @method_decorator(ratelimit(key='ip', rate='3/m', block=True))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)  

    def post(self, request, *args, **kwargs):
        user = request.user
        id = request.data.get('id')

        try:
            to_user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        if FriendRequest.objects.filter(from_user=user, status='pending').count() >= 3:
            return Response({'error': 'Rate limit exceeded. You cannot send more than 3 friend requests within a minute.'}, status=status.HTTP_429_TOO_MANY_REQUESTS)

        # serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        FriendRequest.objects.get_or_create(from_user=user, status='pending', to_user=to_user)
        return Response({'success': 'Friend Request Sent successfully!'},status=status.HTTP_201_CREATED)

class AcceptFriendRequestAPIView(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = FriendRequestSerializer

    def post(self, request, *args, **kwargs):    
        user = request.user
        id = request.data.get('id')
        try:
            to_user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            friend = FriendRequest.objects.get(to_user=to_user, status='pending',from_user=user)
            friend.status = 'accepted'
            friend.save()
            return Response({'success': 'Friend Request Accepted!'},status=status.HTTP_200_OK)
        except FriendRequest.DoesNotExist:
            return Response({'error': 'No Such Friend Request!'}, status=status.HTTP_404_NOT_FOUND)

    # def perform_update(self, serializer):
        # serializer.save(status='accepted')


class RejectFriendRequestAPIView(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = FriendRequestSerializer

    def post(self, request, *args, **kwargs):    
        user = request.user
        id = request.data.get('id')
        try:
            to_user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            friend = FriendRequest.objects.get(to_user=to_user, status__in = ['pending','accepted'],from_user=user)
            friend.status = 'rejected'
            friend.save()
            return Response({'success': 'Friend Request Rejected!'},status=status.HTTP_200_OK)
        except FriendRequest.DoesNotExist:
            return Response({'error': 'No Such Friend Request!'}, status=status.HTTP_404_NOT_FOUND)



class FriendListAPIView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = FriendRequestSerializer 

    def get_queryset(self):
        user = self.request.user
        friends = FriendRequest.objects.filter(from_user=user, status='accepted').select_related('to_user')
        return friends
        # return User.objects.filter(id__in=friends)

class PendingFriendRequestListAPIView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = FriendRequestSerializer

    def get_queryset(self):
        user = self.request.user
        pending_requests = FriendRequest.objects.filter(to_user=user, status='pending').select_related('from_user')
        return pending_requests
        