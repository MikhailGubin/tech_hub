from datetime import date
from rest_framework_simplejwt.tokens import AccessToken


from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

from electronics.models import Contact, Product, NetworkNode
from users.models import User


class ContactTestCase(APITestCase):
    """ Тесты API для модели 'Contact' """

    def setUp(self):
        """Создает базовый набор параметров для тестов для модели "Контакт" """

        # Создание Пользователя
        self.user = User.objects.create(
            email="admin1@example.com",
            name="Александр",
            surname="Александров",
            patronymic="Александрович",
            password="12345",
            position="team_leader",
        )
        self.user.save()
        # Авторизуем пользователя
        self.client.force_authenticate(user=self.user)

        # Создание тестового контакта
        self.valid_contact = Contact.objects.create(
            email="test@example.com",
            country="Россия",
            city="Москва",
            street="Тверская",
            house_number="10А"
        )
        self.contact_data = {
            "email": "test2@example.com",
            "country": "Россия",
            "city": "Ростов",
            "street": "Тверская",
            "house_number": "12А",
        }

    def test_contact_retrieve(self):
        """Проверяет процесс просмотра одного объекта класса "Контакт" """

        url = reverse('electronics:contact-detail', args=[self.valid_contact.pk])

        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("email"), self.valid_contact.email)
        self.assertEqual(data.get("house_number"), self.valid_contact.house_number)

    def test_contact_create(self):
        """Проверяет процесс создания одного объекта класса "Контакт" """
        url = reverse("electronics:contact-list")
        response = self.client.post(url, self.contact_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Contact.objects.all().count(), 2)

        created_contact = Contact.objects.get(email=self.contact_data["email"])
        self.assertEqual(created_contact.city, self.contact_data["city"])
        self.assertEqual(created_contact.house_number, self.contact_data["house_number"])

    def test_list_contacts(self):
        """Проверяет получение списка контактов."""
        # Создаю ещё один контакт
        url = reverse("electronics:contact-list")
        self.client.post(url, self.contact_data, format="json")

        url = reverse("electronics:contact-list")
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data["results"]), 2)

    def test_delete_contact_success(self):
        """Проверяет процесс удаления одного объекта класса "Контакт"."""

        url = reverse("electronics:contact-detail", kwargs={"pk": self.valid_contact.pk})

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Проверяем, что контакт действительно удален из базы данных
        self.assertFalse(Contact.objects.filter(id=self.valid_contact.pk).exists())

    def test_contact_error_no_city(self):
        """Проверяет, что нельзя создать контакт с улицей и домом без указания города """
        self.contact_data['city'] = ''
        url = reverse("electronics:contact-list")
        response = self.client.post(url, self.contact_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('city', response.data)
        self.assertEqual(
            response.data['city'][0],
            'Если указан номер дома, необходимо указать и город.'
        )

    def test_contact_authentication_error(self):
        """Проверяем сообщение об ошибке аутентификации """
        self.client.force_authenticate(user=None)
        url = reverse("electronics:contact-list")
        response = self.client.post(url, self.contact_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], "Authentication credentials were not provided.")


class ProductTestCase(APITestCase):
    """ Тесты API для модели 'Product' """

    def setUp(self):
        """Создает базовый набор параметров для тестов для модели "Продукт" """
        # Создание Пользователя
        self.user = User.objects.create(
            email="admin1@example.com",
            name="Александр",
            surname="Александров",
            patronymic="Александрович",
            password="12345",
            position="team_leader",
        )
        self.user.save()
        # Авторизуем пользователя
        self.client.force_authenticate(user=self.user)

        # Создание тестового продукта
        self.valid_product = Product.objects.create(
            name="Телефон",
            model="Iphone 5",
            release_date=date(2025, 1, 1)
        )
        self.product_data = {
            "name": "Телевизор",
            "model": "OLED55",
            "release_date": date(2024, 12, 1)
        }

    def test_product_retrieve(self):
        """Проверяет процесс просмотра одного объекта класса "Продукт" """

        url = reverse('electronics:product-detail', args=[self.valid_product.pk])

        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.valid_product.name)
        self.assertEqual(data.get("release_date"), '2025-01-01')

    def test_product_create(self):
        """Проверяет процесс создания одного объекта класса "Продукт" """
        url = reverse("electronics:product-list")
        response = self.client.post(url, self.product_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.all().count(), 2)

        created_product = Product.objects.get(name=self.product_data["name"])
        self.assertEqual(created_product.model, self.product_data["model"])
        self.assertEqual(created_product.release_date, date(2024, 12, 1))

    def test_list_contacts(self):
        """Проверяет получение списка продуктов."""
        # Создаю ещё один продукт
        url = reverse("electronics:product-list")
        self.client.post(url, self.product_data, format="json")

        url = reverse("electronics:product-list")
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data["results"]), 2)

    def test_delete_product(self):
        """Проверяет процесс создания одного объекта класса "Продукт"."""

        url = reverse("electronics:product-detail", kwargs={"pk": self.valid_product.pk})

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Проверяем, что продукт действительно удален из базы данных
        self.assertFalse(Product.objects.filter(id=self.valid_product.pk).exists())

    def test_product_error_no_city(self):
        """Проверяет, что нельзя создать продукт с датой выхода на рынок в будущем """
        self.product_data['release_date'] = date(2034, 12, 1)
        url = reverse("electronics:product-list")
        response = self.client.post(url, self.product_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('release_date', response.data)
        self.assertEqual(
            response.data['release_date'][0],
            'Дата выхода продукта на рынок не может быть в будущем.'
        )

    def test_product_authentication_error(self):
        """Проверяем сообщение об ошибке аутентификации """
        self.client.force_authenticate(user=None)
        url = reverse("electronics:product-list")
        response = self.client.post(url, self.product_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], "Authentication credentials were not provided.")


