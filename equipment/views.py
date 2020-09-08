from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotAllowed

from equipment.models import Equipment
from user.models import User
# Create your views here.


def create_new_equipment(request):

    if request.method == 'POST':
        name = request.POST.get('name', '')
        address = request.POST.get('address', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        description = request.POST.get('description', '')

        owner_name = request.POST.get('owner', '')
        try:
            owner = User.objects.get(username=owner_name)
        except:
            return JsonResponse({'error': 'no such a user'})

        equipment = Equipment(name=name, address=address, email=email, phone=phone, description=description, owner=owner)

        equipment.save()

        return JsonResponse({'equipment': name})

    else:
        if request.method != 'GET':
            return HttpResponseNotAllowed(['GET'])
        else:
            return get_all_equipments(request)


def get_all_equipments(request):

    equipment_list = Equipment.objects.all()
    equipment_list_json = []
    for item in equipment_list:
        if item.status == 'REN':
            equipment_list_json.append({
                "name": item.name,
                "owner": item.owner.username,
                "address": item.address,
                "email": item.email,
                "phone": str(item.phone),
                "status": item.status,
                "lease_term_end": item.lease_term_end
            })
        else:
            equipment_list_json.append({
                "name": item.name,
                "owner": item.owner.username,
                "address": item.address,
                "email": item.email,
                "phone": str(item.phone),
                "status": item.status,
                "lease_term_end": "尚未租出"
            })

    return JsonResponse(equipment_list_json, safe=False)
