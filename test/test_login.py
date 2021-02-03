from django.test import TestCase
import requests

url = "http://127.0.0.1:8000"

#
# class AnimalTestCase(TestCase):
#     def setUp(self):
#         pass
#
#     def test_login_failed(self):
#         """Animals that can speak are correctly identified"""
#         rep = requests.post(url + "/api/v1/account/user/login/", json={"username": 1, "is_ldap": 1, "password": 123})
#
#         self.assertEqual(rep.status_code, 200)
#         self.assertEqual(rep.json(), 'The cat says "meow"')

rep = requests.post(url + "/api/v1/account/user/login/", json={"username": "test", "is_ldap": 1, "password": "123"})
print(rep.status_code, rep.json())

rep = requests.post(url + "/api/v1/account/user/login/",
                    json={"username": "admin", "is_ldap": False, "password": "123456"})
print(rep.status_code, rep.json())

# rep = requests.post(url + "/api/v1/account/user/login/",
#                     json={"username": "buxingxing", "is_ldap": False, "password": "123456"})
# print(rep.status_code, rep.json())
token = rep.json().get('data').get('token')
rep = requests.get(url + "/api/v1/account/user/current/", params={'token': token}, headers={'token': token})
print(rep.status_code, rep.json())
