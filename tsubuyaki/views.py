from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Message, Good, Share, Follow, Notification
from .forms import PostForm, SignUpForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/tsubuyaki/')
    else:
        form = SignUpForm()

    params = {'form':form}
    return render(request, 'registration/signup.html', params)

# Create your views here.
@login_required(login_url='/accounts/login/')
def index(request):

    if request.method == 'POST':
        obj = Message()
        obj.user = request.user
        obj.picture = request.FILES.get('picture')
        form = PostForm(request.POST, instance=obj)
        form.save()

    message = Message.objects.all()
    params = {
        'form': PostForm(),
        'content': message,
        'user': request.user,
        'share': False,
    }
    return render(request, 'registration/index.html', params)

@login_required(login_url='/accounts/login/')
def good(request, good_id):
    good_msg = Message.objects.get(id=good_id)
    is_good = Good.objects.filter(user=request.user).filter(message=good_msg).count()
    if is_good > 0:
        good_msg.good_count -= 1
        good_msg.save()
        Good.objects.filter(user=request.user).filter(message=good_msg).delete()
        return redirect(to='/tsubuyaki/')
    good_msg.good_count += 1
    good_msg.save()
    good = Good()
    good.user = request.user
    good.message = good_msg
    good.save()
    notification(request.user, good_msg.user, good_msg.content, 'good')
    return redirect(to='/tsubuyaki/')

@login_required(login_url='/accounts/login/')
def delete(request, del_id):
    del_msg = Message.objects.get(id=del_id)
    if del_msg.user == request.user:
        if del_msg.share_id != None:
            if Message.objects.filter(id=del_msg.share_id).count() > 0:
                message = Message.objects.get(id=del_msg.share_id)
                message.share_count -= 1
                message.save()
        Message.objects.filter(id=del_id).delete()
    return redirect(to='/tsubuyaki/')

@login_required(login_url='/accounts/login/')
def share(request, share_id):

    share_msg = Message.objects.get(id=share_id)

    if request.method == 'POST':
        obj = Message()
        obj.user = request.user
        obj.picture = request.FILES.get('picture')
        obj.share_id = share_id
        obj.share_user = share_msg.user
        obj.share_content = share_msg.content
        form = PostForm(request.POST, instance=obj)
        form.save()
        share_msg.share_count += 1
        share_msg.save()
        share = Share()
        share.user = share_msg.user
        share.message = share_msg
        share.save()
        notification(request.user, share_msg.user, share_msg.content, 'share')
        return redirect(to='/tsubuyaki/')

    message = Message.objects.all()
    params = {
        'form': PostForm(),
        'content': message,
        'share': True,
        'share_id': share_id,
        'share_msg': share_msg,
        'user': request.user,
    }
    return render(request, 'registration/index.html', params)

@login_required(login_url='/accounts/login/')
def user(request, username):
    user = User.objects.get(username=username)
    content = Message.objects.filter(user=user)
    following = Follow.objects.filter(owner=user)
    follower = Follow.objects.filter(follow_user=user)
    params = {
        'user': user,
        'owner': request.user,
        'content': content,
        'following': following.count(),
        'follower': follower.count(),
    }
    return render(request, 'registration/user.html', params)

@login_required(login_url='/accounts/login/')
def follow(request, follow_user):
    follow_user = User.objects.get(username=follow_user)
    if follow_user == request.user:
        return  redirect('user', username=follow_user)
    if Follow.objects.filter(owner=request.user).filter(follow_user=follow_user).count() > 0:
        Follow.objects.filter(owner=request.user).filter(follow_user=follow_user).delete()
        return redirect('user', username=follow_user)
    obj = Follow()
    obj.owner = request.user
    obj.follow_user = follow_user
    obj.save()
    notification(request.user, follow_user, '', 'follow')
    return redirect('user', username=follow_user)

@login_required(login_url='/accounts/login/')
def following(request, owner):
    owner = User.objects.get(username=owner)
    following = Follow.objects.filter(owner=owner)
    params = {'following': following}
    return render(request, 'registration/following.html', params)

@login_required(login_url='/accounts/login/')
def follower(request, follow_user):
    follow_user = User.objects.get(username=follow_user)
    follower = Follow.objects.filter(follow_user=follow_user)
    params = {'follower': follower}
    return render(request, 'registration/follower.html', params)

@login_required(login_url='/accounts/login/')
def following_content(request):
    following = Follow.objects.filter(owner=request.user).values_list('follow_user')
    following_content = Message.objects.filter(user__in=following)
    params = {
        'content': following_content,
        'user': request.user,
        }
    return render(request, 'registration/following_content.html', params)

def notification(owner, user, content, action):
    if action == 'good':
        is_good = Notification.objects.filter(owner=owner).filter(content=content).count()
        if is_good > 0:
            return
    elif action == 'follow':
        is_follow = Notification.objects.filter(owner=owner).filter(user=user).count()
        if is_follow > 0:
            return

    if owner == user:
        return

    obj = Notification()
    obj.owner = owner
    obj.user = user
    obj.content = content
    obj.action = action
    obj.save()

@login_required(login_url='/accounts/login/')
def show_notification(request):
    notification = Notification.objects.filter(user=request.user)
    params = {
        'notification': notification,
        'user': request.user,
        }
    return render(request, 'registration/notification.html', params)