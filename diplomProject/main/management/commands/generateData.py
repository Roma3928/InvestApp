from django.core.management.base import BaseCommand
import random
from faker import Faker
from main.models import *
from django_bulk_update.helper import bulk_update


usersCount = 10000
questionsCount = 100000
answersCount = 1000000
tagsCount = 10000
likeCount = 2000000

fake = Faker()


class Command(BaseCommand):

    def __init__(self, *args, **kwargs):
        BaseCommand.__init__(self, *args, **kwargs)
        self.users = []
        self.tags = []
        self.questions = []
        self.answers = []

    def handle(self, *args, **options):
        print('started')
        if User.objects.count() < usersCount:
            print("creating users")
            self.create_users()
        else:
            self.users = User.objects.all()
        if Tag.objects.count() < tagsCount:
            print("creating tags")
            self.create_tags()
        else:
            self.tags = Tag.objects.all()
        if Question.objects.count() < questionsCount:
            print("creating questions")
            self.create_questions()
            print("creating tags for questions")
            self.add_tags_to_questions()
        else:
            self.questions = Question.objects.all()
        if Answer.objects.count() < answersCount:
            print("creating answers")
            self.create_answers()
        else:
            self.answers = Answer.objects.all()
        LikeDislike.objects.all().delete()
        if LikeDislike.objects.count() < likeCount:
            print('creating likes')
            self.create_likes()
        print("ended")

    def create_users(self):
        for i in range(usersCount):
            user = User(username=fake.user_name() + str(i), first_name=fake.first_name(),
                        last_name=fake.last_name(),
                        email=fake.email())
            self.users.append(user)

        User.objects.bulk_create(self.users, batch_size=120)

    def create_tags(self):

        for j in range(tagsCount):
            tag = Tag(title=fake.word() + str(j))
            self.tags.append(tag)
        Tag.objects.bulk_create(self.tags, batch_size=120)

    def create_questions(self):
        for i in range(questionsCount):
            author = random.choice(self.users)
            question = Question(author=author, title=fake.text(40), text=fake.text(250))
            self.questions.append(question)

        Question.objects.bulk_create(self.questions, batch_size=120)

    def add_tags_to_questions(self):
        for question in self.questions:
            tags = []
            for _ in range(random.randint(1, 4)):
                tag = random.choice(self.tags)
                if tag not in tags:
                    tags.append(tag)
            question.tags.add(*tags)

        bulk_update(self.questions, update_fields=['tags'], batch_size=120)

    def create_answers(self):
        for _ in range(answersCount):
            answer = Answer(author=random.choice(self.users), question=random.choice(self.questions),
                            text=fake.text())
            self.answers.append(answer)

        Answer.objects.bulk_create(self.answers, batch_size=120)

    def create_likes(self):
        i = 0
        LikeDislike.objects.all().delete()
        likes = []
        while len(likes) < likeCount:
            q_like = LikeDislike(vote=random.choice([-1, 1]), user=random.choice(self.users),
                                 content_object=random.choice(self.questions))
            print(i)
            i += 1
            a_like = LikeDislike(vote=random.choice([-1, 1]), user=random.choice(self.users),
                                 content_object=random.choice(self.answers))
            print(i)
            i += 1
            likes.append(a_like)
            likes.append(q_like)
        LikeDislike.objects.bulk_create(likes, batch_size=120)
        for like in likes:
            like.content_object.rate += like.vote
        bulk_update(self.questions, update_fields=['rate'], batch_size=120)
        bulk_update(self.answers, update_fields=['rate'], batch_size=120)
