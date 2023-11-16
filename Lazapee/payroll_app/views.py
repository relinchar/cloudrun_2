from django.shortcuts import render, redirect, get_object_or_404
from .models import *
# Create your views here.

def employees(request): 
    employees = Employee.objects.all()
    return render(request, 'payroll_app/Employees.html', {'employees': employees})

def payslips(request): 
    employees = Employee.objects.all()
    return render(request, 'payroll_app/Payslips.html', {'employees': employees,})

def addEmployee(request):
    if(request.method=="POST"):
        name = request.POST.get('Name')
        id_number = request.POST.get('IDNumber')
        rate = request.POST.get('Rate')
        allowance = request.POST.get('Allowance', '')

        idnum = Employee.objects.filter(id_number=id_number)
        
        if allowance == '':
            allowance = 0

        if idnum.exists() == False:
            Employee.objects.create(
                name=name,
                id_number=id_number,
                rate=rate,
                allowance=allowance,
                )
            return redirect('employees') 
        else:
            return render (request, 'payroll_app/AddEmployees.html', {'error':'ID Number already exists.'})
    else:
        return render(request, 'payroll_app/AddEmployees.html')

def updateEmployee(request, id_number):
    e = get_object_or_404(Employee, id_number=id_number)
    if (request.method == "POST"):
        name = request.POST.get("Name")
        id_num = request.POST.get("IDNumber")
        allowance = request.POST.get("Allowance", '')
        if allowance == '':
            allowance = 0
        rate = request.POST.get("Rate")
        Employee.objects.filter(id_number=id_number).update(name = name, id_number = id_num, allowance = allowance, rate = rate)
        return redirect('employees') 
    else:
        return render(request, 'payroll_app/UpdateEmployee.html', {'id_number': id_number, 'e':e})
    
def deleteEmployee(request, id_number):
    a = Employee.objects.filter(id_number=id_number)
    a.delete()
    return redirect('employees')

def addOvertime(request, id):
    employees = Employee.objects.all()
    e = Employee.objects.get(id_number=id)
    if (request.method == "POST"):
        otHours = request.POST.get("OvertimeHours",'')
        rate = e.getRate()
        oldOTP = e.getOvertime()
        
        if otHours == '':
            otHours = 0
        if oldOTP == None:
            oldOTP = 0
        
        otp = (float(rate)/160) * 1.5 * float(otHours)
        otp = round(otp, 2)
        newOTP = float(oldOTP) + otp
    
        Employee.objects.filter(id_number=id).update(overtime_pay=newOTP)
    return render(request, 'payroll_app/Employees.html', {'employees': employees})

def viewPayslips(request, id):
    payslip = get_object_or_404(Payslip, pk=id)
    employee_id = int(payslip.getIDNumber())
    employee = get_object_or_404(Employee, id_number = employee_id)
 
    # earnings
    base_pay = float(employee.getRate())/2
    allowance = employee.getAllowance()
    overtime = employee.getOvertime()
            
    # Deductions
    wTax= float(payslip.getDeductions_tax())
    ph = float(payslip.getDeductions_health())
    if ph == '':
        ph = 0
    sss = float(payslip.getSSS())
    if sss == '':
        sss = 0

    # Misc.
    rate = float(payslip.getRate())
    allowances = float(payslip.getEarnings_allowance())
    overtime = float(payslip.getOvertime())
    payslipID = payslip.getPay_cycle()
    pagIbig = payslip.getPag_ibig()
    if pagIbig == '':
        pagIbig = 0
      
    deductions = wTax + ph + sss
    gp = (base_pay) + allowances + overtime
    grossPay = round(gp, 2)
    netPay = grossPay - deductions
        
    return render(request, 'payroll_app/ViewPayslips.html', 
                  {'p':payslip, 'e':employee, 'base_pay':base_pay,
                   'allowance':allowance, 'overtime':overtime,
                   'wTax': wTax, 'ph':ph, 'sss':sss, 'rate':rate,
                   'deductions':deductions, 'grossPay':grossPay,
                   'payslipID':payslipID, 'netPay':netPay,
                   'pagIbig':pagIbig,
                   })
    

def createPayslip(request):  
    employees = Employee.objects.all()
    payslips = Payslip.objects.all()
    pTable = [] 
    if (request.method == "POST"):
        id_in = request.POST.get("payFor")
        month = request.POST.get("monthSelect")
        year = request.POST.get("Year")
        pay_cycle = request.POST.get("Cycle")
        
        if id_in != "all employees":
            employee = get_object_or_404(Employee, id_number=id_in)
            employees_to_process = [employee]
        else:
            employees_to_process = employees

        for e in employees_to_process:
            rate = e.getRate()
            earnings_allowance = e.getAllowance()
            overtime = e.getOvertime()

            if (pay_cycle == "1"):
                pag_ibig = 100
                deductions_health = 0
                sss = 0
                deductions_tax = (((rate/2)+ earnings_allowance + overtime - pag_ibig) * 0.2)
                pay = (deductions_tax/0.2) - deductions_tax
                date_range = f"{month} 1-15, {year}"
                
            elif (pay_cycle == "2"):
                pag_ibig = 0
                deductions_health = 0.04*rate
                sss = 0.045*rate
                deductions_tax = (((rate/2) + earnings_allowance + overtime - deductions_health - sss) * 0.2)
                pay = (deductions_tax/0.2) - deductions_tax
                date_range = f"{month} 16-30, {year}"

            payslip = Payslip.objects.create(
                id_number=e,
                month=month,
                year=year,
                pay_cycle=pay_cycle,
                rate=rate,
                earnings_allowance=earnings_allowance,
                date_range=date_range,
                overtime=overtime,
                deductions_tax=deductions_tax,
                deductions_health=deductions_health,
                sss=sss,
                pag_ibig=pag_ibig,
                total_pay=pay,
            )
            pTable.append(payslip)
            Employee.objects.filter(id_number=e.id_number).update(overtime_pay=0)
        
        pTable = Payslip.objects.all()
        return render(request, 'payroll_app/Payslips.html', {'employees':employees, 'pTable': pTable, 'payslips':payslips})
    else:
        pTable = Payslip.objects.all()
        return render(request, 'payroll_app/Payslips.html', {'employees':employees, 'pTable': pTable, 'payslips':payslips})
    