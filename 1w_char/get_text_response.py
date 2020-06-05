from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.ocr.v20181119 import ocr_client, models
import base64
import json


with open("1w_char/tencent.key",'r') as fd:
    s_id = fd.readline()[:-1]
    s_pw = fd.readline()


def requset_tc(base64_data):
    try:

        cred = credential.Credential(s_id, s_pw)
        httpProfile = HttpProfile()
        httpProfile.endpoint = "ocr.tencentcloudapi.com"

        clientProfile = ClientProfile("TC3-HMAC-SHA256")
        clientProfile.httpProfile = httpProfile
        client = ocr_client.OcrClient(cred, "ap-guangzhou", clientProfile)

        req = models.GeneralHandwritingOCRRequest()
        # print(str(base64_data,'utf-8'))
        params = "{\"ImageBase64\":\"" + str(base64_data,'utf-8') + "\"}"
        # params = '{\"ImageUrl\":\"http://121.199.60.137:8888/1.jpg\"}'
        req.from_json_string(params)

        resp = client.GeneralHandwritingOCR(req)
        return json.loads(resp.to_json_string())

    except TencentCloudSDKException as err:
        print(err)
        return str(err)


data = []

for i in range(1,274):
    with open("imgs/{}.jpg".format(i), "rb") as f:
        base64_data = base64.b64encode(f.read())
    data.append(requset_tc(base64_data))
    print("imgs/{}.jpg Finish".format(i))

with open("1w_char/tc_api_data/10w_API_response.json", 'w') as fd:
    fd.write(json.dumps(data))
