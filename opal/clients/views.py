import struct
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from clients.models import Client, Email, Phone

# Create your views here.
@login_required
def index(request):
    data = {}

    all_clients = get_clients(request)

    data['clients'] = all_clients
    return render(request, 'clients/index.html', data)

@login_required
def get_clients(request):
    try:
        if request.POST['sort'] == 'az':
            all_clients = Client.objects.order_by('first_name').all()
        elif request.POST['sort'] == 'za':
            all_clients = Client.objects.order_by('-first_name').all()
        is_sorted = True;
    except:
        all_clients = Client.objects.all()
        is_sorted = False;
    clients = {}
    i = 0
    for client in all_clients:
        full_name = client.first_name + " " + client.last_name
        clients[i] = client
        i += 1

    if is_sorted:
        return HttpResponse(client_list_html(clients))
    else:
        return clients

def client_list_html(client):
    html = ""
    for key, value in client.items():
        html += "<li class='list-group-item' value='%s'>" % (value.id)
        html += "%s %s" % (value.first_name, value.last_name)
        html += "</li>"
    return html

@login_required
def add_client(request):
    return render(request, 'clients/add_client.html')

@login_required
def client_info(request):
    try:
        client_id = request.POST['client']
        client = Client.objects.get(pk=client_id)
        emails = Email.objects.filter(client=client_id).all()
        email_list = []
        for email in emails:
            email_list.append(email.email)

        data = {}
        data['client_id'] = client.id
        data['full_name'] = "%s %s" % (client.first_name, client.last_name)
        data['emails'] = email_list

        return render(request, "clients/client_info.html", data)
    except:
        raise BaseException
    return render(request, "clients/empty.html")

@login_required
def add_client_submit(request):
    full_name = request.POST['full_name'].split(" ")
    last_name = full_name[-1]
    first_name = " ".join(full_name[0:-1])
    email = request.POST['email']
    phone = request.POST['phone']
    address = request.POST['address']
    city = request.POST['city']
    state = request.POST['state']
    zip_code = request.POST['zip']

    client = Client(
        first_name=first_name,
        last_name=last_name,
        street_address=address,
        city=city,
        state=state,
        zipcode=zip_code
    )

    client.save()

    if email is not "":
        email_info = Email(
            client=client,
            email=email
        )
        email_info.save()

    if phone is not "":
        phone_info = Phone(
            phone=phone,
            client=client
        )
        phone_info.save()

    return redirect('clients:index')
