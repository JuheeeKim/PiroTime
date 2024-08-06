# 표준 라이브러리
import json
from datetime import timedelta

# Django 모듈
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models import Q
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import strip_tags

# 프로젝트 내 모듈
from .models import CoffeeChat, Hashtag, CoffeeChatRequest, Review
from .forms import CoffeeChatForm, ReviewForm

def home(request):
    reviews = Review.objects.all().order_by('-created_at')[:27]  # 최신 27개 리뷰 가져오기
    context = {
        'reviews': reviews
    }
    return render(request, 'coffeechat/home.html', context)

def list(req):
    query = req.GET.get('search')
    if query:
        profiles = CoffeeChat.objects.filter(
            Q(hashtags__name__icontains=query) | Q(receiver__username__icontains=query) | Q(job__icontains=query)
        ).distinct()
    else:
        profiles = CoffeeChat.objects.all()
    
    ctx = {
        "profiles": profiles
    }
    return render(req, 'coffeechat/list.html', ctx)

@login_required
def create(req):
    # 현재 사용자가 이미 프로필을 가지고 있는지 확인
    existing_profile = CoffeeChat.objects.filter(receiver=req.user).first()
    if existing_profile:
        return redirect('coffeechat:coffeechat_detail', pk=existing_profile.pk)  # 이미 존재하면 자신의 detail 페이지로 리디렉션

    if req.method == "POST": #생성 후
        form = CoffeeChatForm(req.POST)
        if form.is_valid():
            coffeechat = form.save(commit=False)
            coffeechat.receiver = req.user
            coffeechat.count = 0  # count 기본값 설정
            coffeechat.content = form.cleaned_data['content']
            coffeechat.save()
            
            # 해시태그 저장
            hashtags = form.cleaned_data['hashtags']
            hashtag_list = json.loads(hashtags)
            hashtag_objects = []
            for tag in hashtag_list:
                hashtag, created = Hashtag.objects.get_or_create(name=tag)
                hashtag_objects.append(hashtag)
            coffeechat.hashtags.set(hashtag_objects)
            
            coffeechat.save()
            return redirect('coffeechat:coffeechat_detail', pk=coffeechat.pk)
    else: #생성 전(GET)
        form = CoffeeChatForm()
    ctx = {
        'form': form
    }
    return render(req, 'coffeechat/create.html', ctx)

@login_required
def create_review(request, coffeechat_request_id):
    coffeechat_request = get_object_or_404(CoffeeChatRequest, id=coffeechat_request_id)

    # 요청을 보낸 사용자가 요청을 받은 사용자인 경우 접근 금지
    if request.user != coffeechat_request.user:
        return HttpResponseForbidden("리뷰 작성 권한이 없습니다.")

    # 이미 리뷰가 존재하는지 확인
    if hasattr(coffeechat_request, 'review'):
        return render(request, 'coffeechat/review_form.html', {
            'error_message': '이미 이 요청에 대한 리뷰가 작성되었습니다.'
        })

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = request.user
            review.coffeechat_request = coffeechat_request
            review.save()
            return redirect('coffeechat:coffeechat_detail', pk=coffeechat_request.coffeechat.pk)
        else:
            return render(request, 'coffeechat/review_form.html', {
                'form': form,
                'error_message': '폼이 유효하지 않습니다.'
            })
    else:
        form = ReviewForm()
    return render(request, 'coffeechat/review_form.html', {'form': form})

@login_required
def accept_request(request, request_id): 
    coffeechat_request = get_object_or_404(CoffeeChatRequest, id=request_id)
    if request.user == coffeechat_request.coffeechat.receiver:
        coffeechat_request.status = 'ACCEPTED'
        coffeechat_request.save()
        
        coffeechat = coffeechat_request.coffeechat
        coffeechat.count += 1
        coffeechat.save()

    return redirect('coffeechat:coffeechat_detail', pk=coffeechat_request.coffeechat.pk)

