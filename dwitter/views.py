from django.shortcuts import render, redirect
from .models import Profile, Dweet
from .forms import DweetForm

def dashboard(request):
	return render(request, 'base.html')


def profile_list(request):
	profiles = Profile.objects.exclude(user=request.user)
	return render(request, 'dwitter/profile_list.html', context={'profiles': profiles})


def profile(request, pk):
	profile = Profile.objects.get(pk=pk)
	if request.method == "POST":
		current_user = request.user.profile
		action = request.POST.get("follow")
		if action == "follow":
			current_user.follows.add(profile)
		elif action == "unfollow":
			current_user.follows.remove(profile)
		current_user.save()

	follows = profile.follows.exclude(pk=pk)
	return render(request, 'dwitter/profile.html', context={'profile': profile, 'follows': follows})


def dashboard(request):
	form = DweetForm(request.POST or None)
	if request.method == "POST":
		if form.is_valid():
			dweet = form.save(commit=False)
			dweet.user = request.user
			dweet.save()
			return redirect("dwitter:dashboard")

	followed_dweets = Dweet.objects.filter(
			user__profile__in=request.user.profile.follows.all()
		)

	return render(request, "dwitter/dashboard.html", context={'form': form, 'dweets': followed_dweets})