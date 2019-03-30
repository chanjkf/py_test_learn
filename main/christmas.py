import requests
import time
import records
import json


class Christmas:

    hosts = "http://hcoin.btb-inc.com"
    login_url = "/api/user/v3/users/login/free-pwd-login"

    users = records.Database('mysql+pymysql://root:btb@192.168.10.6:3306/newex_out_users?charset=utf8')
    account = records.Database('mysql+pymysql://root:btb@192.168.10.6:3306/btb_account?charset=utf8')

    def make_random_phone(self, count):
        print("随机生成手机号中。。。")
        phones = []
        for a in range(count):
            time.sleep(1/1000)
            phones.append("132" + str(round(time.time() * 1000))[5:])
        print("手机号生成完毕。。。。")
        return phones

    def get_token(self, phone):
        param = {"loginName": phone,
                 "areaCode": 86,
                 "validateCode": "888888"}
        response = requests.post(self.hosts + self.login_url, json=param).json()
        return response["data"]["token"]

    def init_user_asset(self, token):
        url = self.hosts + '/api/spot/v2/spot/accounts/user-all-currency-asset?'
        headers = {
            'Authorization': token
        }
        result = requests.get(url, headers=headers).json()
        if result["code"] != 0:
            print("请求失败")

    def get_uid_by_phone(self, phones):
        user_info_list = []
        query = self.users.query("select id, phone from user_info where phone in(%s)" % str(phones)[1:-1])
        for i in query.dataset._data:
            user_info = {}
            user_info["uid"] = i[0]
            user_info["phone"] = int(i[1])
            user_info_list.append(user_info)
        return user_info_list

#[{"uid":1, "phone":2, "token":"12313"},{"uid":1, "phone":2, "token":"12313"},{"uid":1, "phone":2, "token":"12313"}]
    def test_christmas(self, info):

        url = self.hosts + "/api/activity/christmas/join"
        for i in info:
            headers = {
                'Authorization': i["token"]
            }
            a = 10
            a = a + 10
            available_before = self.account.query("SELECT available from account_balance WHERE user_id =%s and currency_id = 64" % i["uid"])
            available_before = available_before.dataset._data[0][0]
            print("该用户持仓数量：" + str(available_before))
            account = records.Database('mysql+pymysql://root:btb@192.168.10.6:3306/btb_account?charset=utf8')
            reward_pool = account.query("SELECT available from account_balance WHERE account_no = 'ACN00527601385577701445323' and currency_id = 64")
            reward_pool = reward_pool.dataset._data[0][0]
            print("奖池余额：" + str(reward_pool))
            result = requests.post(url, headers=headers)
            result = json.loads(result.text)
            if result["code"] == 0 and result["data"] != "":
                account = records.Database('mysql+pymysql://root:btb@192.168.10.6:3306/btb_account?charset=utf8')
                available_after = account.query("SELECT available from account_balance WHERE user_id =%s and currency_id = 64" % i["uid"])
                available_after = available_after.dataset._data[0][0]
                print("用户id：" + str(i["uid"]))
                print("用户助力后余额：" + str(available_after))
                if available_after - available_before != 3:
                    print("测试失败")
                else:
                    print("测试成功")
            elif result["code"] == 502:
                if available_before < 10000:
                    print("测试通过，用户持仓不足10000")
                elif reward_pool < 3:
                    print("测试成功，帐户余额不足")
                elif reward_pool > 3:
                    print("测试失败")

            elif result["code"] == 0 and result["data"] == "":
                print("测试通过， 再次点击")
            else:
                print("请求失败")

    def test_no_available(self):
        christmas = Christmas()
        phones = christmas.make_random_phone(10)
        user_info_list = []
        for i in phones:
            user_info = {}
            print("生成token中。。。。")
            token = christmas.get_token(i)
            christmas.init_user_asset(token)
            user_info["phone"] = int(i)
            user_info["token"] = token
            user_info_list.append(user_info)
        uid_phone = christmas.get_uid_by_phone(phones)
        print("token 生成完毕。。。。")
        for i in user_info_list:
            for n in uid_phone:
                if i["phone"] == n["phone"]:
                    i["uid"] = n["uid"]
        christmas.test_christmas(user_info_list)

    def charge_uid(self, uid):
        self.account.query("update account_balance set available = available + 10001 where user_id in(%s)" % str(uid)[1:-1])

    def test_has_available(self):
        christmas = Christmas()
        phones = self.make_random_phone(10)
        user_info_list = []

        for i in phones:
            user_info = {}
            print("生成token中。。。。")
            token = self.get_token(i)
            christmas.init_user_asset(token)
            user_info["phone"] = int(i)
            user_info["token"] = token
            user_info_list.append(user_info)
# [{"uid":1, "phone":2}, {"uid":5, "phone":2}]
        uid_phone = self.get_uid_by_phone(phones)

        print("token 生成完毕。。。。")
        uid = []
        for a in uid_phone:
            uid.append(a["uid"])

        for i in user_info_list:
            for n in uid_phone:
                if i["phone"] == n["phone"]:
                    i["uid"] = n["uid"]

        christmas.charge_uid(uid)
        christmas.test_christmas(user_info_list)
        print("------本次测试完成-------")


if __name__ == '__main__':
    christmas = Christmas()
    phone = christmas.make_random_phone(100)
    #
    for i in phone:
        #
        user_info = {}
        token = christmas.get_token(i)
        user_info["phone"] = i
        user_info["token"] = token



