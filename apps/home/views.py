
from meraki import DashboardAPI
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse


apikey = "b9c05b6593f70a18ce35f16b2210df31baa73267"

itemslist = []
dash = DashboardAPI(apikey)


@login_required(login_url="/login/")
def index(request):

    
    my_list = dash.organizations.getOrganizations()
    myorganizationList = []
    organizationids = []
    for i in my_list:
        myorganizationList.append(i['name'])
        organizationids.append(i['id'])
    
    
    for i in organizationids:        
        itemslist.append(i)

    NetworkDict = dash.organizations.getOrganizationDevices(itemslist[1],1)
    networklist = []

    for i in NetworkDict:
        #print("Network ID:",i['networkId'])
        #print("Network Details:",i)
        networklist.append(i['networkId'])



    networklist = list(dict.fromkeys(networklist))
    devicesList = []
    devicesClientList = []
    for k in networklist:
        #print("Devices :",dash.networks.getNetworkDevices(k))
        devicesList.append(dash.networks.getNetworkDevices(k))
        #devicesClientList.append()
    
    #for k in devicesList:
    #    devicesClientList.append(dash.devices.getDeviceClients(k["serial"]))
    #devicesClientList.append(dash.devices.getDeviceClients(devicesList[0]["serial"]))

    for dList in devicesList:
    #print("Devices:",dList)
        for sList in dList:
        #print("Model:",sList["model"],"Serial:",sList["serial"],"NetworkId:",sList["networkId"],
        #      "Lan IP:",sList["lanIp"],"firmware:",sList["firmware"])
        #print("Devices client list:",dash.devices.getDeviceClients(sList["serial"]))
            devicesClientList.append(dash.devices.getDeviceClients(sList["serial"]))


    

    context = {'segment': 'index'}
    context = {'organizationsList': myorganizationList,'networklist':networklist,'devicesList':devicesList,
            'devicesClientList':devicesClientList}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
