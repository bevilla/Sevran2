from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views import generic

from .models import Question

def has_voted(request, question):
    if question.get_cookie_key() not in request.session:
        set_vote(request, question, None)
    return request.session[question.get_cookie_key()] is not None

def set_vote(request, question, vote):
    request.session['last_answered_question'] = question.get_cookie_key()
    request.session[question.get_cookie_key()] = vote

def should_dipsplay_result(request, question):
    try:
        return request.session['last_answered_question'] == question.get_cookie_key()
    except KeyError:
        return False

class IndexView(generic.View):
    def get(self, request, *args, **kwargs):
        question = Question.pick_or_create()
        if not question.is_available():
            return redirect('polls:index')
        return redirect('polls:poll', question.id)

class PollView(generic.View):
    def get(self, request, question_id, *args, **kwargs):
        question = get_object_or_404(Question, pk=question_id)
        context = {
            'question': question,
            'display_result': should_dipsplay_result(request, question),
            'voteApercent': int(question.voteA / max(1, question.voteA + question.voteB)) * 100,
            'voteBpercent': int(question.voteB / max(1, question.voteA + question.voteB)) * 100,
        }
        return render(request, 'polls/poll.html', context)

class VoteView(generic.View):
    def post(self, request, question_id, choice_number, *args, **kwargs):
        question = get_object_or_404(Question, pk=question_id)

        if not has_voted(request, question):
            if choice_number == 0:
                question.voteA += 1
            if choice_number == 1:
                question.voteB += 1

            if question.voteA > question.voteB:
                question.choiceA.win_against(question.choiceB)
            elif question.voteB > question.voteA:
                question.choiceB.win_against(question.choiceA)
            else:
                question.choiceA.draw_against(question.choiceB)

            question.save()

        set_vote(request, question, choice_number) # we always store the cookie
        return redirect('polls:poll', question.id)
