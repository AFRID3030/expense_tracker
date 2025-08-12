from rest_framework import viewsets
from rest_framework.response import Response
#from rest_framework import status
from .serializers import RegisterSerializer,IncomeSerializer,ExpenseSerializer
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from rest_framework import status, permissions
from .models import Expense,Income
from rest_framework.permissions import IsAuthenticated
from openpyxl import Workbook
from rest_framework.permissions import AllowAny
from datetime import datetime


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only return expenses for the logged-in user
        return Expense.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically assign the user
        serializer.save(user=self.request.user)
@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def register_user(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'User registered successfully.'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#EXpense GET,POST
@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def expense_list_create(request):
    if request.method == 'GET':
        expenses = Expense.objects.filter(user=request.user)
        serializer = ExpenseSerializer(expenses, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Expense PUT,DELETE
@api_view(['PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def expense_update_delete(request, pk):
    try:
        expense = Expense.objects.get(pk=pk, user=request.user)
    except Expense.DoesNotExist:
        return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = ExpenseSerializer(expense, data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        expense.delete()
        return Response({'message': 'Deleted'}, status=status.HTTP_204_NO_CONTENT)



class IncomeViewSet(viewsets.ModelViewSet):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only return INCOME for the logged-in user
        return Expense.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically assign the user
        serializer.save(user=self.request.user)

#INCOME GET,POST
@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def income_list_create(request):
    if request.method == 'GET':
        incomes = Income.objects.filter(user=request.user)
        serializer = IncomeSerializer(incomes, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = IncomeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#INCOME PUT DELETE
@api_view(['PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def income_update_delete(request, pk):
    try:
        income = Income.objects.get(pk=pk, user=request.user)
    except Income.DoesNotExist:
        return Response({'error': 'Income not found'}, status=404)

    if request.method == 'PUT':
        serializer = IncomeSerializer(income, data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        income.delete()
        return Response({'message': 'Income deleted'}, status=204)

#DOWNLOAD EXPENSE API
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def download_expenses(request):
    user = request.user
    expenses = Expense.objects.filter(user=user)

    # Month/year filtering
    month = request.GET.get('month')
    year = request.GET.get('year')
    if month and year:
        expenses = expenses.filter(date__month=int(month), date__year=int(year))
    elif year:
        expenses = expenses.filter(date__year=int(year))

    wb = Workbook()
    ws = wb.active
    ws.title = "Expenses"

    ws.append(['Title', 'Amount', 'Category', 'Date', 'Notes'])
    total_amount = 0

    for expense in expenses:
        ws.append([
            expense.title,
            expense.amount,
            expense.category,
            expense.date.strftime("%Y-%m-%d"),
            expense.notes or ""
        ])
        total_amount += expense.amount

    ws.append(['', '', '', '', ''])
    ws.append(['Total', total_amount, '', '', ''])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=expenses.xlsx'
    wb.save(response)
    return response

#DOWNLOAD INCOME API
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def download_income(request):
    user = request.user
    incomes = Income.objects.filter(user=user)

    # Month/year filtering
    month = request.GET.get('month')
    year = request.GET.get('year')
    if month and year:
        incomes = incomes.filter(date__month=int(month), date__year=int(year))
    elif year:
        incomes = incomes.filter(date__year=int(year))

    wb = Workbook()
    ws = wb.active
    ws.title = "Income"

    ws.append(['Source', 'Amount', 'Date', 'Notes'])
    total = 0
    for income in incomes:
        ws.append([
            income.source,
            income.amount,
            income.date.strftime('%Y-%m-%d'),
            income.notes
        ])
        total += income.amount

    ws.append(["Total", total, "", ""])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=income.xlsx'
    wb.save(response)
    return response

#frontend code
from django.shortcuts import render

def welcome(request):
    return render(request, 'welcome.html')
def register_page(request):
    return render(request, 'register.html')
def login_page(request):
    return render(request, 'login.html')
    return render(request, 'login.html')
def dashboard(request):
    return render(request, 'dashboard.html')
def expenses_page(request):
    return render(request, "expenses-page.html")
def income_page(request):
    return render(request, "income_page.html")
def download_page(request):
    return render(request, 'download_report.html')


