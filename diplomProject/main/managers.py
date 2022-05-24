from django.db import models


class TagManager(models.Manager):
    def questions_by_tag(self, title):
        return self.get(title=title).questions.all()


class QuestionManager(models.Manager):
    pass


class AnswerManager(models.Manager):
    pass


class LikeDislikeManager(models.Manager):
    pass

