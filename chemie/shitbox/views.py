from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import Postform
from .models import Submission

@login_required
def post_votes(request):
    form = Postform(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.author = request.user
        instance.save()
        messages.add_message(request, messages.SUCCESS,
                             'Sladderet ble mottatt, tusen takk!',
                             extra_tags='Du sladret')
        return redirect(reverse('frontpage:home'))
    context = {
        "form": form,
    }

    return render(request, "shitbox/post_form.html", context)


@login_required
@permission_required('shitbox.submission.can_view')
def submissions_overview(request, page=1):
    all_submissions = Submission.objects.all().order_by('-date')
    paginator = Paginator(all_submissions, 20)

    try:
        submissions = paginator.page(page)
    except PageNotAnInteger:
        submissions = paginator.page(1)
    except EmptyPage:
        submissions = paginator.page(paginator.num_pages)

    context = {
        'submissions': submissions
    }

    return render(request, 'shitbox/list_submissions.html', context=context)
