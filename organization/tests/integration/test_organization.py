from rest_framework.test import APIClient

from organization.models import Organization
from organization.tests import base_test


class OrganizationTestCreateCase(base_test.NewUserTestCase):
    """
    Organization Create API Test Case
    """

    def setUp(self) -> None:
        super().setUp()
        self.client = APIClient()
        self.login_response = self.client.post('/api/v1/user/login/',
                                               {'username': self.username,
                                                'password': self.password},
                                               format='json')

        self.access_token = self.login_response.json()['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

    def test_organization_create_api(self):
        self.create_organization = self.client.post('/api/v1/organization/',
                                                    {
                                                        'name': 'Robert Bosch',
                                                        'established_on': '1886-11-15',
                                                        'registration_code': '123456'
                                                    }, format='json')
        self.assertEquals(self.create_organization.status_code, 201)
        self.assertTrue('Robert Bosch' in self.create_organization.json()['data']['name'])
        self.assertTrue('1886-11-15' in self.create_organization.json()['data']['established_on'])
        self.assertTrue('123456' in self.create_organization.json()['data']['registration_code'])

    def tearDown(self) -> None:
        self.client.logout()
        Organization.objects.filter().delete()
        super().tearDown()


class OrganizationTestListingCase(base_test.NewUserTestCase):
    """
    Organization List API Test Case
    """

    def setUp(self) -> None:
        super().setUp()
        self.client = APIClient()
        self.login_response = self.client.post('/api/v1/user/login/',
                                               {'username': self.username,
                                                'password': self.password},
                                               format='json')

        self.access_token = self.login_response.json()['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        # Create a new Organization
        self.organization = Organization.objects.create(name='Robert Bosch GmbH',
                                                        established_on='1886-11-15',
                                                        registration_code='112211')

    def test_organization_listing_api(self):
        self.list_organizations = self.client.get('/api/v1/organization/', format='json')
        self.assertEquals(self.list_organizations.status_code, 200)
        self.assertTrue('Robert Bosch GmbH' in self.list_organizations.json()['results'][0]['name'])

    def tearDown(self) -> None:
        self.client.logout()
        Organization.objects.filter().delete()
        super().tearDown()


class OrganizationTestReadByIdCase(base_test.NewUserTestCase):
    """
    Organization Read API by Id Test Case
    """
    def setUp(self):
        super().setUp()
        self.client = APIClient()
        self.login_response = self.client.post('/api/v1/user/login/',
                                               {'username': self.username, 'password': self.password},
                                               format='json')

        self.access_token = self.login_response.json()['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        # Create Organization
        self.organization = Organization.objects.create(name='Robert Bosch GmbH',
                                                        established_on='1886-11-15',
                                                        registration_code='555111')

    def test_organization_read_by_id_api(self):
        self.read_organization_by_id = self.client.get(f'/api/v1/organization/{self.organization.id}', format='json')

        self.assertEquals(self.read_organization_by_id.status_code, 200)
        self.assertTrue('Robert Bosch' in self.read_organization_by_id.json()['name'])
        self.assertTrue('1886-11-15' in self.read_organization_by_id.json()['established_on'])
        self.assertTrue('555111' in self.read_organization_by_id.json()['registration_code'])

    def tearDown(self):
        self.client.logout()
        self.organization.delete()
        super().tearDown()


class OrganizationTestUpdateByIdCase(base_test.NewUserTestCase):
    """
    Organization Update API By Id Test Case
    """

    def setUp(self):
        super().setUp()
        self.client = APIClient()
        self.login_response = self.client.post('/api/v1/user/login/',
                                               {'username': self.username, 'password': self.password},
                                               format='json')

        self.access_token = self.login_response.json()['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        # Create Organization
        self.organization = Organization.objects.create(name='Robert Bosch GmbH',
                                                        established_on='1886-11-15',
                                                        registration_code='855111')

    def test_organization_update_by_id_api(self):
        self.update_organization_by_id = self.client.put(f'/api/v1/organization/{self.organization.id}',
                                                         {
                                                             'name': 'ROBERT BOSCH',
                                                             'established_on': '1886-11-14',
                                                             'registration_code': 'BOSCH112233'
                                                         }, format='json')

        self.assertEquals(self.update_organization_by_id.status_code, 200)
        self.assertTrue(self.update_organization_by_id.json()['status'], True)
        self.assertEquals(self.update_organization_by_id.json()['message'], 'Organization Updated !')
        self.assertEquals(self.update_organization_by_id.json()['data']['name'], 'ROBERT BOSCH')
        self.assertEquals(self.update_organization_by_id.json()['data']['registration_code'], 'BOSCH112233')
        self.assertEquals(self.update_organization_by_id.json()['data']['established_on'], '1886-11-14')

    def tearDown(self):
        self.client.logout()
        self.organization.delete()
        super().tearDown()


class OrganizationTestDeleteByIdCase(base_test.NewUserTestCase):
    def setUp(self):
        super().setUp()
        self.client = APIClient()
        self.login_response = self.client.post('/api/v1/user/login/',
                                               {'username': self.username, 'password': self.password},
                                               format='json')

        self.access_token = self.login_response.json()['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        # Create Organization
        self.organization = Organization.objects.create(name='Robert Bosch GmbH',
                                                        established_on='1886-11-15',
                                                        registration_code='777111')

    def test_organization_delete_by_id_api(self):
        self.delete_organization_by_id = self.client.delete(f'/api/v1/organization/{self.organization.id}',
                                                            format='json')

        self.assertEquals(self.delete_organization_by_id.status_code, 204)

    def tearDown(self):
        self.client.logout()
        super().tearDown()
