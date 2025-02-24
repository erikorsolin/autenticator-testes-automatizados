from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

# Create your tests here.

class AccountsTestCase(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword123"
        )


    def test_user_registration(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123'
        })
        self.assertEqual(response.status_code, 302)  # Redirecionamento esperado após o sucesso
        self.assertTrue(get_user_model().objects.filter(username="newuser").exists())


    def test_login_successful(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpassword123'
        })
        self.assertEqual(response.status_code, 302)  # Redirecionamento esperado após login


    def test_login_invalid_credentials(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)  # A página de login deve recarregar
        self.assertContains(response, "Credenciais inválidas")


    def test_logout(self):
        self.client.login(username="testuser", password="testpassword123")
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Deve redirecionar para a home
        self.assertRedirects(response, reverse('home'))  # Confirma que redireciona para a página correta


    def test_login_empty_data(self):
        response = self.client.post(reverse('login'), {
            'username': '',
            'password': ''
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Credenciais inválidas")


    def test_register_with_existing_username(self):
        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            'email': 'newemail@example.com',
            'password1': 'password123',
            'password2': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Usuário já existe")


    def test_register_with_existing_email(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'testuser@example.com',
            'password1': 'password123',
            'password2': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Email já cadastrado")


    def test_register_with_mismatched_passwords(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'password123',
            'password2': 'password456'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "As senhas não coincidem")


    def test_dashboard_access_authenticated_user(self):
        self.client.login(username="testuser", password="testpassword123")
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testuser")  # Verifica se o nome do usuário está na página


    def test_dashboard_access_unauthenticated_user(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)  # Deve redirecionar para login
        self.assertRedirects(response, reverse('login') + "?next=" + reverse('dashboard'))


    def test_password_reset(self):
        response = self.client.post(reverse('forget_password'), {
            'email': 'testuser@example.com'
        })
        self.assertEqual(response.status_code, 302)  # Redirecionamento esperado