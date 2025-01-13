import json
import urllib3
import warnings

def getTokenUserID(key:str, account:str, password:str, logintype:str, accesskey=''):
    header = {'sys_code':'901','Content-Type':'application/json;charset=UTF-8'}
    if accesskey != '':
        header['x-access-key'] = accesskey
    params = json.dumps({'appkey':key, 'user_account':account, 'user_password':password, 'lang': '_en_US' })
    data = json.loads(urllib3.PoolManager().request('POST','https://gateway.isolarcloud.com.hk/openapi/login',body=params,headers=header).data.decode('utf-8'))
    token = data.get('result_data').get('token')
    user_id = data.get('result_data').get('user_id')
    return token, user_id

def getData(key:str, token:str, starttime:str, endtime:str, interval:str, pointlist:list, devicelist:list, accesskey=''):
    header = {'sys_code':'901','Content-Type':'application/json;charset=UTF-8'}
    if accesskey != '':
        header['x-access-key'] = accesskey
    point = ','.join([str(item) for item in pointlist])
    field = json.dumps({'appkey':key, 'token':token, 'start_time_stamp':starttime, 'end_time_stamp':endtime, 'minute_interval':interval, 'points':point, 'ps_key_list':devicelist})
    data = json.loads(urllib3.PoolManager().request('POST','https://gateway.isolarcloud.com.hk/openapi/getDevicePointMinuteDataList',body=field, headers=header).data.decode('utf-8'))
    if data.get('result_data') == None:
        warnings.warn(str(data.get('result_msg')))
        return []
    else:
        reading = data.get('result_data')
        return reading
    
