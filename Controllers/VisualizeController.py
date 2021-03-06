from Services.VisualizeService import VisualizeService
from flask import request
from Services.AuthenticationService import AuthenticationService
import requests
from Response import Response
import json

from flask_restplus import Api, Resource, fields, Namespace

VisualizeService = VisualizeService()
visualize_ns = Namespace('visualize', 'visualize methods')

@visualize_ns.route("/getFormattedData")
class GetFormattedData(Resource):
    @visualize_ns.doc(
        responses={
            200: "Success",
            400: "Failed to generate dataset for visualization"
        },
        params={
            'dataset': {'in': 'formData', 'required': True},
            'xAxis': {'in': 'formData', 'required': True},
            'yAxis': {'in': 'formData', 'required': True},
        }
    )
    def post(self):
        dataset = json.loads(request.form['dataset'])
        xAxis = request.form['xAxis']
        yAxis = request.form['yAxis']
        try:
            datacollection = VisualizeService.getFormattedData(dataset, xAxis, yAxis) 
        except:
            return Response("Failed to generate dataset for visualization",status=400)
        return Response({"datacollection": datacollection}, status=200)
