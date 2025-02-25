from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

# Create your tests here.

class AccountsTestCase(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="eriktester",
            email="eriktester@gmail.com",
            password="erik234"
        )


    def test_user_registration(self):
        response = self.client.post(reverse('register'), {
            'username': 'novousuario',
            'email': 'novousuario@gmail.com',
            'password1': 'senha123',
            'password2': 'senha123'
        })
        self.assertEqual(response.status_code, 302)  # Redirecionamento esperado após o sucesso
        self.assertTrue(get_user_model().objects.filter(username="novousuario").exists())


    def test_login_successful(self):
        response = self.client.post(reverse('login'), {
            'username': 'eriktester',
            'password': 'erik234'
        })
        self.assertEqual(response.status_code, 302)  # Redirecionamento esperado após login


    def test_login_invalid_credentials(self):
        response = self.client.post(reverse('login'), {
            'username': 'eriktester',
            'password': 'errada'
        })
        self.assertEqual(response.status_code, 200)  # A página de login deve recarregar
        self.assertContains(response, "Credenciais inválidas")


    def test_logout(self):
        self.client.login(username="eriktester", password="erik234")
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
            'username': 'eriktester',
            'email': 'novoemail@gmail.com',
            'password1': 'senha123',
            'password2': 'senha123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Usuário já existe")


    def test_register_with_existing_email(self):
        response = self.client.post(reverse('register'), {
            'username': 'novousuario',
            'email': 'eriktester@gmail.com',
            'password1': 'senha123',
            'password2': 'senha123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Email já cadastrado")


    def test_register_with_mismatched_passwords(self):
        response = self.client.post(reverse('register'), {
            'username': 'novousuario',
            'email': 'novousuario@gmail.com',
            'password1': 'senha123',
            'password2': 'senha456'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "As senhas não coincidem")


    def test_dashboard_access_authenticated_user(self):
        self.client.login(username="eriktester", password="erik234")
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "eriktester")  # Verifica se o nome do usuário está na página


    def test_dashboard_access_unauthenticated_user(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)  # Deve redirecionar para login
        self.assertRedirects(response, reverse('login') + "?next=" + reverse('dashboard'))


    def test_password_reset(self):
        response = self.client.post(reverse('forget_password'), {
            'email': 'eriktester@gmail.com'
        })
        self.assertEqual(response.status_code, 302)  # Redirecionamento esperado



class SecurityTestCase(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="securetester",
            email="securetester@gmail.com",
            password="securepass"
        )


    def test_sql_injection_login(self):
        response = self.client.post(reverse('login'), {
            'username': "' OR '1'='1",
            'password': "any_password"
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Credenciais inválidas")  # Não deve permitir acesso


    def test_sql_injection_login_comment(self):
        response = self.client.post(reverse('login'), {
            'username': "admin' --",
            'password': "any_password"
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Credenciais inválidas")


    def test_sql_injection_login_union(self):
        response = self.client.post(reverse('login'), {
            'username': "' UNION SELECT 1, username, password FROM auth_user --",
            'password': "any_password"
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Credenciais inválidas")


    def test_sql_injection_password_reset(self):
        response = self.client.post(reverse('forget_password'), {
            'email': "' OR '1'='1"
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Email inexistente")


    def test_sql_injection_dashboard_access(self):
        response = self.client.get(reverse('dashboard') + "?id=' OR '1'='1")
        self.assertEqual(response.status_code, 302)  # Deve redirecionar para login


    def test_sql_injection_logout(self):
        response = self.client.get(reverse('logout') + "?id=1 OR 1=1")
        self.assertEqual(response.status_code, 302)  # Deve redirecionar para home


    def test_sql_injection_order_by(self):
        response = self.client.get(reverse('dashboard') + "?order=1; DROP TABLE auth_user;")
        self.assertEqual(response.status_code, 302)  # Não deve executar comandos arbitrários'''