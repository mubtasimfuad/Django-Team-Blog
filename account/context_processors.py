from .models import Profile

def get_profile(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user.id)
        return{"profile_context":profile}
    else:
         return {}