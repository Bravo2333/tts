# app/api/routes.py
import json
from flask import Blueprint, jsonify, request
from app.service.Masterservice import  Masterservice
from app.service.Videoservice import Videoservice
from app.service.Diagramservice import Diagramservice

api_blueprint = Blueprint('api', __name__)
@api_blueprint.route('/masterinit', methods=['POST'])
def masterinit():
    parameters = request.json
    ownerlink = parameters['ownerlink']
    ms= Masterservice()
    vs = Videoservice()
    print(type(ownerlink))
    if type(ownerlink)==list:
        for i in ownerlink:
            ms.masterinit(i)
        print('批量导入达人元数据成功')
        for i in ownerlink:
            vs.videoinit(i)
        print('批量导入视频元数据成功')
        return '0'
    vs.videoinit(ownerlink)
    ms.masterinit(ownerlink)

    return '0'
@api_blueprint.route('/masterlist', methods=['POST'])
def masterlist():
    parameters = request.json
    ownerlink = parameters['ownerlink']
    dg = Diagramservice()
    return jsonify(dg.get_master_list())
@api_blueprint.route('/masterdetial', methods=['POST'])
def masterdetial():
    parameters = request.json
    ownerlink = parameters['ownerlink']+'\n'
    print(ownerlink)
    dg = Diagramservice()
    result = dg.get_master_videolist(ownerlink)
    result= jsonify(result)
    return result
@api_blueprint.route('/masterbaseinfo', methods=['POST'])
def getmasterbaseinfo():
    parameters = request.json
    ownerlink = parameters['ownerlink'] + '\n'
    dg = Diagramservice()
    result = dg.get_master_totalinfo(ownerlink)
    return result
@api_blueprint.route('/masterrankinfo', methods=['POST'])
def getmasterrankinfo():
    parameters = request.json
    ownerlink = parameters['ownerlink'] + '\n'
    dg = Diagramservice()
    result = dg.get_Masterrankinfo()
    return result
@api_blueprint.route('/videorankinfo', methods=['POST'])
def getvideorankinfo():
    parameters = request.json
    ownerlink = parameters['ownerlink'] + '\n'
    dg = Diagramservice()
    result = dg.get_video_rank()
    return result
@api_blueprint.route('/videobaseinfo', methods=['POST'])
def getvideobaseinfo():
    parameters = request.json
    ownerlink = parameters['ownerlink'] + '\n'
    dg = Diagramservice()
    result = dg.get_video_base_info()
    return result
