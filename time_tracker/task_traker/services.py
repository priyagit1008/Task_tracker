from .models.users import Task_tracker



class TaskServices:

            
    def get_task(self,id):
        return Task_tracker.objects.get(id=id)
