import xmlrpclib
import uuid
import pyclbr
import sys

#this class will be calling method on base of method name
class CustomResponse():
    @staticmethod
    def callMethod(requestData,methodName): 
        methodName = methodName.replace('.','_')
        __import__('mock_server.custom.customresponse')
        module = sys.modules['mock_server.custom.customresponse']
        classes = pyclbr.readmodule('mock_server.custom.customresponse').items()
        
        for claName,cla in classes:
            if claName == 'CustomResponse':
                continue
            
            mockClass = getattr(module, claName)
            if(CustomResponse.hasMethod(methodName, cla)):
                response = getattr(mockClass, methodName)(requestData)       
                return response
                
        return None

    @staticmethod
    def hasMethod(methodName,cla):
        methods = cla.methods.items()
        for methodNm, lineno in methods:
            if methodNm == methodName:  
                return True
        return False


class BrewHubMock():
    
    global dynData # build related data, some of data are unique
    global buildroot_id # build root unique id 
    global nvr_id # package nvr unique id 
    global paramSettings # setup parameters    
    
    # initial data
    dynData = {'package_name':'libwacom','task_id':8708068,'creation_event_id':9360886,
                      "nvr":"libwacom-0.8-1.el6","version":"0.8","release":"1.el6","package_id":49335,
                      "id":779902,"name":"libwacom"}
    buildroot_id = 7160000
    nvr_id = 7962202
    paramSettings = {}


    @staticmethod
    def callMethod(requestData,methodName):
        return getattr(BrewHubMock, methodName)(requestData)  
        
    @staticmethod
    def getBuild(request):       
        requestRPC = xmlrpclib.loads(request)
        dynData['nvr'] = requestRPC[0][0]
        buildParts = str(dynData['nvr']).split('-')
        dynData['name'] = buildParts[0]
        dynData['package_name'] = buildParts[0]   
        dynData['version'] = buildParts[1]
        dynData['release'] = buildParts[2]
        dynData['task_id'] = dynData['task_id'] +1
        dynData['creation_event_id'] = dynData['creation_event_id'] +1
        dynData['package_id'] = dynData['package_id'] + 1
        dynData['id'] = dynData['id'] + 1 
        
        response="<?xml version=\"1.0\" encoding=\"utf-8\"?><methodResponse><params><param><value><struct><member><name>owner_name</name><value><string>ajackson</string></value></member><member><name>package_name</name><value><string>${package_name}</string></value></member><member><name>task_id</name><value><int>${task_id}</int></value></member><member><name>volume_name</name><value><string>DEFAULT</string></value></member><member><name>owner_id</name><value><int>169</int></value></member><member><name>creation_event_id</name><value><int>${creation_event_id}</int></value></member><member><name>creation_time</name><value><string>2014-04-24 10:06:10.693793</string></value></member><member><name>state</name><value><int>1</int></value></member><member><name>nvr</name><value><string>${nvr}</string></value></member><member><name>completion_time</name><value><string>2014-04-24 10:09:17.513764</string></value></member><member><name>epoch</name><value><nil/></value></member><member><name>version</name><value><string>${version}</string></value></member><member><name>creation_ts</name><value><double>1398348370.69379</double></value></member><member><name>volume_id</name><value><int>0</int></value></member><member><name>release</name><value><string>${release}</string></value></member><member><name>package_id</name><value><int>${package_id}</int></value></member><member><name>completion_ts</name><value><double>1398348557.5137601</double></value></member><member><name>id</name><value><int>${id}</int></value></member><member><name>name</name><value><string>${name}</string></value></member></struct></value></param></params></methodResponse>"
        
        for key in dynData:
            varData = "${"+key+"}"
            response = response.replace(varData, str(dynData[key]))
        
        return response
    
    @staticmethod    
    def getProductListings_fix(request):   
        response = ''
        if(request.count('RHEL-6-Client')>0):        
            response = "<?xml version='1.0'?><methodResponse><params><param><value><struct><member><name>Client</name><value><struct><member><name>${name}-${version}-${release}</name><value><struct><member><name>x86_64</name><value><array><data><value><string>x86_64</string></value></data></array></value></member><member><name>src</name><value><array><data><value><string>x86_64</string></value><value><string>i386</string></value></data></array></value></member><member><name>i686</name><value><array><data><value><string>x86_64</string></value><value><string>i386</string></value></data></array></value></member></struct></value></member><member><name>${name}-data-${version}-${release}</name><value><struct><member><name>noarch</name><value><array><data><value><string>x86_64</string></value><value><string>i386</string></value></data></array></value></member></struct></value></member><member><name>${name}-debuginfo-${version}-${release}</name><value><struct><member><name>x86_64</name><value><array><data><value><string>x86_64</string></value></data></array></value></member><member><name>i686</name><value><array><data><value><string>x86_64</string></value><value><string>i386</string></value></data></array></value></member></struct></value></member></struct></value></member><member><name>optional</name><value><struct><member><name>${name}-debuginfo-${version}-${release}</name><value><struct><member><name>x86_64</name><value><array><data><value><string>x86_64</string></value></data></array></value></member><member><name>i686</name><value><array><data><value><string>x86_64</string></value><value><string>i386</string></value></data></array></value></member></struct></value></member><member><name>${name}-devel-${version}-${release}</name><value><struct><member><name>x86_64</name><value><array><data><value><string>x86_64</string></value></data></array></value></member><member><name>i686</name><value><array><data><value><string>x86_64</string></value><value><string>i386</string></value></data></array></value></member></struct></value></member></struct></value></member></struct></value></param></params></methodResponse>"
        elif(request.count('RHEL-6-ComputeNode')>0):
            response = "<?xml version='1.0'?><methodResponse><params><param><value><struct><member><name>optional</name><value><struct><member><name>${name}-${version}-${release}</name><value><struct><member><name>x86_64</name><value><array><data><value><string>x86_64</string></value></data></array></value></member><member><name>src</name><value><array><data><value><string>x86_64</string></value></data></array></value></member><member><name>i686</name><value><array><data><value><string>x86_64</string></value></data></array></value></member></struct></value></member><member><name>${name}-data-${version}-${release}</name><value><struct><member><name>noarch</name><value><array><data><value><string>x86_64</string></value></data></array></value></member></struct></value></member><member><name>${name}-debuginfo-${version}-${release}</name><value><struct><member><name>x86_64</name><value><array><data><value><string>x86_64</string></value></data></array></value></member><member><name>i686</name><value><array><data><value><string>x86_64</string></value></data></array></value></member></struct></value></member><member><name>${name}-devel-${version}-${release}</name><value><struct><member><name>x86_64</name><value><array><data><value><string>x86_64</string></value></data></array></value></member><member><name>i686</name><value><array><data><value><string>x86_64</string></value></data></array></value></member></struct></value></member></struct></value></member></struct></value></param></params></methodResponse>"
        elif(request.count('RHEL-6-Workstation')>0):
            response = "<?xml version='1.0'?><methodResponse><params><param><value><struct><member><name>Workstation</name><value><struct><member><name>${name}-${version}-${release}</name><value><struct><member><name>x86_64</name><value><array><data><value><string>x86_64</string></value></data></array></value></member><member><name>src</name><value><array><data><value><string>x86_64</string></value><value><string>i386</string></value></data></array></value></member><member><name>i686</name><value><array><data><value><string>x86_64</string></value><value><string>i386</string></value></data></array></value></member></struct></value></member><member><name>${name}-data-${version}-${release}</name><value><struct><member><name>noarch</name><value><array><data><value><string>x86_64</string></value><value><string>i386</string></value></data></array></value></member></struct></value></member><member><name>${name}-debuginfo-${version}-${release}</name><value><struct><member><name>x86_64</name><value><array><data><value><string>x86_64</string></value></data></array></value></member><member><name>i686</name><value><array><data><value><string>x86_64</string></value><value><string>i386</string></value></data></array></value></member></struct></value></member></struct></value></member><member><name>optional</name><value><struct><member><name>${name}-debuginfo-${version}-${release}</name><value><struct><member><name>x86_64</name><value><array><data><value><string>x86_64</string></value></data></array></value></member><member><name>i686</name><value><array><data><value><string>x86_64</string></value><value><string>i386</string></value></data></array></value></member></struct></value></member><member><name>${name}-devel-${version}-${release}</name><value><struct><member><name>x86_64</name><value><array><data><value><string>x86_64</string></value></data></array></value></member><member><name>i686</name><value><array><data><value><string>x86_64</string></value><value><string>i386</string></value></data></array></value></member></struct></value></member></struct></value></member></struct></value></param></params></methodResponse>"
        elif(request.count('RHEL-6-Server')>0):
            response = "<?xml version='1.0'?><methodResponse><params><param><value><struct><member><name>optional</name><value><struct><member><name>${name}-${version}-${release}</name><value><struct><member><name>s390</name><value><array><data><value><string>s390x</string></value></data></array></value></member><member><name>s390x</name><value><array><data><value><string>s390x</string></value></data></array></value></member><member><name>src</name><value><array><data><value><string>x86_64</string></value><value><string>i386</string></value><value><string>ppc64</string></value><value><string>s390x</string></value></data></array></value></member></struct></value></member><member><name>${name}-data-${version}-${release}</name><value><struct><member><name>noarch</name><value><array><data><value><string>s390x</string></value></data></array></value></member></struct></value></member><member><name>${name}-debuginfo-${version}-${release}</name><value><struct><member><name>ppc</name><value><array><data><value><string>ppc64</string></value></data></array></value></member><member><name>x86_64</name><value><array><data><value><string>x86_64</string></value></data></array></value></member><member><name>s390</name><value><array><data><value><string>s390x</string></value></data></array></value></member><member><name>ppc64</name><value><array><data><value><string>ppc64</string></value></data></array></value></member><member><name>i686</name><value><array><data><value><string>x86_64</string></value><value><string>i386</string></value></data></array></value></member><member><name>s390x</name><value><array><data><value><string>s390x</string></value></data></array></value></member></struct></value></member><member><name>${name}-devel-${version}-${release}</name><value><struct><member><name>ppc</name><value><array><data><value><string>ppc64</string></value></data></array></value></member><member><name>x86_64</name><value><array><data><value><string>x86_64</string></value></data></array></value></member><member><name>s390</name><value><array><data><value><string>s390x</string></value></data></array></value></member><member><name>ppc64</name><value><array><data><value><string>ppc64</string></value></data></array></value></member><member><name>i686</name><value><array><data><value><string>x86_64</string></value><value><string>i386</string></value></data></array></value></member><member><name>s390x</name><value><array><data><value><string>s390x</string></value></data></array></value></member></struct></value></member></struct></value></member><member><name>Server</name><value><struct><member><name>${name}-${version}-${release}</name><value><struct><member><name>ppc</name><value><array><data><value><string>ppc64</string></value></data></array></value></member><member><name>x86_64</name><value><array><data><value><string>x86_64</string></value></data></array></value></member><member><name>src</name><value><array><data><value><string>x86_64</string></value><value><string>i386</string></value><value><string>ppc64</string></value></data></array></value></member><member><name>ppc64</name><value><array><data><value><string>ppc64</string></value></data></array></value></member><member><name>i686</name><value><array><data><value><string>x86_64</string></value><value><string>i386</string></value></data></array></value></member></struct></value></member><member><name>${name}-data-${version}-${release}</name><value><struct><member><name>noarch</name><value><array><data><value><string>x86_64</string></value><value><string>i386</string></value><value><string>ppc64</string></value></data></array></value></member></struct></value></member><member><name>${name}-debuginfo-${version}-${release}</name><value><struct><member><name>ppc</name><value><array><data><value><string>ppc64</string></value></data></array></value></member><member><name>x86_64</name><value><array><data><value><string>x86_64</string></value></data></array></value></member><member><name>ppc64</name><value><array><data><value><string>ppc64</string></value></data></array></value></member><member><name>i686</name><value><array><data><value><string>x86_64</string></value><value><string>i386</string></value></data></array></value></member></struct></value></member></struct></value></member></struct></value></param></params></methodResponse>"
        
        response = response.replace('${name}', dynData['name']);
        response = response.replace('${version}', dynData['version']);
        response = response.replace('${release}', dynData['release']);
        return response   
     
    @staticmethod    
    def listBuildRPMs_fix(request):
 
        archs= ["s390x","s390x","s390x","i686","i686","i686","ppc64","ppc64","ppc64","x86_64","x86_64","x86_64","s390","s390","s390","ppc","noarch","ppc","ppc","src"]
        pckgs = ["libwacom-debuginfo","libwacom-devel","libwacom","libwacom-devel","libwacom","libwacom-debuginfo","libwacom-debuginfo","libwacom","libwacom-devel","libwacom-debuginfo","libwacom-devel","libwacom","libwacom-debuginfo","libwacom-devel","libwacom","libwacom-debuginfo","libwacom-data","libwacom","libwacom-devel","libwacom"]
        buildRoot = [1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,0,0]
        dataBlock = "<?xml version=\"1.0\" encoding=\"utf-8\"?><methodResponse><params><param><value><array><data>"
        
        for i in range(20):
            global buildroot_id
            global nvr_id

            payloadhash = str(uuid.uuid1()).replace('-','')
            buildroot_id = buildroot_id + buildRoot[i]
            nvr_id = nvr_id +1

            dataBlock = "".join([dataBlock,"<value><struct><member><name>build_id</name><value><int>",str(dynData.get("id")),
                                 "</int></value></member><member><name>nvr</name><value><string>",pckgs[i],"-",dynData['version'],"-",
                                 dynData['release'],"</string></value></member><member><name>buildroot_id</name><value><int>",str(buildroot_id),
                                 "</int></value></member><member><name>buildtime</name><value><int>1398348462</int></value></member><member><name>payloadhash</name><value><string>",
                                 payloadhash,"</string></value></member><member><name>epoch</name><value><nil/></value></member><member><name>version</name><value><string>",
                                 dynData.get("version"),"</string></value></member><member><name>external_repo_id</name><value><int>0</int></value></member><member><name>release</name><value><string>",
                                 dynData.get("release"),"</string></value></member><member><name>size</name><value><int>48700</int></value></member><member><name>arch</name><value><string>",
                                 archs[i],"</string></value></member><member><name>id</name><value><int>",str(nvr_id),
                                 "</int></value></member><member><name>external_repo_name</name><value><string>INTERNAL</string></value></member><member><name>name</name><value><string>",
                                 pckgs[i],"</string></value></member></struct></value>"])       
        response = "".join([dataBlock,'</data></array></value></param></params></methodResponse>'])
        response = response.replace('libwacom', dynData['name']);
    
        return response   
      

    @staticmethod    
    def getProductListings(request):   
        prix = ['','aa', 'bb', 'cc','dd','ee','ff','gg','hh','ii','jj','kk'] 
        num = 1 # number times of baseline number of packages
        numstr = dynData['name'][1:2]
        if (numstr.isdigit()):
            num = int (numstr)
 
        response = ''
        if(request.count('RHEL-6-Client')>0):
            fix1 = "<?xml version=\"1.0\" encoding=\"utf-8\"?><methodResponse><params><param><value><struct><member><name>Client</name><value><struct>"
            body1 = "<member><name>${name}-${version}-${release}</name><value><struct><member><name>x86_64</name><value><array><data><value><string>x86_64</string></value></data></array></value></member><member><name>src</name><value><array><data><value><string>x86_64</string></value><value><string>i386</string></value></data></array></value></member><member><name>i686</name><value><array><data><value><string>x86_64</string></value><value><string>i386</string></value></data></array></value></member></struct></value></member><member><name>${name}-data-${version}-${release}</name><value><struct><member><name>noarch</name><value><array><data><value><string>x86_64</string></value><value><string>i386</string></value></data></array></value></member></struct></value></member><member><name>${name}-debuginfo-${version}-${release}</name><value><struct><member><name>x86_64</name><value><array><data><value><string>x86_64</string></value></data></array></value></member><member><name>i686</name><value><array><data><value><string>x86_64</string></value><value><string>i386</string></value></data></array></value></member></struct></value></member>"
            fix2 = "</struct></value></member><member><name>optional</name><value><struct>"
            body2 = "<member><name>${name}-${version}-${release}</name><value><struct><member><name>ppc</name><value><array><data><value><string>ppc64</string></value></data></array></value></member><member><name>x86_64</name><value><array><data><value><string>x86_64</string></value></data></array></value></member><member><name>src</name><value><array><data><value><string>x86_64</string></value><value><string>i386</string></value><value><string>ppc64</string></value></data></array></value></member><member><name>ppc64</name><value><array><data><value><string>ppc64</string></value></data></array></value></member><member><name>i686</name><value><array><data><value><string>x86_64</string></value><value><string>i386</string></value></data></array></value></member></struct></value></member><member><name>${name}-data-${version}-${release}</name><value><struct><member><name>noarch</name><value><array><data><value><string>x86_64</string></value><value><string>i386</string></value><value><string>ppc64</string></value></data></array></value></member></struct></value></member><member><name>${name}-debuginfo-${version}-${release}</name><value><struct><member><name>ppc</name><value><array><data><value><string>ppc64</string></value></data></array></value></member><member><name>x86_64</name><value><array><data><value><string>x86_64</string></value></data></array></value></member><member><name>ppc64</name><value><array><data><value><string>ppc64</string></value></data></array></value></member><member><name>i686</name><value><array><data><value><string>x86_64</string></value><value><string>i386</string></value></data></array></value></member></struct></value></member>"
            fix3="</struct></value></member></struct></value></param></params></methodResponse>"        
            
            response  = fix1
            body = ""
            for m in range(num):
                part1 = body1.replace('${name}', prix[m] + dynData['name']);
                part1 = part1.replace('${version}', dynData['version']);
                part1 = part1.replace('${release}', dynData['release']);
     
                part2 = body2.replace('${name}', prix[m] + dynData['name']);
                part2 = part2.replace('${version}', dynData['version']);
                part2 = part2.replace('${release}', dynData['release']);
                
                response =  response + part1
                body = body + part2
            response = response + fix2 + body + fix3   
            
        elif(request.count('RHEL-6-ComputeNode')>0):
            fix1 = "<?xml version='1.0'?><methodResponse><params><param><value><struct><member><name>optional</name><value><struct>"
            response = fix1
            for m in range(num):
                body1 = "<member><name>${name}-${version}-${release}</name><value><struct><member><name>x86_64</name><value><array><data><value><string>x86_64</string></value></data></array></value></member><member><name>src</name><value><array><data><value><string>x86_64</string></value></data></array></value></member><member><name>i686</name><value><array><data><value><string>x86_64</string></value></data></array></value></member></struct></value></member><member><name>${name}-data-${version}-${release}</name><value><struct><member><name>noarch</name><value><array><data><value><string>x86_64</string></value></data></array></value></member></struct></value></member><member><name>${name}-debuginfo-${version}-${release}</name><value><struct><member><name>x86_64</name><value><array><data><value><string>x86_64</string></value></data></array></value></member><member><name>i686</name><value><array><data><value><string>x86_64</string></value></data></array></value></member></struct></value></member><member><name>${name}-devel-${version}-${release}</name><value><struct><member><name>x86_64</name><value><array><data><value><string>x86_64</string></value></data></array></value></member><member><name>i686</name><value><array><data><value><string>x86_64</string></value></data></array></value></member></struct></value></member>"
                part1 = body1.replace('${name}', prix[m] + dynData['name']);
                part1 = part1.replace('${version}', dynData['version']);
                part1 = part1.replace('${release}', dynData['release']);
                response =  response + part1
            fix2= "</struct></value></member></struct></value></param></params></methodResponse>"
            response = response + fix2
        
        elif(request.count('RHEL-6-Workstation')>0):
            fix1  = "<?xml version=\"1.0\" encoding=\"utf-8\"?><methodResponse><params><param><value><struct><member><name>Workstation</name><value><struct>"    
            body1 = "<member><name>${name}-${version}-${release}</name><value><struct><member><name>x86_64</name><value><array><data><value><string>x86_64</string></value></data></array></value></member><member><name>src</name><value><array><data><value><string>x86_64</string></value><value><string>i386</string></value></data></array></value></member><member><name>i686</name><value><array><data><value><string>x86_64</string></value><value><string>i386</string></value></data></array></value></member></struct></value></member><member><name>${name}-data-${version}-${release}</name><value><struct><member><name>noarch</name><value><array><data><value><string>x86_64</string></value><value><string>i386</string></value></data></array></value></member></struct></value></member><member><name>${name}-debuginfo-${version}-${release}</name><value><struct><member><name>x86_64</name><value><array><data><value><string>x86_64</string></value></data></array></value></member><member><name>i686</name><value><array><data><value><string>x86_64</string></value><value><string>i386</string></value></data></array></value></member></struct></value></member>"
            fix2 = "</struct></value></member><member><name>optional</name><value><struct>"
            body2 = "<member><name>${name}-debuginfo-${version}-${release}</name><value><struct><member><name>x86_64</name><value><array><data><value><string>x86_64</string></value></data></array></value></member><member><name>i686</name><value><array><data><value><string>x86_64</string></value><value><string>i386</string></value></data></array></value></member></struct></value></member><member><name>${name}-devel-${version}-${release}</name><value><struct><member><name>x86_64</name><value><array><data><value><string>x86_64</string></value></data></array></value></member><member><name>i686</name><value><array><data><value><string>x86_64</string></value><value><string>i386</string></value></data></array></value></member></struct></value></member>"
            fix3="</struct></value></member></struct></value></param></params></methodResponse>"        
            
            response  = fix1
            body = ""
            for m in range(num):
                part1 = body1.replace('${name}', prix[m] + dynData['name']);
                part1 = part1.replace('${version}', dynData['version']);
                part1 = part1.replace('${release}', dynData['release']);
     
                part2 = body2.replace('${name}', prix[m] + dynData['name']);
                part2 = part2.replace('${version}', dynData['version']);
                part2 = part2.replace('${release}', dynData['release']);
                
                response =  response + part1
                body = body + part2
            response = response + fix2 + body + fix3

        elif(request.count('RHEL-6-Server')>0):
            fix1  = "<?xml version=\"1.0\" encoding=\"utf-8\"?><methodResponse><params><param><value><struct><member><name>optional</name><value><struct>"    
            body1 = "<member><name>${name}-${version}-${release}</name><value><struct><member><name>s390</name><value><array><data><value><string>s390x</string></value></data></array></value></member><member><name>s390x</name><value><array><data><value><string>s390x</string></value></data></array></value></member><member><name>src</name><value><array><data><value><string>x86_64</string></value><value><string>i386</string></value><value><string>ppc64</string></value><value><string>s390x</string></value></data></array></value></member></struct></value></member><member><name>${name}-data-${version}-${release}</name><value><struct><member><name>noarch</name><value><array><data><value><string>s390x</string></value></data></array></value></member></struct></value></member><member><name>${name}-debuginfo-${version}-${release}</name><value><struct><member><name>ppc</name><value><array><data><value><string>ppc64</string></value></data></array></value></member><member><name>x86_64</name><value><array><data><value><string>x86_64</string></value></data></array></value></member><member><name>s390</name><value><array><data><value><string>s390x</string></value></data></array></value></member><member><name>ppc64</name><value><array><data><value><string>ppc64</string></value></data></array></value></member><member><name>i686</name><value><array><data><value><string>x86_64</string></value><value><string>i386</string></value></data></array></value></member><member><name>s390x</name><value><array><data><value><string>s390x</string></value></data></array></value></member></struct></value></member><member><name>${name}-devel-${version}-${release}</name><value><struct><member><name>ppc</name><value><array><data><value><string>ppc64</string></value></data></array></value></member><member><name>x86_64</name><value><array><data><value><string>x86_64</string></value></data></array></value></member><member><name>s390</name><value><array><data><value><string>s390x</string></value></data></array></value></member><member><name>ppc64</name><value><array><data><value><string>ppc64</string></value></data></array></value></member><member><name>i686</name><value><array><data><value><string>x86_64</string></value><value><string>i386</string></value></data></array></value></member><member><name>s390x</name><value><array><data><value><string>s390x</string></value></data></array></value></member></struct></value></member>"
            fix2 = "</struct></value></member><member><name>Server</name><value><struct>"
            body2 = "<member><name>${name}-${version}-${release}</name><value><struct><member><name>ppc</name><value><array><data><value><string>ppc64</string></value></data></array></value></member><member><name>x86_64</name><value><array><data><value><string>x86_64</string></value></data></array></value></member><member><name>src</name><value><array><data><value><string>x86_64</string></value><value><string>i386</string></value><value><string>ppc64</string></value></data></array></value></member><member><name>ppc64</name><value><array><data><value><string>ppc64</string></value></data></array></value></member><member><name>i686</name><value><array><data><value><string>x86_64</string></value><value><string>i386</string></value></data></array></value></member></struct></value></member><member><name>${name}-data-${version}-${release}</name><value><struct><member><name>noarch</name><value><array><data><value><string>x86_64</string></value><value><string>i386</string></value><value><string>ppc64</string></value></data></array></value></member></struct></value></member><member><name>${name}-debuginfo-${version}-${release}</name><value><struct><member><name>ppc</name><value><array><data><value><string>ppc64</string></value></data></array></value></member><member><name>x86_64</name><value><array><data><value><string>x86_64</string></value></data></array></value></member><member><name>ppc64</name><value><array><data><value><string>ppc64</string></value></data></array></value></member><member><name>i686</name><value><array><data><value><string>x86_64</string></value><value><string>i386</string></value></data></array></value></member></struct></value></member>"
            fix3="</struct></value></member></struct></value></param></params></methodResponse>"        
            
            response  = fix1
            body = ""
            for m in range(num):
                part1 = body1.replace('${name}', prix[m] + dynData['name']);
                part1 = part1.replace('${version}', dynData['version']);
                part1 = part1.replace('${release}', dynData['release']);
     
                part2 = body2.replace('${name}', prix[m] + dynData['name']);
                part2 = part2.replace('${version}', dynData['version']);
                part2 = part2.replace('${release}', dynData['release']);
                
                response =  response + part1
                body = body + part2
            response = response + fix2 + body + fix3
            
        return response


    @staticmethod    
    def listBuildRPMs(request):
        global paramSettings
        print paramSettings
        if (paramSettings.has_key('build_type') and paramSettings.get('build_type').count('rpm')==0):
            return BrewHubMock.respondNone(request)       
 
        archs= ["s390x","s390x","s390x","i686","i686","i686","ppc64","ppc64","ppc64","x86_64","x86_64","x86_64","s390","s390","s390","ppc","noarch","ppc","ppc","src"]
        pckgs = ["libwacom-debuginfo","libwacom-devel","libwacom","libwacom-devel","libwacom","libwacom-debuginfo","libwacom-debuginfo","libwacom","libwacom-devel","libwacom-debuginfo","libwacom-devel","libwacom","libwacom-debuginfo","libwacom-devel","libwacom","libwacom-debuginfo","libwacom-data","libwacom","libwacom-devel","libwacom"]
        buildRoot = [1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,0,0]
        dataBlock = "<?xml version=\"1.0\" encoding=\"utf-8\"?><methodResponse><params><param><value><array><data>"
        
        prix = ['','aa', 'bb', 'cc','dd','ee','ff','gg'] 
        num = 1
        numstr = dynData['name'][1:2]
        if (numstr.isdigit()):
            num = int (numstr)

        for k in range(num * 20):
            
            global buildroot_id
            global nvr_id
            
            i = k % 20
            p = k / 20
            pckg = prix[p]+ pckgs[i]

            payloadhash = str(uuid.uuid1()).replace('-','')
            buildroot_id = buildroot_id + buildRoot[i]
            nvr_id = nvr_id +1

            dataBlock = "".join([dataBlock,"<value><struct><member><name>build_id</name><value><int>",str(dynData.get("id")),
                                 "</int></value></member><member><name>nvr</name><value><string>",pckg,"-",dynData['version'],"-",
                                 dynData['release'],"</string></value></member><member><name>buildroot_id</name><value><int>",str(buildroot_id),
                                 "</int></value></member><member><name>buildtime</name><value><int>1398348462</int></value></member><member><name>payloadhash</name><value><string>",
                                 payloadhash,"</string></value></member><member><name>epoch</name><value><nil/></value></member><member><name>version</name><value><string>",
                                 dynData.get("version"),"</string></value></member><member><name>external_repo_id</name><value><int>0</int></value></member><member><name>release</name><value><string>",
                                 dynData.get("release"),"</string></value></member><member><name>size</name><value><int>48700</int></value></member><member><name>arch</name><value><string>",
                                 archs[i],"</string></value></member><member><name>id</name><value><int>",str(nvr_id),
                                 "</int></value></member><member><name>external_repo_name</name><value><string>INTERNAL</string></value></member><member><name>name</name><value><string>",
                                 pckg,"</string></value></member></struct></value>"])       
        response = "".join([dataBlock,'</data></array></value></param></params></methodResponse>'])
        response = response.replace('libwacom', dynData['name']);
    
        return response

 
    @staticmethod      
    def listTags(request):
        #response = "<?xml version='1.0'?><methodResponse><params><param><value><array><data><value><struct><member><name>maven_support</name><value><boolean>1</boolean></value></member><member><name>locked</name><value><boolean>0</boolean></value></member><member><name>name</name><value><string>RHEL-6.6-pending</string></value></member><member><name>perm</name><value><string>trusted</string></value></member><member><name>id</name><value><int>5533</int></value></member><member><name>arches</name><value><nil/></value></member><member><name>maven_include_all</name><value><boolean>1</boolean></value></member><member><name>perm_id</name><value><int>6</int></value></member></struct></value><value><struct><member><name>maven_support</name><value><boolean>1</boolean></value></member><member><name>locked</name><value><boolean>0</boolean></value></member><member><name>name</name><value><string>RHEL-6.6-override</string></value></member><member><name>perm</name><value><string>trusted</string></value></member><member><name>id</name><value><int>5536</int></value></member><member><name>arches</name><value><nil/></value></member><member><name>maven_include_all</name><value><boolean>1</boolean></value></member><member><name>perm_id</name><value><int>6</int></value></member></struct></value><value><struct><member><name>maven_support</name><value><boolean>1</boolean></value></member><member><name>locked</name><value><boolean>0</boolean></value></member><member><name>name</name><value><string>RHEL-6.6-internal-compose-1.0-set</string></value></member><member><name>perm</name><value><nil/></value></member><member><name>id</name><value><int>6386</int></value></member><member><name>arches</name><value><nil/></value></member><member><name>maven_include_all</name><value><boolean>1</boolean></value></member><member><name>perm_id</name><value><nil/></value></member></struct></value><value><struct><member><name>maven_support</name><value><boolean>1</boolean></value></member><member><name>locked</name><value><boolean>0</boolean></value></member><member><name>name</name><value><string>RHEL-6.6-alpha-1.0-set</string></value></member><member><name>perm</name><value><nil/></value></member><member><name>id</name><value><int>6456</int></value></member><member><name>arches</name><value><nil/></value></member><member><name>maven_include_all</name><value><boolean>1</boolean></value></member><member><name>perm_id</name><value><nil/></value></member></struct></value><value><struct><member><name>maven_support</name><value><boolean>1</boolean></value></member><member><name>locked</name><value><boolean>0</boolean></value></member><member><name>name</name><value><string>RHEL-6.6-beta-1.0-set</string></value></member><member><name>perm</name><value><nil/></value></member><member><name>id</name><value><int>6572</int></value></member><member><name>arches</name><value><nil/></value></member><member><name>maven_include_all</name><value><boolean>1</boolean></value></member><member><name>perm_id</name><value><nil/></value></member></struct></value><value><struct><member><name>maven_support</name><value><boolean>1</boolean></value></member><member><name>locked</name><value><boolean>0</boolean></value></member><member><name>name</name><value><string>RHEL-6.6-snapshot-1.0-set</string></value></member><member><name>perm</name><value><nil/></value></member><member><name>id</name><value><int>6658</int></value></member><member><name>arches</name><value><nil/></value></member><member><name>maven_include_all</name><value><boolean>1</boolean></value></member><member><name>perm_id</name><value><nil/></value></member></struct></value><value><struct><member><name>maven_support</name><value><boolean>1</boolean></value></member><member><name>locked</name><value><boolean>0</boolean></value></member><member><name>name</name><value><string>RHEL-6.6-snapshot-2.0-set</string></value></member><member><name>perm</name><value><nil/></value></member><member><name>id</name><value><int>6671</int></value></member><member><name>arches</name><value><nil/></value></member><member><name>maven_include_all</name><value><boolean>1</boolean></value></member><member><name>perm_id</name><value><nil/></value></member></struct></value></data></array></value></param></params></methodResponse>"
                
        global paramSettings
        if (paramSettings.has_key('build_type') and paramSettings.get('build_type').count('rpm')==0):
           isMaven = "1"
        else:
           isMaven = "0" 

        response = "<?xml version='1.0' encoding='utf-8'?><methodResponse><params><param><value><array><data><value><struct><member><name>maven_support</name><value><boolean>${isMaven}</boolean></value></member><member><name>locked</name><value><boolean>0</boolean></value></member><member><name>name</name><value><string>RHEL-6.6-pending</string></value></member><member><name>perm</name><value><string>trusted</string></value></member><member><name>id</name><value><int>5533</int></value></member><member><name>arches</name><value><nil/></value></member><member><name>maven_include_all</name><value><boolean>${isMaven}</boolean></value></member><member><name>perm_id</name><value><int>6</int></value></member></struct></value><value><struct><member><name>maven_support</name><value><boolean>${isMaven}</boolean></value></member><member><name>locked</name><value><boolean>0</boolean></value></member><member><name>name</name><value><string>RHEL-6.6-override</string></value></member><member><name>perm</name><value><string>trusted</string></value></member><member><name>id</name><value><int>5536</int></value></member><member><name>arches</name><value><nil/></value></member><member><name>maven_include_all</name><value><boolean>${isMaven}</boolean></value></member><member><name>perm_id</name><value><int>6</int></value></member></struct></value><value><struct><member><name>maven_support</name><value><boolean>${isMaven}</boolean></value></member><member><name>locked</name><value><boolean>0</boolean></value></member><member><name>name</name><value><string>RHEL-6.6-internal-compose-1.0-set</string></value></member><member><name>perm</name><value><nil/></value></member><member><name>id</name><value><int>6386</int></value></member><member><name>arches</name><value><nil/></value></member><member><name>maven_include_all</name><value><boolean>${isMaven}</boolean></value></member><member><name>perm_id</name><value><nil/></value></member></struct></value><value><struct><member><name>maven_support</name><value><boolean>${isMaven}</boolean></value></member><member><name>locked</name><value><boolean>0</boolean></value></member><member><name>name</name><value><string>RHEL-6.6-alpha-1.0-set</string></value></member><member><name>perm</name><value><nil/></value></member><member><name>id</name><value><int>6456</int></value></member><member><name>arches</name><value><nil/></value></member><member><name>maven_include_all</name><value><boolean>${isMaven}</boolean></value></member><member><name>perm_id</name><value><nil/></value></member></struct></value><value><struct><member><name>maven_support</name><value><boolean>${isMaven}</boolean></value></member><member><name>locked</name><value><boolean>0</boolean></value></member><member><name>name</name><value><string>RHEL-6.6-beta-1.0-set</string></value></member><member><name>perm</name><value><nil/></value></member><member><name>id</name><value><int>6572</int></value></member><member><name>arches</name><value><nil/></value></member><member><name>maven_include_all</name><value><boolean>${isMaven}</boolean></value></member><member><name>perm_id</name><value><nil/></value></member></struct></value><value><struct><member><name>maven_support</name><value><boolean>${isMaven}</boolean></value></member><member><name>locked</name><value><boolean>0</boolean></value></member><member><name>name</name><value><string>RHEL-6.6-snapshot-1.0-set</string></value></member><member><name>perm</name><value><nil/></value></member><member><name>id</name><value><int>6658</int></value></member><member><name>arches</name><value><nil/></value></member><member><name>maven_include_all</name><value><boolean>${isMaven}</boolean></value></member><member><name>perm_id</name><value><nil/></value></member></struct></value><value><struct><member><name>maven_support</name><value><boolean>${isMaven}</boolean></value></member><member><name>locked</name><value><boolean>0</boolean></value></member><member><name>name</name><value><string>RHEL-6.6-snapshot-2.0-set</string></value></member><member><name>perm</name><value><nil/></value></member><member><name>id</name><value><int>6671</int></value></member><member><name>arches</name><value><nil/></value></member><member><name>maven_include_all</name><value><boolean>${isMaven}</boolean></value></member><member><name>perm_id</name><value><nil/></value></member></struct></value></data></array></value></param></params></methodResponse>"
        
        response = response.replace('${isMaven}', isMaven);

        return response    


    @staticmethod
    def listArchives(request):
        global paramSettings
        type = xmlrpclib.loads(request)[0][4]
        
        if(paramSettings==None):
            paramSettings=(({'build_type': 'maven'},),'setParams')

        if (paramSettings.has_key('build_type')):
            if (type.count('maven') >0 and paramSettings.get('build_type').count('maven')>0):            
                return BrewHubMock.listArchives_maven(request)
            elif (type.count('image') >0 and paramSettings.get('build_type').count('image')>0):
                return BrewHubMock.listArchives_image(request)
            elif (type.count('win') >0 and paramSettings.get('build_type').count('win')>0):
                return BrewHubMock.listArchives_win(request)
        
        return BrewHubMock.respondNone(request)

 
    # if type is NON-RPM packges, image
    @staticmethod
    def listArchives_image(request):
        
        archs= ["s390x","s390x","s390x","i686","i686","i686","ppc64","ppc64","ppc64","x86_64","x86_64","x86_64","s390","s390","s390","ppc","noarch","ppc","ppc","src"]
        pckgs = ["libwacom-debuginfo","libwacom-devel","libwacom","libwacom-devel","libwacom","libwacom-debuginfo","libwacom-debuginfo","libwacom","libwacom-devel","libwacom-debuginfo","libwacom-devel","libwacom","libwacom-debuginfo","libwacom-devel","libwacom","libwacom-debuginfo","libwacom-data","libwacom","libwacom-devel","libwacom"]
#        buildRoot = [1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,0,0]
        dataBlock = "<?xml version=\"1.0\" encoding=\"utf-8\"?><methodResponse><params><param><value><array><data>"

        prix = ['','aa', 'bb', 'cc','dd','ee','ff','gg']
        num = 1
        numstr = dynData['name'][1:2]
        if (numstr.isdigit()):
            num = int (numstr)
        for k in range(num * 20):

            global buildroot_id
            global nvr_id

            i = k % 20
            p = k / 20
            pckg = prix[p]+ pckgs[i]

            payloadhash = str(uuid.uuid1()).replace('-','')
#            buildroot_id = buildroot_id + buildRoot[i]
            nvr_id = nvr_id +1

            dataBlock = "".join([dataBlock,"<value><struct><member><name>build_id</name><value><int>",str(dynData.get("id")),
                                 "</int></value></member><member><name>type_description</name><value><string>XML file</string></value></member><member><name>type_id</name><value><int>5</int></value></member><member><name>checksum</name><value><string>",
                                 payloadhash,"</string></value></member><member><name>type_name</name><value><string>xml</string></value></member><member><name>filename</name><value><string>",
                                 pckg,"-",dynData['version'],"-",dynData['release'],"</string></value></member><member><name>arch</name><value><string>",
                                 archs[i],"</string></value></member><member><name>type_extensions</name><value><string>xml</string></value></member><member><name>checksum_type</name><value><int>0</int></value></member><member><name>buildroot_id</name><value><nil/></value></member><member><name>id</name><value><int>",
                                 str(nvr_id),"</int></value></member><member><name>size</name><value><int>641</int></value></member></struct></value>"])
        
        response = "".join([dataBlock,'</data></array></value></param></params></methodResponse>'])
        
        response = response.replace('libwacom', dynData['name']);

        return response 
    
    #if type is NON-RPM packges, maven
    @staticmethod
    def listArchives_maven(request):
        artifact_ids = ["jboss-eap-parent","com.jboss.eap","jboss-eap-parent","jboss-eap","jboss-eap",
                        "jboss-eap","jboss-eap","jboss-eap","jboss-eap-a","jboss-eap-b","jboss-eap-c","jboss-eap-d",
                        "jboss-eap-e","jboss-eap-f","jboss-eap-g","jboss-eap-h","jboss-eap-i","jboss-eap-j","jboss-eap-k","jboss-eap-build"]
        prexNames = ['-sources.zip','-patches.zip','.pom','-src.tar.gz','.tar.gz','.pom','.zip','.tar.gz','.tar.gz',
                     '.tar.gz','.tar.gz','.tar.gz','.tar.gz','.tar.gz','.tar.gz','.tar.gz','.tar.gz','.tar.gz','.tar.gz','.pom']

        buildRoot = [1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0]

        dataBlock = "<?xml version=\"1.0\" encoding=\"utf-8\"?><methodResponse><params><param><value><array><data>"

        prix = ['','aa', 'bb', 'cc','dd','ee','ff','gg']
        num = 1
        numstr = dynData['name'][1:2]
        if (numstr.isdigit()):
            num = int (numstr)
        for k in range(num * 20):

            global buildroot_id
            global nvr_id

            i = k % 20
            p = k / 20
            
            artifact_id = prix[p]+ artifact_ids[i]
            payloadhash = str(uuid.uuid1()).replace('-','')
            buildroot_id = buildroot_id + buildRoot[i]
            filename = ''.join([artifact_id,"-",dynData.get("version"),prexNames[i]])
            nvr_id = nvr_id +1

            dataBlock = "".join([dataBlock,"<value><struct><member><name>build_id</name><value><int>",
                                 str(dynData.get("id")),"</int></value></member><member><name>type_description</name><value><string>Jar file</string></value></member><member><name>artifact_id</name><value><string>",
                                 artifact_id,"</string></value></member><member><name>type_id</name><value><int>2</int></value></member><member><name>checksum</name><value><string>",
                                 payloadhash,"</string></value></member><member><name>type_name</name><value><string>zip</string></value></member><member><name>filename</name><value><string>",
                                 filename,"</string></value></member><member><name>version</name><value><string>",
                                 dynData.get("version"),"</string></value></member><member><name>type_extensions</name><value><string>zip</string></value></member><member><name>checksum_type</name><value><int>0</int></value></member><member><name>group_id</name><value><string>com.jboss.eap</string></value></member><member><name>buildroot_id</name><value><int>",
                                 str(buildroot_id),"</int></value></member><member><name>id</name><value><int>",str(nvr_id),"</int></value></member><member><name>size</name><value><int>89428632</int></value></member></struct></value>"])
        
        response = "".join([dataBlock,'</data></array></value></param></params></methodResponse>'])
        response = response.replace('com.jboss.eap', dynData['name']);

        return response

    
    #if type is NON-RPM packges, win
    @staticmethod
    def listArchives_win(request):
        return BrewHubMock.respondNone(request)
           

    #return nothing
    @staticmethod
    def respondNone(request):
        response = "<?xml version='1.0'?><methodResponse><params><param><value><array><data></data></array></value></param></params></methodResponse>"
        return response    

    
    #only for setting some parameters
    @staticmethod      
    def setParams(request):
        global paramSettings;
        requestRPC = xmlrpclib.loads(request)
        paramSettings = requestRPC[0][0]   
        return request


class BugzillaMock():
    global bugid, bugid_init # bugid
    global compid # component id which is related to bugid
    global flagid # flag id
    global component_id
    global component_id_id
    global release
    global product
    global releaseCompNum
    
    bugid = 1210000
    compid = 1
    flagid=2010000
    #bugid = 1220000
    #compid = 1000
    #flagid = 2010000 + 20000*4

    component_id=144320
    component_id_id = 810000
    release = "rhel-7.1.0"
    product = "Red Hat Enterprise Linux 7"
    bugid_init = bugid
    releaseCompNum = 1500
    
    @staticmethod
    def callMethod(requestData,methodName):
        methodName = methodName.replace('.','_')
        return getattr(BugzillaMock, methodName)(requestData) 
    
    @staticmethod
    def User_login(request):
        
        response = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><methodResponse><params><param><value><struct><member><name>id</name><value><int>241731</int></value></member><member><name>token</name><value><string>241731-Pqde868rmU</string></value></member></struct></value></param></params></methodResponse>"
        
        return response     
    
    @staticmethod
    def Bug_get1(request):
        global bugid # bugid
        global compid # component id which is related to bugid
        global flagid # flag id
        global component_id
        global component_id_id
        global release
        component= "testcomponent_" + str(compid + ((int)(bugid-1200000))/10)
        
        response = "<?xml version=\"1.0\" encoding=\"utf-8\"?><methodResponse><params><param><value><struct><member><name>faults</name><value><array><data/></array></value></member><member><name>bugs</name><value><array><data><value><struct><member><name>priority</name><value><string>low</string></value></member><member><name>status</name><value><string>MODIFIED</string></value></member><member><name>last_change_time</name><value><dateTime.iso8601>20140822T15:40:36</dateTime.iso8601></value></member><member><name>keywords</name><value><array><data/></array></value></member><member><name>cf_qa_whiteboard</name><value><string/></value></member><member><name>summary</name><value><string>bug_${component}_1408722027952</string></value></member><member><name>groups</name><value><array><data/></array></value></member><member><name>id</name><value><int>${bugid}</int></value></member><member><name>severity</name><value><string>low</string></value></member><member><name>flags</name><value><array><data><value><struct><member><name>modification_date</name><value><dateTime.iso8601>20140822T15:40:29</dateTime.iso8601></value></member><member><name>is_active</name><value><int>1</int></value></member><member><name>creation_date</name><value><dateTime.iso8601>20140822T15:40:29</dateTime.iso8601></value></member><member><name>status</name><value><string>+</string></value></member><member><name>type_id</name><value><int>245</int></value></member><member><name>name</name><value><string>${release}</string></value></member><member><name>id</name><value><int>"+ str(flagid) + "</int></value></member><member><name>setter</name><value><string>zxiong@redhat.com</string></value></member></struct></value><value><struct><member><name>modification_date</name><value><dateTime.iso8601>20140822T15:40:29</dateTime.iso8601></value></member><member><name>is_active</name><value><int>1</int></value></member><member><name>creation_date</name><value><dateTime.iso8601>20140822T15:40:29</dateTime.iso8601></value></member><member><name>status</name><value><string>+</string></value></member><member><name>type_id</name><value><int>11</int></value></member><member><name>name</name><value><string>pm_ack</string></value></member><member><name>id</name><value><int>"+str(flagid+1)+"</int></value></member><member><name>setter</name><value><string>zxiong@redhat.com</string></value></member></struct></value><value><struct><member><name>modification_date</name><value><dateTime.iso8601>20140822T15:40:29</dateTime.iso8601></value></member><member><name>is_active</name><value><int>1</int></value></member><member><name>creation_date</name><value><dateTime.iso8601>20140822T15:40:29</dateTime.iso8601></value></member><member><name>status</name><value><string>+</string></value></member><member><name>type_id</name><value><int>10</int></value></member><member><name>name</name><value><string>devel_ack</string></value></member><member><name>id</name><value><int>"+str(flagid+1)+"</int></value></member><member><name>setter</name><value><string>zxiong@redhat.com</string></value></member></struct></value><value><struct><member><name>modification_date</name><value><dateTime.iso8601>20140822T15:40:29</dateTime.iso8601></value></member><member><name>is_active</name><value><int>1</int></value></member><member><name>creation_date</name><value><dateTime.iso8601>20140822T15:40:29</dateTime.iso8601></value></member><member><name>status</name><value><string>+</string></value></member><member><name>type_id</name><value><int>9</int></value></member><member><name>name</name><value><string>qa_ack</string></value></member><member><name>id</name><value><int>"+str(flagid+1)+"</int></value></member><member><name>setter</name><value><string>zxiong@redhat.com</string></value></member></struct></value></data></array></value></member><member><name>cf_pm_score</name><value><string>0</string></value></member><member><name>component</name><value><array><data><value><string>${component}</string></value></data></array></value></member><member><name>classification</name><value><string>Red Hat</string></value></member><member><name>product</name><value><string>Red Hat Enterprise Linux 7</string></value></member><member><name>cf_release_notes</name><value><string/></value></member><member><name>cf_verified</name><value><array><data/></array></value></member><member><name>alias</name><value><array><data/></array></value></member></struct></value></data></array></value></member></struct></value></param></params></methodResponse>"
        
        response = response.replace('${bugid}', str(bugid));
        response = response.replace('${component}', component);
        response = response.replace('${release}', release);
        
        bugid = bugid +1
        flagid = flagid + 1
        
        return response
        

    @staticmethod
    def Bug_get2(request):
        prebody = "<?xml version=\"1.0\" encoding=\"utf-8\"?><methodResponse><params><param><value><struct><member><name>faults</name><value><array><data/></array></value></member><member><name>bugs</name><value><array><data>"
        body = ""
        endbody = "</data></array></value></member></struct></value></param></params></methodResponse>"
        
        for i in range(100):
            global bugid # bugid
            global compid # component id which is related to bugid
            global flagid # flag id
            global component_id
            global component_id_id
            global release
            
            part = "<value><struct><member><name>priority</name><value><string>low</string></value></member><member><name>status</name><value><string>NEW</string></value></member><member><name>last_change_time</name><value><dateTime.iso8601>20140822T15:40:36</dateTime.iso8601></value></member><member><name>keywords</name><value><array><data/></array></value></member><member><name>cf_qa_whiteboard</name><value><string/></value></member><member><name>summary</name><value><string>bug_${component}_1408722027952</string></value></member><member><name>groups</name><value><array><data/></array></value></member><member><name>id</name><value><int>${bugid}</int></value></member><member><name>severity</name><value><string>low</string></value></member><member><name>flags</name><value><array><data><value><struct><member><name>modification_date</name><value><dateTime.iso8601>20140822T15:40:29</dateTime.iso8601></value></member><member><name>is_active</name><value><int>1</int></value></member><member><name>creation_date</name><value><dateTime.iso8601>20140822T15:40:29</dateTime.iso8601></value></member><member><name>status</name><value><string>+</string></value></member><member><name>type_id</name><value><int>245</int></value></member><member><name>name</name><value><string>${release}</string></value></member><member><name>id</name><value><int>"+ str(flagid) + "</int></value></member><member><name>setter</name><value><string>zxiong@redhat.com</string></value></member></struct></value><value><struct><member><name>modification_date</name><value><dateTime.iso8601>20140822T15:40:29</dateTime.iso8601></value></member><member><name>is_active</name><value><int>1</int></value></member><member><name>creation_date</name><value><dateTime.iso8601>20140822T15:40:29</dateTime.iso8601></value></member><member><name>status</name><value><string>+</string></value></member><member><name>type_id</name><value><int>11</int></value></member><member><name>name</name><value><string>pm_ack</string></value></member><member><name>id</name><value><int>"+str(flagid+1)+"</int></value></member><member><name>setter</name><value><string>zxiong@redhat.com</string></value></member></struct></value><value><struct><member><name>modification_date</name><value><dateTime.iso8601>20140822T15:40:29</dateTime.iso8601></value></member><member><name>is_active</name><value><int>1</int></value></member><member><name>creation_date</name><value><dateTime.iso8601>20140822T15:40:29</dateTime.iso8601></value></member><member><name>status</name><value><string>+</string></value></member><member><name>type_id</name><value><int>10</int></value></member><member><name>name</name><value><string>devel_ack</string></value></member><member><name>id</name><value><int>"+str(flagid+1)+"</int></value></member><member><name>setter</name><value><string>zxiong@redhat.com</string></value></member></struct></value><value><struct><member><name>modification_date</name><value><dateTime.iso8601>20140822T15:40:29</dateTime.iso8601></value></member><member><name>is_active</name><value><int>1</int></value></member><member><name>creation_date</name><value><dateTime.iso8601>20140822T15:40:29</dateTime.iso8601></value></member><member><name>status</name><value><string>+</string></value></member><member><name>type_id</name><value><int>9</int></value></member><member><name>name</name><value><string>qa_ack</string></value></member><member><name>id</name><value><int>"+str(flagid+1)+"</int></value></member><member><name>setter</name><value><string>zxiong@redhat.com</string></value></member></struct></value></data></array></value></member><member><name>cf_pm_score</name><value><string>0</string></value></member><member><name>component</name><value><array><data><value><string>${component}</string></value></data></array></value></member><member><name>classification</name><value><string>Red Hat</string></value></member><member><name>product</name><value><string>Red Hat Enterprise Linux 7</string></value></member><member><name>cf_release_notes</name><value><string/></value></member><member><name>cf_verified</name><value><array><data/></array></value></member><member><name>alias</name><value><array><data/></array></value></member></struct></value>"
           
            component= "testcomponent_" + str(compid + ((int)(bugid-1210000))/10)
            
            body = body.replace('${bugid}', str(bugid));
            body = body.replace('${component}', component);
            body = body.replace('${release}', release);
            
            body = "".join([body, part])
        
            bugid = bugid +1
            flagid = flagid + 1
        
        response = prebody + body + endbody
        
        return response   

    #each component contain 20 bugs, 10 eligible and 10 ineligible bugs
    @staticmethod
    def Bug_get(request):
        prebody = "<?xml version=\"1.0\" encoding=\"utf-8\"?><methodResponse><params><param><value><struct><member><name>faults</name><value><array><data/></array></value></member><member><name>bugs</name><value><array><data>"
        body = ""
        endbody = "</data></array></value></member></struct></value></param></params></methodResponse>"
        
        for i in range(100):
            global bugid,bugid_init # bugid
            global compid # component id which is related to bugid
            global flagid # flag id
            global release
            
            #first 10 are eligible bugs and following 10 are ineligible bugs
            status = 'MODIFIED'
            if(i%20 >= 10):
                status = 'NEW'
            
            part = "<value><struct><member><name>priority</name><value><string>low</string></value></member><member><name>status</name><value><string>"+status+ "</string></value></member><member><name>last_change_time</name><value><dateTime.iso8601>20140822T15:40:36</dateTime.iso8601></value></member><member><name>keywords</name><value><array><data/></array></value></member><member><name>cf_qa_whiteboard</name><value><string/></value></member><member><name>summary</name><value><string>bug_${component}_1408722027952</string></value></member><member><name>groups</name><value><array><data/></array></value></member><member><name>id</name><value><int>${bugid}</int></value></member><member><name>severity</name><value><string>low</string></value></member><member><name>flags</name><value><array><data><value><struct><member><name>modification_date</name><value><dateTime.iso8601>20140822T15:40:29</dateTime.iso8601></value></member><member><name>is_active</name><value><int>1</int></value></member><member><name>creation_date</name><value><dateTime.iso8601>20140822T15:40:29</dateTime.iso8601></value></member><member><name>status</name><value><string>+</string></value></member><member><name>type_id</name><value><int>245</int></value></member><member><name>name</name><value><string>${release}</string></value></member><member><name>id</name><value><int>"+ str(flagid) + "</int></value></member><member><name>setter</name><value><string>zxiong@redhat.com</string></value></member></struct></value><value><struct><member><name>modification_date</name><value><dateTime.iso8601>20140822T15:40:29</dateTime.iso8601></value></member><member><name>is_active</name><value><int>1</int></value></member><member><name>creation_date</name><value><dateTime.iso8601>20140822T15:40:29</dateTime.iso8601></value></member><member><name>status</name><value><string>+</string></value></member><member><name>type_id</name><value><int>11</int></value></member><member><name>name</name><value><string>pm_ack</string></value></member><member><name>id</name><value><int>"+str(flagid+1)+"</int></value></member><member><name>setter</name><value><string>zxiong@redhat.com</string></value></member></struct></value><value><struct><member><name>modification_date</name><value><dateTime.iso8601>20140822T15:40:29</dateTime.iso8601></value></member><member><name>is_active</name><value><int>1</int></value></member><member><name>creation_date</name><value><dateTime.iso8601>20140822T15:40:29</dateTime.iso8601></value></member><member><name>status</name><value><string>+</string></value></member><member><name>type_id</name><value><int>10</int></value></member><member><name>name</name><value><string>devel_ack</string></value></member><member><name>id</name><value><int>"+str(flagid+1)+"</int></value></member><member><name>setter</name><value><string>zxiong@redhat.com</string></value></member></struct></value><value><struct><member><name>modification_date</name><value><dateTime.iso8601>20140822T15:40:29</dateTime.iso8601></value></member><member><name>is_active</name><value><int>1</int></value></member><member><name>creation_date</name><value><dateTime.iso8601>20140822T15:40:29</dateTime.iso8601></value></member><member><name>status</name><value><string>+</string></value></member><member><name>type_id</name><value><int>9</int></value></member><member><name>name</name><value><string>qa_ack</string></value></member><member><name>id</name><value><int>"+str(flagid+1)+"</int></value></member><member><name>setter</name><value><string>zxiong@redhat.com</string></value></member></struct></value></data></array></value></member><member><name>cf_pm_score</name><value><string>0</string></value></member><member><name>component</name><value><array><data><value><string>${component}</string></value></data></array></value></member><member><name>classification</name><value><string>Red Hat</string></value></member><member><name>product</name><value><string>Red Hat Enterprise Linux 7</string></value></member><member><name>cf_release_notes</name><value><string/></value></member><member><name>cf_verified</name><value><array><data/></array></value></member><member><name>alias</name><value><array><data/></array></value></member></struct></value>"
           
            component= "testcomponent_" + str(compid + ((int)(bugid-bugid_init))/20)
            
            body = body.replace('${bugid}', str(bugid));
            body = body.replace('${component}', component);
            body = body.replace('${release}', release);
            
            body = "".join([body, part])
        
            bugid = bugid +1
            flagid = flagid + 1
        
        response = prebody + body + endbody
        
        return response


    #syn with errata tool, this is only changes rhel7.1.0 ACL
    @staticmethod
    def Releases_getReleaseComponents(request):      
        global releaseCompNum

        releaseCompNum = releaseCompNum + 500
        compid = 1
        component_id = 144320
        component_id_id = 810000

	prebody_all = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><methodResponse><params><param><value><struct>"
        endbody_all = "</struct></value></param></params></methodResponse>"
        print releaseCompNum
        body = ""
        for k in range(releaseCompNum):
            #global compid,component_id,component_id_id
            component= "testcomponent_" + str(compid) 
            part1 = "".join(["<value><struct><member><name>initialowner</name><value><string>zxiong@redhat.com</string></value></member><member><name>name</name><value><string>",component,"</string></value></member><member><name>type</name><value><string>approved</string></value></member><member><name>product</name><value><string>Red Hat Enterprise Linux 7</string></value></member><member><name>component_id</name><value><int>",str(component_id),"</int></value></member><member><name>id</name><value><int>",str(component_id_id),"</int></value></member><member><name>initialqacontact</name><value><string>zxiong@redhat.com</string></value></member></struct></value>"])
        
            component_id = component_id + 1
            component_id_id = component_id_id + 1     
            compid = compid +1
            
            body = "".join([body,part1])

        prebody1 = "<member><name>nack</name><value><array><data>"
        prebody2 = "<member><name>approved</name><value><array><data>"
        prebody3 = "<member><name>ack</name><value><array><data>"
        endbody = "</data></array></value></member>"
        allbody = prebody1 + body +endbody + prebody2 + body +endbody +prebody3 + body +endbody + "<member><name>capacity</name><value><array><data/></array></value></member>"
        response = prebody_all + allbody + endbody_all

        return response

    @staticmethod
    def resetReleaseComponentNum(request): 
        global releaseCompNum
        requestRPC = xmlrpclib.loads(request)
        releaseCompNum = int(requestRPC[0][0])
        return "The number of Components: " + str(releaseCompNum)
