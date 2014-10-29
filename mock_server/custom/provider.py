from mock_server.api import Response
from mock_server.custom.customresponse import CustomResponse 
import json
import xmlrpclib
import jsonrpclib

def provider(request):
    if request.uri == '/abc':
        headers = [("Content-Type", "application/json; charset=utf-8")]
        content = {"name": "Tomas", "surname": "Hanacek"}
        return Response(json.dumps(content), headers, 200)

    if request.uri == '/bugzilla':
        headers = [("Content-Type", request.headers["Content-Type"]+"; charset=utf-8")]
        method_name = ''
        if request.headers["Content-Type"].find('application/jsonrpc')>=0:
            data = jsonrpclib.loads(request.body)
            method_name = data["method"]
        elif request.headers["Content-Type"].find('text/xml')>=0:
            method_name =  xmlrpclib.loads(request.body)[1]

        reponseData = CustomResponse.callMethod(request.body,method_name)
        return Response(responseData, headers, 200)