def detail(request, pk):
    profile = CoffeeChat.objects.get(pk=pk)
    coffeechat_requests = CoffeeChatRequest.objects.filter(coffeechat=profile)
    
    if request.method == "POST" and request.user != profile.receiver:
        existing_request = CoffeeChatRequest.objects.filter(user=request.user, coffeechat=profile).exists()
        
        if not existing_request:
            start_of_day = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
            end_of_day = start_of_day + timedelta(days=1)
            daily_requests = CoffeeChatRequest.objects.filter(
                coffeechat__receiver=profile.receiver,
                created_at__range=(start_of_day, end_of_day),
                status='WAITING'
            ).count()

            if daily_requests < 5:
                CoffeeChatRequest.objects.create(
                    user=request.user,
                    coffeechat=profile,
                    status='WAITING'
                )
            else:
                profile.status = 'LIMITED'
                profile.save()
    
    is_waiting = CoffeeChatRequest.objects.filter(user=request.user, coffeechat=profile, status='WAITING').exists()
    waiting_requests = CoffeeChatRequest.objects.filter(coffeechat__receiver=profile.receiver, status='WAITING').count()
    is_limited = waiting_requests >= 5 and not is_waiting
    hashtags = profile.hashtags.all()
    requests = CoffeeChatRequest.objects.filter(coffeechat=profile)

    show_review_button = False
    coffeechat_request = None
    if profile.receiver == request.user:
        for req in coffeechat_requests:
            if req.status == 'ACCEPTED':
                show_review_button = True
                coffeechat_request = req
                break

    ctx = {
        'profile': profile,
        'is_waiting': is_waiting,
        'is_limited': is_limited,
        'hashtags': hashtags,
        'requests': requests,
        'show_review_button': show_review_button,
        'coffeechat_request': coffeechat_request
    }
    return render(request, 'coffeechat/detail.html', ctx)

@login_required
def accept_request(request, request_id): #수락 시 
    coffeechat_request = CoffeeChatRequest.objects.get(id=request_id)
    if request.user == coffeechat_request.coffeechat.receiver:
        coffeechat_request.status = 'ACCEPTED'
        coffeechat_request.save()
        
        # CoffeeChat 모델의 count 필드 증가
        coffeechat = coffeechat_request.coffeechat
        coffeechat.count += 1
        coffeechat.save()

        #메일 보내기
        if not cor_mail(coffeechat.receiver, coffeechat_request.user):
            return redirect('coffeechat:coffeechat_detail', pk=coffeechat_request.coffeechat.pk)        #에러 메세지 보내고 싶음

    return redirect('coffeechat:coffeechat_detail', pk=coffeechat_request.coffeechat.pk)

@login_required
def update(req, pk):
    profile = CoffeeChat.objects.get(pk=pk)
    if req.method == "POST": # 수정 후
        form = CoffeeChatForm(req.POST, instance=profile)
        if form.is_valid():
            coffeechat = form.save(commit=False)
            coffeechat.receiver = req.user
            coffeechat.count = 0  # count 필드에 기본값 설정
            coffeechat.content = form.cleaned_data['content']
            coffeechat.save()
            
            # 해시태그 저장
            hashtags = form.cleaned_data['hashtags']
            hashtag_list = json.loads(hashtags)
            hashtag_objects = []
            for tag in hashtag_list:
                hashtag, created = Hashtag.objects.get_or_create(name=tag)
                hashtag_objects.append(hashtag)
            coffeechat.hashtags.set(hashtag_objects)
            
            coffeechat.save()
            return redirect('coffeechat:coffeechat_detail', pk=profile.pk)
    else: # 수정 전(위한 load, GET)
        form = CoffeeChatForm(instance=profile)
        # 수정을 위해서 기존 콘텐츠와 해시태그 로드(JSON)
        initial_hashtags = json.dumps([{'value': hashtag.name} for hashtag in profile.hashtags.all()])
        form.fields['hashtags'].initial = initial_hashtags
        form.fields['content'].initial = profile.content

    ctx = {
        'form': form,
        'profile': profile
    }
    return render(req, 'coffeechat/update.html', ctx)

@login_required
def delete(req, pk):
    profile = CoffeeChat.objects.get(pk=pk)
    if req.method == "POST":
        profile.delete()
        return redirect('coffeechat:coffeechat_list')
    ctx = {
        'profile': profile
    }
    return render(req, 'coffeechat/delete.html', ctx)


def generate_email_content(sender, receiver):
    subject = "PiroTime: 협력 제안이 왔습니다!"
    message = f"{sender.username}님으로 부터 협력 제안이 왔습니다. PiroTime에 접속해서 내용을 확인하세요!"
    from_email = 'pirotimeofficial@gmail.com'
    recipient_list = [receiver.email]
    return subject, message, from_email, recipient_list

def cor_mail(receiver, sender):

    subject, message, from_email, recipient_list = generate_email_content(sender, receiver)

    html_message = render_to_string(
        "corboard/message.html",
        {"sender": sender.username, "receiver": receiver.username,
         "content": "커피챗 신청이 들어왔습니다! 아래 링크로 들어와 확인해 보세요!"},
    )
    plain_message = strip_tags(html_message)
    send_mail(
        subject,
        plain_message,
        from_email,
        recipient_list,
        html_message=html_message,
    )
    return True