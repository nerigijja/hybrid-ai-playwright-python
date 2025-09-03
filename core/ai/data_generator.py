from faker import Faker
fake = Faker()

class DataGenerator:
    def generate_user(self):
        return {
            'username': fake.user_name(),
            'password': fake.password(length=10),
            'email': fake.email()
        }

    def generate_edge_cases(self):
        return [
            '',
            'a'*500,
            "' OR '1'='1",
            '<script>alert(1)</script>',
            fake.password(length=100)
        ]
