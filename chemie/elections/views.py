from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.shortcuts import redirect, reverse
from django.contrib import messages
from django.forms import modelformset_factory


from .forms import AddPositionForm, AddCandidateForm, CastVoteForm
from .forms import AddPrevoteForm, AddPreVoteToCandidateForm
from .models import Election, Position, Candidate
from .models import VOTES_REQUIRED_FOR_VALID_ELECTION


from chemie.customprofile.forms import GetRFIDForm, AddCardForm
from chemie.customprofile.models import ProfileManager, User, Profile


def election_is_open():
    is_open = True
    try:
        election = Election.objects.latest('id')
        if not election.is_open:
            is_open = False
    except ObjectDoesNotExist:
        is_open = False
    return is_open


def voting_is_active():
    active = False
    election = Election.objects.latest('id')
    if election.current_position_is_open:
        active = True
    return active


@login_required
def vote(request):
    try:
        election = Election.objects.latest('id')
        voted = request.user.profile.voted
        context = {'election': election, 'voted': voted}
    except:
        context = {'election': None, 'voted': False}
    return render(request, 'elections/election/index.html', context)


@login_required
def results(request):
    try:
        elections = Election.objects.all()
    except:
        elections = None
    context = {
        'elections': elections,
    }
    return render(request, 'elections/election/resultater.html', context)


@login_required
def voting(request):
    if not election_is_open():
        return redirect('elections:vote')
    else:
        voted = request.user.profile.voted
        election = Election.objects.latest('id')
        if election.current_position_is_open:
            if not voted:
                form = CastVoteForm(request.POST or None, election=election)
                if request.method == 'POST':
                    profile = request.user.profile
                    if 'Stem blankt' in request.POST.getlist('Blank'):
                        successful_vote = election.vote(
                            profile, candidates=None, blank=True
                            )
                    elif 'Avgi stemme' in request.POST.getlist('Stem'):
                        if form.is_valid():
                            candidates = form.cleaned_data.get('candidates')
                            successful_vote = election.vote(
                                profile, candidates, blank=False
                                )
                        else:
                            # Un-checks all candidates, since form is invalid
                            form.fields['candidates']\
                                .widget.checked_attribute['checked'] = False
                            cands = election.current_position.candidates.all()
                            context = {
                                'form': form,
                                'position': election.current_position,
                                'candidates': cands,
                            }
                            return render(
                                request, 'elections/election/vote.html',
                                context
                                )
                    else:
                        cands = election.current_position.candidates.all()
                        context = {
                            'form': form,
                            'position': election.current_position,
                            'candidates': cands,
                        }
                        return render(
                            request, 'elections/election/vote.html',
                            context
                            )
                    if successful_vote:
                        return redirect('elections:has_voted')
                else:
                    cands = election.current_position.candidates.all()\
                                .order_by('id')
                    context = {
                        'form': form,
                        'position':  election.current_position,
                        'candidates': cands,
                    }
                    return render(
                        request, 'elections/election/vote.html',
                        context
                        )
        return redirect('elections:vote')


@login_required
def has_voted(request):
    if not election_is_open():
        return redirect('elections:vote')
    else:
        election = Election.objects.latest('id')
        if not election.current_position_is_open:
            return redirect('elections:vote')
        voted = request.user.profile.voted
        if not voted:
            return redirect('elections:voting')
        return render(request, 'elections/election/vote_ended.html')


@permission_required('elections.add_election')
@login_required
def admin_start_election(request):
    if election_is_open():
        election = Election.objects.latest('id')
        if voting_is_active():
            return redirect(
                'elections:admin_start_voting',
                pk=election.current_position.id
                )
        return redirect('elections:admin_register_positions')
    if request.method == 'POST':  # brukeren trykker på knappen
        Election.objects.create(is_open=True)
        return redirect('elections:admin_register_positions')
    return render(request, 'elections/admin/admin_start_election.html')


