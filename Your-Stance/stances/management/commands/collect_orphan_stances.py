from django.core.management import BaseCommand
from stances import orphan_collector as oc

class Command(BaseCommand):
    
    help = 'Create answers for all stances without those'
    
    def __init__(self, stdout=None, stderr=None, no_color=False):
        super(Command, self).__init__(stdout, stderr, no_color)
        self.collector = oc.OrphanCollector()
    
    def list_orphans(self, orphans):
        for orphan in orphans:
            self.stdout.write(str(orphan.pk) + " "+orphan.question.slug+" "+orphan.user.username)
    
    def handle(self, *args, **options):
        self.stdout.write('Collecting orphaned stances')
        
        orphans = self.collector.find_orphans()
        
        self.stdout.write("Following stances will be unorphaned:\n")
        self.list_orphans(orphans)
            
        orphans = self.collector.find_orphans(oc.OrphanCollector.assign_answer)
        
        self.stdout.write("Processed stances:\n")
        self.list_orphans(orphans)