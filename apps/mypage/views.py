# Django 내장 모듈
from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import JsonResponse

# 프로젝트 내 모듈
from apps.accounts.models import CustomUser
from apps.accounts.forms import CustomUserChangeForm
from apps.review.models import Review, Comment as ReviewComment
from apps.corboard.models import Corboard, Comment as CorboardComment
from apps.trend.models import Trend, Comment as TrendComment

# 프로필 보기 뷰
class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'mypage/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.request.user
        return context

# 프로필 수정 뷰
class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'mypage/profile_edit.html'
    success_url = reverse_lazy('mypage:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        # messages.success(self.request, '프로필이 성공적으로 업데이트되었습니다.')
        return response

    def form_invalid(self, form):
        messages.error(self.request, '오류가 발생했습니다. 입력 내용을 다시 확인해 주세요.')
        return super().form_invalid(form)

# AJAX
class ActivitiesAjaxView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        filter_type = request.GET.get('filter', 'my_posts')
        category = request.GET.get('category', 'all')

        # 내가 쓴 글 필터링
        if filter_type == 'my_posts':
            if category == 'review':
                posts = Review.objects.filter(writer=request.user)
            elif category == 'trend':
                posts = Trend.objects.filter(writer=request.user)
            elif category == 'corboard':
                posts = Corboard.objects.filter(writer=request.user)
            else:
                posts = list(Trend.objects.filter(writer=request.user)) + \
                        list(Review.objects.filter(writer=request.user)) + \
                        list(Corboard.objects.filter(writer=request.user))

        # 내가 북마크한 글 필터링
        elif filter_type == 'bookmarked':
            if category == 'review':
                posts = Review.objects.filter(bookmarks=request.user)
            elif category == 'trend':
                posts = Trend.objects.filter(bookmarks=request.user)
            elif category == 'corboard':
                posts = Corboard.objects.filter(bookmarks=request.user)
            else:
                posts = list(Trend.objects.filter(bookmarks=request.user)) + \
                        list(Review.objects.filter(bookmarks=request.user)) + \
                        list(Corboard.objects.filter(bookmarks=request.user))

        # 내가 좋아요한 글 필터링
        elif filter_type == 'liked':
            if category == 'review':
                posts = Review.objects.filter(likes=request.user)
            elif category == 'trend':
                posts = Trend.objects.filter(likes=request.user)
            elif category == 'corboard':
                posts = Corboard.objects.filter(likes=request.user)
            else:
                posts = list(Trend.objects.filter(likes=request.user)) + \
                        list(Review.objects.filter(likes=request.user)) + \
                        list(Corboard.objects.filter(likes=request.user))

        # 내가 댓글을 단 글 필터링
        elif filter_type == 'commented':
            if category == 'review':
                post_ids = ReviewComment.objects.filter(writer=request.user).values_list('review_id', flat=True)
                posts = Review.objects.filter(id__in=post_ids)
            elif category == 'trend':
                post_ids = TrendComment.objects.filter(writer=request.user).values_list('trend_id', flat=True)
                posts = Trend.objects.filter(id__in=post_ids)
            elif category == 'corboard':
                post_ids = CorboardComment.objects.filter(writer=request.user).values_list('corboard_id', flat=True)
                posts = Corboard.objects.filter(id__in=post_ids)
            else:
                trend_ids = TrendComment.objects.filter(writer=request.user).values_list('trend_id', flat=True)
                review_ids = ReviewComment.objects.filter(writer=request.user).values_list('review_id', flat=True)
                corboard_ids = CorboardComment.objects.filter(writer=request.user).values_list('corboard_id', flat=True)
                posts = list(Trend.objects.filter(id__in=trend_ids)) + \
                        list(Review.objects.filter(id__in=review_ids)) + \
                        list(Corboard.objects.filter(id__in=corboard_ids))

        else:
            posts = list(Trend.objects.filter(writer=request.user)) + \
                    list(Review.objects.filter(writer=request.user)) + \
                    list(Corboard.objects.filter(writer=request.user))

        posts_data = [{
            'title': post.title, 
            'content': post.content[:100],
            'writer': post.writer.username, 
            'date': post.date.isoformat(),
            'url': post.get_absolute_url(),
            'category': getattr(post, 'category', '일반')
        } for post in posts]

        return JsonResponse({'posts': posts_data})