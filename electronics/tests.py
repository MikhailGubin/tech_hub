from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

from electronics.models import Contact
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

        # Создание другого сотрудника
        self.other_user = User.objects.create(
            email="other_user@example.com",
            password="45678",
            surname="Иванов",
            name="Иван",
            patronymic="Иванович",
            position="employee",
        )
        self.other_user.save()

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

        # Проверяем, что привычка действительно удалена из базы данных
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
