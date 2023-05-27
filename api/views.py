from django.contrib.auth.hashers import make_password

from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from knox.auth import AuthToken, TokenAuthentication

from core.serializers import ReportSerializer, AccountSerializer
from core.models import Report, Account
from users.serializers import UserSerializer, LoginSerializer
from users.models import User

# Create your views here.

@api_view(['GET'])
@authentication_classes([])
def validate(request, number):
    try:
        account = Account.objects.filter(number=number).first()

        if account:
            score = 0

            reports = Report.objects.filter(account_number=account)
            # Get report count
            reported_count = reports.count()
            
            # Premium user count
            premium_user_count = 0
            for report in reports:
                if report.reported_by.credibility >= 5:
                    premium_user_count += 1
            
            # Rate
            rate = 0
            ordered_reports = reports.order_by('datetime')
            if(ordered_reports.count() >= 2):
                latest = ordered_reports[0]
                second_latest = ordered_reports[1]

                rate = reported_count/((latest.datetime - second_latest.datetime).days)
                

            # Finalizing score
            score += reported_count*4
            score += premium_user_count*3
            score += rate
            score += account.evidence_score

            serializer = AccountSerializer(account)

            return Response(data={'account': serializer.data, 'score': score},status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ReportView(APIView):
    authentication_classes = []

    def post(self,request):
        user = User.objects.first()

        serializer = ReportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            account = data['account_number']

            if not Account.objects.filter(number=account).first():
                Account.objects.create(
                    number=account
                )

            report_data = dict(account_number = data['account_number'], category = data['category'])

            if data.get("evidence") is not None:
                report_data.append['evidence'] = data['evidence']

            if data.get("evidence_description") is not None:
                report_data['evidence_description'] = data['evidence_description']            

            report = Report.objects.create(
                account_number=data['account_number'],
                category=data['category'],
                evidence=None if data.get("evidence") is None else data['evidence'],
                evidence_description=None if data.get("evidence_description") is None else data['evidence_description'],
                reported_by=user,
                )

            serializer = ReportSerializer(report)

            return Response(data=serializer.data,status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        user = User.objects.first()

        reports = Report.objects.filter(reported_by_id=user.id)
        serializer = ReportSerializer(reports, many=True)

        return Response(data=serializer.data,status=status.HTTP_200_OK)

@api_view(['POST'])
@authentication_classes([])
def register(request):
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        data = serializer.validated_data
        
        user = User.objects.create(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            password=make_password(data['password']),
        )

        token = AuthToken.objects.create(user=user)[1]
        serializer = UserSerializer(user)

        return Response(data={'user':serializer.data, 'token': token,},status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([])
def login(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        data = serializer.validated_data

        user = User.objects.filter(email=data['email']).first()

        if user is None:
            return Response(data= {'message': 'Email or password is invalid'},status=status.HTTP_400_BAD_REQUEST)
        
        if not user.check_password(data['password']):
            return Response(data= {'message': 'Email or password is invalid'},status=status.HTTP_400_BAD_REQUEST)
        
        token = AuthToken.objects.create(user=user)[1]

        serializer = UserSerializer(user)

        return Response(data={'user':serializer.data, 'token': token,},status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST)