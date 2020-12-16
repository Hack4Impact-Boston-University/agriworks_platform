from flask import Blueprint, request
from Response import Response
from Services.UploadService import UploadService
from Services.MailService import MailService 
from Services.AuthenticationService import AuthenticationService
import datetime
from flask_restplus import Api, Resource, Namespace


UploadService = UploadService()
MailService = MailService()
AuthenticationService = AuthenticationService()
upload_ns = Namespace('upload', 'dataset methods')

@upload_ns.route('/') 
class UploadNewFile(Resource):
    @upload_ns.doc(
        responses={
            400: "No session detected", 
            400: "Prohibited file type",
            400: "Empty fields detected. Please remove empty values from your dataset and try again.", 
            400: "Error Creating Datset",
            503: "Error Sending Email",
        },
        params={
            'SID': {'in': 'cookies', 'required': True},
        }
    )   
    def post(self):
        try:

            uploadRequestDate = str(datetime.datetime.now()).split(".")[0]
            if ("SID" not in request.cookies):
                return Response("No session detected", status=400)
            if ('file' not in request.files):
                return Response("No file detected", status=400)
            if (not UploadService.allowed_file(request.files["file"].filename)):
                return Response("Prohibited file type", status=400) #TODO: Append to response: Dynamically return the types of allowed files
            
            dataset, error = UploadService.createDataset(request, uploadRequestDate)

            if (dataset and error != "Mail"):
                return Response(str(dataset.id), status=200)
            else:
                if(error == "Mail"):
                    return Response({"message": "Error Sending Email", "dataset":str(dataset.id), "status": 503})
                elif(error == "User"):
                    return Response("Invalid Session ID", status=403)
                else:
                    return Response("Error Creating Dataset", status=400)

            
        except ValueError:
            return Response("Empty fields detected. Please remove empty values from your dataset and try again.", status=400) 


@upload_ns.route("/getTags/<datasetType>") 
class GetTags(Resource): 
    def get(self, datasetType):
        try:
            return Response(UploadService.getTags(datasetType))
        except:
            return Response("Unable to get tags")