@permission_required('elections.add_election')
@login_required
def admin_register_positions(request):
    if not election_is_open():
        return redirect('elections:admin_start_election')
    else:
        form = AddPositionForm(request.POST or None)
        election = Election.objects.latest('id')
        if voting_is_active():
            return redirect(
                'elections:admin_start_voting',
                pk=election.current_position.id
                )
        if request.method == "POST":
            if "Delete" in request.POST:  # delete posisjon
                position_id = request.POST.get("Delete", "0")
                position = election.positions.get(id=int(position_id))
                election.delete_position(position)
                form = AddPositionForm(None)
            # Selve formen fr registrering av posisjon
            if form.is_valid():
                # lager et nytt position objekt som vi legger inn i election
                # position field
                new_position = form.cleaned_data['position_name']
                # lager en liste som skjekker at vi ikke alt har
                # lagt til vervet i election
                current_positions_in_election = list()
                for i in election.positions.all():
                    current_positions_in_election.append(i.position_name)
                if new_position not in current_positions_in_election:
                    # hvis vi ikke har lagt til vervet allerede
                    spots = form.cleaned_data['spots']  # spots field
                    new_position_object = Position.objects.create(
                        position_name=str(new_position),
                        spots=int(spots)
                        )  # lager et position objetkt
                    election.positions.add(new_position_object)
                    election.save()
        positions = election.positions.all()
        context = {
            'form': form,
            'positions': positions
        }
        return render(request, 'elections/admin/admin_positions.html', context)


@permission_required('elections.add_election')
@login_required
def admin_register_candidates(request, pk):
    if not election_is_open():
        return redirect('elections:admin_start_election')
    else:
        if voting_is_active():
            election = Election.objects.latest('id')
            return redirect(
                'elections:admin_start_voting',
                pk=election.current_position.id
                )
        # henter ut position som skal legge verv til
        position = get_object_or_404(Position, pk=pk)
        add_candidate_form = AddCandidateForm(request.POST or None)
        if request.method == 'POST':
            if 'Delete' in request.POST:
                # hvis brukeren skal slette candidaten fra posisjonen.
                candidate_username = request.POST.get("Delete", "0")
                candidate_user_object = User.objects.get(
                    username=candidate_username
                    )
                all_candidates = position.candidates.all()
                candidate_object = all_candidates.get(
                    user=candidate_user_object
                    )
                position.delete_candidates(candidate_object)
                position.save()
            elif 'addCandidate' in request.POST:
                if add_candidate_form.is_valid():
                    user = add_candidate_form.cleaned_data['user']
                    position_candidates = position.candidates.all()
                    to_be_added = False\
                        if user in [usr.user for usr in position_candidates]\
                        else True
                    if to_be_added:
                        candidate = Candidate.objects.create(user=user)
                        position.candidates.add(candidate)
                        position.save()
            elif 'startVoting' in request.POST:
                election = Election.objects.latest('id')
                if not election.current_position_is_open:
                    election.start_current_election(position)
                return redirect('elections:admin_start_voting', pk=position.id)

        candidates = position.candidates.all()
        context = {
            'candidates': candidates,
            'position': position,
            'add_candidate_form': add_candidate_form
        }
        return render(
            request, 'elections/admin/admin_candidates.html',
            context)


@permission_required('elections.add_election')
@login_required
def admin_register_prevotes(request, pk):
    if not election_is_open():
        return redirect('elections:admin_start_election')
    else:
        if voting_is_active():
            election = Election.objects.latest('id')
            return redirect(
                'elections:admin_start_voting',
                pk=election.current_position.id
                )
        # Fetch position
        position = get_object_or_404(Position, pk=pk)
        # For for editing total number of people prevoting
        prevote_form = AddPrevoteForm(
            request.POST or None,
            instance=position,
            prefix='total_voters'
        )

        # Form for adjusting individual candidate's votes
        CandidateFormSet = modelformset_factory(
            Candidate, form=AddPreVoteToCandidateForm, extra=0
            )
        formset = CandidateFormSet(
            request.POST or None,
            queryset=position.candidates.all(),
            prefix='candidate_forms',
            )
        if request.method == 'POST':
            if formset.is_valid() and prevote_form.is_valid():
                prevote_form.save()
                for form in formset:
                    # Increment both candidate and positions votes
                    candidate_pk = form.instance.pk
                    candidate = Candidate.objects.get(pk=candidate_pk)
                    old_votes = candidate.votes
                    new_votes = form.cleaned_data['votes']
                    position.total_votes = \
                        position.total_votes + (new_votes - old_votes)
                    position.save()
                    form.save()
                return redirect(reverse(
                    'elections:admin_register_candidates',
                    kwargs={'pk': position.id}
                    ))
        context = {
            'prevote_form': prevote_form,
            'candidate_formset': formset,
            'position': position
        }
        return render(
            request, 'elections/admin/admin_add_prevotes.html',
            context
            )


