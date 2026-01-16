from django.contrib.auth import get_user_model
User = get_user_model()

test_user = User.objects.create_user(
    email='test@test.com',
    password='test',
    first_name='Test',
    last_name='User'
)
print('Созддан',test_user)