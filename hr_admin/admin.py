from django.contrib import admin
from .models import *



admin.site.register(Company)
admin.site.register(Consultant)

admin.site.register(InputsForm)
admin.site.register(InputsCategory)
admin.site.register(InputsQuestion)
admin.site.register(InputsAnswer)

admin.site.register(Attachment)

admin.site.register(Competency)
admin.site.register(CompetencyRecord)

admin.site.register(EvaluationForm)
admin.site.register(EvaluationCategory1)
admin.site.register(EvaluationCategory2)
admin.site.register(EvaluationQuestion)
admin.site.register(EvaluationAnswer)

admin.site.register(ActionPlanForm)
admin.site.register(UserProfile)
#admin.site.register(Comment)
#admin.site.register(CommentAnswer)
#admin.site.register(CommentActionPlan)



