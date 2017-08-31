from django.db.models import Q
from django.contrib.auth.models import User
from stances.models import Stance
from questions.models import Question, Answer


class OrphanCollector(object):
    
    @staticmethod
    def assign_answer(stance):
        answer = Answer(stance=stance, user=stance.user, created=stance.created, modified=stance.modified)
        answer.save()
    
    def find_orphans(self, callback=None):
        
        stances = Stance.objects.all()
        orphan_stances = []
        
        for stance in stances:
            answers = Answer.objects.filter(Q(stance=stance) & Q(user=stance.user))
            
            if len(answers) == 0:
                orphan_stances.append(stance)
                if callback is not None:
                    callback(stance)
        
        return orphan_stances
        
        