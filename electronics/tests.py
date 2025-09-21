from datetime import date, datetime

from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

from electronics.models import Contact, Product
from users.models import User


class ContactTestCase(APITestCase):

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

    def test_delete_contact_success(self):
        """Проверяет успешное удаление контакта."""

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

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], "Authentication credentials were not provided.")


class ProductTestCase(APITestCase):

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

        # Создание тестового продукт
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

    def test_delete_product_success(self):
        """Проверяет успешное удаление продукта."""

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

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], "Authentication credentials were not provided.")