@permission_required('elections.add_election')
@login_required
def admin_voting_is_active(request, pk):
    if not election_is_open():
        return redirect('elections:admin_start_election')
    if not voting_is_active():
        return redirect('elections:admin_register_positions')
    election = Election.objects.latest('id')
    if request.method == 'POST':
        if 'endVoting' in request.POST:
            election.current_position.end_voting_for_position()
            return redirect('elections:admin_results', pk=pk)
    total_voters = election.current_position.number_of_voters
    context = {
        'election': election,
        'total_voters': total_voters
    }
    return render(request, 'elections/admin/admin_start_voting.html', context)


@permission_required('elections.add_election')
@login_required
def admin_results(request, pk):
    if not election_is_open():
        return redirect('elections:admin_start_election')
    election = Election.objects.latest('id')
    if voting_is_active():
        return redirect('elections:admin_start_voting', pk=pk)
    position = election.positions.get(id=pk)
    total_votes = position.total_votes
    winners = position.winners.all()
    blank_votes = total_votes - \
        sum([c.votes for c in position.candidates.all()])
    number_of_voters = position.number_of_voters
    if number_of_voters < VOTES_REQUIRED_FOR_VALID_ELECTION:
        messages.add_message(
            request,
            messages.ERROR,
            'OBS!',
            extra_tags='Det ble kun avgitt {} stemmesedler.'
            .format(number_of_voters)
        )
    context = {
        'candidates': position.candidates.all(),
        'total_votes': total_votes,
        'winners': winners,
        'number_of_voters': number_of_voters,
        'blank_votes': blank_votes
    }
    return render(request, 'elections/admin/admin_results.html', context)


@permission_required('elections.add_election')
@login_required
def admin_end_election(request):
    if not election_is_open():
        return redirect('elections:admin_start_election')
    election = Election.objects.latest('id')
    if voting_is_active():
        return redirect(
            'elections:admin_start_voting',
            pk=election.current_position.id
            )
    election.end_election()
    return redirect('elections:results')


@permission_required('elections.add_election')
@login_required
def change_rfid_status(request):
    if request.method == "POST":
        form = GetRFIDForm(request.POST)
        if form.is_valid():
            rfid = form.cleaned_data.get('rfid')
            em_code = ProfileManager.rfid_to_em(rfid)
            try:
                profile = Profile.objects.get(access_card=em_code).first()
            except ObjectDoesNotExist or None:
                return redirect('elections:add_rfid')
            except:
                raise Http404
            eligible = profile.eligible_for_voting
            if eligible:
                profile.eligible_for_voting = False
            else:
                profile.eligible_for_voting = True
            profile.save()
            status = profile.eligible_for_voting
            messages.add_message(request, messages.SUCCESS, 'Statusen din ble endret til {}'.format(status))
        return redirect('elections:checkin')
    else:
        form = GetRFIDForm()
        context = {'form': form}
    return render(request, 'elections/check_in.html', context)


def add_rfid(request):
    if request.method == 'POST':
        form = AddCardForm(request)
        if form.is_valid:
            username = form.cleaned_data.get('username')
            try:
                user = User.objects.get(username=username).first()
            except:
                messages.add_message(request, messages.ERROR, 'Det finnes ingen bruker med brukernavn {}'.format(username))
            card_nr = form.cleaned_data.get('card_nr')
            user.access_card = card_nr
            messages.add_message(request, messages.SUCCESS, 'Studentkortnr ble endret')
            return redirect('elections:checkin')
    return