class NetworkNodeTestCase(APITestCase):
    """ Тесты API для модели 'NetworkNode' """

    def setUp(self):
        """Создает базовый набор параметров для тестов для модели "NetworkNode" """
        # Создание Пользователя
        self.user = User.objects.create(
            email="admin1@example.com",
            name="Александр",
            surname="Александров",
            patronymic="Александрович",
            password="12345",
            position="team_leader",
            is_staff=True
        )
        self.user.save()

        self.valid_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.valid_token}")

        # Создаем контакты
        self.factory_contact = Contact.objects.create(
            email="factory@example.com",
            country="Россия",
            city="Москва"
        )
        self.retail_contact = Contact.objects.create(
            email="retail@example.com",
            country="Россия",
            city="Санкт-Петербург"
        )

        # Создаем продукты
        self.product = Product.objects.create(
            name="Смартфон",
            model="Galaxy S23",
            release_date=date(2023, 1, 1)
        )

        # Создаем завод (уровень 0)
        self.factory = NetworkNode.objects.create(
            name="Завод Электроникс",
            node_type=0,
            contact=self.factory_contact,
            debt=0.00,
        )
        self.factory.products.add(self.product)

        # Создаем розничную сеть (уровень 1)
        self.retail = NetworkNode.objects.create(
            name="Розничная сеть Техно",
            node_type=1,
            contact=self.retail_contact,
            debt=150000.50,
        )
        self.retail.products.add(self.product)

        # Данные для создания розничной сети
        self.retail_data = {
            "name": "Розничная сеть СитиЛинк",
            "node_type": 1,
            "contact": self.retail_contact.id,
            "supplier": self.factory.id,
            "debt": 10000.10,
            "products": [self.product.id]
        }
        self.url_create = reverse("electronics:network-node-create")

    def test_network_node_retrieve(self):
        """ Проверяет процесс просмотра одного объекта класса "Сетевое звено" """

        url = reverse('electronics:network-node-retrieve', args=[self.factory.pk])

        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.factory.name)
        self.assertEqual(data.get("products"), [self.product.id,])

    def test_create_network_node(self):
        """ Проверяет процесс создания одного объекта класса "Сетевое звено" """

        response = self.client.post(self.url_create, self.retail_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(NetworkNode.objects.count(), 3)
        self.assertEqual(response.data["name"], self.retail_data['name'])

    def test_list_contacts(self):
        """Проверяет получение списка продуктов."""
        # Создаю ещё одно сетевое звено
        url = reverse("electronics:network-node-create")
        self.client.post(url, self.retail_data, format="json")

        url = reverse("electronics:network-nodes-list")
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data["results"]), 3)

    def test_network_node_update(self):
        """ Проверяет процесс редактирования одного объекта класса "Сетевое звено" """

        url = reverse('electronics:network-node-update', args=[self.factory.pk])
        update_data = {"name": "Обновленный завод"}

        response = self.client.patch(url, update_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.factory.refresh_from_db()
        self.assertEqual(self.factory.name, "Обновленный завод")

    def test_delete_network_node(self):
        """ Проверяет процесс удаления одного объекта класса "Сетевое звено" """

        url = reverse('electronics:network-node-delete', args=[self.factory.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(NetworkNode.objects.count(), 1)

    def test_cannot_update_debt_via_api(self):
        """ Проверяет, что нельзя обновить задолженность через API"""

        url_detail = reverse("electronics:network-node-update", args=[self.retail.pk])

        # Пытаемся обновить задолженность
        update_data = {"debt": 999999.99}
        response = self.client.patch(url_detail, update_data, format="json")

        # Проверяем, что задолженность НЕ изменилась
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data["debt"], 999999.99)
        self.assertEqual(response.data["debt"], "150000.50")

    def test_factory_cannot_have_supplier(self):
        """ Проверяет, что завод не может иметь поставщика"""

        factory_data = {
            "name": "Неверный завод",
            "node_type": 0,
            "contact": self.factory_contact.id,
            "products": [self.product.id],
            "supplier": self.retail.id,  # Завод не должен иметь поставщика!
            "debt": 0.00
        }

        response = self.client.post(self.url_create, factory_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("supplier", response.data)
        self.assertIn("Завод не может иметь поставщика.", response.data['supplier'])

    def test_hierarchy_validation(self):
        """Проверяет, что у розничной сети не может быть поставщиком индивидуальный предприниматель """
        # Создаем ИП с поставщиком-розничной сетью
        entrepreneur_contact = Contact.objects.create(
            email="entrepreneur@example.com",
            country="Россия",
            city="Казань"
        )

        entrepreneur_data = {
            "name": "ИП Петров",
            "node_type": 2,  # ИП
            "contact": entrepreneur_contact.id,
            "supplier": self.retail.id,
            "products": [self.product.id],
            "debt": 50000.00
        }

        response = self.client.post(self.url_create, entrepreneur_data, format="json")
        entrepreneur_id = response.data["id"]

        # Пытаюсь создать розничную сеть с поставщиком - ИП
        self.retail_data["supplier"] = entrepreneur_id

        response = self.client.post(self.url_create, self.retail_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("supplier", response.data)
        self.assertIn(
        "У розничной сети не может быть поставщиком индивидуальный предприниматель.",
                response.data['supplier']
        )

    def test_network_node_creation_with_invalid_jwt_token(self):
        """Проверка с невалидным JWT токеном"""
        # Повреждаем токен
        invalid_token = "invalid"
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {invalid_token}")

        response = self.client.post(self.url_create, self.retail_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)
        self.assertIn('Given token not valid for any token type', response.data['detail'])
