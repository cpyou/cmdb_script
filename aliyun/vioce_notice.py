
from aliyunsdkdyvmsapi.request.v20170525 import SingleCallByTtsRequest
# from aliyunsdkdyvmsapi.request.v20170525 import SingleCallByVoiceRequest
from aliyunsdkcore.profile import region_provider
from aliyunsdkcore.client import AcsClient
import uuid
"""
语音业务调用接口示例，版本号：v20170525
Created on 2017-06-12
"""
# 初始化AcsClient
access_key_id = ''
access_key_secret = ''
# region_id = config.region_id
region_id = 'cn-beijing'

acs_client = AcsClient(access_key_id, access_key_secret, region_id)
region_provider.add_endpoint("Dyvmsapi", "cn-beijing", "dyvmsapi.aliyuncs.com")


def tts_call(business_id, called_number, called_show_number, tts_code, tts_param=None):
    ttsRequest = SingleCallByTtsRequest.SingleCallByTtsRequest()
    # 申请的语音通知tts模板编码,必填
    ttsRequest.set_TtsCode(tts_code)
    # 设置业务请求流水号，必填。后端服务基于此标识区分是否重复请求的判断
    ttsRequest.set_OutId(business_id)
    # 语音通知的被叫号码，必填。
    ttsRequest.set_CalledNumber(called_number)
    # 语音通知显示号码，必填。
    ttsRequest.set_CalledShowNumber(called_show_number)
    # tts模板变量参数
    if tts_param is not None:
        ttsRequest.set_TtsParam(tts_param)
    ttsResponse = acs_client.do_action_with_exception(ttsRequest)
    return ttsResponse


# 模板中不存在变量的情况下为{}
params = {
    'msg': '测试kube-controller-manager 172.16.63.211:10252 宕机'
}
# times = 5
# for i in range(times):
#     __business_id = uuid.uuid1()
#     print(__business_id)
#     print(tts_call(__business_id, "18616312713", "073182705980", "TTS_148865200", params))
__business_id = uuid.uuid1()
print(tts_call(__business_id, "18616312713", "02160556070", "TTS_148865200", params))
# print(tts_call(__business_id, "17621421476", "073182705980", "TTS_148865200", params))
# print(tts_call(__business_id, "18501700165", "073182705980", "TTS_148865200", params))
# print(tts_call(__business_id, "15618395683", "073182705980", "TTS_148865200", params))
