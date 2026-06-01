from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker

from tasks.models import Priority, Category, Task, Note, SubTask


class Command(BaseCommand):
    help = "Seed database with sample data for Hangarin app"

    def handle(self, *args, **kwargs):
        fake = Faker()

        priorities = ["High", "Medium", "Low", "Critical", "Optional"]
        categories = ["Work", "School", "Personal", "Finance", "Projects"]

        for priority in priorities:
            Priority.objects.get_or_create(name=priority)

        for category in categories:
            Category.objects.get_or_create(name=category)

        priority_objects = list(Priority.objects.all())
        category_objects = list(Category.objects.all())

        statuses = ["Pending", "In Progress", "Completed"]

        for _ in range(20):
            task = Task.objects.create(
                title=fake.sentence(nb_words=5),
                description=fake.paragraph(nb_sentences=3),
                deadline=timezone.make_aware(fake.date_time_this_month()),
                status=fake.random_element(elements=statuses),
                priority=fake.random_element(elements=priority_objects),
                category=fake.random_element(elements=category_objects),
            )

            for _ in range(2):
                Note.objects.create(
                    task=task,
                    content=fake.paragraph(nb_sentences=2)
                )

            for _ in range(3):
                SubTask.objects.create(
                    parent_task=task,
                    title=fake.sentence(nb_words=4),
                    status=fake.random_element(elements=statuses)
                )

        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))