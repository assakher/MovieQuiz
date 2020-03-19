from app import db
from config import LENGTH
import random


class Questions(db.Model):
    __tablename__ = 'questions'

    id_ = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String)
    answer = db.Column(db.String)
    answer_type = db.Column(db.String)
    tag = db.Column(db.String)


class Dates(db.Model):
    __tablename__ = 'Dates'

    value = db.Column(db.String)
    tag = db.Column(db.String)
    id = db.Column(db.Integer, primary_key=True)


class ActorNames(db.Model):
    __tablename__ = 'ActorNames'

    name = db.Column(db.String)
    tag = db.Column(db.String)
    id = db.Column(db.Integer, primary_key=True)


class DirectorNames(db.Model):
    __tablename__ = 'Directornames'

    value = db.Column(db.String)
    tag = db.Column(db.String)
    id = db.Column(db.Integer, primary_key=True)


class Titles(db.Model):
    __tablename__ = 'Titles'

    value = db.Column(db.String)
    tag = db.Column(db.String)
    id = db.Column(db.Integer, primary_key=True)


class Card:
    def __init__(self, id_, question, variants, answer, answer_index):
        self.id = id_
        self.question = question
        self.answer = answer
        self.variants = variants
        self.answer_index = answer_index

    def to_json(self):
        return self.__dict__


class QuizSession:
    def __init__(self, quiz_length, question_ids, quiz_queue):
        self.quiz_length = quiz_length
        self.queue_ids = question_ids
        self.quiz_queue = quiz_queue

    def fetch_card(self):
        return next(self.quiz_queue)

    def to_json(self):
        return {
            "quiz_length": self.quiz_length,
            "queue_ids": self.queue_ids,
            "quiz_queue": [card.to_json() for card in list(self.quiz_queue)]
        }


def card_factory(question_id):
    data = Questions.query.filter(Questions.id_ == question_id).one()
    print(f'Card Data {data}')

    def get_variants():
        reference_tables = {
            'DirectorName': DirectorNames,
            'ActorName': ActorNames,
            'Title': Titles,
            'Date': Dates
        }
        reference_table = reference_tables.get(data.answer_type)

        tricky_variants = [row.value for row in reference_table.query.\
            filter(reference_table.tag == f'{data.tag}', reference_table.value != data.answer)]
        fluff_variants = [row.value for row in reference_table.query.\
            filter(reference_table.tag != f'{data.tag}')]
        variants = [data.answer] + [random.choice(tricky_variants)] + random.sample(fluff_variants, k=2)
        random.shuffle(variants)
        return variants

    variants = get_variants()
    return Card(question_id, data.question, variants, data.answer, variants.index(data.answer))


def quiz_factory(length):

    def queue_generator(ids):
        for question in ids:
            yield card_factory(question)

    all_questions = [item for item, in Questions.query.with_entities(Questions.id_)]
    queue_ids = random.sample(all_questions, k=length)
    queue = queue_generator(queue_ids)
    return QuizSession(quiz_length=LENGTH, question_ids=queue_ids, quiz_queue=queue)

if __name__ == "__main__":
    o = card_factory(1)
    print(type(o))
    print(o.__class__.__name__)
    print(o.__class__ == type(o))